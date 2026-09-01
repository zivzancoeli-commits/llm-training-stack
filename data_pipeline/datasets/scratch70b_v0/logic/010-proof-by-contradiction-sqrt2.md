---
id: logic-010
category: logic
subcategory: proof-technique
difficulty: hard
source_model: fable-5
skills:
  - worked-solution
  - counterexample
title: Proof by contradiction and the square root of two
approx_words: 640
---

# Proof by contradiction: the square root of two is irrational

Proof by contradiction works like this: to prove a claim, assume its opposite, reason correctly until you hit an impossibility, and conclude the opposite cannot stand. Since the assumption's failure is the claim's success, you are done. The classic showcase is the irrationality of √2.

## The claim

There are no whole numbers a and b (b nonzero) with (a/b)² = 2. In other words, √2 is not a ratio of integers.

## The proof, sketched carefully

**Step 1 — assume the opposite.** Suppose √2 *is* rational: √2 = a/b for some positive integers a, b. Crucially, we may insist the fraction is in lowest terms — a and b share no common factor greater than 1 — because any fraction can be fully reduced first. Flag this; the contradiction will strike exactly here.

**Step 2 — clear the square root.** Squaring both sides: 2 = a²/b², so

> a² = 2b².

**Step 3 — a must be even.** The right side is 2 times an integer, so a² is even. Could a be odd? An odd number has the form 2k+1, and (2k+1)² = 4k² + 4k + 1 = 2(2k² + 2k) + 1, which is odd. So odd numbers have odd squares; since a² is even, a must be even. Write a = 2c.

**Step 4 — b must be even too.** Substitute: (2c)² = 2b², so 4c² = 2b², so

> b² = 2c².

The same argument now runs on b: b² is even, so b is even.

**Step 5 — contradiction.** Both a and b are even, so both are divisible by 2. But Step 1 stipulated they share no common factor. The assumption has torn itself apart: it demanded a fully reduced fraction and then forced that fraction to be reducible. No such a and b can exist, so √2 is irrational. ∎

Notice the proof's honest structure: every step from the assumption onward is ordinary, checkable algebra. The absurdity is not sprinkled in; it is *derived*. That is what licenses the final reversal.

## The tempting invalid cousin

A pattern that impersonates this proof:

1. Assume my opponent's position.
2. Derive something *false, surprising, or unwelcome* — using an extra premise I slipped in along the way.
3. Declare the opponent's position refuted.

**Counterexample.** "Assume the earth is round. Then people in the southern hemisphere would be upside down and would fall off. Nobody falls off. Therefore the earth is flat." The structure looks identical to the √2 proof, but the absurdity does not follow from roundness alone — it follows from roundness *plus* the smuggled premise that "down" is a universal direction rather than "toward the center of mass." When a contradiction pops out of a bundle of assumptions, logic only tells you *some member of the bundle* is false. The honest conclusion was: roundness and naive-down cannot both be true. The arguer pinned the blame on the target and quietly acquitted the smuggled premise.

A second corruption: deriving something merely *counterintuitive* rather than contradictory. "Assume time has no beginning; then an infinite past has already elapsed; how strange; therefore time began." Strangeness is not impossibility. The √2 proof did not end at "a and b are both even, which is weird" — evenness is fine — but at a flat violation of a stipulation made under our full control.

## What makes the real thing work

- The absurdity must be a genuine contradiction (P and not-P), not a discomfort.
- Every auxiliary premise must be one *both sides accept*, so the assumed claim alone bears the blame.
- Each derivation step must be independently valid.

Meet those three conditions and contradiction is among the most powerful tools in mathematics. Miss any one, and you have theater.
