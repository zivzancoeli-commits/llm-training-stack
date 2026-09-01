---
id: code-004
category: code
subcategory: algorithms
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - complexity
title: Reversing words in place with two pointers
approx_words: 640
---

Task: given a sentence, reverse the order of its words. `"cats chase mice"` should become `"mice chase cats"`. The one-liner is `" ".join(s.split()[::-1])`, which allocates several intermediate arrays. The interesting version is the in-place one, built from a single primitive: two-pointer reversal of a slice.

A caveat up front: Python strings are immutable, so true in-place work requires a mutable buffer such as a list of characters (in C or Rust you would operate on the byte array directly). The algorithmic idea is the point; the buffer is just where we practice it.

## The primitive: reverse a slice with two pointers

```python
def reverse_range(buf, i, j):
    """Reverse buf[i..j] inclusive, in place."""
    while i < j:
        buf[i], buf[j] = buf[j], buf[i]
        i += 1
        j -= 1
```

Two indices march toward each other, swapping as they go, and stop when they meet. Each element is touched once, so a slice of length \(k\) costs \(k/2\) swaps and no extra memory.

## The trick: reverse everything, then un-reverse each word

Reversing the whole buffer puts the words in the right *order* but leaves each word's letters backwards. A second pass reverses each word individually, restoring the letters:

```python
def reverse_words(s):
    buf = list(s)
    n = len(buf)
    reverse_range(buf, 0, n - 1)      # pass 1: whole buffer
    start = 0
    for k in range(n + 1):            # pass 2: each word
        if k == n or buf[k] == " ":
            reverse_range(buf, start, k - 1)
            start = k + 1
    return "".join(buf)
```

The `k == n` check handles the final word, which ends at the buffer boundary rather than at a space — forgetting it is the classic bug here, and it silently leaves the last word reversed.

## Trace on "ab cd"

The buffer starts as `a b _ c d` (underscore marking the space), indices 0–4.

**Pass 1** reverses indices 0..4: swap positions 0 and 4 (`d b _ c a`), swap positions 1 and 3 (`d c _ b a`), pointers meet at index 2, stop. Buffer: `"dc ba"`. The words are now in reversed order — `dc` before `ba` — but each is internally backwards.

**Pass 2** scans for word boundaries:

- `k = 2` finds a space, so reverse indices 0..1: `dc` becomes `cd`. Buffer: `"cd ba"`. Set `start = 3`.
- `k = 5` equals `n`, so reverse indices 3..4: `ba` becomes `ab`. Buffer: `"cd ab"`.

Result: `"cd ab"`, which is `"ab cd"` with the words swapped. Correct.

It is worth pausing on why this works: reversal of the whole string reverses the sequence of words *and* the letters within each word. Word-wise reversal is only the first of those two effects, so we apply the second effect again to cancel it — reversing each word twice returns its letters to normal.

## Complexity

Pass 1 performs \(n/2\) swaps. Pass 2 performs at most \(n/2\) swaps total across all words, since the word slices are disjoint. Total: \(O(n)\) time. Extra space is \(O(1)\) beyond the buffer itself — two indices and a `start` marker — which is the entire point of the exercise. The `split`-based one-liner is also \(O(n)\) time but allocates a list of word strings plus the reversed copy; on a memory-constrained system or a hot path, the two-pointer version wins.

## Edge cases to note

Multiple consecutive spaces survive this algorithm oddly: `"a  b"` reverses to `"b  a"`, which happens to be fine, but leading/trailing spaces stay glued to the ends (`" hi bye"` becomes `" eyb ih"` after pass 1, and pass 2 yields `" bye hi"` — the leading space stays leading). If the spec says to normalize whitespace, add a third compaction pass with — naturally — two more pointers, one reading and one writing.
