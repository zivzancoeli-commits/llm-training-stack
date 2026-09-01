---
id: how-012
category: how_things_work
subcategory: thermodynamics
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How a heat pump can heat a house while being "colder" than the air inside
approx_words: 750
---

# How a heat pump can heat a house while being "colder" than the air inside

The objection sounds decisive: it is -5 C outside and 21 C inside, so how
can outdoor air heat the house? Heat flows from hot to cold, and outside
is the cold side.

The objection confuses two different quantities: *temperature* and
*quantity of thermal energy*. Cold air is not empty of heat. At -5 C the
air is still 268 kelvin above absolute zero, and every cubic metre holds
an enormous amount of molecular kinetic energy. The problem is only that
it sits at an inconveniently low temperature, and a heat pump's job is to
move it to a higher one.

## The refrigerant is the cold thing, not the outdoors

Here is the resolution. Nothing in the system ever asks heat to flow from
cold to hot on its own. The heat pump arranges for the surfaces doing
each job to be at the right temperature, using pressure as the control
knob.

Recall that a fluid's boiling point depends on pressure. Squeeze a
refrigerant and it condenses at a high temperature; let it expand and it
boils at a low one. The heat pump uses both ends of that fact.

**Outdoors, at low pressure.** Refrigerant enters the outdoor coil at
maybe -15 C. The outdoor air at -5 C is *warmer* than that, so heat flows
the ordinary direction, from air into refrigerant, boiling it into vapor.
The outdoors is the hot side of this particular exchange.

**Compressor.** The vapor is compressed. Compression does work on the
gas and raises both its pressure and its temperature, so it emerges at
perhaps 60 C. This is the step that costs electricity, and it is the step
that promotes the energy from a low temperature to a higher one.

**Indoors, at high pressure.** The hot vapor flows to the indoor coil.
At 60 C it is far warmer than the 21 C room, so heat flows the ordinary
direction again, from refrigerant into the house, and the refrigerant
condenses back to liquid.

**Expansion valve.** The liquid passes through a restriction into the low
pressure side, flash-cools to -15 C, and returns to the outdoor coil.

At no point does heat move from a colder body to a warmer one. The
refrigerant is deliberately made colder than the outdoor air when it is
collecting, and hotter than the indoor air when it is delivering. A heat
pump is a refrigerator pointed at your house; a reversing valve lets most
units swap which coil does which job, which is why the same box provides
air conditioning in summer.

## Why this beats burning something

An electric resistance heater turns 1 kW of electricity into exactly 1 kW
of heat. It cannot do better; 100 percent is the ceiling for converting
work into heat.

A heat pump is not converting, it is *pumping*, and the ceiling does not
apply. Spend 1 kW on the compressor and you might deliver 3 kW into the
house: 1 kW of compressor work plus 2 kW scavenged from outdoor air. The
ratio of heat delivered to work spent is the *coefficient of performance*,
and a COP of 3 is unremarkable for a modern unit in mild conditions.

The second law is not violated. It forbids moving heat from cold to hot
*without* doing work, and it bounds how efficient that pumping can be.
The Carnot limit for a heat pump is

    COP_max = T_hot / (T_hot - T_cold)

in kelvin. For 294 K indoors and 268 K outdoors that is 294/26 = 11.3.
Real machines reach a quarter to a third of the Carnot ceiling because of
compressor inefficiency, finite temperature differences across the coils,
and fan power. But the ceiling is well above 1, which is why the whole
approach works.

## Limiting case: what if it gets really cold outside?

The Carnot formula already warns you. Widen the gap and the ceiling
falls. At -20 C outdoors the limit drops to 294/41 = 7.2, and real
performance falls faster than the ideal does, because the compressor must
achieve a larger pressure ratio and refrigerant vapor density at the
suction side drops, so each compressor revolution moves less mass. A COP
that was 3.5 at 7 C may be 2 at -15 C.

At the same time the house needs *more* heat, since heat loss is
proportional to the indoor-outdoor difference. Capacity falls as demand
rises — the two curves converge at what installers call the *balance
point*, below which the heat pump alone cannot keep up and backup
resistance heat or a furnace takes over.

There is a second, subtler failure. When the outdoor coil runs below
freezing while outdoor air is humid, moisture condenses on it and freezes.
Frost insulates the coil and blocks airflow, so heat collection collapses.
The unit responds by running a defrost cycle: it briefly reverses,
sending hot gas to the outdoor coil to melt the ice, which means it is
momentarily air-conditioning your house. Frequent defrosts in damp
near-freezing weather are why real seasonal performance is lower than a
steady-state COP suggests. Cold-climate models fight back with
variable-speed compressors and vapor injection, and hold usable COPs well
below -20 C — but the colder it gets, the harder the pump works per unit
of heat delivered.
