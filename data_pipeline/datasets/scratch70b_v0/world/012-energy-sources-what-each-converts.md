---
id: world-012
category: world
subcategory: energy
difficulty: medium
source_model: opus-5
skills:
  - general-knowledge
  - comparative-analysis
title: Energy — fossil vs nuclear vs hydro vs wind and solar, and what each is converting
approx_words: 790
---

No power plant creates energy. Every one of them takes energy that is
already stored somewhere and converts it into electricity. The clearest
way to compare them is to ask, for each: **what store is it drawing
down, and what conversion steps stand between that store and the wire?**

## Fossil fuels: ancient sunlight, released as heat

Coal, oil, and gas are chemical energy locked in reduced carbon
compounds. That carbon was reduced by photosynthesis tens to hundreds of
millions of years ago and buried before it could decay. Burning it
reverses the reaction with oxygen and releases the difference as heat.

The chain is: chemical → heat → steam or hot gas → turbine rotation →
generator → electricity.

That first heat step is the expensive one. Any engine that turns heat
into work is bounded by the Carnot limit, which depends on the
temperatures of the hot and cold sides. Real plants come in well under
the theoretical ceiling: a conventional coal plant converts roughly
33–40% of the fuel's chemical energy into electricity, and a modern
combined-cycle gas plant — which runs a gas turbine and then reuses its
exhaust heat to run a steam turbine — reaches roughly 55–64%. The rest
leaves as warm water and warm air. Combustion also unavoidably produces
CO2, because the carbon is the fuel.

## Nuclear fission: nuclear binding energy, also released as heat

A uranium-235 nucleus absorbs a neutron and splits. The fragments plus
the freed neutrons weigh slightly less than the original; that missing
mass appears as kinetic energy of the fragments, per E = mc². The
fragments slam into surrounding material and the reaction becomes heat.

From there the chain is identical to a coal plant — heat, steam,
turbine, generator — and so is the Carnot penalty, giving thermal
efficiencies typically around a third. The difference is entirely in the
density of the store. Fission releases on the order of a million times
more energy per kilogram of fuel than chemical burning, which is why
fuel logistics are trivial and waste volumes are tiny, and why the
engineering problems are instead about containment, decay heat after
shutdown, and long-lived radioactive fission products.

## Hydro: gravitational potential energy, no heat engine

Water behind a dam has potential energy because it is above the
turbines. Release it and the potential converts to kinetic energy, which
spins a turbine directly.

There is no heat step, so there is no Carnot limit, and modern hydro
plants convert something like 85–90% or more of the available potential
energy into electricity. What lifted the water in the first place was
solar evaporation, so hydro is stored sunlight too — with the atmosphere
acting as the pump and the reservoir acting as the battery. That storage
is hydro's most valuable and under-appreciated property: output can be
dispatched on demand, and pumped-storage schemes can run the cycle
backwards to absorb surplus power.

## Wind: kinetic energy of moving air

Sunlight heats the surface unevenly, air masses of different density
move, and a turbine extracts some of that kinetic energy.

Two relationships govern everything. Available power is proportional to
the swept area — the square of blade length — and to the **cube** of
wind speed. Doubling wind speed gives eight times the power, which is
why site selection dominates economics and why turbines keep getting
larger. And a turbine cannot take all the energy in the wind, because
the air must keep moving to get out of the way; the theoretical maximum
share, the Betz limit, is 16/27, about 59%. Good turbines get a
substantial fraction of that.

## Solar photovoltaic: photons to charge carriers, directly

A PV cell is the odd one out: no turbine, no moving parts, no heat
engine. A photon with enough energy knocks an electron loose in a
semiconductor, and the junction's built-in electric field pushes
electron and hole in opposite directions, producing a current.

Efficiency is limited differently. Photons below the band gap pass
through unused; photons well above it lose the excess as heat. For a
single-junction silicon cell this Shockley–Queisser reasoning caps
efficiency near 33%; commercial modules today are typically around
20–23%, and multi-junction cells do better at higher cost.

## The comparison that matters

Group them by conversion type and the trade-offs fall out. **Heat-engine
sources** (fossil, nuclear) pay the Carnot tax but store their fuel, so
they run when asked. **Direct-conversion sources** (hydro, wind, solar)
skip the tax but depend on a flow they do not control — except hydro,
which has a reservoir. That is why the systems question is rarely "which
is most efficient" and usually "what mix of dispatchable capacity,
storage, transmission, and demand flexibility makes the variable
sources usable."
