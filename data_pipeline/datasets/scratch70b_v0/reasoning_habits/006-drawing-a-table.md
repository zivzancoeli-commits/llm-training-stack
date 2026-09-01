---
id: habits-006
category: reasoning_habits
subcategory: representation
difficulty: easy
source_model: fable-5
skills:
  - external-representation
  - organization
title: Drawing a table instead of holding five numbers in your head
approx_words: 590
---

# Drawing a Table Instead of Holding Five Numbers in Your Head

Working memory holds about four things. Not four easy things — four things, period. The moment a problem involves five interacting quantities, some part of your mental state is silently evicted, and you will not feel it happen. You will simply, at step six, use the Tuesday number where the Wednesday number belonged, with total confidence. The cure is not concentration. The cure is paper.

Take a small logistics puzzle: three friends — Ana, Ben, Cal — split gas, food, and lodging on a trip. Ana paid $90 for gas, Ben paid $120 for food, Cal paid $60 for lodging, and they want to settle up so each bears an equal share. Attempted in the head, this problem is a juggling act: three people, three payments, a total, a fair share, and three balances — nine live quantities. Attempted on paper, it is nearly trivial:

| Person | Paid | Fair share | Balance |
|--------|------|-----------|---------|
| Ana    | 90   | 90        | 0       |
| Ben    | 120  | 90        | +30     |
| Cal    | 60   | 90        | −30     |

Total paid: 270. Share: 270 / 3 = 90. Read the balance column: Cal pays Ben $30. Done. Nothing clever happened; the table did not know any mathematics. What it did was hold the state, so that the only thing your head had to do at each moment was one subtraction.

This is the general principle: **externalize state, compute in your head only the current step.** The brain is a superb processor and a terrible register file. A table plays to that division of labor. Each cell is a fact that, once written, cannot be forgotten, swapped, or drift-corrupted. Errors become visible instead of silent — a column that should sum to 270 and doesn't is a bug you can *see*.

Tables earn their keep in several recurring situations:

**Cross-classified information.** Whenever facts come as "each X has a Y" — each person has a payment, each machine has a rate, each trial has an outcome — rows for the X's and columns for their attributes is the natural shape. Logic-grid puzzles ("the doctor lives next to the person with the cat") are essentially unsolvable without one and mechanical with one.

**Evolving processes.** For anything that changes step by step — a bank balance under repeated interest, a game state, a recursion — make columns for the step number and each tracked quantity, and fill rows downward. This turns "simulate in your imagination" into "transcribe what row n says and apply one rule."

**Case analysis.** When a problem splits into cases (even/odd, win/lose/draw), a row per case with a column per consequence prevents the classic failure of analyzing three cases and forgetting the fourth.

Two habits make tables effective rather than decorative. First, **label everything, with units.** A grid of naked numbers is a trap you set for your future self; "Paid ($)" and "Balance ($)" cost two seconds and prevent the exact swap-errors the table exists to stop. Second, **add a check row or column when the structure offers one.** Totals that must match, balances that must sum to zero, probabilities that must sum to 1 — build the invariant into the table and it audits you for free. In the trip example, the balance column summing to 0 is a proof that no money leaked.

The habit is a matter of self-respect, oddly enough. Refusing to write a table often comes from a feeling that needing one is weak. It isn't. Every accountant, physicist, and chess annotator externalizes state, precisely because their problems matter. Holding five numbers in your head isn't rigor. It's gambling — with the odds unposted.
