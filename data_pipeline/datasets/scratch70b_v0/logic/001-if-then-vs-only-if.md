---
id: logic-001
category: logic
subcategory: deduction
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - counterexample
title: If-then vs only-if
approx_words: 600
---

# If-then vs only-if

"If it rains, the street gets wet" and "the street gets wet only if it rains" sound like restatements of each other. They are not, and the difference is the source of a whole family of reasoning mistakes.

## What "if" claims

Take the sentence:

> If it rains, then the street is wet.

Write it as *rain → wet*. The claim is one-directional: rain is enough to guarantee a wet street. It says nothing about what else could wet the street. A street cleaner, a burst pipe, or a neighbor washing a car can all soak the pavement on a cloudless day, and the sentence remains perfectly true.

A valid argument using this sentence looks like:

1. If it rains, the street is wet.
2. It is raining.
3. Therefore, the street is wet.

This form is called *modus ponens*: affirm the "if" part, conclude the "then" part. There is no possible situation where premises 1 and 2 hold and the conclusion fails, which is exactly what validity means.

Equally valid is the contrapositive direction:

1. If it rains, the street is wet.
2. The street is dry.
3. Therefore, it is not raining.

If rain guaranteed wetness, a dry street rules rain out. This is *modus tollens*, and it is just as airtight.

## What "only if" claims

Now compare:

> The street is wet only if it rained.

This flips the arrow: *wet → rain*. It asserts that rain is the *only* route to a wet street — no street cleaners, no pipes. In symbols, "A only if B" means A → B, not B → A. English hides this because "if" appears in both sentences, but the logical content points in opposite directions.

## The tempting invalid cousin

Here is the argument that trips people up:

1. If it rains, the street is wet.
2. The street is wet.
3. Therefore, it rained.

This *feels* reasonable, especially if rain is the most common cause of wet streets in your town. But it silently swaps "if it rains, the street is wet" for "the street is wet only if it rains." The premise licenses travel from rain to wetness; the argument travels from wetness to rain, against the arrow.

**Counterexample.** Suppose a street-cleaning truck sprayed the block at dawn under a clear sky. Premise 1 is still true (rain, had it occurred, would have wet the street). Premise 2 is true (the street is visibly wet). The conclusion is false (it did not rain). One concrete situation where the premises hold and the conclusion fails is all it takes: the argument form is invalid, no matter how often it happens to land on the right answer.

## A quick test you can reuse

When you meet a conditional, ask two separate questions:

- **Is the condition sufficient?** Does A, by itself, guarantee B? That is what "if A then B" claims.
- **Is the condition necessary?** Is A the only way to get B? That is what "B only if A" claims.

Rain is sufficient for a wet street but not necessary. Being 18 is necessary for voting in many countries but not sufficient (you also need citizenship and registration). Some conditions are both: being an unmarried man is both necessary and sufficient for being a bachelor, which is why "if and only if" gets its own phrase.

The habit to build: whenever you hear "if," pause and ask which direction the arrow points before you let the argument carry you across it. Most conditional fallacies are just arrows walked backwards.
