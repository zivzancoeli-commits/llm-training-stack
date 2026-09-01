---
id: math-017
category: math
subcategory: trigonometry
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - concept-building
  - check-your-work
title: Unit circle intuition for sin and cos of 30/45/60 without memorizing only
approx_words: 660
---

The values sin(30) = 1/2, cos(45) = sqrt(2)/2, and their cousins are usually served as a table to memorize. Memorized tables evaporate under exam pressure. The better plan is to know two small geometric derivations that regenerate the whole table in under a minute, plus a checking discipline that catches transposed values.

First, what the unit circle says these numbers mean. Take a circle of radius 1 centered at the origin. Stand at angle theta from the positive x-axis; the point where your ray meets the circle has coordinates (cos(theta), sin(theta)). Cosine is the x-coordinate (horizontal reach), sine is the y-coordinate (height). Everything below is just finding coordinates of three specific points.

The 45-degree derivation. The ray at 45 degrees splits the first quadrant symmetrically, so its point has equal coordinates: x = y. The point is on the unit circle, so x^2 + y^2 = 1, giving 2x^2 = 1, x = 1/sqrt(2) = sqrt(2)/2. Therefore cos(45) = sin(45) = sqrt(2)/2 ≈ 0.707. One line of algebra from one symmetry observation.

The 30/60 derivation. Take an equilateral triangle with side 1. All its angles are 60 degrees. Drop a perpendicular from one vertex to the opposite side: it splits the triangle into two right triangles, each with angles 30-60-90, hypotenuse 1, and shortest side 1/2 (half the base — that's the split doing the work). The remaining leg comes from Pythagoras: sqrt(1 - 1/4) = sqrt(3)/2. Now read off coordinates. In a right triangle with hypotenuse 1, sine of an angle is the side opposite it. Opposite the 30-degree angle is the short side: sin(30) = 1/2. Opposite the 60-degree angle is the long leg: sin(60) = sqrt(3)/2. Cosines are the complementary reads: cos(60) = 1/2, cos(30) = sqrt(3)/2.

That's the whole table, from one square-ish symmetry and one bisected equilateral triangle:

- sin: 30 -> 1/2, 45 -> sqrt(2)/2, 60 -> sqrt(3)/2
- cos: 30 -> sqrt(3)/2, 45 -> sqrt(2)/2, 60 -> 1/2

A pattern worth noticing once you've derived it honestly: the sines are sqrt(1)/2, sqrt(2)/2, sqrt(3)/2 as the angle climbs, and the cosines run the same list backwards. Use it as a mnemonic only after the derivations justify it; a mnemonic without a derivation is just a different thing to misremember.

Now the checks. Sanity check one: sine should increase with angle in the first quadrant (you climb higher as the ray rises), and 1/2 < sqrt(2)/2 ≈ 0.707 < sqrt(3)/2 ≈ 0.866 — increasing, correct. Cosine should decrease (your horizontal reach shrinks), and it does. Sanity check two: every pair must satisfy sin^2 + cos^2 = 1, because the point is on the unit circle. Test 30 degrees: (1/2)^2 + (sqrt(3)/2)^2 = 1/4 + 3/4 = 1. Test 45: 1/2 + 1/2 = 1. Any transposition error fails one of these two checks immediately.

The common mistake is swapping sin(30) with sin(60), usually from recalling "one of them is 1/2" without the geometry. The monotonicity check is the antidote: 30 degrees is a shallow ray, barely off the ground, so its height must be the small value — sin(30) = 1/2, and if you find yourself writing sin(30) = sqrt(3)/2 ≈ 0.87, ask whether a shallow ramp can be at 87% of maximum height. It can't. Anchoring each value to the picture ("shallow angle, small height; steep angle, big height") makes the swap almost impossible.

Worked application to close the loop: a 4-meter ladder leans at 60 degrees from the ground. How high does it reach? Height = 4 * sin(60) = 4 * sqrt(3)/2 = 2 * sqrt(3) ≈ 3.46 meters. Check: at 60 degrees the ladder is steep, so it should reach most of its length — 3.46 out of 4 is 87%, consistent with a steep angle. The horizontal footprint is 4 * cos(60) = 2 meters, and 3.46^2 + 2^2 = 11.97 + 4 ≈ 16 = 4^2. Pythagoras closes the books.
