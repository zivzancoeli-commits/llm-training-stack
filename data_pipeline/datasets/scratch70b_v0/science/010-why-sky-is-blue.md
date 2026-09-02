---
id: science-010
category: science
subcategory: physics
difficulty: hard
source_model: fable-5
skills:
  - causal-explanation
  - order-of-magnitude
  - limiting-case-check
title: Why the sky is blue, Fermi-style
approx_words: 630
---

# Why the Sky Is Blue, at a Fermi-Explanation Level

First, clear the wrong answer: air is not blue. A roomful of air is colorless; so is the air between you and a mountain ten kilometers away (mostly). If air were a blue substance, distant white objects would look blue-tinted in proportion to distance far more strongly than they do, and the sky would not turn red at sunset. The blue is not a pigment. It is a *scattering* phenomenon — a statement about which light gets redirected toward your eye.

## The mechanism: molecules re-radiate, unevenly across color

Sunlight is a mix of wavelengths — violet through red, roughly 400 to 700 nanometers. Air molecules (N₂, O₂) are about a thousand times smaller than these wavelengths. When a light wave passes over such a tiny molecule, its oscillating electric field shakes the molecule's electrons, and the shaken charges re-radiate a little light in all directions. That redirection is scattering.

The crucial fact is that this scattering is drastically stronger for short wavelengths. For particles much smaller than the wavelength (the Rayleigh regime), scattered power scales as **1/λ⁴**. A hand-waving reason for the steep dependence: a short-wavelength wave wiggles the electrons faster, and accelerating charges radiate much more effectively at higher frequencies — the radiated power of an oscillating dipole grows as frequency to the fourth power.

Run the key number. Compare blue light (λ ≈ 450 nm) to red (λ ≈ 650 nm):

(650/450)⁴ ≈ (1.44)⁴ ≈ 4.3

Blue is scattered roughly four to five times more than red. So when you look at a patch of sky *away* from the Sun, the light reaching your eye is sunlight that got redirected by molecules along that line of sight — and that redirected light is heavily enriched in short wavelengths. Blue sky.

Why not violet, which scatters even more? Three honest reasons: the Sun emits somewhat less violet than blue; the atmosphere absorbs some of it; and human eyes are much less sensitive to violet. The sky's *physical* spectrum does rise into the violet — our perception renders the mixture as blue.

## The same mechanism, run in reverse: sunsets

At sunset you look *toward* the Sun through a few hundred kilometers of low, dense air instead of tens of kilometers. The blue has been scattered *out* of the direct beam all along that path, leaving the transmitted light red-orange. One mechanism, two colors: sky-blue is the scattered light, sunset-red is what survives the sieve. Any correct explanation of the blue sky must also predict red sunsets for free; this one does.

## Fermi-style checks

**Limiting case, no atmosphere:** with nothing to scatter, light travels only in straight lines from source to eye. Look away from the Sun and you see black, stars included, day or night. This is exactly what Apollo astronauts saw from the Moon — the daytime lunar sky is black. The counterfactual is observed, which is strong confirmation.

**Limiting case, big particles:** droplets in clouds and fog are much *larger* than a wavelength, and in that regime scattering no longer prefers short wavelengths — all colors scatter about equally. Prediction: clouds should be white or gray, not blue. They are. The same logic explains why milk is white and why skies over humid, hazy regions look washed-out rather than deep blue.

**Sanity check on strength:** the effect must be weak per molecule, or the atmosphere would be opaque; strong in aggregate, or the sky would be black. A photon's chance of scattering while crossing the whole atmosphere is of order tens of percent — enough to paint the sky, not enough to blot out the Sun. The observed bright Sun *plus* bright blue sky sits comfortably in that middle range, which is the regime the mechanism requires.
