---
id: math-015
category: math
subcategory: statistics
difficulty: easy
source_model: fable-5
skills:
  - worked-solution
  - concept-contrast
  - check-your-work
title: Mean vs median on a skewed income-like list of 9 numbers
approx_words: 600
---

The mean and the median both claim to describe a "typical" value, and on lopsided data they can disagree so badly that choosing the wrong one amounts to misinformation. Incomes are the classic case, so let's build a small income-like list and watch the two statistics come apart.

Nine people work at a small firm. Their annual salaries, in thousands of dollars:

32, 35, 38, 41, 44, 47, 52, 58, 495

Eight ordinary salaries and one founder who pays herself 495.

The median is the middle value once the list is sorted. The list is already sorted, it has 9 entries, and the middle is the 5th (four values below, four above): median = 44. Half the staff earns 44 or less, half earns 44 or more.

The mean is the sum divided by the count. Add carefully, in stages so the addition is checkable: 32 + 35 + 38 = 105; 41 + 44 + 47 = 132; 52 + 58 = 110. Then 105 + 132 + 110 = 347, and 347 + 495 = 842. Mean = 842 / 9 ≈ 93.6.

So the "average salary" at this firm is about 93.6 thousand — more than double what eight of the nine employees actually make, and higher than every single salary except the founder's. Nothing is wrong with the arithmetic; the mean is doing what it always does, letting every dollar vote. The founder's 495 contributes as much to the sum as five ordinary employees combined, so she drags the average toward herself. The median, which only cares about order, barely notices her: replace 495 with 4,950 and the median stays exactly 44 while the mean quadruples to about 588.6. That property is called robustness — the median resists outliers; the mean does not.

Verify the median claim by counting: below 44 sit {32, 35, 38, 41}, four values; above sit {47, 52, 58, 495}, four values. Balanced, as required. Verify the mean differently: if 93.6 is the mean, then 9 * 93.6 should recover the total: 9 * 93.6 = 842.4 ≈ 842 (the small gap is rounding). Multiplying the mean back by the count is the standard mean-check and catches most addition slips.

Which statistic should you report? It depends on the question. "What does a typical employee here earn?" wants the median; 44 describes the experience of the people in the building, and 93.6 describes no one. "What is the firm's total payroll?" wants the mean, since payroll = mean * headcount = 842, and the median tells you nothing about totals (median * 9 = 396, off by more than half). Means answer questions about sums; medians answer questions about typical individuals. Skewed data doesn't make either statistic wrong — it makes the choice consequential.

The common mistake is treating "average" as a synonym for "typical" without checking the shape of the data. A rental listing site advertising "average rent in this neighborhood: $2,900" may be arithmetically honest while a handful of luxury penthouses hide the fact that the median unit rents for $1,800. The diagnostic is free: compute both. When mean and median roughly agree, the data is roughly symmetric and either serves. When the mean sits far above the median, suspect a long right tail (a few huge values); far below, a long left tail. The gap between the two statistics is itself information — in our firm it's 93.6 - 44 ≈ 50, a flashing sign reading "someone up top is skewing this."

Habit to keep: never summarize a list with one number until you've at least glanced at both, and when someone hands you only an "average," ask which one and what the other says.
