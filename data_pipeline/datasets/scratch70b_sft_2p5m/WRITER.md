# Writer spec — scratch70b_sft_2p5m

Each assignment is one markdown file under
`/workspace/data_pipeline/datasets/scratch70b_sft_2p5m/<category>/<id>.md`.

## Frontmatter (required)

```yaml
---
id: chat-0001
category: chat
subcategory: everyday-dialogue
difficulty: medium
source_model: cursor-grok
skills:
  - conversational
  - instruction-following
title: "Exact title from the batch JSON"
approx_words: 700
---
```

`title` must be quoted if it contains a colon.

## Body

- **650–800 words** (hard: 400–900). Original prose. No lorem. No pasted Wikipedia.
- Fit in **5,120 tokens** easily.
- `source_model` is always `cursor-grok`.
- Do not change `id` or `category`.

### If category is `chat`

Write a **dialogue** people would actually speak. Use:

```
### User
...
### Assistant
```

The assistant should sound like a competent person, not a corporate bot. Ask a
clarifying question when the user was vague. Do not invent laws, medical
diagnoses, or prices as facts.

### If category is code / math / science / logic / reasoning_habits

One concrete problem, steps, a numeric or test-case **check**, then a
limiting case. ASCII math is fine (`x^2`).

### If category is world / how_things_work

A mechanism explainer. Flag uncertainty. No fake citations.

## Do not

- Write files outside your batch ids
- Copy another document and search-replace
- Use copyrighted lyrics, news dumps, or textbook pages
- Keep writing once the mix is near **1 million** heuristic tokens.
  The hard cap is 2.5 million; do not treat that as a target.
