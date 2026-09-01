---
id: logic-007
category: logic
subcategory: statistical-reasoning
difficulty: hard
source_model: fable-5
skills:
  - worked-solution
  - counterexample
title: Simpson's paradox with two hospitals
approx_words: 620
---

# Simpson's paradox with two hospitals

Two hospitals each treated 10 patients last month. Here are the survival numbers:

- **Hospital A:** 8 of 10 patients survived (80%).
- **Hospital B:** 7 of 10 patients survived (70%).

The tempting argument writes itself:

1. Hospital A's survival rate is 80%; Hospital B's is 70%.
2. Higher survival rate means better care.
3. Therefore, if you are sick, choose Hospital A.

Ten percentage points, honestly computed from complete data, no sampling error story. What could go wrong?

## Split the data by patient condition

Every patient was classified on arrival as a *mild* or *severe* case. Here is the same month, broken out:

| | Mild cases | Severe cases | Overall |
|---|---|---|---|
| **Hospital A** | 7/8 survived (87.5%) | 1/2 survived (50%) | 8/10 (80%) |
| **Hospital B** | 2/2 survived (100%) | 5/8 survived (62.5%) | 7/10 (70%) |

Check every cell. Among mild cases, Hospital B wins: 100% versus 87.5%. Among severe cases, Hospital B wins again: 62.5% versus 50%. Hospital B is better for *every kind of patient there is* — and still loses the overall comparison. The totals add up; nothing is fudged. This reversal is Simpson's paradox.

## Where the reversal comes from

Look at the case mix. Hospital A treated 8 mild patients and only 2 severe ones. Hospital B treated 2 mild and 8 severe. Severe patients die more often *everywhere*, and Hospital B — plausibly the regional trauma center that takes the hardest cases — is drenched in them. Its overall rate is dragged down not by worse care but by a harder job. Hospital A's shiny 80% is mostly a report about the easiness of its caseload.

The aggregate comparison silently assumes the two hospitals faced the same distribution of patients. They did not, and the variable that differs (severity) independently affects the outcome (survival). Whenever a lurking variable is correlated with both group membership and outcome, aggregated rates can point in the opposite direction from every stratum.

**Counterexample recap.** The tempting argument's premises are true — the 80% and 70% figures are exact. Yet a patient who follows its advice makes a worse choice whichever condition they have: mild patients survive at 100% at B versus 87.5% at A; severe patients at 62.5% versus 50%. Premises true, conclusion false; the inference from aggregate rates to "better care" is invalid.

## The valid argument

1. Within every severity stratum, Hospital B's survival rate exceeds Hospital A's.
2. Any individual patient belongs to exactly one stratum, and severity is determined by the patient's condition, not by the choice of hospital.
3. Therefore, for any given patient, Hospital B offers the better survival prospect.

Premise 2 is doing quiet but essential work. The stratified comparison is the right one *because* severity is settled before the hospital choice and influences the outcome on its own. If instead the strata were something the hospital caused — say, splitting patients by "responded well to initial treatment" — conditioning on it would introduce bias rather than remove it. Which breakdown is correct is a question about causal structure, not arithmetic; the numbers alone cannot tell you.

## Carry-away rules

- An overall rate is a weighted average, and the weights (case mix) can differ wildly between groups. Comparing weighted averages with different weights compares apples to fruit salad.
- When a comparison flips under stratification, ask which variable was fixed before the choice you are evaluating. Condition on those; do not condition on downstream effects.
- Treat league tables — hospitals, schools, fund managers — with suspicion until you know who got the hard cases.
