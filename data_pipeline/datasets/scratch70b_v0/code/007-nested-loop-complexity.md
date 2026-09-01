---
id: code-007
category: code
subcategory: complexity
difficulty: easy
source_model: fable-5
skills:
  - complexity
  - worked-solution
title: Why n squared is not twice as slow as n
approx_words: 570
---

A common early misconception: "this algorithm is \(O(n^2)\) and that one is \(O(n)\), so the first is about twice as slow." The exponent gets read as a multiplier. It is not a multiplier — it is a statement about how cost *scales*, and the gap it creates grows without bound.

## Two functions, one job

Both of these check whether a list contains a duplicate:

```python
def has_dup_quadratic(a):
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] == a[j]:
                return True
    return False

def has_dup_linear(a):
    seen = set()
    for x in a:
        if x in seen:
            return True
        seen.add(x)
    return False
```

## Counting the work on n = 4

Take `a = [7, 3, 9, 5]` (no duplicates, so both run to completion — the worst case).

The nested version compares every pair once: `i = 0` pairs with indices 1, 2, 3 (three comparisons); `i = 1` with 2, 3 (two); `i = 2` with 3 (one). Total \(3 + 2 + 1 = 6\) comparisons, which is \(\binom{4}{2} = \frac{4 \cdot 3}{2}\).

The set version does 4 membership checks and 4 insertions: 8 constant-time operations.

At \(n = 4\) the difference is a shrug. Now scale \(n\) and watch the *ratio*, not the difference:

| n         | pairwise comparisons ≈ n²/2 | set operations ≈ 2n | ratio    |
|-----------|-----------------------------|---------------------|----------|
| 4         | 6                           | 8                   | ~1x      |
| 100       | 4,950                       | 200                 | ~25x     |
| 10,000    | ~50 million                 | 20,000              | ~2,500x  |
| 1,000,000 | ~500 billion                | 2 million           | ~250,000x |

If one operation takes a nanosecond, the linear scan at a million elements finishes in about 2 milliseconds. The quadratic one takes roughly 8 minutes. Same machine, same data, and no constant-factor optimization — a better compiler, a faster CPU — closes that gap, because doubling hardware speed merely halves both times while the ratio keeps growing with \(n\).

## The doubling test

Here is the cleanest way to internalize the difference. Ask: *what happens when the input doubles?*

- \(O(n)\): double the input, double the time. \(2n\) vs \(n\).
- \(O(n^2)\): double the input, **quadruple** the time. \((2n)^2 = 4n^2\).
- Ten-x the input: linear cost goes up 10x, quadratic cost goes up 100x.

So "twice as slow" is not even a coherent claim about a quadratic algorithm — its slowdown factor depends on \(n\) and increases forever. At \(n = 10\) the quadratic version might genuinely be faster (fewer allocations, better cache behavior, no hashing); at \(n = 10^6\) it is unusable. Big-O tells you which regime you will end up in as data grows, not who wins the sprint.

## Bug-note corollary: accidental quadratics

Most quadratic code in the wild is not a deliberate nested loop. It hides:

```python
out = ""
for chunk in chunks:
    out += chunk        # each += copies the whole string so far
```

Each concatenation copies everything accumulated, so the total work is \(1 + 2 + \dots + n \approx n^2/2\) character copies — the same triangular sum as the pairwise loop above, wearing a disguise. The fix, `"".join(chunks)`, is linear. Similar traps: `list.insert(0, x)` in a loop, `x in some_list` inside a loop, repeated `del a[0]`.

The reviewing habit that catches these: for every loop, ask "does the work *inside* this iteration secretly depend on \(n\)?" If yes, you have \(n \cdot n\), whatever the indentation says.
