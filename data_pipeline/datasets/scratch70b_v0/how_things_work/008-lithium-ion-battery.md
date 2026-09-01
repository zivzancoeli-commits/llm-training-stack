---
id: how-008
category: how_things_work
subcategory: chemistry
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How a lithium-ion battery stores energy at a high-school chemistry level
approx_words: 750
---

# How a lithium-ion battery stores energy at a high-school chemistry level

A lithium-ion cell stores energy by putting lithium somewhere it does not
want to be, and releases it by letting the lithium go back. The clever
part is that the return trip is only possible if an electron takes the
long way around, through your phone or your motor, doing work on the way.

## Four parts

**Cathode** (positive electrode): a lithium metal oxide, commonly lithium
cobalt oxide, LiCoO2, or lithium iron phosphate, LiFePO4. Its crystal has
sites that hold lithium ions comfortably, at low energy.

**Anode** (negative electrode): almost always graphite. Graphite is
stacked sheets of carbon, and lithium ions can slot into the gaps between
sheets. This slotting-in is called *intercalation* — the lithium is a
guest in a host lattice, not a new compound. Roughly one lithium per six
carbons at full charge, giving LiC6.

**Electrolyte**: a lithium salt such as LiPF6 dissolved in organic
solvents. It conducts lithium ions and blocks electrons. That electronic
insulation is what forces electrons through the external circuit.

**Separator**: a thin porous plastic film that keeps the electrodes from
touching while letting ions pass.

Note that no lithium *metal* is present in a working cell. It is lithium
ions moving between two hosts, which is why the technology is called
"lithium-ion" and why it is far safer than the lithium-metal cells that
preceded it.

## Charging: pushing lithium uphill

Apply an external voltage that pulls electrons out of the cathode. Each
lithium that loses its electron partner leaves the oxide as Li+ and
migrates through the electrolyte to the graphite. The electrons the
charger stripped away travel through the wire and arrive at the graphite
too, where they rejoin the lithium as it intercalates.

    Cathode, charging:   LiCoO2 -> Li(1-x)CoO2 + x Li+ + x e-
    Anode, charging:     6 C + x Li+ + x e- -> Li(x)C6

Chemically, cobalt is being oxidised from Co(III) toward Co(IV) as
lithium leaves, and the lithium in graphite ends up in a much
higher-energy environment than it occupied in the oxide. That energy
difference — about 3.7 V per electron for a graphite/LiCoO2 pair — is the
stored energy. It is chemical potential energy, held in the arrangement
of electrons and ions, exactly like the energy in a stretched spring is
held in the arrangement of atoms.

## Discharging: letting it run downhill

Connect a load and the reactions reverse spontaneously. Lithium leaves
the graphite as Li+ and swims back to the cathode. Its electron cannot
follow through the electrolyte, so it goes through your circuit,
delivering energy to whatever is in the way, and arrives at the cathode
just in time for the lithium to re-insert.

The cell voltage, about 3.6-3.7 V nominal for graphite/LiCoO2 and about
3.2 V for LiFePO4, is set by the energy difference per electron between
the two hosts. It is a property of the chemistry, not the size. Making a
cell bigger adds capacity — more lithium to shuttle, measured in
amp-hours — but not voltage. That is why battery packs wire cells in
series for voltage and parallel for capacity.

Because the lithium is only being relocated, not consumed, the process is
reversible for hundreds to thousands of cycles. Nothing is burned;
recharging is literally pushing the ions back.

## What wears out

Real cells degrade for a few concrete reasons. The electrolyte reacts at
the graphite surface to form a thin *solid electrolyte interphase*, a
passivating film. A stable SEI is essential — it stops further reaction —
but it consumes some lithium permanently, and it keeps thickening slowly,
raising internal resistance. Repeated intercalation also mechanically
strains the electrodes; particles crack and lose electrical contact.

## Limiting case: what if you charge a cold cell too fast?

Below roughly 0 C, lithium diffuses much more slowly into graphite. If
the charger keeps pushing current anyway, ions arrive at the anode
surface faster than the graphite can absorb them. They have to go
somewhere, so instead of intercalating they take an electron at the
surface and deposit as *lithium metal*. This is called lithium plating.

Two bad things follow. First, plated lithium immediately reacts with
electrolyte and is largely lost, so capacity drops permanently — a cold
fast-charge can cost measurable capacity in a single event. Second, the
plating grows as needle-like dendrites. A dendrite that grows far enough
punctures the separator and shorts the cell internally. An internal short
dumps the full stored energy as heat in a tiny volume, the electrolyte
solvents are flammable, and the cathode can decompose and release oxygen.
That combination is thermal runaway.

This is why every serious battery management system refuses or heavily
limits charging below freezing, why electric cars preheat the pack before
a fast charge, and why the same cell will happily *discharge* in the cold
(the reverse direction plates nothing; it just sags in voltage because
internal resistance is up). The asymmetry falls straight out of the
mechanism: what fails is not "the battery," but one specific step,
lithium entering graphite, becoming the bottleneck.
