# fine_tune/

Fine-tune an **existing** instruct checkpoint on **8x H200 SXM**.
This is not the 200B-from-scratch path. Context stays **5,120**.

```bash
uv run lmm ft-plan --recipe 7b_lora
uv run lmm ft-launch --dry-run --recipe 7b_lora
```

See `WALKTHROUGH.md` §3 for MCP / `--confirm`. Recipes live in `recipes/`.
The on-pod loop is `train.py` → `runtime.py` (torch is imported only
when CUDA exists).
