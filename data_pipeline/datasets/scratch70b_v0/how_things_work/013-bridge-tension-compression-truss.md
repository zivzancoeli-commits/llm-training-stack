---
id: how-013
category: how_things_work
subcategory: engineering
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: "How a bridge carries load: tension, compression, a simple truss"
approx_words: 750
---

# How a bridge carries load: tension, compression, a simple truss

A bridge has one requirement: every newton of weight placed on the deck
must find a continuous path down to the ground. Structural engineering is
largely the discipline of drawing that path explicitly and checking that
each member along it survives the kind of force it carries.

## Two kinds of force, and why the distinction matters

A member in **tension** is being pulled at both ends and wants to
lengthen. A member in **compression** is being pushed and wants to
shorten. The natural assumption is that these are symmetric. They are
not, for two reasons.

First, materials are asymmetric. Concrete and stone handle compression
extremely well — concrete's compressive strength is on the order of ten
times its tensile strength — and crack readily in tension. Steel handles
both about equally. This is why reinforced concrete exists: steel bars go
where the tension will be, and concrete takes the compression.

Second, and more importantly, compression has a failure mode tension does
not: **buckling**. A slender member in tension fails only when the
material itself yields, so its capacity depends on cross-sectional area
alone. A slender member in compression can fail by suddenly bowing
sideways at a load far below the material's crushing strength. Euler's
formula for a pin-ended column gives the critical load as

    P_cr = pi^2 * E * I / L^2

where E is stiffness, I is a measure of how the cross-section is
distributed away from the bending axis, and L is length. Note the L^2 in
the denominator: double a strut's length and its buckling capacity drops
by a factor of four. This is why compression members are fat tubes or box
sections while tension members can be thin cables. A steel cable can hold
tonnes and be coiled up; a rod of the same area used as a long column is
nearly useless.

## What a beam actually does

Set a simple beam across two supports and load the middle. The beam bends
into a shallow curve. Its top surface gets shorter and its bottom gets
longer, so the top is in compression and the bottom in tension, with a
*neutral axis* between them carrying almost nothing. That is why an
I-beam looks the way it does: material sits in the top and bottom flanges
where the stresses live, and the thin web only holds the flanges apart
and carries shear. Material at the neutral axis earns nothing.

A plain beam works, but its efficiency falls apart at long spans: the
required depth grows and the beam ends up carrying mostly its own weight.

## The truss: turn bending into pure axial force

A truss replaces the solid web with a triangulated frame. The key insight
is geometric: a triangle is the only polygon that cannot change shape
without changing the length of a side. A four-bar square can be pushed
into a parallelogram with rigid members and pinned joints; a triangle
cannot. So a triangulated frame with pinned joints deforms only by
stretching or squashing its members — which means every member carries
pure tension or pure compression and nothing else.

Take a simple Warren truss: a bottom chord, a top chord, and diagonals
zigzagging between them. Load the deck in the middle and the truss bends
like a beam. The top chord shortens, so it is in compression; the bottom
chord lengthens, so it is in tension. The diagonals carry the shear,
alternating tension and compression toward the supports.

Now you can design each piece for the job it has. Bottom chords: slender,
efficient, tension-only. Top chords and compression diagonals: stocky and
braced, because buckling governs. This selective assignment is why a
truss spans much further than a solid beam of the same weight.

The same logic drives other bridge types. A suspension bridge puts the
main cables in pure tension and the towers in compression. An arch puts
the whole span in compression and pushes outward at its feet, which is
why arches need abutments that resist thrust, and why an arch on soft
ground will spread and collapse.

## Limiting case: what if one diagonal fails?

Cut a single diagonal in the Warren truss and follow the consequences.

The immediate effect is local. The panel that lost its diagonal is now a
four-bar quadrilateral, free to rack into a parallelogram. The truss has
lost its shear path at that station, so the load that diagonal was
carrying has to redistribute into neighbouring members that were not
sized for it.

Whether the bridge survives depends on whether it is *statically
determinate* or *redundant*. A determinate truss has exactly enough
members to be stable and no more; every member is essential, so losing
one turns the structure into a mechanism and it collapses. A redundant
truss has extra load paths, so the force finds another route, neighbours
go over their design stress but perhaps not to failure, and you get
visible sag rather than sudden loss.

This is why "fracture-critical" is a term inspectors use with alarm. It
labels a structure where one member's failure would collapse the span,
and it is why modern design pays for redundant load paths even though
they add material that, on a good day, does nothing at all. The extra
steel is insurance that the force-path diagram has a second answer.
