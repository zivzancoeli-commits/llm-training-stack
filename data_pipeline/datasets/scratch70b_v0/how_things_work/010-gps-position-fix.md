---
id: how-010
category: how_things_work
subcategory: technology
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How GPS needs several satellites to fix a position
approx_words: 750
---

# How GPS needs several satellites to fix a position

A GPS receiver is not tracked by anything. Satellites broadcast; the
receiver listens and does arithmetic. The whole system is a distance
measurement problem solved with clocks, and the reason you need four
satellites rather than three is that one of the clocks — yours — cannot
be trusted.

## Distance from time of flight

Each satellite in the constellation continuously broadcasts a signal that
encodes two things: an identifying code unique to that satellite, and the
precise time of transmission according to the atomic clocks aboard, plus
orbital data (the ephemeris) describing where the satellite is.

The receiver knows the speed of light, roughly 299,792,458 m/s. If it
knows when the signal left and when it arrived, distance is just

    range = c x (arrival time - transmission time)

A satellite about 20,200 km up gives a travel time around 67
milliseconds. Note the brutal precision requirement: light travels 30 cm
in a nanosecond, so a clock error of one microsecond is a 300 m position
error. This is why the satellites carry atomic clocks and why the ground
control segment continuously corrects them.

## Each range is a sphere

One measured range says only "I am somewhere on a sphere of radius r
centred on that satellite." Not useful alone.

Two ranges intersect two spheres in a circle. Three spheres generally
intersect in two points, and one of those two is usually absurd — far out
in space or moving at an implausible speed — so it can be discarded. So
geometrically, three satellites would locate you in three dimensions.

## Why four, then?

Because the receiver's own clock is a cheap quartz oscillator, not an
atomic standard. It might be off by a millisecond, which is a 300 km
error. If the receiver simply computed three ranges with a bad clock, all
three spheres would be wrong by the same amount and would not intersect
anywhere near the truth.

The fix is elegant. Treat the receiver clock offset as a fourth unknown
alongside x, y, z. Every measurement is then a *pseudorange*: the true
range plus c times the same unknown offset b. With four satellites you
get four equations:

    sqrt((x-x1)^2 + (y-y1)^2 + (z-z1)^2) + c*b = p1
    ... and similarly for satellites 2, 3, 4

Four equations, four unknowns. Solve, and you get position *and* an
extremely accurate time correction as a bonus. This is why GPS receivers
are used as precision time sources for telecom networks and data centres,
often more valuable there than the position.

## Corrections that matter

The naive picture needs several adjustments to reach metre-level
accuracy. Relativity is one: satellite clocks run faster than ground
clocks by about 45 microseconds a day from weaker gravity (general
relativity) and slower by about 7 microseconds a day from orbital
velocity (special relativity), a net gain near 38 microseconds a day.
Uncorrected, that alone would accumulate roughly 10 km of error per day,
so the correction is designed into the system.

The ionosphere and troposphere slow the signal in ways that vary with
water vapour and solar activity, worth several metres. Dual-frequency
receivers estimate the ionospheric delay directly, because the delay
depends on frequency. Augmentation systems broadcast correction data from
surveyed ground stations, and differential techniques can reach
centimetre-level accuracy for surveying.

## Geometry matters as much as count

Four satellites is a minimum, not a target. If all four sit clustered in
one part of the sky, the intersecting spheres cross at a shallow angle
and small range errors smear into large position errors. This is
quantified as *dilution of precision*. Satellites spread widely across
the sky give a sharp intersection and a good fix; satellites bunched near
the horizon in one direction give a poor one even with identical signal
quality. Modern receivers also use several constellations at once —
GPS, Galileo, GLONASS, BeiDou — which mostly buys better geometry and
more redundancy rather than fundamentally different physics.

## Limiting case: what if you are in an urban canyon?

Stand between tall buildings and two things go wrong at once.

First, satellites are blocked. You may see only three or four, and those
are the ones directly overhead in a narrow strip of visible sky — the
worst possible geometry. Dilution of precision balloons, and your
position wanders even though each individual measurement is fine.

Second, and worse, *multipath*. A signal from a satellite you cannot see
directly bounces off a glass facade and reaches your antenna anyway. The
receiver has no way to know the path was folded, so it computes a
pseudorange that is too long by the extra path length. That is not noise
that averages out; it is a consistent bias, and it can be tens of metres.

The symptom is familiar: your blue dot on the map sits on the wrong side
of the street, or jumps a block, or shows you inside a building. It is
also why phones fuse GPS with other sources — Wi-Fi access point
databases, cell tower positions, and the accelerometer and magnetometer
for dead reckoning. When the range measurements are geometrically weak
and biased, the honest answer is to stop trusting them alone.
