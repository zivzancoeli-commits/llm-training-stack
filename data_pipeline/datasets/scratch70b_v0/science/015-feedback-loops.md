---
id: science-015
category: science
subcategory: systems
difficulty: medium
source_model: fable-5
skills:
  - causal-explanation
  - systems-thinking
title: "Feedback loops: thermostat vs ice-albedo"
approx_words: 640
---

# Feedback Loops: Thermostat vs Runaway Ice-Albedo

"Feedback" gets used loosely, but in science it has a precise skeleton: a system's output loops back to influence its own input. The character of the loop — damping or amplifying — determines whether the system settles or runs away. Two examples, one of each kind, carry most of the intuition.

## Negative feedback: the thermostat

A home thermostat senses temperature and acts *against* deviations. Room too cold? Heater on, temperature rises. Room warm enough? Heater off, temperature drifts down. Every disturbance triggers a response that pushes back toward the set point.

That "pushes back" is what makes the feedback **negative** — negative in the sense of *opposing the deviation*, not in the sense of bad. Negative feedback is the signature of self-stabilizing systems, and it's everywhere: your body holds ~37 °C by sweating and shivering; blood sugar is steered by insulin and glucagon; a marble in a bowl rolls back toward the bottom when nudged. The common structure: displacement generates a restoring influence proportional (roughly) to the displacement, so deviations shrink.

One realistic wrinkle: negative feedback with delays doesn't hold a perfect constant — it *oscillates* around the set point. Furnaces overshoot slightly before the thermostat reacts; predator and prey populations cycle. Stability here means bounded wobble, not stillness.

## Positive feedback: ice-albedo

Now the amplifying kind. Ice and snow are bright, reflecting much of the sunlight that hits them (high **albedo** — reflectivity); open ocean and bare ground are dark, absorbing most of it.

Suppose a cooling nudge lets ice sheets grow. More ice → more sunlight reflected to space → less energy absorbed → further cooling → still more ice. The output (cooling) feeds back to strengthen its own cause. The same loop runs equally well in reverse: a warming nudge melts sea ice, exposing dark ocean, which absorbs more sunlight, warming things further and melting more ice. Positive feedback doesn't prefer a direction; it amplifies *whatever* deviation exists. That's why it shows up in explanations of both ancient "Snowball Earth" episodes and today's rapid Arctic warming — the Arctic is warming several times faster than the global average, with shrinking sea ice as a substantial contributor.

"Runaway," qualitatively, means the loop's amplification compounds: each round of the loop produces a bigger deviation than the last, like a microphone squealing next to its own speaker. In practice, real runaways eventually hit limits — the microphone's amplifier saturates; an ice-albedo cooling runs out of dark ocean to whiten once ice reaches the equator; a warming runs out of ice to melt. Positive feedback ends by exhausting its fuel or handing control to some other process, not by politely returning to the start. The old state is not restored; the system lands somewhere new.

## The qualitative check: nudge the loop and trace the sign

You can classify any feedback loop with a paper-and-pencil limiting-case test: impose a small deviation, trace one full lap around the causal loop, and ask whether the loop's effect *opposes* or *reinforces* the original deviation.

- Thermostat: +1° of extra warmth → heater turns off sooner → less heat input → temperature falls. The lap returns a push of opposite sign. Negative feedback; expect settling (perhaps with wobble).
- Ice-albedo: +1° of warmth → less ice → lower reflectivity → more absorbed sunlight → more warmth. The lap returns a push of the same sign. Positive feedback; expect amplification until some limit intervenes.

The test also guards against a common mix-up: whether a feedback is negative or positive is a fact about the *loop's sign*, not about whether we like the outcome. A thermostat holding a house at an uncomfortable temperature is still negative feedback; a positive feedback that amplifies cooling is still positive. Sign of the loop, not sentiment about the result.
