# specs/

Source of truth for **numbers**, not kernels. If a later FlashAttention-3
hook, ZeRO config, or dataloader disagrees with these contracts, the contract
wins and the implementation is wrong.

## What lives here

| Path | Role |
| --- | --- |
| `contracts/attention_shapes.py` | Q/K/V/GQA/output shape tuples |
| `contracts/initialization.py` | GPT-2 residual std + µP width std |
| `contracts/memory.py` | Naive vs FlashAttention working-set bytes, OOM tripwire |
| `chinchilla.py` | `tokens ≈ 20N` and `FLOPs ≈ 6ND` |
| `hyperparameter_profiles/` | Frozen YAML per phase (100M → 200B) |
| `scaling_laws.md` | Why 5,120 context until 200B, then 350,208 |

Do not put training loops, CUDA, or cluster scripts in this folder.

## Context policy (locked)

- Every model **below 200B**, and the 200B **pretrain** itself: **5,120** tokens.
- 200B **context-extension** phase only: **350,208** tokens (350k aligned to 128).

That split is the main cost control in this repo. Attention memory is
quadratic if scores are materialized; we refuse those configs in tests
before anyone rents a 256-GPU job.
