---
id: math-016
category: math
subcategory: functions
difficulty: easy
source_model: fable-5
skills:
  - worked-solution
  - check-your-work
title: Inverse of a linear function and how to check by composition
approx_words: 590
---

An inverse function runs a machine backwards: if f takes inputs to outputs, f^(-1) takes each output back to the input it came from. For linear functions the mechanics are short, which makes them the right place to build the habit that matters for every inverse you'll ever compute — checking by composition.

Problem: find the inverse of f(x) = 3x - 6, and verify it.

Think about what f does as a two-step process: multiply by 3, then subtract 6. To undo it, reverse the steps in reverse order, like taking off shoes and socks: first add 6 back, then divide by 3. So the inverse should be f^(-1)(x) = (x + 6)/3. That's the conceptual route, and it's worth doing first because it predicts the answer the algebra should produce.

Now the algebraic route. Write y = 3x - 6, then swap the roles of input and output (because the inverse's input is f's output) and solve for the new output:

x = 3y - 6
x + 6 = 3y
y = (x + 6)/3

So f^(-1)(x) = (x + 6)/3, matching the undo-the-steps prediction. When two different methods agree, confidence is earned rather than assumed.

But the real certificate is composition. The defining property of an inverse is that applying f then f^(-1) (or the other way) lands every number exactly where it started: f^(-1)(f(x)) = x and f(f^(-1)(x)) = x. Check both directions.

Direction one: f^(-1)(f(x)) = f^(-1)(3x - 6) = ((3x - 6) + 6)/3 = 3x/3 = x. Good.

Direction two: f(f^(-1)(x)) = f((x + 6)/3) = 3 * (x + 6)/3 - 6 = (x + 6) - 6 = x. Good.

Both compositions collapse to x, so the inverse is correct — not "probably correct," but certified, because that collapse is what "inverse" means. A quick numeric spot-check adds comfort: f(4) = 6, and f^(-1)(6) = 12/3 = 4. Round trip complete.

The common mistake is confusing the inverse function f^(-1)(x) with the reciprocal 1/f(x). The notation invites the error: x^(-1) means 1/x, so surely f^(-1) means 1/f? It doesn't. Here 1/f(x) = 1/(3x - 6), and composing it with f gives f(1/(3x-6)) = 3/(3x - 6) - 6, which is nowhere near x. The composition check exposes the impostor instantly, which is exactly why the check should be reflexive: it distinguishes the true inverse from every plausible-looking wrong answer. A second frequent slip is undoing the steps in the original order (dividing by 3 first, then adding 6), yielding x/3 + 6. Test it: composing gives (3x - 6)/3 + 6 = x - 2 + 6 = x + 4, not x. Wrong, and the check said so. Reverse order is essential: last operation applied is first operation undone.

Two structural observations that deepen the picture. First, the inverse of a linear function y = mx + b is again linear, with slope 1/m: ours went from slope 3 to slope 1/3. That's forced by geometry — the graph of f^(-1) is the graph of f reflected across the line y = x, and reflecting a line of slope m produces a line of slope 1/m. (You can spot-check the reflection: f passes through (4, 6), and f^(-1) passes through (6, 4).) Second, the slope observation explains when the method fails: a horizontal line y = b (slope 0) has no inverse, since every input produces the same output and the machine can't be run backwards — given output b, there's no way to know which input you started from. Invertibility requires distinct inputs to give distinct outputs, and for lines that means m ≠ 0.
