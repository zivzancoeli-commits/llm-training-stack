# Walkthrough — where everything is, how to change it, how to know it’s good

This is the file to read first if you want to poke at the stack without
setting fire to an 8x H200 bill.

There is a from-scratch loop (`lmm scratch-plan` / `scratch-train`)
with **random init** and a **1M-token cap** (2.5M hard; prefer 1M or less). It is not Qwen.
What you can still do on a laptop: pytest, dry-run plans, review data.

## 0. One-time setup (laptop, no GPU)

```bash
uv sync --group dev
uv run lmm tour
uv run lmm check
```

`lmm tour` prints the map below. `lmm check` is `pytest`. Both are free.

## 1. Map of the repo

```
.
├── WALKTHROUGH.md          ← you are here
├── README.md               what this repo is
├── SCALING_MANIFEST.md     100M → 200B phases (5,120 ctx until 200B)
├── DECISIONS.md            defaults we did not block on
│
├── specs/                  NUMBERS (edit these first)
│   ├── hyperparameter_profiles/*.yaml
│   ├── contracts/          shape / init / OOM math
│   ├── chinchilla.py
│   └── profiles.py         YAML loader the tests use
│
├── data_pipeline/          tokenizer / stream / dedup (skeletons)
│   ├── loader.py
│   └── datasets/scratch70b_v0/   70B seed corpus — go through this
├── model/                  Llama-like block, FA-3 hook, RoPE, TP/PP maps
├── infra/
│   ├── overseer.py         heartbeat + InfiniBand halt
│   ├── deepspeed/          ZeRO JSON for 8x H200
│   └── runpod/             8x H200 SXM pod automation
│
├── fine_tune/              fine-tune recipes + launcher + on-pod train
│   ├── recipes/*.yaml      ← edit a recipe here
│   ├── cli.py              `lmm` command
│   └── runpod.py           REST body; dry-run until --confirm
│
└── tests/                  the gate. run after every small edit
```

## 2. The small-change loop

Change **one** thing. Re-run the **smallest** test that covers it. Then
the full suite.

| If you change… | Run |
| --- | --- |
| `specs/hyperparameter_profiles/7b.yaml` (heads, context, mix) | `uv run lmm check tests/test_profiles.py` |
| `specs/contracts/attention_shapes.py` | `uv run lmm check tests/test_attention_shapes.py` |
| `specs/contracts/initialization.py` | `uv run lmm check tests/test_layer_init.py` |
| `specs/contracts/memory.py` | `uv run lmm check tests/test_oom_thresholds.py tests/test_finetune_plan.py` |
| `model/transformer_block.py` | `uv run lmm check tests/test_attention_shapes.py tests/test_component_skeletons.py` |
| `data_pipeline/loader.py` or `infra/overseer.py` | `uv run lmm check tests/test_component_skeletons.py` |
| `fine_tune/recipes/*.yaml` | `uv run lmm check tests/test_finetune_plan.py` then `uv run lmm ft-plan --recipe …` |
| `fine_tune/runpod.py` | `uv run lmm check tests/test_runpod_dry_run.py tests/test_cli.py` |

Then always:

```bash
uv run lmm check
```

If that is green, the laptop believes the change. It has **not** rented
GPUs.

### A concrete 30-second drill

1. Open `specs/hyperparameter_profiles/100m.yaml`.
2. Change `reasoning_mix_ratio` from `0.50` to `0.55`.
3. `uv run lmm check tests/test_profiles.py` — should pass (mix still in 0.2–0.8).
4. Change `context_length` to `350208` on that same 100M file.
5. The same test **must fail** (only 200B may declare long context, and
   only as `context_length_extension`). Put `5120` back.
6. `uv run lmm check`.

That is the whole culture: illegal configs die on a laptop.

## 3. Go through the 70B seed corpus (do this before any 70B run)

```bash
uv run lmm data-review
```

Opens http://127.0.0.1:43147/ — keep / drop / edit on each document.
Notes save to `data_pipeline/datasets/scratch70b_v0/review_decisions.json`.
No GPU. No Fable/Opus calls.

Or read the markdown in `data_pipeline/datasets/scratch70b_v0/{math,code,...}/`.
`source_model` in the frontmatter is `fable-5`, `opus-5`, or `cursor-grok`.

When you are done marking, say so. Then we can talk 70B-from-scratch on
8× H200. Not before.

## 4. From-scratch 70B on 8x H200 SXM

This is **random init**, not Qwen. Context is **200,000** on `70b_scratch`
(CPU offload + activation checkpointing). Data is ~706k tokens, packed
into 200k-length rows (about four rows). That will not make a fluent
70B; it is a slow systems smoke. 100M/7B scratch jobs stay at 5,120.

Do **not** use `lmm ft-launch` or recipe `70b_lora` for this job.

### Download the zip

The **updated** mix (628 chats + seed docs) is in this repo:

`data_pipeline/datasets/scratch70b_1m_takehome.zip`

