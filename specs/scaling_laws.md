# Scaling laws used by this stack

This file is the math companion to `SCALING_MANIFEST.md`. It is not a
training recipe.

## Compute-optimal tokens (Chinchilla)

Hoffmann et al. (2022) give the public rule of thumb:

```
N_tokens_opt ≈ 20 × N_params
C_train     ≈ 6 × N_params × N_tokens
```

We **do not** chase `N_tokens_opt` on the 70B or 200B runs. Those phases
are capacity and systems probes first. Token mass is spent earlier on the
100M / 1B / 7B models, where a reasoning-heavy mix is cheap.

| Phase | Params | Chinchilla tokens | Planned tokens | Planned / Chinchilla |
| --- | ---: | ---: | ---: | ---: |
| 0 proxy | 1.0e8 | 2.0e9 | 2.0e9 | 1.00 |
| 1 reasoning | 1.0e9 | 2.0e10 | 1.0e10 | 0.50 |
| 2 stable | 7.0e9 | 1.4e11 | 4.0e10 | 0.29 |
| 3 70B probe | 7.0e10 | 1.4e12 | 1.0e11 | 0.07 |
| 4 200B pretrain | 2.0e11 | 4.0e12 | 3.0e11 | 0.075 |
| 5 350k extension | 2.0e11 | (same) | +1.0e10 long-context | n/a |

## Why 5,120 context until 200B

Naive attention scores are `(batch, heads, seq, seq)`. Doubling context
quadruples that tensor. 5,120 is:

- a multiple of 128 (FlashAttention-3 tile size)
- long enough for GSM8K / short chain-of-thought / packed documents
- short enough that a 7B fit on 8×80GB is still a laptop-budget experiment
  compared with 350k

350,208 context is enabled **only** in Phase 5, after the 200B weights exist,
and only behind the FlashAttention / context-parallel path. Tests in
`tests/test_oom_thresholds.py` encode that refusal.

## Residual and width scaling (init)

- Residual **output** matrices (`W_o`, `W_down`): `std = 0.02 / sqrt(2 L)`
  so stream variance does not explode with depth (GPT-2).
- Width: µP `std = 1 / sqrt(fan_in)` so the 100M proxy can donate a learning
  rate to later widths instead of a full grid search.
- Attention logits: `1 / sqrt(head_dim)`.

These are asserted in `tests/test_layer_init.py`. Depth-64 70B and depth-82
200B must get **smaller** residual std than the 12-layer proxy.

## Reasoning at small size

Quality at 100M–7B is a **data** problem, not a context-length problem.
Profiles pin `reasoning_mix_ratio` (math, code, worked solutions, short
CoT) rather than stretching context. Exit criteria in the manifest are
reasoning evals, not just training loss.
