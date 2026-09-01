---
id: logic-004
category: logic
subcategory: causal-reasoning
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - counterexample
title: Correlation is not causation
approx_words: 610
---

# Correlation is not causation

Track two numbers for a beach town across a year: monthly ice cream sales and monthly drowning deaths. Plot them and you will see the lines rise and fall together with uncanny precision. High-sales months are high-drowning months. The correlation is real, strong, and reproducible year after year. Does ice cream cause drowning?

## The valid inference

Here is what a strong correlation between A and B legitimately licenses:

1. Ice cream sales and drownings move together far more tightly than chance would produce.
2. Systematic co-movement demands *some* explanation: either A causes B, B causes A, some third factor drives both, or the pattern is a selection artifact in how the data were gathered.
3. Therefore, at least one causal or structural connection exists somewhere in the system — and it is worth locating.

This is genuinely useful reasoning. Correlation is a *clue*, a flare in the night saying "dig here." Epidemiology found the smoking–cancer link, and astronomers found extrasolar planets, by chasing correlations. The valid conclusion stops at: *something* links these variables.

## The tempting invalid cousin

1. Ice cream sales and drownings are strongly correlated.
2. Therefore, ice cream causes drowning (perhaps cramps from eating before swimming?).

The argument leaps from "some link exists" to "this specific arrow exists, pointing this specific way." The premises are compatible with at least three rival structures, and the argument does nothing to eliminate them.

**Counterexample by confounder.** The third factor here is summer heat. Hot weather independently causes people to buy ice cream *and* causes people to swim, and more swimmers means more drownings. Draw it as a fork:

```
        heat
       /    \
      v      v
  ice cream   swimming --> drownings
```

In this world, both premises of the invalid argument are true — the correlation is exactly as strong as claimed — yet the conclusion is false. You could ban ice cream entirely and the drowning numbers would not move, because no causal path runs from cones to the water. One coherent world where premises hold and the conclusion fails: the inference is invalid.

The test that separates the structures is *intervention*. If you force ice cream sales down (close every shop in July) and drownings stay flat, the direct arrow is refuted. If you compare months with equal temperatures — statisticians call this conditioning on the confounder — the ice-cream–drowning correlation evaporates. Correlation that vanishes when you hold the third variable fixed was never causation between the pair.

## Why the mistake is so sticky

Human minds are causation detectors running on correlation data; jumping to the arrow is the default, not a lapse. The jump even works often enough to feel reliable: many correlations *are* causal. The discipline is to hold the four possibilities open — A→B, B→A, confounder, artifact — and ask which observations would distinguish them.

Reverse causation deserves its own caution. "Depressed people exercise less, so lack of exercise causes depression" may have the arrow backwards: depression saps the motivation to exercise. Both directions can even hold at once in a feedback loop, which no single correlation coefficient can reveal.

## Take-away rules

- A correlation supports "these variables are connected somehow," never, by itself, "this one drives that one."
- Before accepting a causal claim, ask: what happens under intervention? What does the relationship look like with the plausible confounders held fixed?
- When you cannot intervene, look for natural experiments — cases where the suspected cause changed for reasons unrelated to the outcome.

Ice cream is innocent. Summer had motive and opportunity all along.
