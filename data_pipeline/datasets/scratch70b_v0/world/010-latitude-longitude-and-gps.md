---
id: world-010
category: world
subcategory: geography
difficulty: easy
source_model: opus-5
skills:
  - general-knowledge
  - mechanism-explanation
title: Latitude vs longitude and why GPS needs both
approx_words: 720
---

## Two angles, not two distances

A point on a sphere needs exactly two numbers to pin it down, because a
surface is two-dimensional. Latitude and longitude are those two
numbers, and both are **angles measured from the centre of the Earth**,
not distances along the ground.

**Latitude** is the angle north or south of the equator, from 0° at the
equator to 90° at each pole. Lines of equal latitude are *parallels*:
circles that shrink as you go poleward.

**Longitude** is the angle east or west of the prime meridian, from 0°
to 180° in each direction. Lines of equal longitude are *meridians*:
half-circles that all run pole to pole and all meet at both poles.

That asymmetry is the key structural fact. Parallels never meet;
meridians always do. Consequences:

- One degree of latitude is about **111 km everywhere** — the spacing
  between parallels barely changes.
- One degree of longitude is about **111 km × cos(latitude)**. At the
  equator, 111 km. At 60° N, about 56 km. At 89°, about 2 km. At the
  pole, zero — which is why longitude is undefined at the poles.

You can use this. A rectangle "one degree by one degree" in Kenya is
roughly square and covers about 12,300 km². The same one-by-one degree
box in Norway is a stretched sliver less than half that area. This is
also the root of the map-projection problem: any flat grid must lie
about how far apart the meridians are.

## Why latitude was easy and longitude was hard

Latitude has a natural zero — the equator — fixed by the Earth's spin
axis. Measure the angle of the Sun above the horizon at local noon, or
the altitude of Polaris at night, apply a table, and you have your
latitude to within a few kilometres with a handheld instrument. Sailors
could do it in antiquity.

Longitude has **no natural zero**; every meridian is like every other,
so the prime meridian is a convention (Greenwich, agreed in 1884 largely
because British charts already used it). Worse, longitude is measured by
comparing *time*. The Earth turns 15° per hour, so if you know local
noon where you are and simultaneously know the time at the reference
meridian, the difference gives your longitude: one hour of difference is
15° of longitude.

That requires a clock that keeps reference time accurately at sea, on a
rolling ship, across temperature and humidity swings. Building one was
the central technical problem of eighteenth-century navigation, solved
in stages by John Harrison's marine chronometers. **Longitude has always
been a timekeeping problem** — which is a nice foreshadowing of GPS.

## What GPS actually does

Each satellite broadcasts a signal saying, in effect, "I am at this
position, and my atomic clock reads this time." A receiver picks up the
signal, compares the timestamp to its own clock, and multiplies the
apparent delay by the speed of light to get a distance. One distance
puts you on a sphere around that satellite. Two spheres intersect in a
circle; three, in essentially two points, one of which is absurd.

So three satellites would suffice — except that your receiver's cheap
quartz clock is not synchronised to atomic time, and at the speed of
light a one-microsecond clock error is a 300-metre position error.
Rather than carry an atomic clock, the receiver treats its own clock
offset as a **fourth unknown** alongside x, y, and z. Four unknowns need
four equations, which is why you need signals from at least four
satellites. A useful side effect: every GPS receiver is also a very
accurate clock.

The solution comes out as a 3-D position in an Earth-centred coordinate
frame. Latitude, longitude, and height are then produced by converting
that into angles relative to a **reference ellipsoid** — a smooth
mathematical figure approximating the Earth's shape, since the Earth is
slightly flattened, about 21 km less in polar radius than equatorial.

This is why the *datum* matters. The same physical point has different
latitude and longitude values under different reference ellipsoids, and
older national datums can differ from the global WGS 84 standard by
tens to hundreds of metres. A coordinate pair without a stated datum is
incomplete information — an easy way to end up hundreds of metres from
where you meant to be.
