---
id: math-013
category: math
subcategory: combinatorics
difficulty: easy
source_model: fable-5
skills:
  - worked-solution
  - check-your-work
title: Inclusion-exclusion counting students in two clubs
approx_words: 400
---

A school has a chess club and a debate club. 18 students are in chess, 12 in debate, and 5 are in both. How many distinct students are in at least one club?

If you add 18 + 12 you get 30, but the 5 students who do both were counted twice. Inclusion-exclusion subtracts the overlap once:

```
|chess ∪ debate| = |chess| + |debate| − |chess ∩ debate|
                 = 18 + 12 − 5
                 = 25
```

Check with a Venn picture: 13 chess-only, 7 debate-only, 5 both. 13 + 7 + 5 = 25. Same number, two methods.

Limiting case: if nobody is in both, the intersection is 0 and the union is just the sum. If every debate student is also in chess, the union equals the larger set (18). Inclusion-exclusion covers both extremes without a special case.
