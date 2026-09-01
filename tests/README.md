# tests/

CPU-only verification loop. Run this on a laptop before any Slurm
allocation. There is no CUDA in CI on purpose.

```bash
uv sync --group dev
uv run pytest
```

## What is asserted today

| File | Marker | Catches |
| --- | --- | --- |
| `test_attention_shapes.py` | `shape` | GQA Q/K/V ranks, residual rejoin, mock FA-3 I/O |
| `test_layer_init.py` | `init` | GPT-2 residual std, µP width std, logit scale |
| `test_oom_thresholds.py` | `oom` | 350k naive scores, 200B weights, 7B@5k fit |
| `test_profiles.py` | (none) | YAML knobs: 5,120 context, GQA, reasoning mix |
| `test_finetune_plan.py` | (none) | 8x H200 SXM recipes fit; 200B full FT does not |
| `test_runpod_dry_run.py` | (none) | Pod JSON pin; no HTTP without `--confirm` |
| `test_scratch70b_dataset.py` | (none) | 114 unique seed docs, reasoning majority |
| `test_cli.py` | (none) | `lmm tour` / `ft-plan` / dry-run launch |
| `test_component_skeletons.py` | (none) | Loader shape, PP map, IB / heartbeat halt |

FlashAttention-3 is **mocked**. A mock that returns `(B, H, S, S)` scores
would fail `test_mock_fa3_preserves_q_shape_and_never_returns_scores`.

## What is not tested yet

Numerical parity against a reference SDPA kernel, tokenizer round-trips,
and multi-node overseer daemons. Those wait until a kernel exists.
