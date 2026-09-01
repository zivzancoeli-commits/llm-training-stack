---
id: math-007
category: math
subcategory: algebra
difficulty: easy
source_model: fable-5
skills:
  - worked-solution
  - method-selection
  - check-your-work
title: "Linear systems: substitution vs elimination, when each is less messy"
approx_words: 640
---

You can solve any two-variable linear system with either substitution or elimination, so the interesting question isn't which one works; it's which one keeps the arithmetic clean. The answer depends on the shape of the coefficients, and you should decide before you start, not three fractions deep.

Substitution shines when a variable is already solved for, or nearly so. Consider:

y = 2x - 3
3x + 4y = 21

The first equation hands you y on a plate. Substitute into the second: 3x + 4(2x - 3) = 21, so 3x + 8x - 12 = 21, so 11x = 33, so x = 3, and then y = 2(3) - 3 = 3. Solution: (3, 3). Two lines of work, no fractions. Using elimination here would first require rearranging y = 2x - 3 into -2x + y = -3, an extra step that buys nothing.

Elimination shines when both equations are in ax + by = c form and no coefficient is 1. Consider:

3x + 4y = 10
5x - 4y = 6

The y-coefficients are already opposites, so add the equations: 8x = 16, so x = 2, then 3(2) + 4y = 10 gives 4y = 4, y = 1. Solution: (2, 1). Try substitution on this system and you'll see the mess: solving the first equation for x gives x = (10 - 4y)/3, and substituting that into the second forces you to push 5(10 - 4y)/3 through the algebra, fractions everywhere. Same answer, triple the opportunities for error.

When the coefficients don't line up so kindly, elimination still usually wins for standard-form systems, at the cost of one scaling step. For

2x + 3y = 7
5x + 2y = 12

multiply the first equation by 2 and the second by 3 to make the y-coefficients both 6: 4x + 6y = 14 and 15x + 6y = 36. Subtract: 11x = 22, x = 2, then y = 1. The multipliers came from cross-scaling the y-coefficients (2 and 3 -> both 6). Choose to eliminate whichever variable has the friendlier least common multiple; eliminating x here would have meant scaling to 10, also fine, but with bigger intermediate numbers.

Whatever route you take, verify in both original equations, not just one. Check (2, 1) in the last system: 2(2) + 3(1) = 7, good; 5(2) + 2(1) = 12, good. Checking only one equation is a half-check: any point on that single line would pass it. The solution of a system is the point on both lines, so the certificate requires both. This costs ten seconds and catches nearly every arithmetic slip.

The common mistake in elimination is a sign error during subtraction: subtracting 15x + 6y = 36 from 4x + 6y = 14 means computing 4x - 15x = -11x and 14 - 36 = -22, every term negated consistently. Students frequently subtract the x-terms one way and the constants the other way, producing 11x = -22 and a wrong answer that looks plausible. A defensive habit: instead of subtracting, multiply one equation by -1 and add, since addition is harder to fumble. The common mistake in substitution is forgetting parentheses: substituting 2x - 3 for y in 4y and writing 4 * 2x - 3 instead of 4(2x - 3). The parentheses are load-bearing.

Decision rule to internalize: if either equation has an isolated variable or a coefficient of 1 or -1, substitute. If both equations are in standard form with coefficients bigger than 1, eliminate, and pick the variable whose coefficients have the smallest common multiple. And if the system comes from a word problem, set it up in whichever form falls out naturally, then choose the method that fits what you wrote, not the one you happen to like. The method is a tool choice, and the best tool is the one that minimizes the number of fractions you have to carry.
