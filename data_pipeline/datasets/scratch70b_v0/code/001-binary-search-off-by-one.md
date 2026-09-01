---
id: code-001
category: code
subcategory: algorithms
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - debugging
title: Binary search off-by-one that never terminates
approx_words: 620
---

Binary search is famous for being easy to describe and easy to get wrong. The most common failure is not returning a wrong index — it is looping forever. Let's build the bug on purpose, watch it spin, and then fix it.

Here is a version that looks reasonable but contains the classic mistake:

```python
def find_leftmost(a, target):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < target:
            lo = mid          # BUG: should be mid + 1
        else:
            hi = mid
    return lo if a and a[lo] == target else -1
```

The intent is a "leftmost occurrence" search: shrink the range until `lo == hi`, keeping the invariant that the answer, if it exists, stays inside `[lo, hi]`.

## Tracing the infinite loop

Take `a = [3, 5]` and `target = 5`.

- Iteration 1: `lo = 0`, `hi = 1`, so `mid = (0 + 1) // 2 = 0`. We compare `a[0] = 3 < 5`, take the first branch, and set `lo = mid = 0`.
- Iteration 2: `lo` is still 0, `hi` is still 1. Nothing changed. `mid` is 0 again, the comparison goes the same way, and we assign `lo = 0` again.

The loop condition `lo < hi` is still true, and the state is identical to the previous iteration, so the program spins forever. The root cause: integer division floors, so when the window has exactly two elements, `mid` equals `lo`. Assigning `lo = mid` fails to shrink the window. A loop that does not strictly reduce its search space has no termination guarantee.

## The fix

Since the branch `a[mid] < target` proves the answer cannot be at `mid` itself, we are allowed — and required — to exclude it:

```python
def find_leftmost(a, target):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < target:
            lo = mid + 1      # exclude mid: it is too small
        else:
            hi = mid          # mid might be the answer; keep it
    return lo if a and a[lo] == target else -1
```

Re-run the trace with `a = [3, 5]`, `target = 5`:

- Iteration 1: `mid = 0`, `a[0] = 3 < 5`, so `lo = 1`. Now `lo == hi == 1`, the loop exits, and `a[1] == 5`, so we return `1`. Correct, and it took one step.

Note the asymmetry: `hi = mid` is safe here because `mid` is computed with floor division, which biases toward `lo`. When the window has two elements, `mid == lo`, so `hi = mid` shrinks the window from the right. If you instead wrote a "rightmost occurrence" search where the surviving branch is `lo = mid`, you would need to bias `mid` upward with `mid = (lo + hi + 1) // 2`, or the same two-element trap reappears on the other side.

## A useful mental checklist

1. **State the invariant.** Example: "the leftmost index of `target`, if present, always lies in `[lo, hi]`."
2. **Prove progress.** In every branch, either `lo` strictly increases or `hi` strictly decreases. Check specifically the two-element window, because floor division makes `mid == lo` there.
3. **Match the exit to the invariant.** With `while lo < hi`, the loop ends with a single candidate to verify. With `while lo <= hi`, the loop ends with an empty range, and you must have returned mid-loop on a hit.

## Complexity note

The corrected search halves the window each iteration, so it runs in \(O(\log n)\) comparisons and \(O(1)\) extra space. The buggy version has no complexity at all in the usual sense — its worst case is nontermination, which is worse than any polynomial. That is why "does the search space strictly shrink?" is the first question to ask when reviewing any binary search.
