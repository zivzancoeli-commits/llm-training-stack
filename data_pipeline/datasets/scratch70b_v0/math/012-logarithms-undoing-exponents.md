---
id: math-012
category: math
subcategory: algebra
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - concept-building
  - check-your-work
title: Logarithms as undoing exponents, change of base with a calculator story
approx_words: 650
---

A logarithm answers one question: what exponent do I need? That's the entire concept. log_2(32) asks "2 to what power gives 32?" and the answer is 5 because 2^5 = 32. Every log rule and every calculator trick follows from keeping that question in view.

Start with a concrete problem. You invest $1,000 at 6% annual growth, compounded yearly, so after t years you have 1000 * 1.06^t. How long until the money doubles?

Set up the equation: 1000 * 1.06^t = 2000, so 1.06^t = 2. The unknown is in the exponent, which is precisely the situation logarithms exist for. Taking the base-1.06 logarithm of both sides "undoes" the exponential:

t = log_1.06(2)

That's an exact answer, but here comes the calculator story. You reach for a calculator and find it has no log-base-1.06 button. It has log (base 10) and ln (base e), and that's all. Are you stuck?

No, because of the change-of-base rule: log_b(x) = log(x) / log(b), using any base you like for the two logs on the right, as long as it's the same base for both. So:

t = log(2) / log(1.06) = 0.30103 / 0.02531 ≈ 11.9 years

Using ln instead: t = ln(2) / ln(1.06) = 0.69315 / 0.05827 ≈ 11.9. Same answer, as the rule promises. The doubling time is about 11.9 years. (The folk "rule of 72" predicts 72/6 = 12 years — a handy plausibility check, and our precise answer sits right next to it.)

Why does change of base work? Go back to the defining question. Let y = log_1.06(2), which means 1.06^y = 2. Take log base 10 of both sides: log(1.06^y) = log(2). The power rule for logs — itself just a restatement of (b^m)^n = b^(mn) — lets the exponent hop down in front: y * log(1.06) = log(2). Divide: y = log(2)/log(1.06). The rule isn't a separate fact to memorize; it's two applications of "a log is an exponent."

Verify the final answer the honest way, by plugging back into the original growth model. 1.06^11.9: compute via exponentials or stepwise — 1.06^12 ≈ 2.012, and 1.06^11.9 ≈ 2.0. Money after 11.9 years: about $2,000. The answer survives contact with the original equation, which is the check that matters; verifying only the log manipulation would test the algebra but not the setup.

While we're here, the three log rules worth owning, each a translation of an exponent law: log(xy) = log(x) + log(y) (because b^m * b^n = b^(m+n): multiplying numbers adds their exponents); log(x/y) = log(x) - log(y); and log(x^n) = n * log(x). Logs turn multiplication into addition, which is why slide rules worked and why plotting data on a log scale turns exponential curves into straight lines: the log of 1000 * 1.06^t is log(1000) + t * log(1.06), literally a line in t.

The common mistake is inventing a fourth rule that doesn't exist: log(x + y) = log(x) + log(y). It's false — logs convert multiplication to addition, so there is no clean rule for the log of a sum. Test it numerically the moment you're tempted: log(10 + 10) = log(20) ≈ 1.30, while log(10) + log(10) = 2. Not equal, not close. A five-second numeric test kills a bad rule faster than any amount of squinting at symbols; make that test a reflex whenever you "remember" an identity you're not sure of.

The takeaway: whenever the unknown is in an exponent, a logarithm is the tool; whenever the base isn't on your calculator, change of base means "divide two logs of any base you do have"; and whenever you finish, substitute the answer back into the original problem, not the transformed one.
