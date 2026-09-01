---
id: math-010
category: math
subcategory: number-theory
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - concept-building
  - check-your-work
title: Modular arithmetic via 12-hour clocks and remainders
approx_words: 640
---

You already do modular arithmetic every day. If it's 9 o'clock and a meeting is in 5 hours, you don't say "14 o'clock" (unless you use a 24-hour clock); you wrap around and say 2. That wrap-around is arithmetic modulo 12, and making it precise unlocks a surprising amount of number theory.

Problem: it is 9:00 now. What time will the clock show in 1,000 hours?

The clock only cares about the remainder of the total hour count when divided by 12, because every 12 hours it returns to the same face. So compute 9 + 1000 = 1009, then find the remainder of 1009 divided by 12. Since 12 * 84 = 1008, we get 1009 = 12 * 84 + 1, remainder 1. The clock will show 1:00.

In notation: 1009 ≡ 1 (mod 12), read "1009 is congruent to 1 modulo 12," meaning 1009 and 1 leave the same remainder on division by 12, or equivalently that 12 divides their difference (1009 - 1 = 1008 = 12 * 84).

Verify by a different route, which is the habit that makes modular arithmetic reliable: reduce early instead of late. Instead of adding first, reduce 1000 mod 12 first: 12 * 83 = 996, so 1000 ≡ 4 (mod 12). Then 9 + 4 = 13 ≡ 1 (mod 12). Same answer. This isn't luck; it's the fundamental theorem of the subject: you may reduce at any point during additions and multiplications without changing the final remainder. (a + b) mod n = ((a mod n) + (b mod n)) mod n, and the same for products. That freedom is what makes huge computations feasible.

Use it on something that looks impossible by hand: what is the remainder of 7^100 divided by 12? Don't compute 7^100. Compute 7^2 = 49, and 49 = 48 + 1, so 7^2 ≡ 1 (mod 12). Then 7^100 = (7^2)^50 ≡ 1^50 = 1 (mod 12). A number with 84 digits, tamed in two lines, because we reduced early and spotted a cycle. Cycles are the signature of modular arithmetic: since only finitely many remainders exist (0 through 11 for mod 12), repeated multiplication must eventually loop, and finding the loop replaces brute force.

Quick checks you can always run. Any claimed remainder mod 12 must lie in 0..11; if your work produces 14, you forgot a final reduction (14 ≡ 2). And you can spot-check congruences with small concrete cases: to trust that reducing early works, test (10 + 7) mod 6 = 17 mod 6 = 5 against ((10 mod 6) + (7 mod 6)) mod 6 = (4 + 1) mod 6 = 5. Testing an algebraic rule on numbers small enough to verify directly is cheap insurance.

The common mistake: assuming the reduce-early freedom extends to division. It doesn't, at least not naively. For example, 12 ≡ 0 (mod 12) obviously, but "dividing both sides by 4" would suggest 3 ≡ 0 (mod 12), which is false. Division in modular arithmetic means multiplying by a modular inverse, and an inverse of a mod n exists only when a and n share no common factor. Since 4 and 12 share the factor 4, dividing by 4 mod 12 is not a legal move. Addition, subtraction, and multiplication are always safe; division requires a coprimality check first.

One closing reframe. "Clock arithmetic" sounds like a toy, but the pattern — do arithmetic, keep only remainders — is how computers handle overflow (arithmetic mod 2^64), how ISBN and credit-card check digits catch typos (checksums mod 10 or 11), and how RSA encryption works (exponentiation mod a large number, made fast by exactly the reduce-early-and-find-cycles technique we used on 7^100). When it's 9:00 and you correctly predict the clock face 1,000 hours out, you're running the same mathematics that verifies your credit card number.
