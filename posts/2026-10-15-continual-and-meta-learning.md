---
title: Where I think continual learning and meta-learning should go
date: 2026-10-15
summary: My views on what comes next in the two areas most of my work sits in.
---

## Continual learning

My work so far has mostly answered *how* a model should take in new knowledge
without forgetting: keep the update close to what the model already is. The
next question is *what kind* of knowledge it is. Some knowledge is
completely new to a model. Some is only slightly new, close to what it can
already do.

I think that distance should decide how the model learns it.

- **When the knowledge is far,** the update needs protecting, so that learning
  it doesn't wear down what the model already knows. Recent work points this
  way: protecting the most sensitive directions of an update helps most when
  the new data is far from the model
  ([Wu et al.](https://arxiv.org/abs/2610.05872)).
- **When the knowledge is within reach,** the model can learn it from its own
  attempts, on-policy. This works well, but struggles when the change needed is
  too large ([Shenfeld et al.](https://arxiv.org/abs/2601.19897)).

Whether on-policy learning is always the best choice for nearby knowledge is
still open; Wu et al. find that off-policy merging beats it in their settings.
Either way, the first question for any new piece of knowledge is how far it is.

## Meta-learning

Meta-learning is a broad term. I read it as "learning to learn ___", where the
blank can be filled in many ways: learning to learn efficiently, continually,
from unstructured data, and so on. Each setting fills in one blank. Because each
one makes a model better at learning something, many of them end up being
called self-improvement.

I believe meta-learning should include all of them. A model that has learned to learn
should be better at learning in every one of these senses, not just one.

The way I work towards this is structured autonomy. Today almost every decision
in training is made for the model: what to learn from, what to change, how
much. In structured autonomy, the model makes some of those decisions itself,
within a structure we design. In multi-role RL, for example, the roles hand part
of the training to the model. Each decision the model takes over is one more way
it is learning to learn. The long-term goal is full autonomy, where the model
directs its own learning.

## Where the two meet

Learning to learn continually is one of the blanks. And deciding how far a piece
of new knowledge is, and how to take it in, is itself a decision a model could
learn to make.
