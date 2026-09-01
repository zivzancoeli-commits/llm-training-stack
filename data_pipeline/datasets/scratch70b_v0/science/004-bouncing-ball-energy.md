---
id: science-004
category: science
subcategory: physics
difficulty: medium
source_model: fable-5
skills:
  - causal-explanation
  - energy-accounting
  - limiting-case-check
title: Energy conservation in a ball that stops bouncing
approx_words: 590
---

# Conservation of Energy in a Ball That Doesn't Bounce Forever

Drop a rubber ball from shoulder height. It bounces, but each bounce is lower than the last, and soon it sits still on the floor. Here's the puzzle as a student often frames it: "Energy is supposed to be conserved. The ball lost all its energy. So is conservation of energy false?"

Conservation of energy is fine. What's false is the hidden assumption that *mechanical* energy — the visible kinds — is the whole ledger.

## The mechanism, bounce by bounce

At the moment of release, the ball has gravitational potential energy, roughly mgh (mass × gravitational field strength × height). As it falls, potential converts to kinetic energy. So far, clean bookkeeping.

The interesting part is the collision. When the ball hits the floor, it deforms — squashes — and the kinetic energy briefly becomes elastic potential energy in the compressed rubber, like a spring. As the ball rebounds, most of that elastic energy converts back to kinetic. But not all of it. Rubber is not a perfect spring. As the material flexes, internal friction between polymer chains converts some energy into random molecular jiggling — that is, heat. The impact also shoves the floor and the air, radiating a little energy as sound (the "thock" you hear is energy leaving the ball).

A typical rubber ball might return about 80% of its energy per bounce (this fraction squared of… careful — the *energy* fraction is what matters; the rebound *height* ratio equals the energy ratio, since height is proportional to energy). So the heights go: h, 0.8h, 0.64h, 0.51h, … a geometric decay. After 20 bounces, 0.8⁲⁰ ≈ 1% of the original height remains. The ball doesn't gradually violate physics; it exponentially pays a heat-and-sound tax.

Where did the energy *go*, finally? Into slightly warmer rubber, a slightly warmer floor patch, and sound waves that themselves dissipate into warm air. Total energy: unchanged. Usable, organized, mechanical energy: gone. That distinction — conserved total versus degraded quality — is the actual lesson, and it's the intuition behind the second law of thermodynamics.

## Check 1: units and magnitude

Estimate the temperature rise. A 0.05 kg ball dropped from 1 m carries mgh ≈ 0.05 × 9.8 × 1 ≈ 0.5 J. Units: kg × (m/s²) × m = kg·m²/s² = joules. ✔

Rubber's specific heat is roughly 2000 J/(kg·K). If all 0.5 J ended up in the ball, the temperature rise would be ΔT = Q/(mc) = 0.5 / (0.05 × 2000) = 0.005 K. Units: J ÷ (kg × J·kg⁻¹·K⁻¹) = K. ✔

Five thousandths of a degree — far too small to feel, which is exactly why the "missing" energy is easy to overlook. The books balance in quantities we don't casually perceive. (Squeeze-and-release a ball rapidly dozens of times, or think of a squash ball after a long rally, and the warming becomes noticeable — a nice confirmation.)

## Check 2: the limiting cases

- **Perfectly elastic limit:** if the ball returned 100% of its energy each bounce, it would bounce forever to the same height. No real macroscopic ball does this, but the model correctly predicts that harder, springier balls (higher return fraction) bounce longer — compare a superball with a beanbag.
- **Perfectly inelastic limit:** a lump of clay returns ~0%. The model predicts one splat and no bounce, all energy immediately converted to deformation and heat. Also observed.

Reality sits between the limits, and the geometric-decay picture interpolates between them smoothly.
