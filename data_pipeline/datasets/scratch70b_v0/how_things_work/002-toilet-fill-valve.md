---
id: how-002
category: how_things_work
subcategory: everyday
difficulty: easy
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How a toilet fill valve stops the water
approx_words: 650
---

# How a toilet fill valve stops the water

A toilet tank refills itself and then shuts off without any electricity,
sensor, or timer. The mechanism is a float that reports water level and
a valve that is held closed by the water supply's own pressure. It is
one of the cleanest examples of mechanical negative feedback in a house.

## The two jobs in the tank

Two separate parts share the tank. The **flush valve** is the big
opening in the bottom, capped by a flapper or a canister seal. Pushing
the handle lifts that seal, the tank dumps its water into the bowl, and
the seal drops back onto its seat as the level falls. The **fill valve**
is the tall column on the left, connected to the supply line under the
tank. Its job is to notice that the tank is empty and refill it to a
precise level. These two are independent; most toilet complaints trace
to one or the other, not both.

## The float is the sensor

Older toilets use a hollow ball on a long brass arm. Newer ones use a
plastic cup float that slides up and down the fill valve's own shaft.
Either way the physics is the same: the float is buoyant, so it rides at
the water surface and its height *is* the water level, converted into
mechanical position. The float is linked to the valve, so the valve
"knows" the level without measuring anything.

## The valve is pressure-assisted, not muscle-powered

Here is the part people usually get wrong. The float is not strong
enough to force a valve shut against 40-60 psi of city water. A ball on
a lever cannot generate that much force. Instead, most fill valves are
*diaphragm* valves that use the supply pressure to shut themselves.

Inside the valve cap is a flexible rubber diaphragm. Supply water sits
under it, and a small chamber sits above it, fed by a pinhole that bleeds
water from the supply side. When the chamber above is full and
pressurized, the pressure on top acts over a larger area than the inlet
port below, so the diaphragm is pressed firmly onto its seat and the
valve is closed. Water pressure holds itself back.

To open, the float only has to uncover a tiny pilot port that lets the
upper chamber drain. That takes almost no force, because the port is
small. Once the upper chamber vents, pressure above the diaphragm
collapses, supply pressure below lifts the diaphragm off its seat, and
full flow rushes into the tank. When the tank refills, the rising float
pushes the pilot port shut, the pinhole slowly re-pressurizes the upper
chamber, and the diaphragm snaps closed again.

Some of that incoming water is diverted through a thin refill tube into
the overflow pipe. That is not waste; it is deliberately restoring the
water seal in the bowl, which is what blocks sewer gas from entering the
room.

## Limiting case: what if the flapper leaks?

Suppose the flapper at the bottom has gone stiff and no longer seats
perfectly. Water trickles from the tank into the bowl continuously. The
tank level drops a few millimetres, the float follows it down, the pilot
port cracks open, and the fill valve turns on to top the tank back up.
Level rises, valve shuts, trickle continues, level falls again.

The result is the "phantom flush": a toilet that hisses for twenty
seconds every few minutes with nobody in the room. Notice that the fill
valve is behaving perfectly. It is a feedback loop doing exactly its job
in the presence of a leak, which is why replacing the fill valve does
not fix this symptom and replacing the eight-dollar flapper does.

The mirror-image failure is a float set too high or a float that has
sprung a leak and taken on water. A waterlogged float rides low, so the
valve never sees "full," and water keeps coming until it pours down the
overflow tube — a toilet that runs forever without the tank ever
overflowing onto the floor. That overflow tube is a deliberate safety
feature, sized so the fill valve cannot outrun it. The failure mode is a
wasted-water bill instead of a flooded bathroom, which is a decent
trade to design in.
