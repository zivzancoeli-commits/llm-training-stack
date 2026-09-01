---
id: math-005
category: math
subcategory: probability
difficulty: easy
source_model: fable-5
skills:
  - worked-solution
  - decision-making
  - check-your-work
title: Expected value of a simple dice game, including when not to play
approx_words: 610
---

Expected value is the single most useful number for deciding whether a bet is good, and also one of the most commonly misread. Let's compute one carefully and then talk about when the number should not be trusted alone.

The game: you pay $2 to roll one fair six-sided die. If you roll a 6, you win $10. If you roll a 4 or 5, you win $3. Anything else (1, 2, or 3) wins nothing. Should you play?

Expected value is the probability-weighted average of outcomes. List every outcome with its probability and its net payoff, remembering that the $2 entry fee applies to every roll, including winners.

- Roll a 6 (probability 1/6): receive $10, paid $2, net +$8.
- Roll 4 or 5 (probability 2/6): receive $3, paid $2, net +$1.
- Roll 1, 2, or 3 (probability 3/6): receive $0, paid $2, net -$2.

EV = (1/6)(8) + (2/6)(1) + (3/6)(-2) = 8/6 + 2/6 - 6/6 = 4/6, which is about +$0.67 per play.

So the game is favorable: on average you gain about 67 cents per roll. Over 600 plays you'd expect to be up around $400, though any single session can lose.

Check the work two ways. First, the probabilities must sum to 1: 1/6 + 2/6 + 3/6 = 6/6. Good; a missing or double-counted outcome is the most common EV bug, and this check catches it. Second, compute EV the other way: expected gross winnings minus the fee. Gross = (1/6)(10) + (2/6)(3) + (3/6)(0) = 10/6 + 6/6 = 16/6, about $2.67. Subtract the $2 fee: $0.67. Same answer by a different route, which is strong evidence the arithmetic is right.

The common mistake is exactly the one that second method guards against done halfway: subtracting the fee only from the losing outcomes, or forgetting it entirely and concluding EV = $2.67, "so the game pays well." The fee is paid unconditionally, so either fold it into every branch's net payoff (method one) or subtract it once at the end (method two). Mixing the two methods double-counts or drops it.

Now, when should you not play a positive-EV game? Expected value is a long-run average, and the long run assumes you survive to reach it.

First: stakes that can ruin you. Suppose the same die, but you must pay $20,000 to roll, winning $100,000 on a 6 and $30,000 on 4-5. The EV is 10,000 times larger, about +$6,700, yet if $20,000 is most of what you own, a 50% chance of losing it is a catastrophe the average does not capture. EV weights dollars linearly; real life doesn't. Losing your last dollar hurts more than winning an extra one helps, which is why bet sizing matters even when the odds favor you.

Second: one-shot situations. EV describes what happens across many repetitions. If you only get to play once and the downside is unacceptable, the average over hypothetical repetitions may be irrelevant to your decision.

Third: doubt about the stated rules. A stranger offering a game with EV of +$0.67 in your favor is a stranger paying you to play. Before trusting the computation, ask whether the die is fair and the payoffs will actually be honored. The math is only as good as the model, and "too good to be true" is a prior worth having.

The takeaway procedure: enumerate outcomes, check probabilities sum to 1, compute net payoff per branch, take the weighted average, verify by an independent route. Then, before acting on a positive number, ask whether you can afford the variance and whether you believe the model. EV tells you which side of the bet to want; it doesn't tell you how much to risk.
