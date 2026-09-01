---
id: math-002
category: math
subcategory: probability
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - check-your-work
title: Bayes rule with a medical false-positive example and a tree check
approx_words: 640
---

Here is a question that trips up doctors, lawyers, and most people meeting it for the first time.

A disease affects 1 in 1,000 people. A screening test catches 99% of people who have the disease (sensitivity 0.99). Among healthy people, it wrongly comes back positive 5% of the time (false-positive rate 0.05). You test positive. What is the probability you actually have the disease?

The instinctive answer is "about 99%," because the test is 99% accurate at detecting the disease. That instinct is wrong, and Bayes rule explains why: it forces you to weigh how rare the disease is against how common false alarms are.

Bayes rule says P(disease | positive) = P(positive | disease) * P(disease) / P(positive). The numerator is the "true positive" pathway. The denominator is all the ways a positive can happen, true or false:

P(positive) = P(positive | disease) * P(disease) + P(positive | healthy) * P(healthy)

Plug in the numbers. P(disease) = 0.001, so P(healthy) = 0.999.

Numerator: 0.99 * 0.001 = 0.00099
Denominator: 0.99 * 0.001 + 0.05 * 0.999 = 0.00099 + 0.04995 = 0.05094

P(disease | positive) = 0.00099 / 0.05094, which is about 0.0194, roughly 1.9%.

A positive result moved you from a 0.1% chance to about a 2% chance. That is a twenty-fold update, which is real information, but it is nowhere near 99%. The disease is so rare that the small false-positive rate applied to the huge healthy population produces far more false alarms than the excellent sensitivity produces true detections.

Now the tree check, which is how you should verify any Bayes computation. Imagine 100,000 people, and split them the way the probabilities dictate.

- 100,000 people total.
- Sick branch: 0.001 * 100,000 = 100 people have the disease. Of these, 99% test positive: 99 true positives, 1 false negative.
- Healthy branch: 99,900 people are healthy. Of these, 5% test positive: 0.05 * 99,900 = 4,995 false positives; the other 94,905 test negative.

Total positives: 99 + 4,995 = 5,094. Of those, only 99 are genuinely sick. So the probability of disease given a positive test is 99 / 5,094, about 1.94%. Same answer as the formula, and now you can see the mechanism: the room full of positive-testers contains 99 sick people standing next to 4,995 healthy people who got unlucky.

The tree also lets you sanity-check the pieces. All four leaf counts (99, 1, 4,995, 94,905) must add back to 100,000; they do. If your leaves don't sum to the population, you've mixed up a conditional probability with a joint one somewhere.

The common mistake has a name: confusing P(positive | disease) with P(disease | positive). The test's 99% is the first quantity, a property of the test measured on sick people. The question asks for the second quantity, a property of your situation, and the two can differ wildly whenever the prior P(disease) is small. Transposing them is sometimes called the prosecutor's fallacy, because it also appears in courtrooms: "the probability of this DNA match if the defendant were innocent is one in a million" is not the same as "the probability the defendant is innocent given the match."

A useful closing habit: before computing, ask what the base rate is. If the condition is rare, expect a positive test to be dominated by false alarms, and expect the honest answer to be "get a second, independent test." Run the numbers again with a prior of 2% (the posterior we just computed) and the same test: a second positive pushes you to roughly 29%, and a third to about 89%. Repeated independent evidence is how a weak posterior becomes a strong one, and Bayes rule is the bookkeeping that keeps each update honest.
