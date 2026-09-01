---
id: habits-001
category: reasoning_habits
subcategory: checking
difficulty: medium
source_model: fable-5
skills:
  - check-your-work
  - estimation
title: Units as a bug detector
approx_words: 600
---

# Units as a Bug Detector

Most arithmetic mistakes are not mistakes of arithmetic. They are mistakes of bookkeeping: a quantity measured in seconds gets treated as if it were measured in hours, and every digit that follows is confidently wrong. The fix is a habit, not a skill. Carry the units through every step, the same way you carry the numbers.

Consider a plain example. A pump moves 3 liters per minute. How much water does it move in a day? A hurried solver writes 3 × 24 = 72 and moves on. But look at the units: liters per **minute** times **hours** gives a unit of liter-hours-per-minute, which is nonsense. Nonsense units are the alarm. The moment you write them down, the error announces itself. The correct chain is 3 L/min × 60 min/hr × 24 hr/day = 4,320 L/day. Each conversion factor is chosen precisely so that the unwanted unit cancels: minutes cancel minutes, hours cancel hours, and only liters per day survives.

This is why physicists call the technique *dimensional analysis*, and why they run it before checking any digit. The units form a small algebra of their own, and that algebra must balance even when the numbers are wrong. If your formula for a distance ends up with units of seconds, no amount of careful multiplication will save it. Conversely, if the units balance, you have not proven the answer right, but you have eliminated a whole family of ways it could be wrong.

The habit pays off most in the seconds-versus-hours trap, because the conversion factor, 3,600, is large enough to be catastrophic and familiar enough to be skipped. A download speed of 5 megabytes per second, sustained for 2 hours, is not 10 megabytes. Writing 5 MB/s × 2 hr and refusing to multiply until the units agree forces the missing step: 2 hr × 3,600 s/hr = 7,200 s, so the total is 36,000 MB, or 36 GB. The person who writes units doesn't need to remember to convert. The mismatched symbols on the page do the remembering.

Three practical rules make the habit stick:

1. **Never write a bare number for a physical quantity.** Write 45 min, not 45. A bare number is a quantity that has lost its passport; you can no longer tell where it is allowed to go.
2. **Treat conversion factors as fractions equal to one.** Since 60 min = 1 hr, the fraction (60 min / 1 hr) equals one, and multiplying by it changes the units without changing the value. Chain as many of these as needed, orienting each fraction so the unwanted unit cancels.
3. **Check the units of the final answer against the question.** If the question asks "how long," the answer must be a time. If your expression simplifies to dollars per kilogram, you answered a different question.

There is also a subtler payoff. Units expose conceptual confusion, not just slips. If you find yourself adding a speed to a distance, the units refuse to combine, and that refusal is telling you that your mental model of the problem is broken, not merely your arithmetic. A student who tries to add 30 km/h to 15 km has misunderstood the situation, and the units catch the misunderstanding before the answer can hide it.

The habit costs perhaps ten extra seconds per problem. Against that, weigh the cost of an answer that is off by a factor of sixty or thirty-six hundred, delivered with full confidence. Units are the cheapest bug detector you will ever install: they run automatically, they never tire, and they catch precisely the errors that feel most like competence while you are making them.
