---
id: math-001
category: math
subcategory: algebra
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - check-your-work
title: Completing the square on a quadratic that is not already monic
approx_words: 560
---

Completing the square is easy to demonstrate on x^2 + 6x + 5 and easy to botch on anything with a leading coefficient. Let's work a non-monic example carefully, because the leading coefficient is exactly where most errors happen.

Problem: rewrite 3x^2 - 12x + 7 in the form a(x - h)^2 + k, and use that form to find the minimum value of the expression.

Step 1: factor the leading coefficient out of the x-terms only. Do not touch the constant yet.

3x^2 - 12x + 7 = 3(x^2 - 4x) + 7

This is the move people skip. If you try to complete the square while the 3 is still glued to x^2, the "add and subtract half the coefficient squared" recipe no longer works, because that recipe assumes the quadratic is monic (leading coefficient 1).

Step 2: inside the parentheses, complete the square on x^2 - 4x. Take half of -4, which is -2, and square it to get 4. Add and subtract 4 inside:

3(x^2 - 4x + 4 - 4) + 7

Step 3: group the perfect square and pull the leftover -4 out. Here is the trap: that -4 lives inside parentheses that are multiplied by 3, so when it leaves, it becomes -12, not -4.

3((x - 2)^2 - 4) + 7 = 3(x - 2)^2 - 12 + 7 = 3(x - 2)^2 - 5

So 3x^2 - 12x + 7 = 3(x - 2)^2 - 5. Since (x - 2)^2 is never negative and equals zero exactly when x = 2, the minimum value is -5, achieved at x = 2.

Now verify, because a completed square that you haven't expanded back out is just a guess with good posture. Expand:

3(x - 2)^2 - 5 = 3(x^2 - 4x + 4) - 5 = 3x^2 - 12x + 12 - 5 = 3x^2 - 12x + 7

That matches the original, so the algebra is sound. A second, independent check: calculus or the vertex formula says the vertex of ax^2 + bx + c sits at x = -b/(2a) = 12/6 = 2, and plugging x = 2 into the original gives 3(4) - 24 + 7 = 12 - 24 + 7 = -5. Both the location and the value agree with our completed-square form.

The common mistake, spelled out: after adding 4 inside the parentheses, students subtract 4 outside the parentheses, writing 3(x^2 - 4x + 4) + 7 - 4. But you didn't add 4 to the expression; you added 4 inside a factor of 3, which means you added 12. The correction must also be 12: 3(x^2 - 4x + 4) + 7 - 12 gives the right answer. Either keep the subtraction inside the parentheses until the end (as we did) or remember that anything crossing the parentheses gets multiplied by the leading coefficient on the way out.

One more habit worth building: before you start, ask what the completed form is for. If you only need the vertex, x = -b/(2a) is faster. If you need to solve an equation, derive the roots, or set up a substitution for an integral, the full completed-square form earns its keep. Completing the square is not just a formula-producing ritual; it is the observation that every quadratic is a shifted, stretched copy of x^2, and the algebra above is how you find the shift and the stretch.
