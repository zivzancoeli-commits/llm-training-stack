---
id: habits-003
category: reasoning_habits
subcategory: estimation
difficulty: medium
source_model: fable-5
skills:
  - estimation
  - check-your-work
title: Bounding an answer before computing it
approx_words: 590
---

# Bounding an Answer Before Computing It

Before you compute anything, decide what range the answer is allowed to live in. This takes fifteen seconds, and it converts your later calculation from an act of faith into a checkable claim. If the exact answer lands outside the fence you built, one of the two is wrong — and the fence, being simpler, is usually right.

The technique is deliberate distortion. Take the numbers in the problem and shove them in a chosen direction. To get an **upper bound**, round every quantity the way that makes the result bigger. To get a **lower bound**, round the other way. Example: what is 487 × 512? Round both up: 500 × 600 = 300,000, so the answer is below that. Round both down: 400 × 500 = 200,000, so it's above that. Now when you compute 249,344, it lands inside the fence and you relax. If you had slipped a digit and gotten 2,493,440, the fence would have caught it immediately — a factor-of-ten error is invisible in a string of digits but glaring against a bound.

Division is where bounding earns its keep, because division errors tend to be large and directional. Splitting a $1,742 bill among 23 people: the share is more than 1,600/25 ≈ $64 and less than 1,800/20 = $90. Any computed answer near $75 is plausible; an answer of $7.57 or $757 is dead on arrival. Notice the trick for quotients: to make a fraction big, inflate the top and shrink the bottom; to make it small, do the reverse. Students who bound both numerator and denominator in the same direction get a fence that isn't one.

Bounding also works structurally, not just numerically. The average of a list is trapped between its minimum and maximum. A probability lives in [0, 1]. The hypotenuse is longer than either leg but shorter than their sum. A discount can't make a price negative. Each of these is a bound you get for free from the *type* of thing being computed, before touching any specific numbers. Half of all "absurd answer" failures — the train that travels at 4,000 km/h, the class with 170% attendance — would be caught by asking, in advance, "what values would even make sense here?"

There is a second, less obvious benefit: bounding forces you to understand the problem's shape. To round in the direction that increases the result, you must know whether each quantity pushes the answer up or down. If you can't tell whether making the denominator bigger increases or decreases the final answer, you've discovered — cheaply, before committing to a long computation — that you don't yet understand the relationship you're computing. That confusion was going to sabotage the exact calculation anyway; better to meet it during the fifteen-second version.

Two habits make bounding routine rather than heroic. First, use *round* numbers aggressively; the whole point is that 500 × 600 can be done while the pencil is still moving toward the paper. A tight bound you can't compute mentally defeats the purpose. Second, write the fence down. "Answer must be between 200k and 300k" written in the margin is a contract; a vague feeling that it's "probably six figures" is one your later self will quietly renegotiate to match whatever the calculator says.

The underlying principle: an exact computation performed once has no witness. It is a single thread of steps, and any broken link breaks silently. A bound is an independent, deliberately crude second thread. Crude is the feature. Because the bound is too simple to fail the same way the computation fails, agreement between them is real evidence — and disagreement is a fire alarm that costs almost nothing to install.
