---
id: how-006
category: how_things_work
subcategory: everyday
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How a microwave oven heats water-rich food, and what metal does
approx_words: 750
---

# How a microwave oven heats water-rich food, and what metal does

A conventional oven heats the outside of food and waits for conduction to
carry that heat inward. A microwave oven skips the surface: it deposits
energy directly into a layer of the food a couple of centimetres thick,
everywhere in that layer at once. The mechanism is a specific interaction
between an oscillating electric field and polar molecules — mostly water.

## The field, and why water cares

Inside the oven a magnetron produces electromagnetic waves at about 2.45
GHz, a frequency reserved internationally for industrial, scientific, and
medical use. A waveguide carries them into the metal cooking cavity,
whose walls reflect them, so the waves bounce around and fill the box.

A water molecule is bent, with the oxygen holding electron density away
from the two hydrogens. That makes it an electric dipole: one end
slightly negative, the other slightly positive. Put a dipole in an
electric field and it experiences a torque trying to align it with the
field. Now flip the field 2.45 billion times a second. The molecules try
to keep re-aligning, and in liquid water they are packed tightly enough
that this reorientation drags against neighbouring molecules through
hydrogen bonding. That friction-like drag — properly, *dielectric loss* —
converts field energy into random molecular motion, which is heat.

It is worth killing a popular myth here. 2.45 GHz is *not* a resonant
frequency of water. Water's rotational resonances are far higher, in the
tens of gigahertz and above. If ovens ran at a true resonance, the outer
millimetre of food would absorb everything and the middle would stay
frozen. 2.45 GHz was chosen partly because it is deliberately *off*
resonance, giving a penetration depth of roughly one to a few centimetres
in moist food — deep enough to heat a real portion, absorptive enough to
be efficient. Regulatory allocation and magnetron cost sealed the choice.

Two corollaries follow. Fats and sugars also absorb, though less
strongly per gram than water, which is why a jam filling scalds you while
the pastry around it is merely warm. And ice absorbs very poorly: in a
rigid crystal the water molecules cannot rotate freely, so frozen food
heats slowly until a bit of it melts, at which point the liquid absorbs
strongly and runs away with the energy. That runaway is exactly why the
defrost setting cycles the magnetron on and off, giving conduction time
to even things out instead of boiling one corner while the centre is
still ice.

## What metal does

Metal is a conductor, so the oscillating field drives real currents in
its surface rather than twisting bound dipoles. Three different outcomes
follow, and conflating them is the source of most confusion.

**Large smooth metal reflects.** The cavity walls, the metal mesh in the
door window, and a flat metal tray are all just mirrors for microwaves.
The mesh works because its holes are far smaller than the roughly 12 cm
wavelength, so the wave sees a continuous sheet while visible light,
with a much shorter wavelength, passes through. Reflection is not
dangerous in itself; it is how the oven works at all.

**Thin, pointed, or crumpled metal arcs.** Induced currents concentrate
at sharp edges and tips. Charge piles up faster than it can flow away,
the local field exceeds the breakdown strength of air (around 3 MV/m),
and you get a spark. A fork, a twist tie, a torn scrap of foil, and the
gold rim on a china plate all fail this way. Repeated arcing pits the
cavity and can ignite anything flammable nearby.

**Metal that blocks the load causes reflected power.** If most of the
energy has nothing to absorb it, it bounces back down the waveguide into
the magnetron, which heats and degrades. This is also why running an
empty oven is bad for it.

The apparent exception, a browning susceptor in packaged popcorn or
pizza, is a very thin metallised film engineered to be lossy rather than
reflective; it absorbs and gets hot enough to crisp the surface. It is
metal used deliberately, at a thickness that dissipates instead of
sparking.

## Limiting case: what if you microwave a cup of pure water in a smooth mug?

Water heats fastest of anything in the box, so this ought to be the easy
case. It is instead the classic hazard. Boiling requires nucleation
sites — scratches, dissolved gas, dust — where bubbles can form.
Microwaves heat the bulk directly rather than from a hot pan surface, so
a very smooth mug of degassed, filtered water can pass 100 C without
forming a single bubble. It becomes *superheated*.

Then you drop in a spoon or a teabag and supply a nucleation site. The
entire volume flashes to steam at once and the water erupts out of the
mug. The fix is to make nucleation easy: use a scratched or rough mug,
put a wooden stick in the cup, or heat in shorter bursts and stir. The
general lesson generalises past microwaves — when you remove the usual
mechanism that releases energy gradually, the energy does not go away,
it just waits and releases all at once.
