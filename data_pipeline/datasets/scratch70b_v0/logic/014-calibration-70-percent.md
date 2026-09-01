---
id: logic-014
category: logic
subcategory: probability
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - counterexample
title: Calibration, what "70% sure" should mean
approx_words: 620
---

# Calibration: saying "70% sure" and meaning it

When someone says "I'm 70% sure the package arrives Friday," what would make that statement *good*? Not the package arriving — a 70% claim explicitly reserves a 30% lane for non-arrival. The statement is good if it comes from a forecaster whose 70% claims, collected over time, come true about 70% of the time. That property is called calibration, and it is checkable.

## The worked example

Imagine Dana keeps a forecasting journal for a year. Every prediction gets a probability, and every outcome gets recorded. At year's end she sorts her predictions into buckets by the confidence she stated:

- Of 40 predictions made at "90%," 35 came true → 87.5% hit rate.
- Of 60 predictions made at "70%," 43 came true → 71.7%.
- Of 50 predictions made at "60%," 29 came true → 58%.

Bucket by bucket, stated confidence tracks realized frequency within noise. Dana is well calibrated. The valid inference her track record supports:

1. Across many past cases, Dana's "70%" statements came true close to 70% of the time.
2. Dana now says a new event is 70% likely, using the same judgment process.
3. Therefore, treating this event as 70% likely — for betting, planning, buying insurance — is the reasonable policy.

Note what calibration does *not* require: it does not require being right, bucket-champion, or bold. A weather forecaster who says "70% rain" on ten days, and sees rain on seven of them, was not "wrong" on the three dry days. She was exactly as advertised. Single outcomes cannot refute a probability statement; only bucketed track records can.

Calibration is also not the whole of forecasting skill. A forecaster who predicts "50%" on every coin-flip-like question is perfectly calibrated and perfectly useless. The other virtue is *resolution* — confidently separating the events that happen from those that don't. The best forecasters have both: their 90s hit ~90%, and they dare to say 90 often.

## The tempting invalid cousin

1. Marcus said he was 70% sure the merger would close, and it fell through.
2. Therefore Marcus was wrong, his judgment failed, and his future percentages mean nothing.

**Counterexample.** Run the tape on a perfectly calibrated oracle — a forecaster who by construction states true probabilities. Give the oracle one hundred 70% predictions and, by its own flawless math, about thirty fail. The argument above convicts the oracle thirty times despite ideal performance. Any test that flunks a perfect performer is not a test of performance; premise-to-conclusion, the inference is invalid. A single miss is evidence of miscalibration only in the way one rainy day is evidence against a climate — nearly weightless alone.

The cousin has a twin that flatters instead of condemns: "She said 95% and it happened — she's brilliant." One hit at 95% is almost equally weightless. Both twins share a root error: scoring probabilistic statements as if they were binary promises.

## What to demand from yourself and others

- **Keep score in buckets.** The only meaningful audit of "70% sure" is the hit rate of many 70% claims. Journals, prediction platforms, and forecasting tournaments all work this way.
- **Expect the humbling pattern.** Untracked humans typically show overconfidence: their "90% sure" buckets land near 70%, their "certain" claims fail more than they imagine. Tracking alone shrinks the gap.
- **Reward honest 70s.** In teams and markets, punishing every individual miss teaches people to say "definitely" or say nothing. If you want informative probabilities from advisors, judge them on bucketed track records, never on single outcomes.

"70% sure" is not hedging or fortune-telling. It is a measurable promise about your long-run relationship with the truth — and the measurement is the whole point.
