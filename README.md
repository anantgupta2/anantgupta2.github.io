# anantgupta2.github.io

Personal academic site. Plain HTML and CSS, with a ~200-line Python script that
turns `posts/*.md` into blog pages. No Jekyll, no Node, no theme.

## The Writing section is currently hidden

It is fully built and deployed — `/blog.html` and `/feed.xml` are live — but
nothing on the site links to it, so visitors will not find it. That way you can
draft posts and preview them at the real URL before making them public.

To turn it on, uncomment four things:

| File                | What to uncomment                     |
| ------------------- | ------------------------------------- |
| `index.html`        | the `<a href="blog.html">` nav link   |
| `index.html`        | the RSS `<link rel="alternate">` in `<head>` |
| `publications.html` | the same two                          |

Each spot has a comment marking it.

## Writing a blog post

Create a file in `posts/`. The filename date is just for sorting on disk — it is
stripped from the URL.

```
posts/2026-10-14-some-title.md
```

```markdown
---
title: Some title
date: 2026-10-14
summary: One or two sentences shown on the blog index and in link previews.
---

Body text in markdown. **Bold**, `code`, fenced code blocks, tables,
footnotes[^1], and blockquotes all work.

Math works too: inline $f_\theta(x)$ and display

$$\mathcal{L}(\theta) = \mathbb{E}\big[\ell(f_\theta(x), y)\big]$$

KaTeX is only loaded on pages that actually contain math.

[^1]: Like this.
```

Then:

```bash
git add posts/ && git commit -m "post: some title" && git push
```

The GitHub Action builds and deploys to the `gh-pages` branch. Live in about a
minute. That is the whole workflow — you never need to run anything locally.

`summary` is optional; the first paragraph is used if you leave it out. `slug`
is also optional if you want a URL that differs from the filename.

## Editing the rest of the site

| What                                   | Where                    |
| -------------------------------------- | ------------------------ |
| Home page (bio, news, research, contact) | `index.html`           |
| Full publication list                    | `publications.html`    |
| Colors, fonts, spacing                   | `assets/css/style.css` |
| Page shell for posts and blog index      | `_templates/`          |
| CV PDF                                   | `assets/pdf/`          |

Colors and typography are CSS custom properties at the top of `style.css` —
`:root` for shared tokens, then `[data-theme="light"]` and `[data-theme="dark"]`.
Changing `--accent` in both blocks retints the whole site.

## Building locally (optional)

```bash
pip install markdown
python build.py --serve     # http://localhost:4173
```

Output goes to `_site/`, which is gitignored.

## Previous site

The old al-folio Jekyll site is preserved on the `al-folio-archive` branch.
