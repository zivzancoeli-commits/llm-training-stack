---
id: math-011
category: math
subcategory: sequences
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - pattern-recognition
  - check-your-work
title: Arithmetic vs geometric sequences, closed form from a table
approx_words: 620
---

Given a table of values, the first diagnostic question is: what stays constant from row to row? If consecutive differences are constant, the sequence is arithmetic. If consecutive ratios are constant, it's geometric. That single test tells you which closed form to write down and, more deeply, whether the process behind the data is additive or multiplicative.

Here are two tables. In each, n counts the term (starting at 1) and a(n) is the value.

Table 1: n = 1, 2, 3, 4, 5 with a(n) = 7, 11, 15, 19, 23
Table 2: n = 1, 2, 3, 4, 5 with b(n) = 6, 12, 24, 48, 96

Run the test on Table 1. Differences: 11-7 = 4, 15-11 = 4, 19-15 = 4, 23-19 = 4. Constant difference d = 4: arithmetic. Ratios, for contrast: 11/7 ≈ 1.57, 15/11 ≈ 1.36 — not constant, confirming it isn't geometric.

The closed form of an arithmetic sequence comes from counting how many jumps of size d occur between term 1 and term n: exactly n - 1 of them. So a(n) = first term + (n-1) * d = 7 + 4(n-1) = 4n + 3. That n-1 (not n) is where most errors live, so verify immediately: a(1) = 4+3 = 7, correct; a(5) = 20+3 = 23, correct. Checking both an early term and a late term guards against off-by-one shifts, which often pass a single-term check by coincidence.

Now Table 2. Differences: 6, 12, 24, 48 — growing, not constant, so not arithmetic. Ratios: 12/6 = 2, 24/12 = 2, 48/24 = 2, 96/48 = 2. Constant ratio r = 2: geometric. Between term 1 and term n there are n - 1 multiplications by r, so b(n) = 6 * 2^(n-1). Verify: b(1) = 6 * 1 = 6, and b(5) = 6 * 16 = 96. Both match.

Notice the parallel structure, because it's the real lesson: arithmetic sequences apply "+d" repeatedly and the closed form is start + d(n-1); geometric sequences apply "*r" repeatedly and the closed form is start * r^(n-1). Repeated addition becomes multiplication; repeated multiplication becomes exponentiation. Same skeleton, one operation up the ladder.

A quick word on prediction, which is why closed forms matter. To find the 50th term you don't need 49 intermediate rows: a(50) = 4(50)+3 = 203, and b(50) = 6 * 2^49, an astronomically large number near 3.4 * 10^15. This contrast is worth pausing on: the arithmetic sequence grows by the same 4 forever, while the geometric one eventually adds more in a single step than the arithmetic one accumulates in its whole lifetime. Salary raises of a fixed dollar amount versus a fixed percentage is exactly this comparison, and the percentage always wins in the long run.

The common mistake is testing only differences, seeing they're not constant, and concluding the data has "no pattern," when checking ratios would have revealed a geometric law. A subtler version: testing only the first pair. The sequence 6, 12, 18 also starts with 12/6 = 2, but its next ratio is 18/12 = 1.5; it's arithmetic with d = 6. One constant difference or ratio proves nothing; you need the constancy to hold across the whole table, and even then, real-world data extends the pattern on faith, not proof.

The procedure to remember: compute all consecutive differences; if constant, write start + d(n-1). Otherwise compute all consecutive ratios; if constant, write start * r^(n-1). Verify the formula on the first term and the last term of the table. If neither test passes, try second differences (constant means quadratic) — but that's the next tool in the kit, and the differences-then-ratios test should always run first because it's the cheapest.
