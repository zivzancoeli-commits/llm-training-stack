---
id: code-011
category: code
subcategory: algorithms
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - complexity
title: Counting calls in naive vs memoized Fibonacci
approx_words: 640
---

Fibonacci is the cleanest demonstration of why caching changes an algorithm's complexity class rather than merely speeding it up. We will count actual function calls at \(n = 6\), not just wave at big-O.

```python
calls = 0

def fib_naive(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

def fib_memo(n, cache={0: 0, 1: 1}):
    global calls
    calls += 1
    if n not in cache:
        cache[n] = fib_memo(n - 1) + fib_memo(n - 2)
    return cache[n]
```

(The mutable-default cache is used deliberately here as a compact demo; in production, `functools.lru_cache` states the intent without the pitfall.)

## Counting naive calls at n = 6

Let \(C(n)\) be the number of calls `fib_naive(n)` triggers, including itself. Base cases cost one call: \(C(0) = C(1) = 1\). Otherwise \(C(n) = 1 + C(n-1) + C(n-2)\). Building up:

| n | C(n) = 1 + C(n−1) + C(n−2) |
|---|-----------------------------|
| 0 | 1                           |
| 1 | 1                           |
| 2 | 1 + 1 + 1 = 3               |
| 3 | 1 + 3 + 1 = 5               |
| 4 | 1 + 5 + 3 = 9               |
| 5 | 1 + 9 + 5 = 15              |
| 6 | 1 + 15 + 9 = **25**         |

Twenty-five calls to compute `fib(6) = 8`. The waste is repetition: expanding the call tree shows `fib(4)` computed twice, `fib(3)` three times, `fib(2)` five times, `fib(1)` eight times, `fib(0)` five times. Those multiplicities are themselves Fibonacci numbers — the tree re-derives the same subproblems in Fibonacci-many places. Since \(C(n) \approx 2 \cdot \mathrm{fib}(n+1)\) and Fibonacci grows as \(\phi^n \approx 1.618^n\), the naive version is exponential. At \(n = 40\) it makes about 330 million calls; at \(n = 100\), more calls than atoms in a bathtub.

## Counting memoized calls at n = 6

With memoization, each value from 2 to 6 is *computed* once; further requests hit the cache and return without recursing. Trace it: `fib_memo(6)` misses, calls `fib_memo(5)`; that misses, calls `fib_memo(4)`; misses cascade down to `fib_memo(2)`, which calls `fib_memo(1)` (cache hit, base) and `fib_memo(0)` (hit). Unwinding, each level's second operand — `fib_memo(3)` inside 5, `fib_memo(4)` inside 6, etc. — is now a one-call cache hit.

The clean way to tally: the root call to `fib_memo(6)` is 1 call, and every value that *misses* the cache spawns exactly 2 child calls, while cache hits spawn none. The missing values are 6, 5, 4, 3, and 2 — five of them. Total: \(1 + 2 \times 5 = 11\) calls. Eleven versus twenty-five.

The gap widens brutally with \(n\): memoized calls grow *linearly* (about \(2n - 1\), naive calls grow *exponentially*. At \(n = 40\): 79 calls versus ~331 million.

## Complexity and a stack caveat

Memoized Fibonacci: \(O(n)\) time, \(O(n)\) space for the cache plus \(O(n)\) recursion depth. That depth matters in Python — `fib_memo(2000)` on a cold cache exceeds the default recursion limit. The bottom-up rewrite keeps \(O(n)\) time, drops to \(O(1)\) space, and cannot overflow:

```python
def fib_iter(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

The transferable lesson: when a recursion's call tree contains repeated subproblems (overlapping subproblems, in DP vocabulary), caching collapses the tree to one node per distinct subproblem. Count distinct subproblems, multiply by per-subproblem work, and you have the memoized complexity — here, \(n+1\) subproblems at \(O(1)\) each.
