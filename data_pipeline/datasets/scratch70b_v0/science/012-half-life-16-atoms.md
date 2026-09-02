---
id: science-012
category: science
subcategory: physics
difficulty: easy
source_model: fable-5
skills:
  - quantitative-reasoning
  - probabilistic-thinking
  - number-check
title: Half-life with 16 atoms you can count
approx_words: 600
---

# Half-Life with a 16-Atom Toy Model You Can Count

Radioactive decay is often stated as "half the atoms decay every half-life," which invites two misreadings: that atoms take turns, or that after two half-lives everything is gone. A toy model small enough to count fixes both.

## The setup: 16 atoms, one rule

Take 16 atoms of an unstable isotope with a half-life of one day. The rule of decay is purely probabilistic: **in any half-life, each atom independently has a 50% chance of decaying.** An atom does not age, does not remember, and does not coordinate with its neighbors. Each day, every surviving atom flips its own fair coin: tails, it decays.

Run the expected counts:

- Day 0: **16** atoms
- Day 1: **8** remain (each of 16 flipped; expect half to survive)
- Day 2: **4** remain
- Day 3: **2** remain
- Day 4: **1** remains
- Day 5: expected ½ an atom — which really means the last atom has a 50% chance of still being there.

Two lessons fall straight out of the countable version.

**First, decay halves; it doesn't subtract.** After two half-lives, you don't lose "two halves = everything." You lose half, then half *of what's left*: 16 → 8 → 4. The fraction remaining after n half-lives is (½)ⁿ. After 4 half-lives, 1/16 remains — matching our count: 16 × 1/16 = 1 atom. ✔

**Second, the law is statistical, and small numbers are noisy.** With 16 real atoms, day 1 might leave 7, or 9, or even 11 survivors — coin flips fluctuate. The "half" is the *expected* fraction. With 10²⁰ atoms (a fingernail-sized sample), the relative fluctuations shrink to invisibility (roughly like 1/√N), and the population tracks the smooth halving curve essentially perfectly. Half-life is a crowd behavior with single-atom randomness underneath — the same way a casino's income is predictable while any one bet is not.

A corollary worth making explicit: a single atom has no schedule. Ask "when will *this* atom decay?" and the only honest answer is a probability: 50% within one half-life, 75% within two, 87.5% within three. An atom that has survived a thousand half-lives is no more "due" than a fresh one — each day is still a fair coin. (This memorylessness is the actual content of exponential decay.)

## Why halving, and not steady loss?

Constant *probability per atom* automatically produces halving. The number decaying per day is proportional to the number present — 16 atoms yield about 8 decays on day one, but the surviving 8 yield only about 4 the next day. When the loss rate is proportional to the amount, the amount falls exponentially. Contrast a steady-loss process (say, exactly 4 atoms per day): that would empty the sample in 4 days flat, hit zero, and stop. Exponential decay never quite reaches zero in the idealized curve; in reality it ends when the last discrete atom finally decays.

## Check: units and a limiting case

The decay rate (activity) is atoms per unit time. Day 0–1: about 8 decays/day. Day 2–3: about 2 decays/day. Activity halves right along with the population — which is why a Geiger counter's click rate itself decays with the same half-life, and why very old samples are hard to date: the clicks get sparse.

Limiting case: extend the table to day 10. Expected survivors: 16 × (½)¹⁰ = 0.016 atoms — meaning almost certainly none, but with about a 1.6% chance one stubborn atom persists. The model handles its own endgame sensibly: no negative atoms, no sharp cutoff, just probabilities thinning toward zero.
