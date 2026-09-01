---
id: math-006
category: math
subcategory: combinatorics
difficulty: easy
source_model: fable-5
skills:
  - worked-solution
  - concept-contrast
  - check-your-work
title: Combinations vs permutations using a lock and a committee
approx_words: 600
---

The whole combinations-versus-permutations question comes down to one test you should run on every counting problem: if I swap two of the chosen items, do I get a different outcome? If yes, order matters and you want permutations. If no, order is irrelevant and you want combinations.

Two problems that look similar and aren't.

Problem A: a padlock opens with a 3-digit code, digits 0-9, no digit repeated. How many possible codes are there?

Problem B: a class of 10 students must send 3 of them to form a committee. How many possible committees are there?

Both problems say "choose 3 from 10." Run the swap test. For the lock: is 4-7-2 the same as 7-4-2? No; entering the digits in a different order fails to open it. Order matters, so this is a permutation count. For the committee: is the committee {Ana, Ben, Cho} different from {Ben, Ana, Cho}? No; it's the same three people in the same room. Order doesn't matter, so this is a combination count.

Count the lock codes by filling slots. The first digit has 10 choices, the second 9 (no repeats), the third 8: 10 * 9 * 8 = 720. In formula language this is P(10,3) = 10! / 7! = 720.

Count the committees by starting from the 720 and repairing the overcount. Each set of 3 people got counted once for every order it could be listed in, and 3 people can be ordered 3! = 6 ways. So the 720 ordered lists collapse into 720 / 6 = 120 distinct committees. In formula language, C(10,3) = 10! / (3! * 7!) = 120. That division by 3! is the entire difference between the two formulas, and it's worth internalizing as "divide out the orderings you don't care about" rather than as a separate fact to memorize.

Verify with a small case you can list by hand. Choose 2 from the 3 letters {A, B, C}. Ordered: AB, BA, AC, CA, BC, CB, which is 6 = P(3,2) = 3 * 2. Unordered: {A,B}, {A,C}, {B,C}, which is 3 = C(3,2) = 6 / 2. The listing matches both formulas, and shrinking a problem until you can enumerate it is the most reliable check in combinatorics; formulas lie less often than setups, and the small case tests the setup.

Another check for the committee answer: C(10,3) should equal C(10,7), because choosing 3 people to serve is the same act as choosing 7 people to stay home. C(10,7) = 10! / (7! * 3!) = 120. It agrees, and this symmetry check costs nothing.

The common mistake is defaulting to whichever formula was taught most recently, but there is a sneakier version: misreading the physical situation. A "combination lock" is the classic offender, since despite its name it is a permutation device: 31-17-25 and 17-31-25 are different states of the dial. Language won't tell you which formula applies; the swap test will. A related error is forgetting the no-repetition condition. If the lock allowed repeated digits, the count would be 10^3 = 1000, a third kind of problem entirely (ordered with repetition). Before computing anything, answer two questions in order: can items repeat, and does order matter? Those two bits select among 10*9*8, 10^3, and C(10,3).

The habit to carry away: don't ask "is this a combination or a permutation?" as a vocabulary question. Ask "if I swap two selections, is the result different?" and "can the same item be picked twice?" Let the answers pick the formula, then confirm on a case small enough to list.
