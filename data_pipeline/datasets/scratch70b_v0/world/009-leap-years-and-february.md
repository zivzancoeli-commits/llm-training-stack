---
id: world-009
category: world
subcategory: calendars
difficulty: easy
source_model: opus-5
skills:
  - general-knowledge
  - quantitative-reasoning
title: Calendar leap years — the extra ~0.24 day and what February is doing
approx_words: 690
---

## The mismatch

A day is one rotation of the Earth. A year is one orbit around the Sun.
Nothing forces these two motions to divide evenly, and they do not.

The relevant year for calendar purposes is the **tropical year** — the
time from one March equinox to the next, which is what keeps the seasons
in place. It is about **365.2422 days**. (The orbital period measured
against the fixed stars, the sidereal year, is about 20 minutes longer;
the difference is caused by the slow precession of Earth's axis. Seasons
follow the tropical year, so that is the one calendars chase.)

So a 365-day calendar loses about 0.2422 days per year. That is under
six hours — invisible in one lifetime, but it compounds. In 100 years
you are 24 days off; in 700 years the March equinox has slid into
February and your midwinter festival is falling in autumn.

## Fix one: the Julian rule

Add one day every fourth year. That makes the average year
365.25 days — four calendar years contain 1,461 days. Compare:

```
Julian average:   365.2500
tropical year:    365.2422
error per year:  +0.0078 days
```

Small, but the wrong sign: the Julian calendar runs *slow* relative to
the seasons, gaining about one extra day every 128 years. By the
sixteenth century, roughly 1,600 years after the rule was set, the
accumulated error was about 10 days, and the equinox was arriving on
about March 11 rather than March 21. That mattered because the date of
Easter is computed from the equinox.

## Fix two: the Gregorian rule

Adopted in 1582, the Gregorian reform kept the four-year rule and added
two exceptions:

1. Years divisible by 4 are leap years.
2. Except years divisible by 100, which are not.
3. Except years divisible by 400, which are.

So 1900 was not a leap year; 2000 was. Count the leap days in a
400-year cycle: 100 multiples of 4, minus 4 century years, plus 1 back
for the multiple of 400, gives **97 leap days per 400 years**.

```
(400 * 365 + 97) / 400 = 146097 / 400 = 365.2425 days
```

That leaves an error of about 0.0003 days per year, or roughly one day
in 3,000-odd years. Good enough that no further rule is scheduled. (The
tropical year is also very slowly changing, so quoting the residual
error to more precision than this is false confidence.)

The reform also required a one-time correction, dropping ten dates in
October 1582 to put the equinox back where it belonged. Adoption was
staggered by religion and politics rather than astronomy: Catholic
countries first, Britain and its colonies in 1752 (skipping eleven days
by then), Russia in 1918, Greece in 1923.

## Why February?

Nothing astronomical. It is a fossil of Roman practice.

In the early Roman calendar the year began in March, which is why the
names of the last four months — September, October, November, December
— mean seventh, eighth, ninth, and tenth. February was the *final*
month of the year, and the tidy place to put a correction is at the end,
where it disturbs the fewest fixed festival dates.

The Roman method was odder than ours. Rather than appending a day, they
**doubled** the sixth day before the Kalends of March — the *bis sextum*
— giving two days with the same name. That is the origin of the word
*bissextile*, still the technical term for a leap year. The modern
convention of a February 29 is a later tidying up.

February's shortness has the same origin: it absorbed the leftover days
when the calendar was regularised, and it kept the intercalation duty
even after January became the start of the year.

## A related thing that is *not* this

**Leap seconds** are a different mechanism entirely. They reconcile
atomic time with the Earth's slightly irregular rotation, not the
calendar with the orbit. They are announced a few months ahead rather
than by a rule, and international bodies have agreed to phase the
practice out around 2035. Leap days handle the orbit; leap seconds
handle the spin.
