---
id: how-007
category: how_things_work
subcategory: electrical
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How a LED differs from an incandescent in where the energy goes
approx_words: 700
---

# How a LED differs from an incandescent in where the energy goes

Both bulbs take electrical energy in and must send all of it back out,
since energy is conserved. The difference is the accounting: what
fraction leaves as visible light versus as heat. An incandescent loses
that argument badly, and the reason is baked into the physics of how it
makes light at all.

## Incandescent: light as a side effect of being hot

An incandescent bulb passes current through a coiled tungsten filament
maybe 0.02 mm thick. Resistance converts electrical energy to heat, and
the filament climbs to roughly 2,700 K. Any object at that temperature
radiates, and the spectrum it radiates is essentially a blackbody curve.

That is the whole problem. Wien's displacement law puts the peak of a
2,700 K blackbody at about 1,070 nm — deep in the infrared, well past
the roughly 400-700 nm band the eye can see. The visible light we use is
just the short-wavelength tail of a curve whose bulk sits in the IR.
Integrate the curve and only about 5-10 percent of the radiated power
lands in the visible. The rest leaves as infrared, which is absorbed by
walls, furniture, and people, and becomes room heat.

You cannot fix this without breaking the bulb. Pushing the filament
hotter would shift the peak toward visible and raise efficiency — but
tungsten melts at 3,695 K, and evaporation rate climbs steeply well
before that, so a hotter filament thins, develops a hot spot, and fails.
Halogen bulbs buy a few hundred kelvin by adding a halogen gas that
redeposits evaporated tungsten back on the filament, which is worth maybe
a 30 percent efficiency gain and no more. Thermal emission is a
fundamentally inefficient way to make a narrow band of wavelengths.

A 60 W incandescent yields roughly 800 lumens, about 13-15 lumens per
watt.

## LED: light from an electronic transition, not from temperature

A light-emitting diode makes light by a completely different route. It is
a semiconductor junction: an n-type region with mobile electrons meets a
p-type region with mobile holes. Forward-bias the junction and carriers
are pushed into an active region where electrons drop into holes. Each
recombination event releases energy equal to the material's band gap, and
in a *direct* band gap semiconductor like indium gallium nitride that
energy leaves as a single photon.

The consequence is that wavelength is set by chemistry, not temperature.
A band gap of about 2.7 eV gives blue photons near 460 nm and essentially
nothing in the infrared. There is no long IR tail to throw away, because
no transition exists at those energies. White LEDs are almost always a
blue die coated in a phosphor that absorbs some blue and re-emits broad
yellow; blue plus yellow reads as white. That phosphor conversion costs
energy — the Stokes shift, the difference between the absorbed blue
photon and the emitted yellow one, is lost as heat — but it is a modest
tax, not a 90 percent one.

A good general-service LED lamp delivers 80-120 lumens per watt today,
with laboratory devices well above that. So replacing 800 lumens of
incandescent takes about 8 W instead of 60 W.

## Where the heat goes matters, not just how much

Here is the part that surprises people. LEDs still make heat — maybe 60
to 75 percent of input power in a real lamp, once you count non-radiative
recombination, phosphor losses, and driver electronics. The difference is
*where* it appears. An incandescent's waste energy leaves as radiation,
so the filament sheds it whether you like it or not. An LED's waste
appears as conducted heat in the semiconductor die itself, a chip a
fraction of a millimetre across, and it must be carried out through the
package into a heat sink. That is why LED bulbs have finned aluminium
bodies and incandescents do not.

## Limiting case: what if the LED cannot get rid of its heat?

Seal an LED lamp into a tight insulated recessed ceiling can, or run one
in a fully enclosed glass fixture, and the heat sink has nowhere to dump
its heat. Junction temperature climbs, and several things degrade at
once.

Efficiency drops, because at higher temperature a larger share of
recombination goes through non-radiative paths — the diode makes fewer
photons per electron. Colour shifts, because the phosphor's conversion
efficiency is temperature-dependent, so the light drifts warmer and
dimmer. And lifetime collapses: LED degradation is strongly
temperature-driven, so a lamp rated for 25,000 hours at an 85 C junction
may reach only a few thousand hours at 120 C. The electrolytic capacitors
in the cheap driver circuit often die even sooner, which is why a failed
LED bulb usually goes dark suddenly rather than fading.

Note the asymmetry this creates. An overheated incandescent simply burns
out slightly sooner; its performance does not sag first. An overheated
LED quietly loses the very efficiency you bought it for. Buying a lamp
marked "suitable for enclosed fixtures" is buying a thermal design, not a
different light source.
