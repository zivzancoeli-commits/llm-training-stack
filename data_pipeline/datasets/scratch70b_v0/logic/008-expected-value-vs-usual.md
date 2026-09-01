---
id: logic-008
category: logic
subcategory: probability
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - counterexample
title: Expected value vs what usually happens
approx_words: 610
---

# Expected value vs what usually happens

A street vendor sells a toy lottery ticket for $2. One ticket in a thousand pays $5,000; the other 999 pay nothing. Should you buy?

Two voices answer. One says: "You will lose. You will almost certainly lose. 99.9% of buyers walk away two dollars poorer." The other says: "The average payout is $5 per ticket, so each $2 ticket earns $3 on average — buy as many as they'll sell you." Both voices are stating facts. The skill is knowing which fact answers which question.

## The worked solution

**Expected value** is the probability-weighted average of outcomes. For one ticket:

- Win: probability 1/1000, net gain $5,000 − $2 = $4,998.
- Lose: probability 999/1000, net −$2.

EV = (1/1000)(4,998) + (999/1000)(−2) = 4.998 − 1.998 = **+$3.00** per ticket.

**What usually happens** is the *mode* or the *median* outcome: you lose $2. These two summaries diverge because the payoff distribution is lopsided — a huge rare gain against a small common loss. Neither number is wrong; they compress the same distribution along different axes.

When does each one matter? Expected value governs *repeated* play or *aggregated* decisions. If a syndicate buys 100,000 tickets for $200,000, it expects around 100 winners paying $500,000 — a nearly certain profit, since the randomness averages out across volume. The law of large numbers slowly transforms "average outcome" into "actual outcome." Insurers, casinos, and index-fund investors live in this regime: they make thousands of small positive-EV bets and let arithmetic do the rest.

## The tempting invalid cousin

1. This ticket has positive expected value (+$3).
2. Positive expected value means the bet is favorable.
3. Therefore, I should bet my rent money on tickets this month.

**Counterexample.** Sharpen the same structure: a bet costs your entire $100,000 life savings and pays $100 million with probability 1/500 (zero otherwise). EV = $200,000 − $100,000 = +$100,000, spectacular. Yet 499 times out of 500 you end up ruined, and you cannot rerun your one life until the average kicks in. If losing your savings means losing your home, the "favorable" bet is a catastrophe with a rounding-error chance of glory. Premise 1 is true; the conclusion is one most people would rightly reject. EV alone does not settle single, unrepeatable, large-stakes decisions — the *spread* of outcomes and the irreversibility of the loss matter too.

The mirror-image fallacy is just as common and runs the other way:

1. Almost everyone who buys these tickets loses.
2. Therefore, the tickets are a bad product for anyone, always.

**Counterexample.** The syndicate above. "Usually loses per ticket" coexists with "reliably profits per thousand tickets." A cheap, oft-repeated bet is governed by its average, and refusing all positive-EV opportunities because each one usually fails is how people talk themselves out of, say, sending applications with a 5% hit rate. Send sixty and the "usual" outcome flips.

## The synthesis

- **Small stakes, many repetitions:** trust expected value; the typical outcome of the *sum* converges to it.
- **Huge stakes, one shot, ruinous downside:** the typical outcome and the worst outcomes dominate; EV is a misleading summary of a distribution you will sample only once.
- Real casino lotteries are negative-EV *and* usually lose — bad on both axes. The interesting cases are the mixed ones, and the mark of clear thinking is refusing to let one summary statistic impersonate the whole distribution.

Ask two questions of every gamble: What happens on average? What happens to *me*, on the draws I can actually afford to experience?
