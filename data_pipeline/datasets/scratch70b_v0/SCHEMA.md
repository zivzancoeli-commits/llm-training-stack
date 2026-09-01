# Document schema (scratch70b_v0)

Each document is a Markdown file with YAML frontmatter.

```yaml
---
id: math-001
category: math
subcategory: algebra
difficulty: medium          # easy | medium | hard
source_model: fable-5       # fable-5 | opus-5 | cursor-grok
skills:
  - worked-solution
  - check-your-work
title: Completing the square
approx_words: 700
---
```

Body rules:

- Original prose. No pasted textbooks, papers, or Wikipedia.
- Teach *how to think*, not only the answer.
- For math/code: a concrete problem, steps, a numeric or test-case check.
- For knowledge: a self-contained explainer a strong high-schooler
  could use. Flag uncertainty instead of inventing citations.
- ASCII math is fine (`x^2`, `->`). No need for LaTeX packages.
- Stay under ~1,500 words so packing into 5,120 tokens is easy.

Allowed `category` values: `math`, `code`, `science`, `logic`,
`world`, `how_things_work`, `reasoning_habits`.
