---
id: code-002
category: code
subcategory: data-structures
difficulty: easy
source_model: fable-5
skills:
  - complexity
  - worked-solution
title: Hash map lookup vs scanning a list
approx_words: 560
---

Suppose you have a list of user IDs and you need to answer many questions of the form "is this ID present?" There are two obvious tools: scan the list each time, or build a hash-based set once and query it. The difference is not a constant-factor tweak — it changes the *shape* of the running time.

```python
ids = [17, 42, 8, 93, 51, 27]

# Option A: scan
def has_id_scan(ids, q):
    for x in ids:          # up to n comparisons
        if x == q:
            return True
    return False

# Option B: hash set
id_set = set(ids)          # built once, O(n)
def has_id_hash(q):
    return q in id_set     # expected O(1)
```

## Walking through one query

Query `q = 51` against the list `[17, 42, 8, 93, 51, 27]`.

The scan compares `51` against `17` (no), `42` (no), `8` (no), `93` (no), then `51` (yes) — five comparisons. If the query were `q = 60`, absent from the list, the scan would touch all six elements before giving up. Misses are the worst case, and in many workloads (spam filters, cache lookups, deduplication) misses dominate.

The hash set instead computes `hash(51)`, reduces it modulo the table size to pick a bucket, and inspects that one bucket. Whether the set holds six elements or six million, the expected work is the same handful of operations.

## A tiny timing thought experiment

Concrete numbers make this vivid. Say one equality comparison costs about 1 nanosecond, and one hash-plus-bucket-probe costs about 50 nanoseconds — the hash is genuinely more expensive *per operation*.

- With `n = 10` elements, an average scan does ~5 comparisons ≈ 5 ns, while the hash lookup costs ~50 ns. **The scan wins by 10x.**
- With `n = 1,000`, the average scan is ~500 ns versus the same ~50 ns. The hash wins by 10x.
- With `n = 1,000,000`, the scan averages ~500,000 ns (half a millisecond) versus still ~50 ns. The hash wins by 10,000x.

The crossover sits somewhere around \(n \approx 100\) with these made-up constants. The exact crossover depends on hardware and data (small scans are cache-friendly and branch-predictable, which is why real crossovers are often higher than naive math suggests), but the trend is inescapable: the scan's cost grows with \(n\), the hash lookup's does not.

Now multiply by query count. If you run \(m\) queries against \(n\) items, scanning costs \(O(m \cdot n)\) total, while build-then-query costs \(O(n + m)\). At \(m = n = 10^6\), that is the difference between ~\(10^{12}\) operations (minutes to hours) and ~\(2 \times 10^6\) (milliseconds).

## Caveats worth remembering

- **"Expected" is doing work in \(O(1)\) expected.** Adversarial or unlucky keys can pile into one bucket, degrading a lookup to \(O(n)\). Python mitigates this by randomizing string hashing per process.
- **Hashing costs memory.** A set stores a table with slack space (load factor below 1), typically several times the raw data size. A list is the compact option.
- **Tiny collections favor the list.** For a handful of items checked a handful of times, building a set is pure overhead. Reach for the set when the collection is large, the queries are many, or both.

The habit to build: before optimizing constants, ask whether the *number of elements touched per query* can be made independent of \(n\). That is the leap from linear to constant, and it dwarfs any micro-optimization.
