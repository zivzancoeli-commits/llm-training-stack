---
id: habits-002
category: reasoning_habits
subcategory: exploration
difficulty: medium
source_model: fable-5
skills:
  - special-cases
  - pattern-finding
title: Working a special case first
approx_words: 620
---

# Working a Special Case First

When a problem asks for a general formula — "for all n," "for any triangle," "for every list" — the worst first move is to attack the general case directly. The general case is abstract, and abstraction is where intuition goes to starve. The better move is almost embarrassingly simple: try n = 1. Then n = 2. Then maybe n = 3. Watch what actually happens.

Suppose you're asked: into how many regions do n straight lines divide the plane, if no two are parallel and no three meet at a point? Staring at "n lines" produces nothing. So start small. Zero lines: 1 region. One line: 2 regions. Two lines: 4 regions. Three lines: 7 regions. Now there is data, and data suggests structure. The differences are 1, 2, 3 — each new line adds one more region than the last. The k-th line crosses the k − 1 existing lines, gets cut into k pieces, and each piece splits one region into two. That observation, discovered in the small cases, *is* the general argument. The formula 1 + n(n + 1)/2 falls out afterward, almost as an afterthought.

Notice what the small cases did. They were not the proof. They were the laboratory where the proof was found. This distinction matters, because students sometimes hear "examples aren't proofs" and conclude examples are worthless. The truth is the opposite: examples are where nearly all mathematical understanding begins. The proof is a report written after the experiment.

Special cases serve three distinct functions, and it helps to know which one you're using:

**Discovery.** As above: small cases generate a conjecture. Compute n = 1 through n = 4 or 5, look at the sequence, look at differences and ratios, guess the pattern.

**Verification.** You've derived a general formula through a page of algebra. Before trusting it, plug in n = 1. If the formula says the sum of the first n odd numbers is n² + 1, the case n = 1 gives 2, but the actual sum is 1. The formula dies in five seconds, and the page of algebra gets rechecked. A special case can never confirm a formula, but it can execute a wrong one instantly.

**Understanding the question.** Sometimes you can't even start because the statement is too abstract to parse. Working n = 2 concretely — with actual numbers, actual objects — forces you to discover what the words mean. If you cannot do the problem for n = 2, you have learned that your confusion is about the setup, not the generality.

Two cautions keep the habit honest. First, tiny cases can be *degenerate*: n = 1 sometimes satisfies a claim for trivial reasons that carry no information about n = 5. A single point is trivially collinear with itself; one team needs no schedule. When n = 1 feels suspiciously effortless, treat it as a warm-up and put your trust in n = 2 and n = 3. Second, patterns can lie. The maximum number of regions a circle is divided into by chords among n boundary points runs 1, 2, 4, 8, 16 — and then 31, not 32. Three or four cases suggest; they do not settle. The habit is "conjecture from small cases, then seek the mechanism," never "conjecture and stop."

The deeper reason this habit works is psychological. A general problem offers your mind nothing to hold. A special case gives it objects: two lines you can draw, three numbers you can add. Hands-on manipulation produces the noticing — "each new line adds one more region than the last" — and noticing is the raw material of proofs. So when you are stuck on "show that for all n," hear it as an instruction: put down the abstraction, pick up n = 2, and go see what is true.
