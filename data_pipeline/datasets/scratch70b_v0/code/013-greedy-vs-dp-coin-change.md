---
id: code-013
category: code
subcategory: algorithms
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - complexity
title: Coin change where greedy fails and DP does not
approx_words: 650
---

Making change with the fewest coins has a seductive greedy strategy: repeatedly take the largest coin that fits. For US-style denominations it happens to be optimal, which trains a dangerous intuition. Change the coin set slightly and greedy confidently produces wrong answers.

## The counterexample: coins {1, 3, 4}, amount 6

Greedy takes the largest coin first: a 4, leaving 2. The largest coin fitting into 2 is a 1, leaving 1; another 1 finishes. Greedy's answer: `4 + 1 + 1` — **three coins**.

The optimum is `3 + 3` — **two coins**. Greedy never considers it, because taking the 4 felt locally best and greedy never revisits a decision. That is the definition of the failure: the locally optimal first move (grab the 4) is not a prefix of any globally optimal solution.

```python
def greedy_coins(coins, amount):
    coins = sorted(coins, reverse=True)
    used = []
    for c in coins:
        while amount >= c:
            amount -= c
            used.append(c)
    return used if amount == 0 else None

def dp_min_coins(coins, amount):
    INF = float("inf")
    best = [0] + [INF] * amount        # best[a] = fewest coins for amount a
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return best[amount] if best[amount] != INF else None
```

## Filling the DP table for amount 6

`best[a]` asks: considering *every* coin as the possible last coin, which choice minimizes the total?

| a | candidates (coin → 1 + best[a−coin]) | best[a] |
|---|--------------------------------------|---------|
| 1 | 1 → 1+best[0] = 1                    | 1       |
| 2 | 1 → 1+best[1] = 2                    | 2       |
| 3 | 1 → 3; **3 → 1+best[0] = 1**         | 1       |
| 4 | 1 → 2; 3 → 2; **4 → 1**              | 1       |
| 5 | 1 → 2; 3 → 3; 4 → 2                  | 2       |
| 6 | 1 → 3; **3 → 1+best[3] = 2**; 4 → 1+best[2] = 3 | 2 |

At `a = 6`, the row lays greedy's mistake bare: ending with a 4 costs \(1 + best[2] = 3\), while ending with a 3 costs \(1 + best[3] = 2\). DP examines both and keeps the smaller; greedy committed to the 4 and never looked back. Recovering the actual coins is a standard walk backwards: from 6, a 3 leads to `best[3] = 1`; from 3, a 3 leads to `best[0] = 0`. Coins: `[3, 3]`.

## Why greedy works for some coin systems

Coin systems where greedy is always optimal are called *canonical* — {1, 5, 10, 25} qualifies, which is why cashiers can be greedy. Canonicity is a property of the whole set, not of any coin: adding or removing one denomination can break it, as {1, 3, 4} shows (and so does the historically real pre-decimal case of systems with a 20 and 25 side by side, where amount 40 trips greedy: 25+20 doesn't fit, 25+1×15 loses to 20+20). There is no shortcut for spotting canonicity by eye; there are algorithms to *test* it, but the safe default for arbitrary denominations is DP.

## Complexity note

DP costs \(O(\text{amount} \times |\text{coins}|)\) time and \(O(\text{amount})\) space — for amount 6 and 3 coins, 18 cell-updates. Greedy runs in \(O(|\text{coins}| \log |\text{coins}|)\) for the sort plus a handful of subtractions, dramatically cheaper. That price gap is exactly the temptation: greedy is fast and *sometimes* right. The discipline is to demand a proof (an exchange argument or matroid structure) before trusting a greedy, and when no proof comes to mind, to hunt for a small counterexample first — they are usually tiny, like this one. A three-coin set and the number 6 were enough.
