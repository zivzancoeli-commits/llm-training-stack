# infra/

Cluster side of the stack. Health lives in `overseer.py`. Fine-tune
pods live in `runpod/`. Slurm / K8s / Megatron folders stay placeholders
so those configs do not get dumped into `model/`.

## Layout

| Path | Status | Role |
| --- | --- | --- |
| `overseer.py` | thin skeleton | Node health, heartbeat timeout, IB Gbit/s floor |
| `runpod/` | dry-run launcher | 8x H200 SXM pod JSON + MCP notes |
| `deepspeed/` | ZeRO-2/3 JSON | `zero2_8x_h200.json`, `zero3_8x_h200.json` |
| `slurm/` | placeholder | `#SBATCH` templates |
| `k8s/` | placeholder | JobSet / Volcano manifests |
| `megatron/` | placeholder | TP/PP/SP flags for 70B and 200B |
| `monitoring/` | placeholder | Later: Prometheus rules, GPU Xid logs |

## How the overseer is meant to be used

A sidecar on each node (not written yet) should POST a `NodeHeartbeat`
every few seconds. The overseer:

- marks a node **stale** after `heartbeat_timeout_s` (default 30s)
- marks IB **degraded** if the link is down *or* below 100 Gbit/s
- returns `should_halt_job=True` if any known node is bad

That halt is how we avoid burning a 256-GPU allocation on a half-dead
rail. Tests inject fake heartbeats; they never call `ibstat`.

## Recorded runtime default

- **Fine-tunes:** RunPod 8x H200 SXM (`infra/runpod/`), dry-run until `--confirm`.
- **Scheduler (pretrain):** Slurm first. Kubernetes manifests stay empty until a
  platform team needs them.
- **≤7B:** DeepSpeed ZeRO-2 on 1–8×80GB.
- **70B / 200B:** Megatron-LM tensor + pipeline parallel. DeepSpeed
  remains an option for ZeRO-1 on the remaining replica dimension.

See `DECISIONS.md` if you want to flip any of those before Phase 2.
