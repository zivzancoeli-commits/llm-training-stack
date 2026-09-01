# Scaling Manifest

Cost-and-compute-aware ladder from a **100M proxy** to a **200B** model
with **350k** context. Every phase before that, including 200B pretrain,
stays at **5,120** context so we do not pay quadratic attention cost while
the architecture is still moving.

This is a plan, not a scheduler. No phase starts until the previous
exit criteria are green. Token counts are **under-Chinchilla** from 1B
upward on purpose (see `specs/scaling_laws.md`).

## Locked constraints

- Context = **5,120** on 100M, 1B, 7B, 70B, and 200B pretrain.
- Context = **350,208** (350k, multiple of 128) only in Phase 5, as a
  **context-extension** run on already-trained 200B weights. We do not
  pretrain 200B at 350k.
- Small models stay *smart* via a **reasoning-heavy data mix**, not via
  long context.
- Hardware is quoted in **80GB-class NVIDIA GPUs** (H100/A100) for the
  pretrain ladder. Fine-tunes use **8x H200 SXM (141 GB)** on RunPod.
- A laptop CPU is enough for this repository's pytest loop.

## Phase table

| Phase | Target Model Size | Target Token Count | Hardware Budgets | Exit criteria (all must pass) |
| --- | --- | --- | --- |
| **0 — Proxy** | **100M** (12L × 768d, MHA) | **2.0B** tokens (1.0× Chinchilla) at **5,120** context. Mix: 50% math/code/short CoT, 50% clean general text. | **$0–low:** this pytest suite on CPU. Optional: 1× 24GB consumer GPU for a later tiny real run. No InfiniBand, no Slurm. | (1) `uv run pytest` is green (shapes, init stds, OOM mocks, overseer). (2) Config YAML matches the 100M profile. (3) Residual-output std equals `0.02/sqrt(24)`. (4) Packed loader shape is `(B, 5120)`. (5) A later real run (not in this scaffold) must show decreasing LM loss and a non-zero score on a tiny GSM-style smoke set — *before* anyone rents more than one GPU. |
| **1 — Reasoning-first** | **1B** (16L × 2048d, GQA 16/4) | **10B** tokens (0.5× Chinchilla) at **5,120**. Mix: **60%** reasoning/code/math. | **1–2× 80GB**, TP=1, PP=1, DeepSpeed ZeRO-2. Single node. Budget: days on one box, not a reservation. | (1) GQA shape tests still pass (KV heads ≠ Q heads). (2) GPU starvation ratio from the loader stays **< 2%**. (3) Loss is stable (no spike-to-NaN over the run). (4) Reasoning evals beat the 100M proxy by a pre-registered delta on the *same* short-context suite (GSM8K-subset, HumanEval-subset, a short MMLU-lite). (5) Checkpoint save/resume once. If evals do not beat 100M, **do not scale width** — fix data mix first. |
| **2 — Cheap 7B** | **7B** (32L × 4096d, GQA 32/8, Llama-7B-shaped) | **40B** tokens (0.29× Chinchilla) at **5,120**. Mix: 45% reasoning. | **8× 80GB**, one node, ZeRO-2. This is the last phase that should *not* need Megatron TP/PP. | (1) Single-rank pessimistic footprint at 5,120 **fits 80GB** in `test_oom_thresholds` (weights + Adam moments + FA workspace). (2) Naive 350k scores **do not** fit — still refused. (3) MFU **> 30%** on the 8-GPU node. (4) Reasoning suite beats Phase 1; 5,120-context quality is the KPI, not a long-context demo. (5) Overseer staging test: inject a down IB link, confirm `should_halt_job`. (6) Resume from checkpoint on a *new* 8-GPU allocation. |
| **3 — 70B probe** | **70B** (80L × 8192d, GQA 64/8) | **100B** tokens (≈0.07× Chinchilla) at **5,120**. This is a **systems probe**, not a 15T frontier run. Mix: 35% reasoning so the probe still has to think. | **64× 80GB** (8 nodes). **TP=4, PP=4**, ZeRO-1 on the replica dim. InfiniBand required. Do not attempt ZeRO-3-only 70B. | (1) `parallel_layer_map` places layers 0–19 / 20–39 / 40–59 / 60–79 on PP stages 0–3. (2) Numerical-parity tests (to be added with the kernel) match a TP=1 reference on a sliced block. (3) Scaling: 70B loss vs tokens sits on the curve extrapolated from 7B (no architecture bug). (4) Zero silent IB degradation over a 24h soak (`InfraOverseer` halt path exercised on a real rail, not just the mock). (5) Reasoning evals do not *collapse* vs 7B (allowed to be flat if tokens are few; a large regression means the MP map is wrong). **Stop here if MP is dirty — do not jump to 200B.** |
| **4 — 200B pretrain** | **200B** (82L × 14336d, GQA 112/8 — proposal) | **300B** tokens (≈0.075× Chinchilla) at **5,120**. Not 4T. Mix: 30% reasoning; do not dump the mix to raw crawl just because the model is wide. | **256× 80GB** (32 nodes). **TP=8, PP=8**. This is the first phase that is *allowed* to be expensive. | (1) 200B **parameter** bytes refuse a single 80GB GPU in OOM tests (400GB weights). (2) FA-3 hook, not naive scores, is on the hot path. (3) Pretrain context remains 5,120 — a job that advertises 350k in this phase is a failed exit. (4) Reasoning suite still competitive with the 7B / 70B short-context numbers (width must not erase the mix). (5) Cluster soak: overseer heartbeats from all 32 nodes, halt on one injected stale rank. (6) Stable MFU and a checkpoint that reloads on a fresh 256-GPU allocation. |
| **5 — 350k extension** | **same 200B weights** | **+5–15B** long-context tokens (plan: **10B**) at **350,208**. Documents packed and/or synthetic long-range tasks. Do not repeat the 300B pretrain at 350k. | **256× 80GB** plus **context / sequence parallel** (ring / striped attention). RoPE theta is extended here (`RopeConfig.extend_theta`), not before. | (1) Naive `(B, H, 350208, 350208)` scores still **OOM** in tests; FA workspace stays O(seq). (2) Needle-in-a-haystack / long-doc QA at 350k meets a pre-registered floor. (3) **5,120-context reasoning suite does not regress** vs Phase 4 (the expensive context must not destroy short-context thinking). (4) Activation checkpointing + context parallel proven by a dry-run memory projection. (5) `extend_theta` is implemented and covered by a new test file before the job is submitted. |
| **FT — 8x H200 SXM** | Existing **7B or 72B instruct** checkpoint (Qwen2.5), **not** our untrained 200B | Smoke: **10 steps**. Full recipe: **300–500** optimizer steps at **5,120** context. LoRA or full FT; see `fine_tune/recipes/`. | **8× H200 SXM** (`gpuTypeIds: ["NVIDIA H200"]`, not NVL). Secure Cloud, on-demand. Dry-run with `lmm ft-launch`; real pod only with `--confirm` + `RUNPOD_API_KEY` (or RunPod MCP). | (1) `uv run lmm check` green on the laptop. (2) `ft-plan` reports `fits_node: true`. (3) Pod bootstrap re-runs pytest before training. (4) Smoke loss is finite. (5) 5,120-context reasoning probes do not collapse vs the base instruct model. **Do not** set context to 350k here. |

