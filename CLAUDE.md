# Notes for Claude

Context for working on this site. Read this before changing anything. The owner
edits it too, so treat it as the current word on preferences. Update it whenever
a decision here changes.

This repo is public, so this file is public too. Keep private details out of it.

## What this is

Anant Gupta's academic homepage, served by GitHub Pages at
https://anantgupta2.github.io. It is plain HTML and CSS with a small Python build
(`build.py`, which needs only the `markdown` package). There is no Jekyll, no Node
and no framework. The owner asked for something light, so keep it that way. Don't
add dependencies, a JS framework or a CSS framework.

| File | Holds |
| --- | --- |
| `index.html` | Home: intro, news, research threads, selected publications, teaching, service, education, contact |
| `publications.html` | Full publication list with filter chips |
| `assets/css/style.css` | All styling. Design tokens are at the top; light and dark palettes are under `[data-theme]` |
| `assets/js/main.js` | Theme toggle, publication filters, scroll-spy nav |
| `assets/pdf/Anant_Gupta_CV.pdf` | The CV. Replace the file to update it |
| `posts/*.md`, `_templates/` | Blog (Writing), built by `build.py`. Currently hidden, see below |
| `build.py` | Copies `index.html`, `publications.html` and `assets/` into `_site/`, renders posts, writes `feed.xml` |
| `.github/workflows/deploy.yml` | On push to `main`: runs `python build.py`, deploys `_site/` to the `gh-pages` branch |

`_site/` is build output and is gitignored. Never edit it by hand. This file and
`README.md` are not copied into `_site/`, so they are never served.

The hero photo floats right and the intro wraps around it and continues
underneath; the owner asked for this (2026-10-01). The intro is capped at 56rem so lines
under the photo stay readable. On phones (≤640px) the photo sits small above
the name instead.

The accent color `#1F3A68` matches the owner's LaTeX CV. Fonts are Newsreader
(serif, for headings) and Inter (sans, for body text).

## Build and check

```bash
pip install markdown
python build.py --serve   # http://localhost:4173
```

After any change, rebuild and check the result:
- No broken internal links. Strip HTML comments first, so hidden links don't count.
- Both light and dark themes look right.
- A narrow phone width (~375px) still works.

If a CSS change doesn't show up, the browser has cached the old stylesheet. Hard-reload.

## Content rules from the owner

