---
id: habits-009
category: reasoning_habits
subcategory: word-problems
difficulty: easy
source_model: cursor-grok
skills:
  - decomposition
title: Break a word problem into given, want, bridge
approx_words: 260
---

Most word-problem disasters are not algebra. They are grabbing the first numbers and adding them.

Write three labels.

Given: what is stated as fact. "A tank holds 120 liters. Pipe A fills at 10 L/min."

Want: the question in one sentence. "Minutes to fill from empty if A runs alone."

Bridge: the relation that ties them. Here, time = amount / rate, so 120/10 = 12 minutes.

If you cannot fill Want in a sentence, you do not know the problem yet. If Given has extra numbers (a second pipe that the question does not use), they are decoys; do not be polite to decoys.

Check by covering the story and looking only at Given/Want/Bridge. If the story's color words vanished and the math still works, you extracted it.

This habit transfers to code (inputs, outputs, invariant) and to science (data, claim, mechanism).
