#!/usr/bin/env python3
"""
Build the static site into _site/.

Static pages (index.html, publications.html, assets/) are copied as-is.
Everything in posts/*.md becomes a page under _site/blog/, plus a blog index
and an RSS feed.

Usage:
    pip install markdown
    python build.py            # build into _site/
    python build.py --serve    # build, then serve on http://localhost:4173
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Missing dependency. Run:  pip install markdown")

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
POSTS = ROOT / "posts"
TEMPLATES = ROOT / "_templates"

SITE_URL = "https://anantgupta2.github.io"
AUTHOR = "Anant Gupta"

# Files and directories copied verbatim into _site/.
STATIC = ["index.html", "publications.html", "assets"]

MD_EXTENSIONS = ["fenced_code", "tables", "smarty", "sane_lists", "footnotes"]

# Math has to be hidden from the markdown processor, or `f_\theta(x)` turns into
# `f<em>\theta(x)` and `\big[...\]` gets mangled. We swap each math span for an
# inert alphanumeric token, run markdown, then swap the originals back.
#
# The `code` alternative is listed first and deliberately left alone, so that a
# literal `$x$` inside backticks or a fenced block stays literal.
MATH_GUARD = re.compile(
    r"(?P<code>```.*?```|~~~.*?~~~|`[^`\n]+`)"
    r"|(?P<math>"
    r"\$\$.*?\$\$"  # $$ display $$
    r"|\\\[.*?\\\]"  # \[ display \]
    r"|\\\(.*?\\\)"  # \( inline \)
    r"|(?<![\w$])\$(?!\s)(?:[^$\n\\]|\\.)+?(?<![\s\\])\$(?![\w$])"  # $ inline $
    r")",
    re.S,
)

MATH_TOKEN = "zZmathZz{}zZmathZz"


def protect_math(text: str) -> tuple[str, list[str]]:
    spans: list[str] = []

    def swap(m: re.Match) -> str:
        if m.group("code") is not None:
            return m.group("code")
        spans.append(m.group("math"))
        return MATH_TOKEN.format(len(spans) - 1)

    return MATH_GUARD.sub(swap, text), spans


def restore_math(html_text: str, spans: list[str]) -> str:
    for i, span in enumerate(spans):
        html_text = html_text.replace(MATH_TOKEN.format(i), span)
    return html_text


# ──────────────────────────────  parsing  ──────────────────────────────


def parse_post(path: Path) -> dict:
    """Split a `---` frontmatter block off the top of a markdown file.

    Frontmatter is plain `key: value` lines — no YAML dependency. Keeping it
    dependency-light means the GitHub Action only ever needs `markdown`.
    """
    raw = path.read_text(encoding="utf-8")

    meta: dict[str, str] = {}
    body = raw

    if raw.lstrip().startswith("---"):
        raw = raw.lstrip()
        end = raw.find("\n---", 3)
        if end == -1:
            sys.exit(f"{path.name}: frontmatter opened with --- but never closed")
        for line in raw[3:end].strip().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                sys.exit(f"{path.name}: frontmatter line is not `key: value` -> {line!r}")
            key, value = line.split(":", 1)
            meta[key.strip().lower()] = value.strip().strip("\"'")
        body = raw[end + 4 :].lstrip("\n")

    if "title" not in meta:
        sys.exit(f"{path.name}: frontmatter is missing a `title:`")
    if "date" not in meta:
        sys.exit(f"{path.name}: frontmatter is missing a `date:` (YYYY-MM-DD)")

    try:
        date = datetime.strptime(meta["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        sys.exit(f"{path.name}: date {meta['date']!r} is not YYYY-MM-DD")

    # Strip a leading date from the filename so posts sort on disk but get clean URLs.
    slug = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)

    guarded, math_spans = protect_math(body)
    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    body_html = restore_math(md.convert(guarded), math_spans)

    summary = meta.get("summary", "")
    if not summary:
        # Fall back to the first paragraph, tags stripped.
        first = re.search(r"<p>(.*?)</p>", body_html, re.S)
        summary = re.sub(r"<[^>]+>", "", first.group(1)).strip() if first else ""

    return {
        "title": meta["title"],
        "date": date,
        "slug": slug,
        "summary": " ".join(summary.split()),
        "body": body_html,
        "needs_math": bool(math_spans),
        "source": path.name,
    }


# ──────────────────────────────  rendering  ──────────────────────────────


def render(template: str, **fields: str) -> str:
    out = template
    for key, value in fields.items():
        out = out.replace("{{" + key + "}}", value)
    leftover = re.findall(r"\{\{(\w+)\}\}", out)
    if leftover:
        sys.exit(f"Template placeholder(s) never filled: {sorted(set(leftover))}")
    return out


KATEX = r"""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" />
    <script>
      // Defined before the CDN scripts so the onload hook below always has a
      // target. Guarded because it is called from two places (whichever wins)
      // and auto-render is not safe to run twice over the same nodes.
      window.__renderMath = function () {
        if (window.__mathDone) return;
        if (typeof renderMathInElement !== "function") return;
        var target = document.querySelector(".prose");
        if (!target) return;
        window.__mathDone = true;
        renderMathInElement(target, {
          delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "\\[", right: "\\]", display: true },
            { left: "$", right: "$", display: false },
            { left: "\\(", right: "\\)", display: false }
          ],
          ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
          throwOnError: false
        });
      };
    </script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
    <script
      defer
      src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
      onload="window.__renderMath()"
    ></script>
    <script>
      // Fallback: if the CDN was slow and onload fired before the DOM was ready,
      // or the script was served from cache without firing onload.
      document.addEventListener("DOMContentLoaded", window.__renderMath);
      window.addEventListener("load", window.__renderMath);
    </script>
