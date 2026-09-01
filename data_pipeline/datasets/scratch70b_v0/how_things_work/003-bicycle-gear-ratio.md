---
id: how-003
category: how_things_work
subcategory: mechanics
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How a bicycle gear ratio trades force for distance
approx_words: 700
---

# How a bicycle gear ratio trades force for distance

A bicycle has no engine and no battery. Everything the rider gets out of
it came from their legs. Gears cannot add energy; they can only change
the *shape* of the energy delivery — trading how hard you push against
how far you travel per push. Understanding that one trade explains
everything about why you shift.

## The chain enforces a conservation rule

Consider a chainring at the pedals with 50 teeth and a rear sprocket
with 25 teeth. The chain is inextensible and its links are a fixed
distance apart, so every tooth that leaves the chainring must arrive at
the sprocket. One full turn of the pedals pulls 50 links of chain
through. Fifty links arriving at a 25-tooth sprocket turn it exactly
twice. So the rear wheel spins twice per pedal stroke: a gear ratio of
50/25 = 2.

Now the force side. Ignore friction for a moment, which for a clean
chain costs only a few percent. Power in must equal power out, and for
rotation power is torque times angular speed. If the wheel spins twice
as fast as the pedals, it must receive half the torque per unit of
crank torque. Doubling speed halves force. That is not a design choice;
it is arithmetic forced by the chain.

## Where the road comes in

Torque at the hub is not what pushes you forward — the tire's contact
patch is. Divide hub torque by the wheel radius to get the thrust at the
road. A 700c road wheel with a tire is about 0.34 m in radius, so its
rolling circumference is about 2.1 m.

With that 2:1 ratio, one pedal revolution rolls 2 x 2.1 = 4.2 m. At a
comfortable cadence of 90 rpm you cover 378 m per minute, about 23 km/h.
Shift to a 50-tooth chainring and an 11-tooth cog and the ratio jumps to
4.5, giving 9.5 m per pedal stroke and 51 km/h at the same cadence — but
each stroke now needs roughly 2.3 times the pedal force for the same
thrust. Shift instead to a 34-tooth chainring and a 32-tooth cog, a
ratio near 1.06, and you crawl at 12 km/h while the road pushes back with
about four times less resistance per stroke than in the tall gear.

That is the whole point. Riders are not power-flexible machines. Human
legs produce their best sustained power in a narrow cadence band, very
roughly 70-100 rpm for most people, and they fatigue fast at very high
pedal forces because slow, heavy contractions restrict blood flow in the
muscle. Gears let a rider hold a good cadence and a tolerable pedal force
across road speeds from 8 km/h up a hill to 50 km/h on a descent.

## A useful shorthand: gear inches and development

Two conventions make gears comparable across bikes. *Development* is
metres travelled per pedal stroke, which is ratio times wheel
circumference. *Gear inches* is ratio times wheel diameter in inches, a
holdover from penny-farthings that answers "how big would the direct-drive
wheel have to be?" A 100 gear-inch setup is a hard sprinting gear; a
20 gear-inch setup is a loaded-touring bailout gear.

## Limiting case: what if you keep shifting to a taller gear?

Push the trade far enough and it stops paying. Suppose you are climbing
an 8 percent grade on an 80 kg bike-plus-rider system. Gravity alone
resists with roughly 0.08 x 80 x 9.8 = 63 N. In a low gear at 90 rpm
this is manageable. Shift to a gear twice as tall and, to maintain the
same road speed, your cadence halves to 45 rpm and the required pedal
force doubles.

Two things break. First, muscle physiology: at low cadence and high
force you shift toward anaerobic recruitment, lactate accumulates, and
you can hold the effort for a minute or two instead of an hour. Second,
momentum: at low cadence there are long gaps between power pulses, so
the bike decelerates noticeably between strokes, and on a steep grade it
may decelerate enough that you cannot restart the pedal stroke through
the dead spot at the top of the crank. You stall, unclip, and walk.

The reverse limit is real too. Spin a gear far too low and cadence rises
past 130 rpm, where you burn energy just accelerating and decelerating
your own legs and start bouncing in the saddle. The optimum is not
"lowest force" or "highest speed" but the ratio that puts your legs in
their efficient band for the grade you are actually on.
