---
title: A fixed dataset has more signal than one pass extracts
date: 2026-09-28
summary: Why I keep coming back to the same idea from three different directions — and what a "role" is doing that a second epoch isn't.
---

This is the first post here, so it may as well be about the thing that keeps
showing up in everything I work on.

Here is the observation. Take a training set and a model. Standard training
does one thing with that pair: predict the target, take the gradient, move on.
But a person handed the same material does something stranger. They re-read it.
They compare problem 4 to problem 11 and notice they are the same problem. They
try to explain it to someone else and discover, mid-sentence, that they did not
understand it. They get it wrong, and the specific way they got it wrong tells
them where to look.

None of that is extra data. It is the same fixed set, worked differently.

## Three angles on the same question

The framing shows up in my work in ways that look unrelated on the surface:

- **Multi-role RL.** Train one model in several roles over the same examples.
  The interesting result is that auxiliary roles which *never produce an answer*
  still improve answer accuracy. The signal was sitting in the data the whole
  time; one role could not reach it.

- **Knowledge consolidation.** When a model reads a passage, which of its own
  layers should change? Treating that as a learned decision rather than a fixed
  schedule gets you more out of each passage than in-context use of the whole
  thing.

- **Concept formation.** Cobweb-style hierarchies reorganize as examples arrive,
  so the same stream of data yields a structure that keeps getting better rather
  than a fixed embedding computed once.

## What a role is not

The obvious objection: isn't this just a second epoch with extra steps?

No, and the distinction matters. A second epoch shows the model the same
$(x, y)$ pair under the same loss. A role changes what is being asked. If the
loss is

$$\mathcal{L}(\theta) = \mathbb{E}_{(x,y)\sim\mathcal{D}}\big[\ell(f_\theta(x), y)\big]$$

then a second epoch resamples from $\mathcal{D}$. A different role changes
$\ell$ and often changes what plays the part of $y$ — comparing two problems has
no answer key at all. You are not re-reading the page; you are being asked a
different question about it.

That is also why the gains do not saturate the way epoch-stacking does.

## What I am still unsure about

Plenty:

- Which roles are worth having? Right now I pick them by hand, which does not
  scale and is almost certainly leaving things on the table. Learning to propose
  roles is where I am headed.
- How much of this survives at scale? Most of my evidence is at sizes I can
  train on an academic budget.
- Is there a clean way to say when a set of roles is *sufficient* — that you have
  wrung the data dry? I do not have a good formalism for this yet.

If you have thoughts on any of that, I would genuinely like to hear them
&mdash; [email me](mailto:agupta886@gatech.edu).