"""


def build() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # 1. Static files
    for name in STATIC:
        src = ROOT / name
        if not src.exists():
            sys.exit(f"Expected static path is missing: {name}")
        if src.is_dir():
            shutil.copytree(src, OUT / name)
        else:
            shutil.copy2(src, OUT / name)

    # GitHub Pages must not run Jekyll over the output.
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    post_tpl = (TEMPLATES / "post.html").read_text(encoding="utf-8")
    index_tpl = (TEMPLATES / "blog.html").read_text(encoding="utf-8")

    posts = sorted(
        (parse_post(p) for p in POSTS.glob("*.md")),
        key=lambda p: p["date"],
        reverse=True,
    )

    seen: dict[str, str] = {}
    for p in posts:
        if p["slug"] in seen:
            sys.exit(f"Duplicate slug {p['slug']!r}: {seen[p['slug']]} and {p['source']}")
        seen[p["slug"]] = p["source"]

    # 2. Individual post pages
    (OUT / "blog").mkdir()
    for p in posts:
        page = render(
            post_tpl,
            title=html.escape(p["title"]),
            description=html.escape(p["summary"]),
            date_iso=p["date"].strftime("%Y-%m-%d"),
            # %-d is not portable to Windows, so strip the pad by hand.
            date_human=f"{p['date'].strftime('%B')} {p['date'].day}, {p['date'].year}",
            body=p["body"],
            slug=p["slug"],
            math=KATEX if p["needs_math"] else "",
        )
        (OUT / "blog" / f"{p['slug']}.html").write_text(page, encoding="utf-8")

    # 3. Blog index
    if posts:
        items = "\n".join(
            f"""          <li class="postlist__item">
            <a class="postlist__link" href="blog/{p['slug']}.html">
              <time datetime="{p['date'].strftime('%Y-%m-%d')}">{p['date'].strftime('%b %Y')}</time>
              <span>
                <span class="postlist__title">{html.escape(p['title'])}</span>
                <span class="postlist__summary">{html.escape(p['summary'])}</span>
              </span>
            </a>
          </li>"""
            for p in posts
        )
        listing = f'<ul class="postlist">\n{items}\n        </ul>'
    else:
        listing = '<p class="muted">No posts yet — check back soon.</p>'

    (OUT / "blog.html").write_text(render(index_tpl, posts=listing), encoding="utf-8")

    # 4. RSS
    entries = "\n".join(
        f"""    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{SITE_URL}/blog/{p['slug']}.html</link>
      <guid isPermaLink="true">{SITE_URL}/blog/{p['slug']}.html</guid>
      <pubDate>{format_datetime(p['date'])}</pubDate>
      <description>{html.escape(p['summary'])}</description>
    </item>"""
        for p in posts
    )
    (OUT / "feed.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{AUTHOR} — Writing</title>
    <link>{SITE_URL}/blog.html</link>
    <description>Notes on continual learning, meta-learning, and self-improving systems.</description>
    <language>en</language>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml" />
{entries}
  </channel>
</rss>
""",
        encoding="utf-8",
    )

    print(f"Built {len(posts)} post(s) into {OUT}/")
    for p in posts:
        print(f"  blog/{p['slug']}.html   {p['title']}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--serve", action="store_true", help="serve _site/ after building")
    ap.add_argument("--port", type=int, default=4173)
    args = ap.parse_args()

    build()

    if args.serve:
        import functools
        from http.server import HTTPServer, SimpleHTTPRequestHandler

        handler = functools.partial(SimpleHTTPRequestHandler, directory=str(OUT))
        print(f"\nServing http://localhost:{args.port}  (Ctrl-C to stop)")
        HTTPServer(("", args.port), handler).serve_forever()


if __name__ == "__main__":
    main()
