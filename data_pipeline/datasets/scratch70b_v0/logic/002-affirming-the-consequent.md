---
id: logic-002
category: logic
subcategory: deduction
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - counterexample
title: Affirming the consequent
approx_words: 560
---

# Affirming the consequent

Every conditional statement has two halves: the *antecedent* (the "if" part) and the *consequent* (the "then" part). Which half you affirm decides whether your argument is valid or worthless.

## The valid form

Consider:

1. If the battery is dead, the car will not start.
2. The battery is dead.
3. Therefore, the car will not start.

This is *modus ponens*: we affirm the antecedent ("the battery is dead") and validly conclude the consequent. Given the premises, the conclusion cannot fail. If someone accepts 1 and 2 but denies 3, they have contradicted themselves.

## The invalid cousin

Now the version that mechanics hear every day:

1. If the battery is dead, the car will not start.
2. The car will not start.
3. Therefore, the battery is dead.

This affirms the *consequent* ("the car will not start") and tries to march backwards to the antecedent. It feels persuasive because dead batteries really are a common cause of no-start conditions. But the premise never said dead batteries are the *only* cause.

**Counterexample.** The battery is fully charged, but the starter motor has failed. Premise 1 remains true. Premise 2 is true — the car will not start. The conclusion is false. The premises are consistent with many worlds, and in some of those worlds the conclusion fails. That is the definition of an invalid argument.

## The four forms at a glance

Given the conditional "if P, then Q":

| You learn... | You conclude... | Name | Valid? |
|---|---|---|---|
| P is true | Q is true | Modus ponens | Yes |
| Q is false | P is false | Modus tollens | Yes |
| Q is true | P is true | Affirming the consequent | **No** |
| P is false | Q is false | Denying the antecedent | **No** |

The two valid rows travel *with* the arrow: forward from P, or backward along the contrapositive from not-Q. The two invalid rows travel *against* it.

## Why the fallacy is tempting

Affirming the consequent is not random noise; it is broken probabilistic reasoning dressed up as deduction. If dead batteries cause 60% of no-starts in your experience, then "the car won't start" genuinely is *evidence* for "the battery is dead" — it raises the probability. The mistake is treating raised probability as certainty. Deductive validity demands that the conclusion hold in *every* situation consistent with the premises, not merely the most familiar one.

Science trips on this constantly. "If my theory is true, the experiment will show X. The experiment showed X. Therefore my theory is true" is affirming the consequent. A rival theory might predict X too. The honest version is weaker: the observation *supports* the theory, and supports it more strongly when few rivals predict the same result. That is why scientists prize experiments whose predicted outcome would be surprising under every competing explanation.

## A repair kit

When you catch yourself concluding P from "if P then Q" and Q, do one of two things:

- **Weaken the conclusion**: "Q makes P more likely," then ask how much, given the alternatives.
- **Strengthen the premise**: if you can honestly assert "Q *only if* P" — Q has no other route — then the inference becomes valid, because "Q only if P" means Q → P, and you are now doing modus ponens with the arrow pointing the right way.

Either move is respectable. Sliding between them without noticing is the fallacy.
