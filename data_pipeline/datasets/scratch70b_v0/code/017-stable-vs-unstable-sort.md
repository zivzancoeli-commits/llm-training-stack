---
id: code-017
category: code
subcategory: algorithms
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - complexity
title: Stable vs unstable sorting with equal keys
approx_words: 620
---

Two sorting algorithms can both be "correct" — output in nondecreasing key order — and still produce different outputs on the same input. The difference appears only when keys tie, and it is called *stability*: a stable sort preserves the original relative order of records with equal keys; an unstable sort may scramble them.

## Records where it matters

Four support tickets, already sorted by arrival time, now to be sorted by priority (lower number = more urgent):

```python
tickets = [
    ("09:00", "Alice",  2),
    ("09:10", "Bob",    1),
    ("09:20", "Carol",  2),
    ("09:30", "Dave",   1),
]
# (arrival, name, priority)
```

**Stable sort by priority** keeps ties in arrival order:

```
("09:10", "Bob",   1)     ← the two priority-1s stay in arrival order
("09:30", "Dave",  1)
("09:00", "Alice", 2)     ← likewise the priority-2s
("09:20", "Carol", 2)
```

An **unstable sort** is free to emit Dave before Bob, or Carol before Alice — still sorted by priority, but the within-priority arrival ordering is destroyed. If the queue's fairness contract is "equal priority is served first-come-first-served," the unstable result is a business-logic bug that no `assert is_sorted(...)` test will ever catch, because the output *is* sorted.

## Watching instability happen

Selection sort is a compact demonstration. It repeatedly swaps the minimum remaining element into the front — and the swap is what breaks stability. Sort keys `[2a, 2b, 1]` (subscripts mark the original order of the equal 2s):

1. The minimum of the whole list is `1` at index 2. Swap it with index 0: `[1, 2b, 2a]`. The swap flung `2a` *behind* `2b`.
2. The minimum of the rest is `2b` — already in place. Done.

Output `[1, 2b, 2a]`: sorted, but the equal keys reversed. Insertion sort on the same input never leapfrogs an equal element (it shifts only *strictly greater* elements rightward), so it yields `[1, 2a, 2b]` — stable. Among the classics: insertion sort and merge sort are stable; selection sort, heapsort, and textbook quicksort are not. Stability is a property of the implementation, not the abstract algorithm family — a quicksort can be made stable by spending \(O(n)\) extra memory.

## The multi-key trick stability enables

Python's `sorted` and `list.sort` use Timsort, which is guaranteed stable, and stability turns multi-key sorting into composable passes — sort by the *secondary* key first, then by the primary:

```python
by_arrival  = sorted(tickets, key=lambda t: t[0])   # secondary key
by_priority = sorted(by_arrival, key=lambda t: t[2])  # primary key
```

The second pass, being stable, cannot disturb the arrival ordering it inherited among equal priorities — so the result is sorted by (priority, then arrival) without ever building a compound key. With an unstable sort, this two-pass idiom silently breaks; you would be forced to sort once on the tuple `(priority, arrival)` instead. Both idioms are worth knowing; only the stable one lets you layer sorts incrementally, e.g. re-sorting a spreadsheet by clicking one column after another and having earlier orderings persist among ties.

## Complexity and bug note

Stability is orthogonal to speed: merge sort is stable at \(O(n \log n)\) with \(O(n)\) auxiliary space; heapsort is unstable at \(O(n \log n)\) with \(O(1)\) space. The historical trade was memory versus stability, which is why systems languages defaulted to unstable sorts (`std::sort` in C++) and offer stability as a named, costlier option (`std::stable_sort`).

The bug pattern to remember: code that works under Python's stable Timsort gets ported to a language whose default sort is unstable, and tie-ordering assumptions break only on datasets containing duplicates — often absent from tests. When your correctness depends on tie order, either verify the sort is documented stable, or make the dependency explicit by putting the tiebreaker into the key itself. Explicit keys survive porting; implicit stability assumptions do not.
