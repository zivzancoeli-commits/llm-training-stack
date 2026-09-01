---
id: habits-013
category: reasoning_habits
subcategory: estimation
difficulty: medium
source_model: fable-5
skills:
  - estimation
  - calibration
title: Fermi estimates as a prior before looking up a number
approx_words: 620
---

# Fermi Estimates as a Prior Before Looking Up a Number

Before you look up a number, guess it — not idly, but by construction. Decompose the quantity into factors you can roughly estimate, multiply, and write down the result. *Then* look it up. This ordering, estimate-then-check, is the whole habit, and reversing it destroys the value. A lookup performed first teaches you a digit string. A lookup performed second grades an estimate, and graded estimates are how physical intuition gets built.

The construction technique is the Fermi estimate, named for the physicist who famously produced usable answers from almost no data. The method: break the unknown into a chain of factors, estimate each to the nearest order of magnitude or so, and multiply. How many piano tuners work in a city of a million people? Estimate households (say 400,000), the fraction with pianos (maybe 1 in 20 → 20,000 pianos), tunings per piano per year (about 1 → 20,000 tunings/year), and one tuner's annual capacity (4 a day, 250 days → 1,000). Then 20,000 / 1,000 suggests roughly 20 tuners. Any individual factor might be off by two- or threefold, but errors in a long product tend to partially cancel — some estimates high, some low — so the final figure usually lands within a factor of a few. For a quantity you knew nothing about, "a few dozen, not three and not three thousand" is enormous progress.

Why do this when the real number is one search away? Three reasons, in ascending importance.

**The estimate is an error detector for the lookup.** Search results are wrong more often than their formatting suggests: units get mangled, a headline says billion where the source said million, a figure describes a different year or country or definition than you need. If your constructed prior says "around 20" and the source says "14,000," the collision forces a reconciliation — and the resolution is sometimes that you misread the source, sometimes that your model is missing a factor, and either way you learn something. With no prior, you'd have absorbed 14,000 without a flicker. A number you cannot sanity-check is a number you cannot really use.

**The decomposition is knowledge; the digit string is not.** The Fermi model — households, pianos per household, tunings per year, capacity — remains useful when the question shifts to a different city, or to guitar repair. It exposes *what the answer depends on*, which is what you actually need for decisions. Someone who knows "the U.S. uses about 4 trillion kWh of electricity a year" knows one fact; someone who built it from population × per-capita use can rebuild it, scale it, and notice when a claim implies something absurd about one of the factors.

**Scored guesses build calibration.** Each estimate-then-lookup cycle tells you whether your gut runs high or low, and on what kinds of quantities. Over dozens of cycles this feedback tunes the instrument. People who skip straight to lookup never receive the signal, which is why a person can consume statistics for years and still have no feel for whether a claimed figure is plausible.

Practical points for the habit. Work in orders of magnitude and round brutally; 8 × 300 is 2,400 but "a couple thousand" is fine — precision in a Fermi estimate is wasted effort. Prefer factors you have some anchor for (populations, lifespans, prices you've paid, sizes of familiar things) and build unfamiliar quantities out of familiar ones. Write the estimate down before searching; an unwritten prior will quietly adjust itself to agree with whatever you find, and you will feel like you "knew it all along."

The habit takes about a minute per number. What it buys is a mind in which looked-up facts have to pass an interview before being hired — and which slowly accumulates the interviewer's skill.
