---
id: code-009
category: code
subcategory: algorithms
difficulty: easy
source_model: fable-5
skills:
  - worked-solution
  - complexity
title: Prefix sums for constant-time range queries
approx_words: 600
---

Suppose you hold daily sales figures and repeatedly need totals over date ranges: "sum of days 2 through 5," "sum of days 0 through 3," hundreds of such questions. Summing the slice each time works, but every query pays for the range's full length. Prefix sums pay once up front and then answer every query with a single subtraction.

## Building the prefix array

Work with `a = [3, 1, 4, 1, 5, 9]`. Define `P[i]` as the sum of the first `i` elements — note *count*, not *index*, which is why `P` has one extra slot:

```python
def build_prefix(a):
    P = [0] * (len(a) + 1)
    for i, x in enumerate(a):
        P[i + 1] = P[i] + x
    return P

def range_sum(P, l, r):
    """Sum of a[l..r] inclusive."""
    return P[r + 1] - P[l]
```

Filling `P` step by step for our array:

| i | a[i] | P[i+1] = P[i] + a[i] |
|---|------|----------------------|
| 0 | 3    | 0 + 3 = 3            |
| 1 | 1    | 3 + 1 = 4            |
| 2 | 4    | 4 + 4 = 8            |
| 3 | 1    | 8 + 1 = 9            |
| 4 | 5    | 9 + 5 = 14           |
| 5 | 9    | 14 + 9 = 23          |

So `P = [0, 3, 4, 8, 9, 14, 23]`. Reading it: `P[3] = 8` means "the first three elements sum to 8."

## Answering a query

Sum of `a[2..4]` (the slice `4, 1, 5`, which should be 10):

```
range_sum(P, 2, 4) = P[5] - P[2] = 14 - 4 = 10  ✓
```

Why it works: `P[5]` is everything through index 4, `P[2]` is everything through index 1. Subtracting cancels the shared prefix `a[0..1]`, leaving exactly `a[2..4]`. Every range is the difference of two prefixes.

The leading zero earns its keep on queries touching the left edge: sum of `a[0..2]` is `P[3] - P[0] = 8 - 0 = 8`. Without the sentinel slot you would special-case `l == 0`, and that special case is where the off-by-one bugs breed.

## Bug note: the off-by-one zoo

Two errors account for nearly all broken prefix-sum code. First, writing `P[r] - P[l]`, which computes `a[l..r-1]` — a half-open range — while the caller expects inclusive. Neither convention is wrong, but mixing them silently drops the last element. Second, sizing `P` as `len(a)` instead of `len(a) + 1`, which forces the `l == 0` special case back in. Pick the convention `P[i] = sum of first i elements`, keep the extra slot, and test one edge query (`l = 0`) plus one single-element query (`l == r`) before trusting anything.

## Complexity accounting

Build: one pass, \(O(n)\) time, \(O(n)\) extra space. Each query: two array reads and one subtraction, \(O(1)\).

Compare against re-summing per query: with \(n\) elements and \(q\) queries of average length \(k\), naive costs \(O(q \cdot k)\); prefix sums cost \(O(n + q)\). At \(n = 10^5\) values and \(q = 10^5\) queries, that is the difference between ~\(10^{9}\)-ish operations and ~\(2 \times 10^5\).

The trade-off appears when the array *changes*: a single update `a[i] = v` invalidates every `P[j]` with `j > i`, an \(O(n)\) repair. Prefix sums fit the "build once, query many" regime. If updates and queries interleave, the successor structures — Fenwick trees or segment trees — restore balance at \(O(\log n)\) for both.

The idea generalizes past sums: any invertible, associative accumulation works (XOR ranges via prefix XOR; count of even numbers via prefix counts), and the 2-D version — summing rectangles via inclusion–exclusion on a prefix grid — is the same subtraction trick applied twice.
