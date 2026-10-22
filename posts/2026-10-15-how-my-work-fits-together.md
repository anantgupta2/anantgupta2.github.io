---
title: How my work fits together
date: 2026-10-15
summary: What I study, the two angles I take, and where each project fits.
---

## The question

I study human-inspired and human-like learning in machine learning models.
Humans and AI systems overlap in some ways and differ in others. Sometimes they
share a property but express it differently. My working belief is that many
intuitions about how people learn can be formalized in models. I hope to
find which intuitions transfer, understand why others don't, and turn the ones
that do into learning methods for these systems. Many won't transfer, and shouldn't be
expected to, so I try to be careful about which ones to build on.

I come at this from two sides:

1. **A model's own properties.** Some properties come from a model's inductive
   biases, and they can be put to use directly.
2. **Properties inspired by humans.** Some of the ways people learn can be
   formalized and built into models.

Most of this work is in continual learning (when and how a model should take in
new information without forgetting) and meta-learning (how a model can get more
out of the data it has).

## A model's own properties

**Continual learning in diffusion models.** The empirical Fisher of a diffusion
model is rank-1 in low-SNR regimes. That makes a rank-1 EWC penalty possible,
and combined with replay it more than halves forgetting on ImageNet-1k relative
to replay and diagonal-EWC baselines.
([ICLR 2026](https://openreview.net/forum?id=zCZcbRsc4g))

**Continual learning as meta-learning.** The Fisher penalty keeps each update
inside a trust region, so we call the method trust region continual learning.
Under local approximations, it is equivalent to one-step MAML, with replay as
the query and the Fisher penalty as the support. In that sense it implicitly
meta-learns previous tasks, and the effect shows up directly: the model
re-learns earlier tasks faster than with other methods.
([NeurIPS 2026](https://arxiv.org/abs/2602.02417))

## Properties inspired by humans

**Multi-role reinforcement learning.** Humans get far more out of very little
data than LLMs do. Part of that is inductive bias; part is how people process
the data. They learn the same material in more than one way, by comparing
problems, identifying subgoals, or explaining, and they abstract across
examples. Multi-role RL trains one language model in several such roles over the
same examples. Roles that never answer a question directly still improve problem
solving. This points to transfer across tasks within LLMs, and to more training
signal in a fixed dataset than standard RL with verifiable rewards extracts.
Learning to abstract improves generalization, looking across several examples at
once gives more signal than seeing one at a time, and learning the same material
from different views helps even when those views are learned separately.
(*Cross-Task Transfer via Multi-Role Reinforcement Learning*, preprint.)

**Test-time compositional generalization via prototype discovery.**
Compositional generalization is producing new configurations from familiar
parts. Humans do this freely, combining concepts they already know into things
they have never seen. We find a way to express this in diffusion models, so that
a pretrained model can compose what it already knows at test time.
([Preprint](https://arxiv.org/abs/2605.07078))
