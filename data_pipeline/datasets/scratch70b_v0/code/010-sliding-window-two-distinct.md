---
id: code-010
category: code
subcategory: algorithms
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - complexity
title: Sliding window for at most two distinct characters
approx_words: 650
---

Problem: given a string, find the length of the longest substring containing at most 2 distinct characters. For `"abaccc"` the answer is 4 — the substring `"accc"` uses only `a` and `c`.

The brute-force framing checks all \(O(n^2)\) substrings, testing each for the distinct-count property. The sliding-window insight is that we never need to re-examine a substring from scratch: maintain one window `[left, right]` that always satisfies the constraint, extend it rightward greedily, and shrink from the left only when the constraint breaks.

```python
def longest_two_distinct(s):
    count = {}                       # char -> occurrences inside window
    left = 0
    best = 0
    for right, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        while len(count) > 2:        # constraint broken: too many distinct
            lc = s[left]
            count[lc] -= 1
            if count[lc] == 0:
                del count[lc]        # crucial: forget fully-evicted chars
            left += 1
        best = max(best, right - left + 1)
    return best
```

## Full trace on "abaccc"

| right | char | count after add     | shrink?                                   | window    | best |
|-------|------|---------------------|-------------------------------------------|-----------|------|
| 0     | a    | {a:1}               | no                                        | `a`       | 1    |
| 1     | b    | {a:1, b:1}          | no                                        | `ab`      | 2    |
| 2     | a    | {a:2, b:1}          | no                                        | `aba`     | 3    |
| 3     | c    | {a:2, b:1, c:1} — 3 distinct | evict `a` (a:1), evict `b` (b:0, delete) → {a:1, c:1}, left = 2 | `ac` | 3 |
| 4     | c    | {a:1, c:2}          | no                                        | `acc`     | 3    |
| 5     | c    | {a:1, c:3}          | no                                        | `accc`    | 4    |

Answer: 4. The interesting step is `right = 3`: adding `c` makes three distinct characters, so the `while` loop advances `left` past positions 0 and 1, decrementing counts as those characters leave. Once `b`'s count hits zero it is deleted from the map, restoring `len(count) == 2`, and the scan resumes without ever revisiting old positions.

## Why this is linear, not quadratic

The nested `while` looks suspicious — a loop inside a loop usually means \(O(n^2)\). The saving argument is *amortized*: `left` only ever moves rightward, and it can move at most \(n\) times over the entire run. So the total work of all shrink steps combined is \(O(n)\), regardless of how it clusters. Add the \(n\) extension steps and the whole algorithm is \(O(n)\) time. Space is \(O(1)\) here because the map never holds more than 3 keys (and \(O(k)\) for the general "at most k distinct" variant, which this code handles by changing the literal `2`).

This amortization argument is the heart of every sliding-window proof, and it is worth rehearsing until it feels obvious: measure total pointer movement across the whole execution, not per-iteration cost.

## Bug note: the deletion you must not skip

The line `del count[lc]` is where implementations quietly break. If you leave zero-count entries in the map, `len(count)` counts characters that are no longer in the window, the `while` condition `len(count) > 2` misfires, and the window shrinks far more than necessary — the code returns answers that are too small, and only on inputs where a character fully exits and later returns. A test case that catches it: `"abcbb"` should give 4 (`"bcbb"` uses only `b` and `c`); the zero-retaining version keeps a ghost entry for `a` after eviction and undershoots. Silent wrong-answer bugs beat crashes for longevity, so this one deserves a regression test.

The window pattern generalizes wherever the constraint is *monotone* — if a window violates it, every superset does too. "At most k distinct," "sum ≤ S with nonnegative values," "no repeated characters" all qualify. When a constraint is not monotone (say, "exactly k distinct"), the plain two-pointer window stops working directly, and the standard trick is to compute atMost(k) − atMost(k−1).