## Why this is cheaper than "train 70B from scratch at long context"

- 5,120 vs 350k is roughly a **68×** sequence ratio and a **~4,700×** naive
  score-tensor ratio. Paying that only once, on frozen 200B weights, is the
  whole cost strategy.
- 70B is **100B tokens**, not 1.4T. If Phase 3 only exists to prove
  tensor/pipeline maps, it can even be shortened further; the table is an
  upper bound.
- 100M and 1B carry the reasoning methodology (eval suite, mix ratios)
  while GPUs are cheap. A dumb 7B is more expensive to fix than a smart 1B.

## What "good reasoning" means at 5,120

Short chain-of-thought fits in 5,120. We optimize for that on purpose:

- Grade-school math and unit-test coding with worked solutions in the mix.
- Pack many short documents per sequence rather than one long one.
- Exit on **eval deltas**, not on "loss went down."

350k context in Phase 5 is for long documents and retrieval-over-sequence,
not for making the 1B "reason better."

## Phase-to-profile map

| Phase | YAML |
| --- | --- |
| 0 | `specs/hyperparameter_profiles/100m.yaml` |
| 1 | `specs/hyperparameter_profiles/1b.yaml` |
| 2 | `specs/hyperparameter_profiles/7b.yaml` |
| 3 | `specs/hyperparameter_profiles/70b.yaml` |
| 4–5 | `specs/hyperparameter_profiles/200b.yaml` |
| FT | `fine_tune/recipes/7b_lora.yaml`, `7b_full.yaml`, `70b_lora.yaml` |
