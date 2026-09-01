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
