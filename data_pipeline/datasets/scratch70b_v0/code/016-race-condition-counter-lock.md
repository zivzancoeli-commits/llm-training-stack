---
id: code-016
category: code
subcategory: concurrency
difficulty: hard
source_model: fable-5
skills:
  - debugging
  - worked-solution
title: A two-thread counter race and why a lock fixes it
approx_words: 680
---

The smallest possible concurrency bug: two threads each increment a shared counter many times, and the final total is *less* than the sum of their increments. No exception, no crash — just missing counts.

```python
import threading

counter = 0

def worker(times):
    global counter
    for _ in range(times):
        counter += 1          # looks atomic; is not

t1 = threading.Thread(target=worker, args=(100_000,))
t2 = threading.Thread(target=worker, args=(100_000,))
t1.start(); t2.start(); t1.join(); t2.join()
print(counter)                # expected 200000; often prints less
```

## Why one line of Python is three operations

`counter += 1` compiles to a read-modify-write sequence: load the current value, add one, store the result. In CPython bytecode that is `LOAD_GLOBAL`, `LOAD_CONST`, `BINARY_OP`, `STORE_GLOBAL` — and the interpreter may switch threads *between* any of them. The GIL guarantees only that individual bytecode-level steps don't interleave mid-instruction; it does not make your source line atomic. (On recent CPython versions the specializing interpreter makes this particular race harder to hit, and free-threaded builds change the landscape again — but "harder to observe" is the most dangerous flavor of race, because tests pass and production doesn't.)

## The interleaving that loses an increment

Suppose `counter` is 41 and both threads execute one increment:

| step | Thread A            | Thread B            | counter |
|------|---------------------|---------------------|---------|
| 1    | reads 41            |                     | 41      |
| 2    | *(preempted)*       | reads 41            | 41      |
| 3    |                     | computes 42, stores | 42      |
| 4    | computes 42, stores |                     | 42      |

Two increments executed; the counter moved by one. Thread A's store at step 4 is based on the stale read from step 1, so it silently overwrites B's update — a *lost update*. Nothing detects this; the program's only symptom is a wrong number. Run the full script and you might see 200000, or 173942, or a different wrong value each run, depending on scheduler timing. Nondeterminism is the tell: a bug that appears and vanishes across identical runs is a race until proven otherwise.

## The fix: make read-modify-write indivisible

```python
lock = threading.Lock()

def worker(times):
    global counter
    for _ in range(times):
        with lock:
            counter += 1
```

The lock enforces *mutual exclusion*: a thread must acquire it before entering the block, and only one holder exists at a time. Replay the bad interleaving — A acquires the lock and reads 41; B attempts to acquire and *blocks* at step 2 instead of reading; A computes and stores 42, releases; B acquires, reads the fresh 42, stores 43. The stale-read window is gone because read, modify, and write now travel as one indivisible unit. The final count is exactly 200000, every run.

Locks also handle *visibility*: acquiring and releasing establishes the memory-ordering guarantees that ensure one thread's write is actually seen by the next reader — an issue that bites harder in C++/Java/Rust than in CPython, but conceptually part of what the lock buys.

## What the fix costs, and its own bug class

Mutual exclusion serializes the protected region, so the two threads no longer increment in parallel — for this workload the "concurrent" program is effectively sequential plus lock overhead. That is the honest trade: correctness first, then shrink the critical section or restructure. Standard alternatives, in rough order of preference: keep a *per-thread* counter and sum after `join` (no sharing, no lock); use an atomic primitive where the platform offers one (`itertools.count` misuse doesn't qualify; C++ `std::atomic` or Java `AtomicLong` do); or use a queue to funnel updates to one owner thread.

Locks introduce their own failure mode — deadlock — the moment code holds one lock while acquiring another. Two threads acquiring locks L1 and L2 in opposite orders can each block forever waiting for the other's. The discipline: keep critical sections tiny, never call unknown code while holding a lock, and if multiple locks are unavoidable, fix a global acquisition order.

The portable takeaway: *check-then-act and read-modify-write on shared state are never atomic by default.* Find every shared mutable variable, and either stop sharing it, stop mutating it, or guard it.
