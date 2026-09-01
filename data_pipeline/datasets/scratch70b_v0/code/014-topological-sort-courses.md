---
id: code-014
category: code
subcategory: algorithms
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - complexity
title: Topological sort of a four-course prerequisite graph
approx_words: 640
---

You are planning a semester sequence. Four courses with prerequisites:

- **Intro** has no prerequisites.
- **DataStructs** requires Intro.
- **Discrete** requires Intro.
- **Algorithms** requires DataStructs *and* Discrete.

As a directed graph, an edge points from a prerequisite to the course that needs it:

```
Intro → DataStructs → Algorithms
Intro → Discrete    → Algorithms
```

A topological order is any listing of the nodes where every edge points forward — every course appears after all its prerequisites. Kahn's algorithm produces one by repeatedly graduating courses whose prerequisites are all satisfied.

```python
from collections import deque

def topo_sort(nodes, edges):
    indeg = {n: 0 for n in nodes}
    adj = {n: [] for n in nodes}
    for pre, post in edges:
        adj[pre].append(post)
        indeg[post] += 1

    ready = deque(n for n in nodes if indeg[n] == 0)
    order = []
    while ready:
        n = ready.popleft()
        order.append(n)
        for m in adj[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                ready.append(m)

    if len(order) < len(nodes):
        raise ValueError("cycle: no valid course order exists")
    return order
```

## Trace on the course graph

Initial in-degrees: Intro 0, DataStructs 1, Discrete 1, Algorithms 2. The ready queue starts holding just `Intro`.

1. **Pop Intro** → order `[Intro]`. Its edges decrement DataStructs to 0 and Discrete to 0; both enter the queue.
2. **Pop DataStructs** → order `[Intro, DataStructs]`. Algorithms drops from 2 to 1 — still blocked, stays out of the queue.
3. **Pop Discrete** → order `[Intro, DataStructs, Discrete]`. Algorithms drops to 0, enters the queue.
4. **Pop Algorithms** → order `[Intro, DataStructs, Discrete, Algorithms]`. Queue empty, all 4 nodes placed. Done.

Step 2 is the moment that shows what in-degree bookkeeping buys: Algorithms had one of its two prerequisites met and the count, not a rescan of the graph, told us it still had to wait.

Note the valid output is not unique — `[Intro, Discrete, DataStructs, Algorithms]` is equally legal, since DataStructs and Discrete don't constrain each other. Topological order is a partial order flattened arbitrarily; if you need determinism (stable builds, reproducible schedules), replace the queue with a min-heap to always pop the alphabetically or numerically smallest ready node.

## The cycle case

Add a perverse edge `Algorithms → Intro` ("Intro now requires Algorithms"). Every node's in-degree becomes ≥ 1, the ready queue starts empty, the loop never runs, and `order` has 0 of 4 nodes — the length check fires. This is the diagnostic superpower of Kahn's algorithm: it doesn't just fail on cyclic input, it *detects* the cycle, and the nodes missing from `order` are exactly the ones tangled in (or downstream of) cycles. Dependency resolvers — package managers, build systems, spreadsheet recalculation engines, task schedulers — all rely on this both to find an execution order and to report "circular dependency" with the offending set.

## Bug note and complexity

The classic implementation bug is decrementing in-degrees but forgetting the final length check, silently returning a *partial* order when the graph has a cycle. Callers then process an incomplete list with no error — the worst failure mode. The check costs one comparison; never omit it.

Complexity: building the adjacency structure touches each edge once, and the main loop pops each node once and relaxes each edge once, giving \(O(V + E)\) time and \(O(V + E)\) space. For our graph that is 4 node-visits and 5 edge-decrements — trivially fast, and the same bound holds at package-registry scale, which is why `pip` and `cargo` can order thousands of dependencies without breaking a sweat. The alternative formulation — DFS with post-order reversal — has identical complexity and is the one to reach for when you also want to classify edges or find the cycle's exact members via back-edge detection.
