---
id: code-015
category: code
subcategory: data-structures
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - debugging
title: Hash collisions and why equality still matters
approx_words: 630
---

A hash table's promise — constant-time lookup — rests on a division of labor that beginners often miss: the *hash* finds the neighborhood, but *equality* identifies the resident. Collisions are why both are mandatory.

## Two keys, one bucket

A toy table with 8 buckets, indexing by `hash(key) % 8`. Suppose we insert `"cat"` and `"dog"`, and imagine their hashes land as:

```
hash("cat") = 5798115  →  5798115 % 8 = 3
hash("dog") = 8214291  →  8214291 % 8 = 3     ← same bucket!
```

Different keys, different hash values even, but the modulo squeezes both into bucket 3. This is not a rare accident to engineer away: with 8 buckets, the pigeonhole principle guarantees collisions by the 9th insert, and the birthday paradox makes them likely far sooner (with just 4 random keys in 8 buckets, the odds of a collision already exceed 75%). Collisions are the normal case, and every hash table is, at its core, a collision-management scheme.

A minimal chaining table makes the machinery visible:

```python
class TinyMap:
    def __init__(self, nbuckets=8):
        self.buckets = [[] for _ in range(nbuckets)]

    def put(self, key, val):
        b = self.buckets[hash(key) % len(self.buckets)]
        for i, (k, _) in enumerate(b):
            if k == key:              # equality check: replace, don't duplicate
                b[i] = (key, val)
                return
        b.append((key, val))

    def get(self, key):
        b = self.buckets[hash(key) % len(self.buckets)]
        for k, v in b:
            if k == key:              # equality check: which resident is it?
                return v
        raise KeyError(key)
```

## Walking through the collision

After `put("cat", 1)` and `put("dog", 2)`, bucket 3 holds `[("cat", 1), ("dog", 2)]` — a two-entry chain.

Now call `get("dog")`. Hashing routes us to bucket 3. If lookup trusted the hash alone and returned the bucket's first entry, we would get 1 — *cat's value*. Instead the loop compares keys: `"cat" == "dog"` is false, move on; `"dog" == "dog"` is true, return 2. The hash narrowed eight buckets to one; equality picked the right tenant among the chain's residents. Neither step alone suffices: equality without hashing is a linear scan of everything (that's just a list), and hashing without equality returns wrong values whenever chains exceed length one.

## The contract this imposes on your classes

Because lookup is "hash to a bucket, then equality-scan the chain," any custom key type must keep the two operations consistent:

> **If `a == b`, then `hash(a) == hash(b)` must hold.**

Violate it and equal keys land in *different* buckets, so a lookup hashes to the wrong chain and never even reaches the equality check that would have matched:

```python
class BadPoint:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    # BUG: __eq__ defined without matching __hash__

d = {}
d[BadPoint(1, 2)] = "here"
d[BadPoint(1, 2)]        # KeyError — equal keys, different buckets
```

(Python partially protects you: defining `__eq__` sets `__hash__` to None, making the class unhashable and turning the design flaw into an immediate `TypeError`. Explicitly writing an inconsistent `__hash__` restores the silent-corruption version.) The converse is not required — unequal keys *may* share a hash; that is precisely what a collision is, and the equality scan absorbs it.

## Complexity note

With chaining and a load factor kept near 1 by resizing, expected chain length is \(O(1)\), so lookups average constant time. The worst case is everything in one bucket — \(O(n)\) per lookup — which adversarial inputs can force if hash values are predictable; that is a real denial-of-service vector, and it is why Python randomizes string hashes per process. The everyday lesson is smaller: the hash is a hint, equality is the truth, and a correct table needs both to agree.
