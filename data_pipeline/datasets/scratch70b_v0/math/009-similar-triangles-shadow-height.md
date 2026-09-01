---
id: math-009
category: math
subcategory: geometry
difficulty: easy
source_model: fable-5
skills:
  - worked-solution
  - modeling
  - check-your-work
title: Similar triangles in a shadow / height measurement
approx_words: 600
---

You can measure the height of a tree, a flagpole, or a building with nothing but a stick and the sun, and the mathematics that makes it work — similar triangles — is worth understanding because it's the same idea behind maps, scale models, and trigonometry itself.

Problem: a tree casts a shadow 18 meters long. At the same moment, a meter stick (1 meter tall) held vertically casts a shadow 1.5 meters long. How tall is the tree?

The physical claim first, because the math is only as good as the model. Sunlight rays are effectively parallel by the time they reach us. A vertical object and its shadow form a right triangle: the object is one leg, the shadow along the ground is the other, and the sun ray from the object's top to the shadow's tip is the hypotenuse. Because the sun's rays hit the stick and the tree at the same angle at the same moment, the two right triangles have equal angles, and triangles with equal angles are similar: same shape, different size. Similarity means corresponding sides are in proportion.

Set up the proportion with a consistent rule: height over shadow equals height over shadow.

tree height / tree shadow = stick height / stick shadow
H / 18 = 1 / 1.5

Solve: H = 18 / 1.5 = 12. The tree is 12 meters tall.

Check it three ways. First, the ratio interpretation: the stick is 1/1.5 = 2/3 as tall as its shadow is long, so every object at this moment is 2/3 as tall as its shadow. Two-thirds of 18 is 12. Consistent. Second, the scale-factor interpretation: the tree's shadow (18) is 12 times the stick's shadow (1.5), so the tree must be 12 times the stick's height, and 12 * 1 = 12. Same answer via a different pairing of sides, which is exactly the cross-check similarity offers: you can compare within a triangle or between the triangles, and the answers must agree. Third, plausibility: a 12-meter tree is a real tree, roughly a four-story building. If your algebra had produced 270 meters or 0.8 meters, the setup deserves a second look before the arithmetic does.

The common mistake is building the proportion inconsistently: writing H / 18 = 1.5 / 1, mixing "height over shadow" on one side with "shadow over height" on the other. That yields H = 27, and nothing about the number 27 announces that it's wrong, which is what makes the error dangerous. The defense is to state your ratio rule in words before writing fractions, then check that both sides obey it. Corresponding parts must occupy corresponding positions.

Two modeling caveats that separate textbook use from field use. The measurements must be simultaneous, or nearly so: the sun moves, and shadow lengths change noticeably within minutes near sunrise or sunset (when shadows are long, the geometry is most sensitive). And the ground must be level; a shadow running downhill is longer than the flat-ground model assumes, inflating your height estimate.

The reason this trick is a big deal historically: it's measurement by proportion, reaching lengths you can't touch. The same reasoning with the ratio given a permanent name — height/shadow is the tangent of the sun's elevation angle — is the start of trigonometry. Similar triangles are the statement that shape determines ratios; trigonometry is the systematic catalog of those ratios by angle. Master the stick-and-shadow argument and you've already understood why a tangent table can exist at all.
