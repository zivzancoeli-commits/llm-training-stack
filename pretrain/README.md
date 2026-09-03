# pretrain/

Random-init Llama-like pretrain. **Not** Qwen/Llama instruct fine-tune.

Token budget: **1M preferred (or less)**, **2.5M hard cap**. Do not
generate toward 2.5M. 1M will not make a 70B generally fluent. It *will*
run a from-scratch loss curve.

```bash
uv run lmm scratch-plan --recipe 100m_scratch
uv run lmm scratch-plan --recipe 70b_scratch
uv run lmm scratch-train --recipe 100m_scratch --dry-run
```

On 8x H200 SXM, `70b_scratch` uses ZeRO-3 and the same 1M-token pack.

## 5B on a 16GB DDR3 Intel Mac (SSD offload)

`5b_mac_scratch` is CPU-only. DDR3 Macs are Intel, so there is **no
MPS** and the 5.1B model plus AdamW cannot live in 16GB of RAM. The
trainer keeps **one transformer block** in memory and streams the rest
from SSD: remaining layers, Adam moments, activations, and gradient
accumulators.

This will be brutally slow (hours to days per optimizer step), it will
thrash the SSD, and the machine may be unusable until you stop the
process. Close other apps. Plug in power. Use `caffeinate` so macOS does
not sleep. Keep **~80GB free** on the disk that holds `outputs/`. ~1M
tokens will not make a capable 5B; this is a loss-curve experiment.

```bash
uv sync --group dev
uv pip install torch   # CPU wheel on Intel Mac
uv run lmm scratch-plan --recipe 5b_mac_scratch

# One microbatch smoke. Still a long wait: it must write every layer to disk.
uv run lmm scratch-train --recipe 5b_mac_scratch

# Full 300-microstep run. Interrupt with Ctrl+C; shards are already on disk.
caffeinate uv run lmm scratch-train --recipe 5b_mac_scratch --full

# Continue after interruption (also auto-resumes if trainer_state.json exists).
caffeinate uv run lmm scratch-train --recipe 5b_mac_scratch --full --resume
```

Checkpoints are the per-layer files under
`outputs/5b_mac_scratch/offload/` (`layers/`, `adam/`, `trainer_state.json`),
not a single 70GB `latest.pt`. Delete that directory only if you want a
fresh random init. Do not `scratch-launch` this recipe; it is not a
RunPod job.