- **Source of truth is the owner's PhD CV.** Don't add anything that isn't in it,
  and don't bring back items the owner removed from it. The one exception so far:
  the SIAM MDS 2024 poster ("A Reduced Operator Newton Method for Bayesian
  Filtering") is commented out in the CV, but the owner asked for it under
  Workshops & talks.
- **Never write "under review."** Unpublished work is labeled **Preprint**.
- **Don't mention papers that are currently under submission.**
- **Don't invent facts:** dates, DOIs, links, names or numbers. Look them up or
  ask. (Earlier, a DOI and a coauthor's first name were guessed wrong and had to
  be fixed.)
- Coauthor: "W. Xu" on the CV is **Wei Xu**.
- The owner is marked in **bold** in author lists; `*` means equal contribution.
- Venue lines keep **Main Track** and **Poster**, e.g. "Conference on Neural
  Information Processing Systems · Main Track · Poster · Atlanta, Dec 2026".
  The News item for NeurIPS does *not* say "as a poster."
- The News dates are confirmed by the owner. Leave them alone.
- The Putnam 2022 Honorable Mention stays.
- Contact section only. No meeting scheduler (Calendly etc.).
- The Service section is service only, with no mentoring entries.

## How to write about the research

- **Describe the core idea of each work, not the owner's personal
  contributions.** Avoid "I designed…" or "I led…".
- Each card has a short note (`.card__why`) on how the work relates to the
  owner's goals. **Keep it to one line.**
- **Be concise.** The owner has repeatedly cut wording down. When unsure, write
  less.
- The intro credits both advisors: Christopher MacLellan (Teachable AI Lab) and
  Vijay Ganesh (Reasoning and Learning Group). Research is organized by
  **question, not by advisor**. Each card says who it is "with".

### The owner's framing (their words, lightly structured)

- They work on **continual learning** and **meta-learning**.
- **Continual learning, i.e. consolidation.** Whatever external memory a model
  has, part of what it learns should become part of the model itself. They are
  not against retrieval (they have worked on it); they just think some knowledge
  must be consolidated into the weights.
- **Updates built from the model's own structure forget less,** because they
  diverge less from the model. Examples are self-distillation and the modes of a
  diffusion model.
- **Meta-learning, i.e. structured autonomy.** Don't mention self-improvement
  in the intro; the owner removed it (2026-10-01). Their framing: current models
  have everything about training defined for them; learning to learn needs the
  training itself to change. The first step is structured autonomy, which means
  the model makes decisions within its own training. That is why multi-role RL
  uses roles. The goal is to go from structured autonomy (the current phase) to
  *full* autonomy. Structured autonomy: models take over parts of their own
  learning, within a structure the researchers design. In the intro, keep this
  to the core idea in a few short sentences; leave the multi-role RL details to
  its card. It is
  not yet self-directed; humans still direct part of it. So never label the
  work "self-directed learning", since that would claim the goal as the result.
  They prefer *agentic* self-evolution (LLM-specific, so it goes last if
  mentioned at all).
- **Continual learning and meta-learning are linked** (the owner's intuition).
  The trust-region work is one concrete link.
- **Human errors.** This comes from teaching: four semesters as a TA for
  Automata and Complexity, and they enjoy tutoring. The goal is an LLM
  grader/tutor, and that starts with models that can reproduce the mistakes
  students actually make.

The home-page intro, in order:
1. The advisors.
2. "Broadly interested in continual learning and meta-learning."
3. **Continual learning.**: consolidation.
4. **Meta-learning.**: working towards structured autonomy.
5. A plain paragraph linking the two. The most natural way to consolidate is
   through what the model already knows (self-distillation or RL in LLMs,
   composing learned knowledge in diffusion models). Such updates diverge less,
   forget less, and hand more of the learning to the model.
6. A plain teaching paragraph: they love to teach and have been a TA for four
   semesters. Grading takes TAs a long time, so they work on training models to
   give feedback in the meantime. The paragraph ends there; the owner removed
   an extra clause about reproducing student mistakes. It motivates the "Human
   errors" card.

Use "I believe" at most once; the owner found repeated "I believe"s too much.

### Research cards on the home page (in this order)

The research section is one grid of cards, not grouped under thread headings,
because most projects span several themes. Each card carries topic tags
(`.card__tags`) at the top. The tag vocabulary is: Continual learning,
Meta-learning, Meta-continual learning, Structured autonomy, Human errors. Structured autonomy is the
owner's name for the "learning from within" side of meta-learning.

1. **Continual Learning in Diffusion Models.** Tags: Continual learning,
   Meta-learning. Titled this way, not "Trust Region Continual Learning",
   because both papers are specific to diffusion models; whether the results
   generalize hasn't been discussed. Don't claim they do. The method is trust
   region continual learning (TRCL), because the Fisher penalty keeps updates
   inside a trust region. It covers two papers:
   - ICLR 2026: the empirical Fisher of a diffusion model is rank-1 in low-SNR
     regimes.
   - NeurIPS 2026: under local approximations, TRCL is equivalent to one-step
     MAML (replay as the query, the Fisher penalty as the support), so it
     implicitly meta-learns previous tasks. Always describe this as a
     *conditional* equivalence.

   The owner wrote the card text, in the active voice ("We show…"). It follows
   their order: rank-1 Fisher, then the rank-1 EWC penalty with replay forgets
   less, then the conditional MAML equivalence, then the observed faster
   re-learning. Keep it simple.
2. **Self-Consolidating Language Models (SCoL).** Tag: Meta-continual learning
   (the owner's label). The same intuition as the
   diffusion work, but the Fisher is too expensive at LLM scale, so the model
   learns it (meta-RL picks which layers to update).
3. **Hierarchical and Incremental Concept Formation (Cobweb, CobwebTM).** Tag:
   Continual learning. This is the external-memory / retrieval side. "Matches or
   beats prior incremental methods" comes from the CobwebTM paper: the owner
   asked for "beats", but the paper says "outperforms or performs competitively".
4. **Multi-Role Reinforcement Learning.** Tag: Structured autonomy. Roles hand
   more of the training to the model; next, the model designs its own roles. The
   paper is "Cross-Task Transfer via Multi-Role Reinforcement Learning". It has
   no public link yet, so the Preprint chip is unlinked.
5. **Test-Time Compositional Generation.** Tag: Structured autonomy. Once the
   algorithm is set, the only question is what to incorporate.
6. **Simulating Student Misconceptions** (with Vijay Ganesh). Tag: Human errors.
   The idea: if models can reproduce the errors people make, those errors can
   benchmark and train models. The task is **single-turn**, and the card says so.
   It is described simply as "a counterfactual generation problem".
   - *LLMs as Debuggers in Unverifiable Domains* (tag: Human errors) is
     **commented out** in `index.html`. The owner wants it back later.
     Uncomment to restore.

Each card ends with `.card__links` chips pointing to the papers. Keep card titles
matching the paper names used on `publications.html`.

## Hidden things (built, not linked)

- **Writing / blog**: `blog.html` and `feed.xml` are built and deployed but not
  linked. To turn it on, uncomment the `Writing` nav link and the RSS
  `<link rel="alternate">` in both `index.html` and `publications.html`. Each spot
  is marked. The owner will turn it on when they start writing.
- **Debuggers card**: see above.

## Deployment status

- Live since 2026-10-01. The site lives at the repo root; pushing to `main`
  deploys it through the Action to `gh-pages`.
- The old al-folio Jekyll site is backed up on the `al-folio-archive` branch
  (local and on GitHub). The owner wants it kept. Don't delete that branch.
- Old al-folio URLs (`/publications/`, `/cv/`, `/news/`) no longer exist. The
  owner said no redirects are needed.
- Only push when the owner asks.

## Open questions for the owner

- **The intro is not final.** As of 2026-09-28 the owner said they will work
  out the intro themselves later; everything else on the page is approved. Two
  ideas they were shown but haven't decided on:
  - Frame consolidation as "where new knowledge should go: in the weights or in
    an external memory". That also gives Cobweb a place in the intro.
  - Use teaching as the lens: treat the model as a student that studies, keeps
    what matters, and makes revealing errors.

- Contact lists "PhD applications" as a topic. Should it instead say whether
  they are applying (e.g. for Fall 2027), or be dropped?
- A public link for the Multi-Role RL preprint.
- A headshot. The current photo is a graduation photo.

## Environment

- Windows. Python is available. There is no Ruby, Node or `gh` CLI, which is
  one reason the site isn't Jekyll.
- `.claude/launch.json` (at the repo root) serves `_site` on port 4173 for
  previews.
