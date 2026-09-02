---
id: science-009
category: science
subcategory: physics
difficulty: easy
source_model: fable-5
skills:
  - quantitative-reasoning
  - unit-check
  - number-check
title: Ohm's law on a simple series circuit
approx_words: 560
---

# Ohm's Law on a Simple Series Circuit

Ohm's law relates three quantities in a circuit:

**V = I R**

- **V**, voltage, in volts (V): the electrical "push," or more precisely the energy given to each unit of charge (1 volt = 1 joule per coulomb).
- **I**, current, in amperes (A): the flow rate of charge (1 ampere = 1 coulomb per second).
- **R**, resistance, in ohms (Ω): how much the component impedes flow.

A water analogy, used carefully: voltage is like pressure difference, current like flow rate, resistance like a narrow pipe. The analogy earns its keep for one insight — pressure differences drive flow through constrictions — and should be dropped before it starts suggesting that electrons are "used up." They aren't; charge flows in a loop.

(Fine print, stated honestly: "Ohm's law" is really an empirical property of certain materials — resistors, metals at steady temperature — not a universal law. Bulbs, diodes, and batteries don't obey it. For this article, our components are plain resistors, where it holds well.)

## The series circuit

Take a 9 V battery connected to two resistors in a single loop: R₁ = 100 Ω, then R₂ = 200 Ω, then back to the battery. "Series" means there is exactly one path, so **the same current flows through everything** — charge has nowhere else to go, and it doesn't pile up in steady state.

Two rules solve every series circuit:

1. Resistances in series add: R_total = R₁ + R₂ = 100 + 200 = 300 Ω. (Two constrictions in a row impede more than either alone.)
2. The battery's voltage is shared across the components: V₁ + V₂ = 9 V. (Each coulomb spends its 9 J budget along the loop — this is energy conservation in circuit clothing.)

Find the current from the total:

I = V / R_total = 9 V / 300 Ω = **0.03 A** (30 milliamps).

Now the voltage across each resistor, using Ohm's law on each one with the shared current:

- V₁ = I R₁ = 0.03 A × 100 Ω = 3 V
- V₂ = I R₂ = 0.03 A × 200 Ω = 6 V

Notice the pattern: the *larger* resistor takes the *larger* share of the voltage, in exact proportion (200 is 2/3 of 300, and 6 V is 2/3 of 9 V). This "voltage divider" behavior is one of the most-used facts in practical electronics.

## The number check

Verify the books balance: V₁ + V₂ = 3 V + 6 V = 9 V, matching the battery. ✔

Units check: amps × ohms must give volts. Since Ω = V/A by definition, A × (V/A) = V. ✔

Limiting cases as a final test: if R₂ → 0 (replace it with plain wire), then R_total → 100 Ω, current rises to 0.09 A, and the full 9 V appears across R₁ — the wire takes no share, as expected. If R₂ → ∞ (cut the wire), current → 0, no voltage drops across R₁ (V₁ = I R₁ = 0), and the full 9 V appears across the gap. Both extremes match what a multimeter actually shows on a broken or shorted circuit, which is why these limiting cases are also the standard way to *diagnose* one: measure where the voltage went, and you've found the break.
