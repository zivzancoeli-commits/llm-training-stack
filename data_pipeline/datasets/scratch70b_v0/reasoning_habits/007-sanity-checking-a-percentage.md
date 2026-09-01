---
id: habits-007
category: reasoning_habits
subcategory: checking
difficulty: medium
source_model: fable-5
skills:
  - check-your-work
  - proportional-reasoning
title: Sanity-checking a percentage over 100%
approx_words: 600
---

# Sanity-Checking a Percentage That Came Out Over 100%

Your calculation says 140%. Stop. Before writing it down, ask one question: *140% of what, and can this quantity exceed its whole?* Sometimes 140% is a legitimate answer. Sometimes it is a flare going up over a broken calculation. The habit is knowing which situation you are in — and the test is fast.

Percentages over 100 are legitimate exactly when the quantity being measured is not a part of the whole it's compared against. Growth can exceed 100%: revenue that goes from $50k to $120k grew by 140%, no contradiction. A comparison between two separate things can exceed 100%: one building can be 300% the height of another. Ratios of unlike quantities can exceed 100%: a loan's total repayment can be 160% of the principal.

But percentages over 100 are *impossible* whenever the numerator is, by definition, a piece of the denominator. No test-taker scores more than 100% of the available points. No survey finds that 104% of respondents agree. No tank is 130% drained. If your quantity answers the question "what fraction of the whole is this part?" then an answer above 100% is not a surprising result — it is a proof that something upstream is wrong. Parts do not exceed wholes. That is not an empirical fact that might have exceptions; it is what "part" means.

So when the alarm fires, where do you look? Three culprits account for nearly all cases:

**Inverted ratio.** The most common bug: you divided the whole by the part. If 40 of 160 students passed, the pass rate is 40/160 = 25%, but a hurried hand computes 160/40 = 400%. The tell is that the wrong answer is the reciprocal of the right one. Check: does the smaller number sit on top? Should it?

**Wrong base.** Percentage problems always have a hidden anchor — the "of what" — and picking the wrong anchor inflates results. A price rises from $80 to $100: that's a 25% increase (20/80), not 20% (20/100). Going the other way, $100 to $80 is a 20% decrease. Increases and decreases between the same two numbers are *not* symmetric percentages, because the base changes. If your answer looks off, re-ask: percent *of which quantity*?

**Percentage points confused with percent.** A rate that moves from 10% to 15% rose by 5 percentage points but by 50 percent. Mixing these mid-calculation can generate figures over 100% that mean nothing at all.

The habit generalizes beyond percentages into a broader discipline: **every quantity has a feasible range, and the range is checkable before and after computing.** Probabilities live in [0, 1]. Fractions of a population live in [0%, 100%]. A count is a nonnegative integer. An average sits between the minimum and maximum of its data. Each computed value should pass through this customs inspection: *what values could you possibly be?* The inspection is instant, requires no recomputation, and catches errors that rechecking the arithmetic often misses — because rechecking tends to repeat the same wrong setup with the same conviction.

One refinement: when a percentage over 100% turns out to be legitimate, say *what it means* in plain words as a final check. "Repayment is 160% of principal" translates to "you pay back the loan plus 60% more" — sensible. "The class scored 140% of the available points" translates to nothing, because there is nothing for it to mean. If the translation into an ordinary sentence produces nonsense, the number was nonsense wearing a percent sign. The percent sign grants no immunity; it just makes nonsense look quantitative.
