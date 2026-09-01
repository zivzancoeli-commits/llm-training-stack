---
id: code-003
category: code
subcategory: algorithms
difficulty: easy
source_model: fable-5
skills:
  - worked-solution
  - complexity
title: Factorial two ways and the stack-depth trap
approx_words: 590
---

Factorial is the "hello world" of recursion, which makes it a good place to see what recursion actually costs at runtime. Both versions below compute the same values, but they behave very differently when \(n\) gets large.

```python
def fact_rec(n):
    if n <= 1:
        return 1
    return n * fact_rec(n - 1)

def fact_iter(n):
    acc = 1
    for k in range(2, n + 1):
        acc *= k
    return acc
```

## Walking through n = 4

The recursive call `fact_rec(4)` does not multiply anything immediately. It must first learn the value of `fact_rec(3)`, which must first learn `fact_rec(2)`, and so on. Each pending call is parked on the call stack:

```
fact_rec(4)                      -> waits for fact_rec(3)
  fact_rec(3)                    -> waits for fact_rec(2)
    fact_rec(2)                  -> waits for fact_rec(1)
      fact_rec(1)  returns 1     (base case)
    fact_rec(2)  returns 2 * 1 = 2
  fact_rec(3)  returns 3 * 2 = 6
fact_rec(4)  returns 4 * 6 = 24
```

At the deepest moment, four stack frames are alive simultaneously. Each frame holds its own `n`, the return address, and bookkeeping — memory that exists only to remember "multiply by my `n` once the inner call finishes."

The iterative version at `n = 4` walks `k = 2, 3, 4`, updating one accumulator: `acc = 2`, then `6`, then `24`. One frame, one variable, done.

## The stack-depth issue

Both functions perform \(n - 1\) multiplications, so their time complexity matches: \(O(n)\) multiplications (each multiplication itself gets slower as the integers grow, but that affects both equally). The difference is space: the recursion uses \(O(n)\) stack frames, the loop uses \(O(1)\).

That space cost is not theoretical. CPython caps recursion depth (the default limit is 1000) precisely because each frame consumes real memory and a runaway recursion would otherwise crash the interpreter at the C level:

```python
>>> fact_rec(5000)
RecursionError: maximum recursion depth exceeded
>>> fact_iter(5000)   # fine; a 16,326-digit integer
```

You can raise the limit with `sys.setrecursionlimit`, but that trades a clean Python exception for the risk of an actual segfault when the OS thread stack overflows. It treats the symptom, not the cause.

## Doesn't tail-call optimization fix this?

In some languages, yes. `fact_rec` as written is *not* tail-recursive — after the inner call returns, there is still a pending multiplication by `n`. A tail-recursive variant threads the accumulator through the call:

```python
def fact_tail(n, acc=1):
    if n <= 1:
        return acc
    return fact_tail(n - 1, acc * n)   # nothing left to do after the call
```

Scheme or an optimizing functional compiler would turn this into a loop, reusing one frame. CPython deliberately does not: Guido has long argued that eliminating frames destroys tracebacks. So in Python, `fact_tail` still consumes \(O(n)\) stack and still hits the recursion limit. The tail-recursive shape is exactly the shape that converts mechanically to `fact_iter` — in Python you just have to do that conversion yourself.

## Bug note and takeaway

A subtle robustness difference: `fact_rec(-3)` hits the `n <= 1` base case and quietly returns 1, and so does `fact_iter(-3)` because `range(2, -2)` is empty. Both silently accept nonsense input; if factorial of a negative number should be an error, validate explicitly rather than relying on the base case.

The general rule: recursion is the right tool when the *structure* is recursive and depth is bounded by something small, like the height of a balanced tree (\(O(\log n)\)). When depth scales linearly with input size, as in factorial, prefer the loop — same time, constant space, no limit to trip over.
