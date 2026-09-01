---
id: logic-011
category: logic
subcategory: proof-technique
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - counterexample
title: The pigeonhole principle and heads of hair
approx_words: 590
---

# The pigeonhole principle and heads of hair

Claim: in any city of at least one million people, at least two residents have *exactly* the same number of hairs on their heads. Not roughly the same — exactly, to the strand. You can know this with certainty without examining a single scalp.

## The principle

If you place more than n items into n boxes, some box receives at least two items. That is the whole pigeonhole principle. It sounds too obvious to be useful, but its power comes from choosing clever boxes.

Stronger version: if you place k items into n boxes, some box receives at least ⌈k/n⌉ items (k/n rounded up). Ten pigeons in three holes force some hole to hold at least ⌈10/3⌉ = 4.

## The worked solution

**Boxes.** Human hair density and scalp area put a hard ceiling on hair count: a human head carries at most about 150,000 hairs (typical heads run 90,000–150,000; we take the generous bound). So every resident's hair count is an integer between 0 and 150,000. That gives 150,001 possible values — our boxes.

**Items.** The residents: at least 1,000,000 of them.

**Apply.** 1,000,000 people distributed among 150,001 possible hair counts. Since 1,000,000 > 150,001, some hair count is shared by at least two people. Using the stronger version: some count is shared by at least ⌈1,000,000 / 150,001⌉ = 7 people. Seven strangers in the city, follicle-for-follicle identical in number — guaranteed.

Notice what the argument did *not* need: no averages, no assumption that hair counts are evenly spread, no sampling, no probability at all. The conclusion is not "very likely"; it is forced. Pigeonhole arguments trade detail for certainty: we learn that a collision exists while learning nothing about *who* collides or *which* count they share. The proof is non-constructive, and that is a fair price.

## The tempting invalid cousin

1. There are 150,001 possible hair counts and a million people.
2. So on average about 7 people share each count.
3. Therefore *every* hair count is shared — in particular, at least two residents are completely bald (0 hairs), at least two have exactly 137,204 hairs, and so on.

The slide is from "some box has at least two" to "each box has at least two," greased by the word "average."

**Counterexample.** Distributions can be as lumpy as they like. Imagine (implausibly but consistently) that every resident happens to have between 90,000 and 110,000 hairs. All million people crowd into 20,001 boxes; collisions are massive there, while the boxes for 0 hairs, 55,000 hairs, and 150,000 hairs sit empty. Every premise of the pigeonhole setup still holds, and the true conclusion (some box has many) still holds, but the cousin's conclusion (all boxes occupied) is flatly false. Averages guarantee that *at least one* box meets or beats them; they promise nothing about any *particular* box.

## Where the same move wins

- **Birthdays:** any group of 367 people contains two who share a birthday (366 possible dates, leap years included). Certainty, unlike the probabilistic "birthday paradox" for 23 people.
- **Handshakes:** at any party of n ≥ 2 people, two attendees have shaken the same number of hands within the party — the counts 0 and n−1 cannot both occur, leaving n guests only n−1 available values.
- **Files and compression:** any lossless compressor that shortens some file must lengthen another, because there are fewer short descriptions than files.

The recipe is constant: count your items, design your boxes, and let arithmetic — not inspection — force the collision.
