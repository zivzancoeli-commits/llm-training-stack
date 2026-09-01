---
id: code-018
category: code
subcategory: distributed-systems
difficulty: hard
source_model: fable-5
skills:
  - worked-solution
  - debugging
title: Idempotent retries, or why PUT is safe to repeat and POST is not
approx_words: 680
---

Networks fail in an especially treacherous way: a request can succeed on the server while the *response* is lost. The client sees a timeout and cannot distinguish "never happened" from "happened, but I didn't hear back." The only universally safe reaction to that ambiguity is to retry — which is safe *only if* repeating the operation is harmless. That property is idempotence: applying the operation once or five times leaves the system in the same state.

## Two updates, same intent, different retry behavior

A tiny in-memory "server" with a balance, and two ways to express "the balance should go up by 50, to 150":

```python
state = {"balance": 100}

def put_balance(value):          # absolute: SET balance = value
    state["balance"] = value

def post_deposit(amount):        # relative: balance += amount
    state["balance"] += amount
```

Now simulate the failure: the client sends a request, the server *executes it*, but the acknowledgment is dropped, so the client retries.

**PUT-style, `put_balance(150)`:**

- Attempt 1: server sets balance to 150. Ack lost.
- Retry: server sets balance to 150. Balance: **150**. Correct.

Ten retries later it is still 150. `set x = v` composed with itself is `set x = v` — formally, \(f(f(s)) = f(s)\), the definition of idempotence.

**POST-style, `post_deposit(50)`:**

- Attempt 1: server adds 50 → balance 150. Ack lost.
- Retry: server adds 50 again → balance **200**. The customer was credited twice (or, with a withdrawal, charged twice).

`add 50` twice is `add 100`. The retry that was mandatory for reliability just corrupted the data — and note that *neither the client nor the server did anything individually wrong*. The bug lives in the combination of a lost ack and a non-idempotent operation.

This is why HTTP's method semantics matter beyond pedantry: PUT and DELETE are specified as idempotent, so clients, proxies, and retry middleware may repeat them on timeout; POST carries no such promise, and infrastructure must not blindly retry it.

## Making the POST safe: idempotency keys

Often you cannot rewrite a relative operation as an absolute one — "deposit 50" from two different customers must both apply, so `PUT balance=150` would be wrong under concurrency. The standard fix keeps the operation's semantics but deduplicates *requests*: the client attaches a unique key per logical operation, and the server remembers which keys it has already processed.

```python
processed = {}   # idempotency_key -> result

def post_deposit_idem(key, amount):
    if key in processed:
        return processed[key]          # replay: return recorded result, no re-apply
    state["balance"] += amount
    processed[key] = state["balance"]
    return processed[key]
```

Replay the failure with `key = "dep-7f3a"`: attempt 1 applies the deposit (balance 150) and records the key; the retry finds the key and returns the stored result without touching the balance. Balance: **150**. Retried safely, applied once. A *different* deposit uses a fresh key and applies normally. This is exactly how payment APIs like Stripe's expose safe retries: same key = same logical operation, replayed for free.

## Bug notes: where real implementations leak

- **The check and the write must be atomic.** `if key in processed` followed by the mutation is a check-then-act race: two concurrent retries can both miss the key and both apply. In a database, that means inserting the key under a unique constraint *in the same transaction* as the state change, and treating a duplicate-key error as "replay."
- **Key storage needs a lifetime policy.** Keys kept forever grow without bound; keys expired too soon reopen the double-apply window for late retries. A TTL comfortably longer than any client's maximum retry horizon is the usual compromise.
- **Idempotent ≠ side-effect-free.** `DELETE /orders/9` is idempotent (deleting twice leaves the same state — order gone) even though it obviously has effects. The retry-safety question is about *repeatability*, not purity. GET is the stronger property, "safe": no state change at all.

The design habit worth internalizing: for every operation that crosses a network, ask "what happens if this executes twice?" If the answer is "something bad," you owe the system either an absolute-state formulation or an idempotency key — because the network *will* eventually eat an ack.
