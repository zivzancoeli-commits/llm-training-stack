# LMM Training Stack

Test-first scaffold for pretraining a dense Llama-like model from a
**100M proxy** up to **200B**, with **5,120** context on every run except
a final **350k** context-extension phase. Fine-tunes of open instruct
models run on **8x H200 SXM** and stay at 5,120.

**New here?** Open [`WALKTHROUGH.md`](WALKTHROUGH.md) and run:

```bash
uv sync --group dev
uv run lmm tour
uv run lmm check
uv run lmm data-review
```

GitHub (what RunPod clones):

- Dataset zip: https://github.com/zivzancoeli-commits/llm-dataset
  (`scratch70b_1m_takehome 2.zip` on `main`)
- Training stack: https://github.com/zivzancoeli-commits/llm-training-stack

Those repos must be **public** (or the pod needs `GITHUB_TOKEN`).

The review UI is how you go through the seed corpus. From-scratch
training is random init on **1M tokens preferred, or less (2.5M hard cap)**:

```bash
uv run lmm scratch-plan --recipe 100m_scratch
uv run lmm scratch-plan --recipe 70b_scratch
uv run lmm scratch-train --recipe 100m_scratch --dry-run
```

That is **not** Qwen. `lmm ft-launch` remains an optional instruct FT.

## Why it looks like this

- **Test-driven architecture:** shapes, init scales, and OOM bounds are
  code in `specs/contracts/` and are asserted in `tests/` *before* anyone
  writes FlashAttention-3 or rents 256 GPUs.
- **Modular extrapolation:** 100M, 7B, 70B, and 200B share one
  `TransformerBlock` blueprint. Width, depth, and GQA change; the
  attention boundary ranks do not.
- **Cost control:** long context is the expensive axis. It is disabled
  until the 200B weights exist. Small models get a reasoning-heavy mix
  instead. Details: [`SCALING_MANIFEST.md`](SCALING_MANIFEST.md).

## Layout

```
specs/           scaling laws, Chinchilla math, hyperparameter YAML
data_pipeline/   tokenizer / stream / dedup placeholders + loader skeleton
model/           Llama-like block, FA-3 hook, RoPE config, TP/PP maps
infra/           overseer, DeepSpeed JSON, RunPod 8x H200 SXM launcher
fine_tune/       recipes + `lmm` CLI + on-pod train entry
tests/           CPU pytest: shapes, init stds, mocked OOM, FT dry-run
```

## Run the verification loop

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/). No GPU.

```bash
uv sync --group dev
uv run lmm check
```

You should see shape, init, OOM, profile, and fine-tune dry-run tests
pass. FlashAttention-3 is mocked; a real kernel that returned a
`(B, H, S, S)` score tensor would fail on purpose.

## Fine-tune on 8x H200 SXM

```bash
uv run lmm ft-plan --recipe 7b_lora
uv run lmm ft-launch --dry-run --recipe 7b_lora
```

Connect RunPod in Cursor with `npx @runpod/mcp-server@latest add`, then
see [`WALKTHROUGH.md`](WALKTHROUGH.md) §3 before `--confirm`.

## What is intentionally missing

- Forward pass for from-scratch 100M/7B/70B (`pretrain/`) on ≤1M tokens
- 32k-slot byte-level BPE (`data_pipeline/tokenization/bpe.py`)
- Slurm/K8s/Megatron config files (folders exist, empty)
- 350k RoPE scaling (`RopeConfig.extend_theta` raises until Phase 5)

Those wait until the contracts in this repo are accepted.

## Defaults we did not wait to ask about

Recorded in [`DECISIONS.md`](DECISIONS.md): PyTorch, Slurm for pretrain
clusters, **RunPod 8x H200 SXM** for fine-tunes, DeepSpeed for ≤7B,
Megatron TP/PP from 70B, 32k BPE. Change those before Phase 1 if you
want a different stack.
