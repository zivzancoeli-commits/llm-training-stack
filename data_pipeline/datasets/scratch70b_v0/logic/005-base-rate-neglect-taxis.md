---
id: logic-005
category: logic
subcategory: probability
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - counterexample
title: Base-rate neglect with city taxis
approx_words: 620
---

# Base-rate neglect with city taxis

A taxi sideswipes a parked car at night and drives off. The city has two cab companies: Green Cab operates 85 of the city's 100 taxis, Blue Cab operates the other 15. A witness says the taxi was blue. Tested under similar nighttime conditions, this witness identifies cab colors correctly 80% of the time and errs 20% of the time.

How confident should you be that the cab was blue?

Most people answer "about 80% — that's how reliable the witness is." The correct answer is closer to 41%. The gap between those numbers is base-rate neglect.

## The worked solution

Run all 100 taxis past the witness on a similar night and tally what happens.

**The 15 blue cabs.** The witness is right 80% of the time, so she calls "blue" for 12 of them and mistakenly calls "green" for 3.

**The 85 green cabs.** She correctly calls "green" for 80% — that is 68 cabs — and mistakenly calls "blue" for the remaining 17.

Now collect every case where she says "blue": 12 true alarms plus 17 false alarms, 29 "blue" reports in all. Of those 29 reports, only 12 involve an actually blue cab.

12 / 29 ≈ 0.41.

So even after this reasonably reliable witness testifies, the odds are slightly *against* the cab being blue. The reason is sheer arithmetic of populations: green cabs so heavily outnumber blue ones that the witness's small error rate, applied to the huge green fleet, manufactures more false "blue" sightings (17) than her accuracy harvests true ones (12).

This argument is valid and the method is general: weigh the evidence's hit rate against its false-alarm rate, *scaled by how common each underlying case is*. The prior population frequencies — the base rates — are not optional trivia; they are half of the calculation.

## The tempting invalid cousin

1. The witness is right 80% of the time.
2. The witness says the cab was blue.
3. Therefore, there is an 80% chance the cab was blue.

The seduction is that the argument quotes a real, correctly measured number. The flaw is that "the probability the witness says blue, given a blue cab" and "the probability of a blue cab, given the witness says blue" are different quantities, and the argument silently swaps one for the other. This swap even has a courtroom name: the prosecutor's fallacy.

**Counterexample.** Push the base rate to an extreme and watch the 80% figure collapse. Suppose the city has 1 blue cab and 99 green ones, same 80%-accurate witness. She says "blue." True alarms: 0.8 cabs' worth from the single blue taxi. False alarms: 20% of 99 ≈ 19.8 from the green fleet. Probability of blue given her report: 0.8 / (0.8 + 19.8) ≈ 4%. Premises 1 and 2 hold exactly as before, yet the conclusion "80% blue" is off by a factor of twenty. An argument form that outputs 80% regardless of whether the truth is 41% or 4% is not tracking the world.

## The habit to build

Whenever a report, test, alarm, or witness says "rare thing happened," ask two questions before believing:

- **How common is the rare thing to begin with?** (the base rate)
- **How often does this source cry wolf when the rare thing is absent?** (the false-alarm rate)

If the thing is rare enough, even an impressive-sounding source generates mostly false alarms, because it has vastly more opportunities to be wrong about the common case than right about the rare one. Reliability percentages describe the *witness*; probabilities about the *world* require folding in how the world was populated before anyone spoke.
