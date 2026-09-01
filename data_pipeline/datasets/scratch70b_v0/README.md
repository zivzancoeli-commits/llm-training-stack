# scratch70b_v0 — seed corpus for a 70B from-scratch run

**Status: for human review. Do not train until you sign off.**

114 documents. Mix is ~70% reasoning / ~30% general knowledge.

Most of the corpus was drafted by **Fable 5** (math, code, science, logic,
habits) and **Opus 5** (world, how-things-work). When API quota got tight,
the remaining holes were filled locally (`source_model: cursor-grok`) so
the set would be complete without more Fable/Opus calls. Frontmatter
`source_model` tells you who wrote each piece.

This folder is a *style and mix* seed, not the full pretrain. A 70B
model with 5,120 context still needs billions of tokens to become
generally useful. 8× H200 SXM can **hold** 70B (ZeRO-3). It cannot eat
Chinchilla-scale tokens in a reasonable wall-clock (see compute note).
After you approve the writing style, we generate more of the *same*
kind of documents.

## Goal of this mix

- **Pretty good reasoning** (primary): worked solutions, explicit checks,
  “why this step”, common mistakes.
- **OK general knowledge** (secondary): accurate, compact explainers.
  Not a Wikipedia dump. Not trivia for its own sake.

Target mix of *this seed* (by document count, ±5%):

| Bucket | Share | Category folders |
| --- | ---: | --- |
| Reasoning | 65% | `math/`, `code/`, `science/`, `logic/`, `reasoning_habits/` |
| General knowledge | 35% | `world/`, `how_things_work/` |

Context: every document is written to **pack into 5,120 tokens**. Most
are 400–1,200 words so several can share a sequence.

## Who wrote what

| Model | Folders |
| --- | --- |
| Fable 5 | math, code, science, logic, reasoning_habits |
| Opus 5 | world, how_things_work |

## How to go through it

```bash
uv run lmm data-review
```

Opens a local page (port **43147**) with every document, filters, and
keep / drop / edit-later. Notes are stored in
`review_decisions.json` next to this README.

Or read the markdown files directly in the category folders. Each file
has YAML frontmatter (`id`, `category`, `difficulty`, `source_model`).

To copy this folder to your own computer, edit it, and send it back,
see [`TAKE_HOME.md`](TAKE_HOME.md).

## Compute note (8× H200 SXM, 70B, 5,120 ctx)

Rough: ~6k tokens/sec at 30% MFU. **10B tokens ≈ 3 weeks** of a packed
node. Chinchilla-optimal 1.4T tokens is not the plan. After this seed
is approved, the from-scratch run should be **high-quality synthetic +
a modest public mix**, on the order of **5–20B tokens**, reasoning-heavy.
That will not match a 15T frontier model on random trivia. It *can*
produce a 70B that thinks in short traces.

## What is not in v0

- Copyrighted books or scraped web dumps
- 350k-context documents
- Instruction-tuning chat templates (this is **pretrain** prose)
- Safety red-teaming corpora
