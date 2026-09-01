---
id: math-003
category: math
subcategory: algebra
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - proof-sketch
  - check-your-work
title: Why the quadratic formula is completing the square in disguise
approx_words: 620
---

Students often meet the quadratic formula as a chant: "negative b, plus or minus the square root of b squared minus four a c, all over two a." It works, but chanting is fragile. If you see where the formula comes from, you can rebuild it on demand and you understand what the discriminant is actually measuring. The secret is that the formula is nothing more than completing the square performed once, in general, with letters instead of numbers.

Start with the general quadratic equation ax^2 + bx + c = 0, with a not zero. Follow exactly the same steps you would use on a numeric problem.

Step 1: make it monic. Divide everything by a:

x^2 + (b/a)x + c/a = 0

Step 2: move the constant to the other side:

x^2 + (b/a)x = -c/a

Step 3: complete the square. Half of b/a is b/(2a); its square is b^2/(4a^2). Add that to both sides:

x^2 + (b/a)x + b^2/(4a^2) = b^2/(4a^2) - c/a

The left side is now a perfect square by construction:

(x + b/(2a))^2 = b^2/(4a^2) - c/a

Step 4: clean up the right side over a common denominator 4a^2:

(x + b/(2a))^2 = (b^2 - 4ac) / (4a^2)

Step 5: take square roots of both sides, remembering both signs:

x + b/(2a) = +/- sqrt(b^2 - 4ac) / (2a)

Step 6: isolate x:

x = (-b +/- sqrt(b^2 - 4ac)) / (2a)

That is the whole derivation. Every piece of the chant now has a meaning. The -b/(2a) term is the center of the parabola, the x-coordinate of the vertex, which the completed square exposed as the shift. The +/- sqrt(b^2 - 4ac)/(2a) term is the distance from that center out to each root; the two roots sit symmetrically around the vertex. And the discriminant b^2 - 4ac is the quantity whose sign decides everything: positive means the parabola crosses the axis twice, zero means it kisses the axis at the vertex, negative means the square root goes imaginary and there are no real roots.

Check it on a concrete case where we can factor by eye. Take 2x^2 - 8x + 6 = 0, which factors as 2(x - 1)(x - 3) = 0, roots 1 and 3. The formula: a = 2, b = -8, c = 6, so the discriminant is 64 - 48 = 16, and x = (8 +/- 4)/4, giving 3 and 1. It agrees. Also check the structure: the vertex should be at -b/(2a) = 2, and indeed 1 and 3 are symmetric about 2, each a distance sqrt(16)/(2*2) = 1 away. The formula isn't just producing numbers; its two halves are reporting the center and the half-width of the root pair.

The common mistake in the derivation is in Step 3: adding b^2/(4a^2) to the left side but forgetting to add it to the right side, or adding b^2/4 instead because the divide-by-a step was skipped. Both errors come from treating "half the coefficient, squared" as an incantation instead of asking: half of which coefficient? The recipe requires the monic form, which is why Step 1 exists.

One more payoff for knowing the derivation. Sum and product of roots fall out for free: the two roots are -b/(2a) + d and -b/(2a) - d where d is the half-width, so their sum is -b/a (the d's cancel) and their product is b^2/(4a^2) - d^2 = c/a. These are Vieta's formulas, and you just proved them without any extra work. A memorized formula gives you answers; a derived one gives you answers plus all its consequences.
