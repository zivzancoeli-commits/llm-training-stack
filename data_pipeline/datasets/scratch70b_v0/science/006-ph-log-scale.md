---
id: science-006
category: science
subcategory: chemistry
difficulty: medium
source_model: fable-5
skills:
  - quantitative-reasoning
  - unit-check
title: pH as a log scale in 10x steps
approx_words: 580
---

# pH Is a Log Scale: Thinking in 10× Steps

The pH scale runs (roughly) from 0 to 14, and it is easy to read it like a thermometer, where 4 is "a bit more" than 5. It isn't. pH is a logarithmic scale, and each step of 1 means a factor of **ten** in acidity. Getting this one idea right prevents most pH mistakes.

## What pH actually measures

Acidity is about hydrogen ions, H⁺ (in water, really hydronium, H₃O⁺, but H⁺ is the standard shorthand). The concentration of H⁺, written [H⁺], is measured in moles per liter (M). In watery solutions this concentration spans an enormous range — from around 1 M in strong acid to around 0.00000000000001 M (10⁻¹⁴ M) in strong base. Fourteen orders of magnitude is unwieldy, so chemists compress it:

pH = −log₁₀[H⁺]

The minus sign flips things so that *more* acid means a *lower* pH. So:

- [H⁺] = 10⁻³ M → pH 3
- [H⁺] = 10⁻⁴ M → pH 4
- [H⁺] = 10⁻⁷ M → pH 7 (pure water at 25 °C, "neutral")

Each pH unit is one power of ten in concentration. pH 3 is not "a little" more acidic than pH 4 — it has **ten times** the H⁺ concentration. Compared with pH 6, pH 3 has 10 × 10 × 10 = 1000 times the H⁺.

A concrete ladder helps. Start with a solution at pH 2 (like stomach acid territory, [H⁺] = 10⁻² M). Dilute it tenfold with pure water: roughly pH 3. Dilute tenfold again: pH 4. Each 10× dilution climbs one rung. (This ladder breaks near pH 7 — you can't dilute an acid into a base; adding pure water just pushes pH toward 7 and no further. That limiting case is itself a useful sanity check: dilution with neutral water can only make a solution more neutral.)

Why neutral is 7: water itself splits slightly into H⁺ and OH⁻, and at 25 °C the product [H⁺][OH⁻] is fixed at 10⁻¹⁴. When neither ion dominates, each is 10⁻⁷ M, giving pH 7. In a base, OH⁻ is high, so H⁺ must be correspondingly low — that's why bases have high pH rather than a separate scale.

## Check: units and a worked comparison

A dimensional subtlety, stated honestly: you can only take a logarithm of a pure number, so formally pH uses the concentration *divided by* a reference of 1 mol/L, making the argument dimensionless. In practice, "pH = −log of the molarity" works whenever you keep concentrations in mol/L. The check: [H⁺] = 10⁻⁵ mol/L → divide by 1 mol/L → 10⁻⁵ (unitless) → pH 5. Consistent. ✔

Now a comparison that exposes the linear-reading error. Rain at pH 5.6 is normal (dissolved CO₂ makes it mildly acidic). Acid rain at pH 4.6 sounds "one unit worse." In concentration terms it carries 10× the H⁺; at pH 3.6, it's 100×. Ecological damage tracks the concentration, not the pH digits — which is why a "small" pH drop in a lake can be a large chemical event. Similarly, ocean surface pH falling from about 8.2 toward 8.1 sounds negligible, but a 0.1 drop is a 10^0.1 ≈ 1.26× rise in H⁺ — about 26% more acidic in the sense that actually matters to shell-forming chemistry.

Rule of thumb worth keeping: on any log scale — pH, decibels, earthquake magnitudes — *differences* in the displayed number correspond to *ratios* in the underlying quantity. Read steps as multipliers, not increments.
