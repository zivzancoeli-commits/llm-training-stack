---
id: how-005
category: how_things_work
subcategory: mechanics
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How a lock and key (pin tumbler) lines up pins
approx_words: 700
---

# How a lock and key (pin tumbler) lines up pins

The pin tumbler lock on most front doors is a mechanical test with one
question: does the object inserted in the keyway have exactly the right
sequence of heights? If yes, a boundary between two sets of pins lines up
into a clean plane and a cylinder is free to rotate. If no, pins bridge
that boundary and the cylinder is physically blocked. Nothing electronic,
nothing clever — just a shear plane.

## The parts

The **shell** (or housing) is the fixed outer body bolted into the door.
Inside it sits the **plug**, a cylinder with the keyway slot cut into its
face. The plug is what turns and drives the bolt. The gap where the plug
meets the shell is the **shear line**, and it is the only thing that
matters.

Drilled through both shell and plug, usually five or six of them in a
row, are pin chambers. Each chamber holds, from the bottom up:

- a **key pin** (also called a bottom pin), of a length particular to
  that position, resting on the key when one is inserted,
- a **driver pin** (top pin), usually uniform in length,
- a light **spring** pressing the stack downward.

## At rest, the lock is jammed on purpose

With no key in the keyway, the springs push each stack down as far as it
goes. Every driver pin ends up straddling the shear line: part of it in
the shell, part of it in the plug. Five pins each acting as a steel dowel
through the boundary means the plug cannot rotate even slightly. That is
the locked state, and note that it is the *default* state — a lock fails
closed, which is why springs and gravity both push the same direction.

## What the key actually does

Look at a house key edge-on. The jagged profile is a series of flat
plateaus at different depths, one per pin position, joined by ramps. The
ramps exist only so the pins can ride up without catching as the key
slides in; the plateaus do the work.

As the key seats fully, each key pin rests on its own plateau and is
lifted by exactly that plateau's height. The key pin pushes the driver
pin above it up too. The design intent is that

    key pin length + plateau lift = distance from chamber bottom to shear line

so the *top* of every key pin arrives precisely at the shear line, and
the *bottom* of every driver pin arrives there as well. No pin crosses
the boundary any more. The plug is now a free cylinder in a hole, and a
few degrees of wrist torque rotate it, which turns the cam or tailpiece
and retracts the bolt.

Two consequences fall out of this. First, cutting depths are quantized —
a typical system uses on the order of six to ten discrete depths per
position, because manufacturing tolerance is around a hundredth of an
inch and adjacent depths must be distinguishable. Second, a five-pin lock
with eight depths has at most 8^5 = 32,768 combinations before you
subtract the ones that are unmakeable (too steep a jump between adjacent
cuts snaps the key or lets a pin fall into the wrong slot). That is a
small number by cryptographic standards, and it is why a lock is a
deterrent and a delay, not a proof.

## Limiting case: what if one pin is a hair too short?

Say a locksmith rekeys the lock and puts a key pin in chamber three that
is 0.015 inches shorter than the design calls for. The key still slides
in and four of the five stacks land perfectly. Chamber three now sits low:
the driver pin above it still crosses the shear line by 0.015 inches.

The plug will rotate a fraction of a degree until the misplaced driver
pin binds against the edge of its chamber, and then stop. From the
outside this feels like a key that "almost turns" — you get a little
motion, a gritty stop, and sometimes it works if you jiggle and lift the
key slightly, because jiggling occasionally lifts that one stack the
missing distance. Every locksmith recognises that symptom as one pin
being out of spec rather than a dead lock.

The opposite error is just as instructive. A key pin a hair too *long*
pushes its driver pin above the shear line, so the driver clears the
boundary but the key pin itself now crosses it, from the plug side into
the shell. The plug is blocked again, by a different pin in a different
direction. Both errors teach the same lesson: the requirement is not
"lift the pins" but "lift every pin to the same plane, simultaneously."
That simultaneity requirement, and the manufacturing slop that makes it
imperfect, is also exactly what lock-picking exploits.
