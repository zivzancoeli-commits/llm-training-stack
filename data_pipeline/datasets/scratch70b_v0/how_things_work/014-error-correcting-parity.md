---
id: how-014
category: how_things_work
subcategory: information
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How error-correcting codes can fix a flipped bit
approx_words: 800
---

# How error-correcting codes can fix a flipped bit

A cosmic ray hits a memory cell, a scratch crosses a disc, a radio packet
picks up noise, and a 0 becomes a 1. The receiver has no independent copy
to compare against, yet storage and networks routinely repair such
damage. The mechanism is sending *more* bits than the message needs,
arranged so corrupted patterns are recognisably not-a-message.

## Start with detection: one parity bit

Take four data bits, say 1011. Append a fifth bit chosen to make the
total number of 1s even. There are three 1s, so the parity bit is 1, and
you transmit 10111.

The receiver counts 1s. Even means "consistent," odd means "something is
wrong." Flip any single bit — data or the parity bit itself — and the
count becomes odd, so any single error is caught. But that is all you
get. The receiver knows *that* an error happened, not *where*, so it can
only ask for a resend. And two flips restore even parity, so a double
error slips through undetected.

## Correction needs the error to point at itself

To fix a bit you must identify which one. A counting argument tells you
how much redundancy that takes. With r parity bits you get 2^r distinct
outcomes. You need one meaning "no error" plus one for each single-bit
error position in an n-bit codeword, so

    2^r >= n + 1

With r = 3 you get 8 outcomes: "clean" plus 7 error positions. A 7-bit
codeword with 3 parity bits and 4 data bits sits exactly at that
boundary. That is the Hamming(7,4) code, and no outcome is wasted.

## Hamming(7,4), worked all the way through

Number the seven positions 1 through 7. Put parity bits at the powers of
two — 1, 2, 4 — and data at the rest — 3, 5, 6, 7. Each parity bit checks
the positions whose number has that bit set:

- p1 (position 1) checks positions 1, 3, 5, 7
- p2 (position 2) checks positions 2, 3, 6, 7
- p4 (position 4) checks positions 4, 5, 6, 7

Encode the data 1011, placing it at positions 3, 5, 6, 7:

    pos:  1  2  3  4  5  6  7
    bit:  ?  ?  1  ?  0  1  1

- p1 covers positions 3, 5, 7 = 1, 0, 1. Sum 2, even, so p1 = 0.
- p2 covers positions 3, 6, 7 = 1, 1, 1. Sum 3, odd, so p2 = 1.
- p4 covers positions 5, 6, 7 = 0, 1, 1. Sum 2, even, so p4 = 0.

The transmitted codeword is:

    pos:  1  2  3  4  5  6  7
    bit:  0  1  1  0  0  1  1

Now let noise flip position 5, so 0 becomes 1:

    pos:  1  2  3  4  5  6  7
    bit:  0  1  1  0  1  1  1

The receiver recomputes each check over its group, recording 0 if even
and 1 if odd:

- c1: positions 1,3,5,7 = 0,1,1,1. Sum 3, odd, so c1 = 1.
- c2: positions 2,3,6,7 = 1,1,1,1. Sum 4, even, so c2 = 0.
- c4: positions 4,5,6,7 = 0,1,1,1. Sum 3, odd, so c4 = 1.

Read the three results as a binary number with c4 as the most
significant bit: c4 c2 c1 = 1 0 1 = **5**. The syndrome is not merely a
flag; it is the address of the broken bit. Flip position 5 back and the
original codeword is restored, so the data 1011 comes back clean.

Why does this work? Each position belongs to a unique combination of
check groups. Position 5 is in p1 and p4 but not p2, and 5 in binary is
101 — the same pattern. Corrupting a position upsets exactly the checks
covering it, so the failing checks spell out that position. A syndrome of
000 means no single-bit error occurred.

## Limiting case: what if two bits flip?

Take the same codeword 0110011 and flip positions 5 and 6:

    pos:  1  2  3  4  5  6  7
    bit:  0  1  1  0  1  0  1

- c1: positions 1,3,5,7 = 0,1,1,1 → odd → 1
- c2: positions 2,3,6,7 = 1,1,0,1 → odd → 1
- c4: positions 4,5,6,7 = 0,1,0,1 → even → 0

Syndrome = 011 = 3. The decoder "corrects" position 3, which was never
damaged, producing a word with *three* wrong bits while reporting
success. Two errors do not merely defeat the code; they make it lie.

This is not a flaw but a consequence of the counting argument. The code
has minimum distance 3: any two valid codewords differ in at least three
positions. One flip leaves you nearer the true codeword than any other,
so nearest-neighbour decoding wins. Two flips can land you nearer a
*different* valid codeword, and the decoder cannot tell.

The standard remedy is one more parity bit over the whole word, giving
the (8,4) extended Hamming code with minimum distance 4. A double error
now produces a syndrome inconsistent with any single error, so the
decoder says "two errors, I cannot fix this" instead of guessing wrong.
That is the SECDED behaviour used in server ECC memory. High-noise
channels go further with Reed-Solomon or LDPC codes, but the trade never
changes: redundancy buys distance between valid codewords, and distance
is what error correction spends.
