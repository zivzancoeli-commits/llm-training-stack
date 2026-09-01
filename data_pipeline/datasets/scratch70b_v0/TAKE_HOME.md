# Take this seed home, edit it, send it back

This folder is the **scratch70b_v0** seed: 114 markdown documents you
can edit in any text editor. It is **not** a trained 70B, and it is
**not** enough tokens to pretrain one.

## 1. What to copy

Copy the whole `scratch70b_v0/` directory. The downloadable zip
`scratch70b_1m_takehome.zip` also includes the extra chat mix
(`scratch70b_sft_2p5m/`). You need:

- the seven category folders (`math`, `code`, `science`, `logic`,
  `reasoning_habits`, `world`, `how_things_work`)
- `SCHEMA.md`, `README.md`, `catalog.py`, `review_server.py`

Skip `__pycache__/`. `export/` is regenerated; you can leave it.

If you also cloned this git repo, you already have the folder at
`data_pipeline/datasets/scratch70b_v0/`. Edit there instead of using
the zip.

## 2. How to edit a document

Each file is YAML frontmatter + markdown body. Keep the frontmatter.
Do not change `id` unless you also add/remove files consistently
(tests expect `math-001`…`how-016`).

Rules that `catalog.py` will reject:

- body shorter than 120 words
- body longer than 1,800 words
- `title:` with an unquoted colon (`title: "Foo: bar"` is fine)
- `source_model` other than `fable-5`, `opus-5`, or `cursor-grok`
- `lorem ipsum` placeholder text

If you rewrite a piece, set `source_model: cursor-grok` (or leave the
original tag if you only fix a typo). Update `approx_words` roughly.

Drop a document by deleting the file. Add one by copying a neighbor
and giving it a **new** `id`.

## 3. Optional: review UI on your laptop

From the **repo root** (not from this folder alone):

```bash
# Python 3.12+  https://docs.astral.sh/uv/
uv sync --group dev
uv run lmm data-review
```

Opens http://127.0.0.1:43147/ — keep / drop / edit-later. Notes go to
`review_decisions.json` (gitignored). Then:

```bash
uv run lmm data-export
uv run lmm check tests/test_scratch70b_dataset.py
```

`data-export` rewrites `export/scratch70b_v0.jsonl`.

If you only have the zip and not the repo, you can still edit the
`.md` files. Re-export needs the repo (`catalog.py` + `uv`).

## 4. Send the edits back

Pick one:

1. Zip the edited `scratch70b_v0/` folder and drop it in the chat.
2. If you have a git remote: commit, push, and say the branch name.
3. Paste a short list of keep/drop/rewrite notes if you used the
   review UI (`review_decisions.json`).

Do **not** start a GPU job until this seed is signed off.

## 5. What you cannot do on a laptop

- Train a **70B from scratch**. Weights + Adam on 70B need on the
  order of a **terabyte of GPU memory** (8× NVIDIA H200 SXM, 141 GB
  each, is the node this repo targets). A desktop GPU will OOM.
- Run `lmm ft-launch --confirm` and expect a from-scratch 70B.
  That command fine-tunes **Qwen2.5 instruct** (an already-trained
  model). Different job.
- Feed these 114 documents into a trainer and get a useful 70B.
  This seed is ~100k tokens of prose. A serious from-scratch run
  on 8× H200 is **5–20 billion** tokens (weeks, not an afternoon).

Laptop = edit, review, pytest. GPU cluster = train.
