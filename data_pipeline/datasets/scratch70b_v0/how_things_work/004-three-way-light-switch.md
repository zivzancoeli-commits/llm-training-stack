---
id: how-004
category: how_things_work
subcategory: electrical
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How a three-way light switch can work from two locations
approx_words: 700
---

# How a three-way light switch can work from two locations

A stairway light you can turn on at the bottom and off at the top looks
like it requires the two switches to communicate. They do not. The trick
is that neither switch is an on/off switch at all. Each one is a
*selector* that routes the circuit down one of two paths, and the light
is on exactly when both switches happen to have picked the same path.

This is a conceptual walkthrough, not a wiring guide. Real household
wiring is governed by electrical codes, involves neutrals, grounds, and
box-fill rules, and mains voltage can kill you. Treat what follows as
the logic, and leave the copper to a licensed electrician.

## An ordinary switch versus a three-way switch

A normal wall switch is a *single pole, single throw* device: one input
terminal, one output terminal, and a contact that either bridges them or
does not. Two of these in series would give you a light that only works
when both are on — annoying, not useful. Two in parallel would give you
a light you can turn on from either end but never turn off from the far
end. Neither behaves like a stairway.

A three-way switch (called a two-way switch in British usage — the names
count different things) is *single pole, double throw*. It has one
"common" terminal and two "traveler" terminals. The internal contact
always connects the common to exactly one traveler. There is no off
position. Flipping the toggle just moves the connection from traveler A
to traveler B.

## The two-rail picture

Imagine the circuit as a path that has to run from the hot supply,
through switch one, along one of two parallel rails, through switch two,
and on to the lamp.

- Hot supply enters switch one's common terminal.
- Switch one's two travelers become the two rails, running to switch
  two's two traveler terminals.
- Switch two's common runs to the lamp, and the lamp returns to neutral.

Current can only flow if the rail that switch one selected is the same
rail switch two selected. Write out the four cases:

| Switch 1 picks | Switch 2 picks | Continuous path? | Lamp |
|---|---|---|---|
| rail A | rail A | yes | on |
| rail A | rail B | no  | off |
| rail B | rail A | no  | off |
| rail B | rail B | yes | on |

That table is exactly the logical operation XNOR — "on when the two
agree." The useful property of XNOR for this job is that flipping either
input always flips the output, no matter what the other input is doing.
That is precisely the behavior you want on a staircase: whoever touches a
switch changes the light, and neither switch has a privileged "on"
position. This is also why the toggles do not stay aligned with up-means-on;
after a while, up on one switch may mean off, which bothers some people
and is inherent to the design.

## Adding a third location

To control the light from three or more places you keep the two
three-way switches at the ends and insert *four-way* switches in the
middle of the traveler pair. A four-way switch has two inputs and two
outputs and does one of two things: pass the pair straight through, or
cross them over. Each crossover flips which rail carries the signal, so
each middle switch also inverts the result. Chain as many as you like;
the "flip any switch, flip the light" property survives, because every
switch in the chain is an inverter of the same shared state.

## Limiting case: what if one traveler wire breaks?

Suppose rail B develops an open, perhaps a wire nut that worked loose in
a junction box. Now trace the table again. Any combination that needed
rail B fails, and only the rail A / rail A case still lights the lamp.

The symptom is characteristic and diagnostic. The light no longer works
from either location independently; instead it works only when both
switches sit in one specific pair of positions. From the top of the
stairs the switch seems dead unless someone has left the bottom switch
"just so." Homeowners usually describe this as "one of the switches is
broken," but the switches are fine — the shared path between them is
not.

A different failure gives a different signature. If the common wire
feeding switch one loses continuity, the lamp is dead in all four
combinations. So the two symptoms separate the two faults cleanly:
*dead in every position* points at the supply or the lamp; *works in
exactly one combination* points at a broken traveler. Reasoning from
which cases of the table survive is faster than pulling every device out
of the wall.
