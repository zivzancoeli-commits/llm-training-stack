---
id: code-006
category: code
subcategory: algorithms
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - complexity
title: BFS vs DFS on a tiny grid and shortest paths
approx_words: 680
---

Breadth-first and depth-first search visit the same set of reachable cells, so for a plain "can I get there?" question they are interchangeable. The moment the question becomes "what is the *fewest steps* to get there?", only one of them answers correctly without extra machinery. A 3×3 grid is enough to see why.

```
S . .        S = start (0,0)
. # .        # = wall  (1,1)
. . G        G = goal  (2,2)
```

Moves are up/down/left/right. The shortest route from S to G is 4 steps — for example right, right, down, down.

```python
from collections import deque

def bfs_dist(grid, start, goal):
    R, C = len(grid), len(grid[0])
    dist = {start: 0}
    q = deque([start])
    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            return dist[(r, c)]
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#" \
                    and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                q.append((nr, nc))
    return -1
```

Swap the `deque` for a plain list used as a stack (`pop()` instead of `popleft()`) and you have DFS.

## Watching BFS expand in rings

BFS processes cells in order of distance from S, like ripples in a pond:

- **Distance 0:** `(0,0)`.
- **Distance 1:** its open neighbors `(0,1)` and `(1,0)`.
- **Distance 2:** `(0,2)` and `(2,0)` — the center `(1,1)` is a wall, so both frontier arms bend around it.
- **Distance 3:** `(1,2)` and `(2,1)`.
- **Distance 4:** `(2,2)` = G. Dequeued with `dist = 4`. Done.

The crucial property: a cell is *first discovered* via a shortest route to it, because all cells at distance \(d\) are enqueued before any cell at distance \(d+1\). The queue enforces this ordering. So the first time G leaves the queue, its recorded distance is provably minimal.

## Watching DFS wander

DFS with a stack commits to one direction and burrows. Starting at `(0,0)` and pushing neighbors in the order given above, it might visit:

```
(0,0) → (1,0) → (2,0) → (2,1) → (2,2)  G reached, path length 4
```

Lucky — that happens to be optimal. But reorder the neighbor list (say, right before down) and DFS can reach G by a longer wandering route first; on larger grids it routinely discovers the goal via a path far longer than optimal. DFS's discovery order reflects the whims of neighbor ordering, not distance. If you record "steps taken when first seen" from a DFS, you get *a* path length, with no guarantee it is *the shortest* one. Turning DFS into a shortest-path finder requires exhaustively trying paths and keeping the minimum — exponential work that BFS avoids entirely.

## When DFS is the right tool anyway

None of this makes DFS worse in general; it answers different questions well. Connectivity ("flood fill this region"), cycle detection, topological ordering, and maze *generation* are natural DFS problems — no distances involved. Recursive DFS is also often the shortest code to write, though on big grids Python's recursion limit (default 1000 frames) argues for the explicit-stack form.

## Complexity note

Both algorithms visit each cell at most once and examine its ≤4 neighbors, so both run in \(O(R \times C)\) time and \(O(R \times C)\) space for the visited set. The space *profile* differs: BFS's queue holds one distance-ring at a time — up to \(O(\min(R, C))\)-ish on open grids but potentially a whole diagonal — while DFS's stack holds one root-to-current path, which can snake through nearly every cell of a maze. Same big-O ceiling, different typical footprint.

One classic bug to avoid in BFS: mark cells as visited *when enqueued*, not when dequeued. Marking at dequeue time lets the same cell be enqueued from several neighbors before its first dequeue, inflating the queue and, on dense grids, the running time — the distances stay right, but the efficiency doesn't.

Rule of thumb: unweighted shortest path → BFS, always. Reachability or structure → whichever is more convenient, and DFS usually is.
