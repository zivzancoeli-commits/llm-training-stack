# Take this corpus home

Two folders. Edit the markdown. Send it back before any GPU job.

| Folder | What it is |
| --- | --- |
| `scratch70b_v0/` | **114** seed docs (~99k heuristic tokens). Math, code, science, logic, habits, world, how-things-work. Review this first. |
| `scratch70b_sft_2p5m/` | Extra mix. Folder name is historical. Reviewed zip: **621 chat** docs (~603k tokens). **Pack at 1M tokens or less** (2.5M hard cap). |

Together this mix is about **702k** heuristic tokens — still under the 1M preferred budget. This is **not** a trained 70B. 1M tokens will not make one talk.

## Token budget

- Preferred: **1,000,000** heuristic tokens (or fewer)
- Hard cap: **2,500,000**
- Do not add documents to chase 2.5M

Heuristic ≈ `1.3 × words + 32` per document.

## How to edit

Each `.md` file is YAML frontmatter plus a body. Keep the frontmatter.

Rules that `catalog.py` will reject:

- body shorter than 120 words
- body longer than 1,800 words
- `title:` with an unquoted colon (`title: "Foo: bar"` is fine)
- `source_model` other than `fable-5`, `opus-5`, or `cursor-grok`
- `lorem ipsum` placeholder text

If you rewrite a piece, set `source_model: cursor-grok` (or leave the
original tag for a typo fix). Update `approx_words` roughly.

Drop a document by deleting the file. Add one with a **new** `id`.

Skip `__pycache__/`. `export/` is regenerated. `batches/` are writer
assignments, not training text.

## Optional: review UI (needs the git repo, not only this zip)

```bash
uv sync --group dev
uv run lmm data-review
```

http://127.0.0.1:43147/ — currently serves `scratch70b_v0`.

```bash
uv run lmm check tests/test_scratch70b_dataset.py tests/test_sft_2p5m_dataset.py
```

## Send edits back

1. Zip the edited folders and drop the zip in chat, or
2. Commit, push, and say the branch name, or
3. Paste keep/drop/rewrite notes.

The signed-off zip is https://github.com/zivzancoeli-commits/llm--dataset
(`scratch70b_1m_takehome.zip`). A copy is also
`data_pipeline/datasets/scratch70b_1m_takehome.zip` in this repo.

https://github.com/zivzancoeli-commits/llm-dataset is the old 228-chat
Mac upload. Do not use it for this run.
