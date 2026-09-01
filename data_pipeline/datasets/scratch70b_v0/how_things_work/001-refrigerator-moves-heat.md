---
id: how-001
category: how_things_work
subcategory: everyday
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How a refrigerator moves heat out of the box
approx_words: 700
---

# How a refrigerator moves heat out of the box

A refrigerator does not make cold. There is no such substance. What the
machine does is *move* heat from the inside of an insulated box to the
room, and heat does not flow that direction on its own. So the fridge
spends electricity to force it.

## The trick: a fluid that boils at a useful temperature

The whole design rests on one fact from physics: a liquid absorbs a
large amount of heat when it boils, and releases that same heat when it
condenses back to liquid. Boiling water takes roughly five times more
energy than heating that water from room temperature to 100 C. That
"latent heat" is the freight truck the fridge uses to haul energy.

The catch is that water boils at the wrong temperature. A refrigerator
needs a fluid that boils at around -25 C at low pressure and condenses
at around 40 C at high pressure. Modern units use hydrofluorocarbon or
hydrocarbon refrigerants chosen for exactly this. The second useful fact
is that the boiling point of any fluid depends on pressure: squeeze it
and it condenses at a higher temperature, let it expand and it boils at
a lower one. The machine manipulates pressure to steer where boiling and
condensing happen.

## The loop, one component at a time

**Evaporator.** Cold low-pressure liquid refrigerant enters a coil
inside the cabinet (in most home fridges it sits behind a panel in the
freezer). The refrigerant is colder than the food and the air, so heat
flows the natural direction, from the box into the refrigerant. That
heat boils the refrigerant into vapor. The box gets colder; the vapor
carries the energy away.

**Compressor.** The vapor is drawn into a compressor, the humming pump
at the bottom of the fridge. The compressor squeezes the vapor into a
much smaller volume. Compression does work on the gas, so the gas comes
out both high pressure and genuinely hot, often 60-80 C, hotter than the
kitchen. This is the step that costs electricity, and it is the step
that makes the whole thing possible: you can only dump heat into the
room if you first raise the refrigerant above room temperature.

**Condenser.** The hot high-pressure vapor flows through coils on the
back or underneath the fridge. Those coils are hotter than the kitchen
air, so heat flows out, again the natural direction. As the refrigerant
gives up heat it condenses back to a warm liquid, still at high
pressure. This is why the space behind a running fridge is warm and why
a fridge with its door open heats a closed room rather than cooling it:
everything it removes from the box, plus the compressor's electrical
work, ends up in the room.

**Expansion device.** The warm liquid passes through a narrow capillary
tube or a metering valve into the low-pressure side. Pressure drops
suddenly, part of the liquid flashes to vapor, and that flash-boiling
chills the mixture down to well below freezing. Now cold and low
pressure, it re-enters the evaporator and the cycle repeats.

A thermostat simply switches the compressor on and off to hold the
cabinet near its setpoint. The cycling you hear is not the fridge
working harder; it is the fridge working intermittently.

## Limiting case: what if the condenser coils are choked with dust?

Follow the chain. Dust is an insulator, so the condenser can no longer
shed heat into the kitchen efficiently. The refrigerant condenses less
readily, so pressure on the high side climbs. A compressor pushing
against higher pressure draws more current and delivers less flow, so
less refrigerant circulates per minute and less heat is carried out of
the box each cycle. The thermostat sees a cabinet that is still too
warm, so it never shuts the compressor off. Run time goes from perhaps
40 percent of the hour to nearly 100 percent.

The symptoms follow directly: a higher electricity bill, a compressor
that is hot to the touch, food that is warmer than the dial claims, and
eventually a thermal-overload cutout tripping the compressor off until
it cools. Pull the fridge out and vacuum the coils and every one of
those symptoms reverses, because you have restored the only path the
heat had out of the system.

The same reasoning covers the other classic failures. A door gasket that
no longer seals lets warm room air leak in, adding heat load the
evaporator must remove, so run time rises again. A refrigerant leak
means less mass circulating, so the evaporator cannot absorb enough
heat, and you get a freezer that half works and a fridge section that
does not. In every case the question to ask is the same one: which link
in the heat-moving chain got blocked?
