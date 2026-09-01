# model/

Llama-like graph only. Custom kernels (FlashAttention-3, RoPE rotation,
fused RMSNorm/SwiGLU) are **hooks**, not code, until the 100M proxy needs
them.

## Layout

| Path | Role |
| --- | --- |
| `transformer_block.py` | Block blueprint + shape / init / MP-PP maps |
| `tensor_config.py` | `TensorView`, `ParallelLayout`, `LayerMap` |
| `layers/flash_attention.py` | FA-3 Protocol; default stub raises |
| `layers/rope.py` | Theta + context; `extend_theta` deferred to Phase 5 |
| `graphs/` | Placeholder for full-model wiring (embed → N blocks → ln → lm_head) |

## Parallelism maps (decoupled on purpose)

`TransformerBlock.parallel_layer_map` returns where a layer **would** sit
on a (TP, PP) grid. It does not call NCCL. That split is so DeepSpeed
ZeRO (≤7B) and Megatron TP/PP (≥70B) can consume the same block without
the block knowing which runtime is live.

Recorded default (see `DECISIONS.md`):

- ≤7B: TP=1, PP=1, ZeRO-2
- 70B: TP=4, PP=4
- 200B: TP=8, PP=8

## Context

Blocks default to 5,120. Do not construct a 350,208 block until Phase 5.
`RopeConfig.extend_theta` exists as a locked door for that phase.
