---
id: code-012
category: code
subcategory: bit-manipulation
difficulty: easy
source_model: fable-5
skills:
  - worked-solution
  - complexity
title: Finding the unpaired number with XOR
approx_words: 560
---

Puzzle: every number in a list appears exactly twice, except one that appears once. Find it. The obvious solutions — sort and scan for the lonely element (\(O(n \log n)\)), or count with a hash map (\(O(n)\) time but \(O(n)\) extra space) — both work. XOR does it in one pass with a single integer of state.

```python
def find_unpaired(a):
    acc = 0
    for x in a:
        acc ^= x
    return acc
```

## The three properties that make it work

XOR (`^`) compares bits: the result bit is 1 where the operands differ. Three algebraic facts carry the whole trick:

1. **Self-inverse:** `x ^ x == 0`. A number cancels itself.
2. **Identity:** `x ^ 0 == x`. Zero is a no-op.
3. **Commutative and associative:** operands can be reordered and regrouped freely.

Property 3 is the subtle load-bearing one. The pairs in the input may be far apart — `[5, 3, 5]` has its 5s separated by a 3 — but associativity plus commutativity mean the fold `5 ^ 3 ^ 5` equals `(5 ^ 5) ^ 3`. Every pair meets and annihilates, order be damned, leaving the singleton XORed with 0.

## Bit-level trace on [5, 3, 5]

Write each number in 3-bit binary: 5 = `101`, 3 = `011`.

| step | acc before | x     | acc after (XOR per bit) |
|------|------------|-------|--------------------------|
| 1    | `000`      | `101` | `101`                    |
| 2    | `101`      | `011` | `110`                    |
| 3    | `110`      | `101` | `011`                    |

Final accumulator: `011` = 3, the unpaired number. Watch the middle step: after absorbing the 3, the accumulator `110` is not any input value — it is a superposition of pending cancellations. Only when the second 5 arrives do its bits cancel the first 5's contribution, leaving pure 3.

## Why not just use a Counter?

`collections.Counter(a)` and picking the key with count 1 is perfectly fine, and clearer for most readers. XOR earns its keep when constraints bite: streaming input you cannot store, embedded environments where \(O(n)\) auxiliary memory is unavailable, or interview settings testing whether you know the trick. Complexity: \(O(n)\) time, \(O(1)\) space — the accumulator — versus the Counter's \(O(n)\) space.

## Bug note: the trick's fragile preconditions

The elegance conceals sharp preconditions, and violating them yields silent garbage rather than errors:

- **"Exactly twice" is a promise, not a check.** If some element appears three times, its third copy survives the cancellation and corrupts the result: `[7, 7, 7, 2, 2]` folds to 7, indistinguishable from a legitimate answer. The function cannot detect a malformed input.
- **Two singletons don't work directly.** `[4, 6]` folds to `4 ^ 6 = 2`, which is neither answer. (The known extension: take that combined XOR, isolate any set bit with `acc & -acc`, and partition the list by that bit into two groups, each containing one singleton — then fold each group separately.)
- **Zero is a valid answer but also the initial state.** If the unpaired number is 0, the function correctly returns 0, but so does an empty list. Distinguish those cases upstream if it matters.

The general pattern worth extracting: when a problem involves *pairwise cancellation*, look for an operation that is its own inverse. XOR for equality-pairs, addition/subtraction against an expected total (the missing-number-from-1-to-n trick), and multiplication by modular inverses all follow the same skeleton — fold everything into one accumulator and let algebra do the bookkeeping.