In Cursor, open that file in the file tree and download it. After you
`git clone` the training stack on the pod, the same path is already
there — you can import it without a second download:

```bash
python -c "from pathlib import Path; from data_pipeline.import_zip import import_takehome_zip; print(import_takehome_zip(Path('data_pipeline/datasets/scratch70b_1m_takehome.zip')))"
```

https://github.com/zivzancoeli-commits/llm-dataset still has the **old**
Mac upload (`scratch70b_1m_takehome 2.zip`, 228 chats). Use the repo zip
above if you want the extra 400 chats.

### A. Laptop (free)

1. Put the zip into the repo (macOS `scratch70b_1m_takehome 2.zip` is fine):

```bash
uv run lmm data-import "/path/to/scratch70b_1m_takehome 2.zip"
uv run lmm check
uv run lmm scratch-plan --recipe 70b_scratch
```

2. Two GitHub repos (HTTPS). RunPod cannot clone a Cursor page.

   | What | URL |
   | --- | --- |
   | Zip you uploaded | https://github.com/zivzancoeli-commits/llm-dataset |
   | Training stack | https://github.com/zivzancoeli-commits/llm-training-stack |

   Both are **public**. Clone the stack for code, clone the dataset for
   the zip (or drag the zip onto the pod). The stack clone on GitHub may
   not include every markdown file; importing the zip is the complete mix.

3. Optional dry-run of the pod JSON (does not bill):

```bash
uv run lmm scratch-launch --recipe 70b_scratch --dry-run \
  --git-url https://github.com/zivzancoeli-commits/llm-training-stack.git \
  --dataset-git-url https://github.com/zivzancoeli-commits/llm-dataset.git
```

### B. RunPod UI (what you are filling in now)

| Field | Set to |
| --- | --- |
| GPU | **8× NVIDIA H200** (SXM). Not H200 NVL. |
| Cloud | **Secure** |
| Image | `runpod/pytorch:2.8.0-py3.11-cuda12.8.1-devel-ubuntu22.04` |
| Container disk | **100 GB** |
| Volume disk | **300 GB** mounted at `/workspace` |
| Encrypt volume | off |
| Start command | leave empty (you will SSH / Jupyter) |

Deploy. Wait until the pod is running. Open a terminal.

### C. On the pod

**Simplest: drag the zip.** Open Jupyter on the pod and drop
`scratch70b_1m_takehome 2.zip` into `/workspace`. You still need the
training code (that is not inside the zip). Clone the public stack,
then import what you uploaded:

```bash
cd /workspace
git clone --depth 1 https://github.com/zivzancoeli-commits/llm-training-stack.git lmm
cd lmm
python -m pip install -U pip
python -m pip install pyyaml pytest deepspeed
python -c "from pathlib import Path; from data_pipeline.import_zip import import_takehome_zip; print(import_takehome_zip(Path('/workspace/scratch70b_1m_takehome 2.zip')))"
python -m pytest tests/test_scratch_pretrain.py tests/test_token_budget.py -q
```

Dragging only the zip is not enough: it has markdown, not DeepSpeed or
the 70B recipe. Dragging the whole training-stack folder also works if
you would rather not `git clone`.

Or clone the zip from GitHub (now public) instead of dragging it:

```bash
git clone --depth 1 https://github.com/zivzancoeli-commits/llm-dataset.git /workspace/llm-dataset
python -c "from pathlib import Path; from data_pipeline.import_zip import find_takehome_zip, import_takehome_zip; print(import_takehome_zip(find_takehome_zip(Path('/workspace/llm-dataset'))))"
```

**10-step smoke first** (still bills the node; 200k context is slow because
params/Adam sit in host RAM). Pick an 8× H200 SXM SKU with **a lot of
system RAM** (on the order of a terabyte). The 300GB volume is not the
offload device.

```bash
deepspeed --num_gpus 8 -m pretrain.train --recipe 70b_scratch --smoke
```

You want finite `step=… loss=…` lines. Then, only if that worked:

```bash
deepspeed --num_gpus 8 -m pretrain.train --recipe 70b_scratch --full
```

Checkpoints land in `outputs/70b_scratch/`. Stop the pod when you are
done. 8× H200 is expensive idle.

### D. What “good” looks like

- `nvidia-smi` shows 8 H200s.
- Smoke prints a loss for 10 steps and does not OOM.
- Full run writes `outputs/70b_scratch/ds/` and `tokenizer.json`.
- The model will **not** chat. ~706k tokens at 200k context on a 70B is a fit/loss check.

Optional Qwen instruct FT is a **different** job (`lmm ft-launch`, recipe
`70b_lora`). Do not mix it with this from-scratch run.

## 5. Laptop gate

- `uv run lmm check` → all tests passed.
- YAML profiles still have `context_length: 5120` (roadmap). `70b_scratch` overrides to **200000**.
- Recipes still say `gpu_type_id: NVIDIA H200` (not `H200 NVL`).
- `scratch-launch` / `ft-launch` without `--confirm` never mentions a `pod_id`.
