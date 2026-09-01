# infra/runpod/

Automation for **8x H200 SXM** fine-tunes. Default is dry-run. This
folder does not create pods by itself.

## GPU pin

| Field | Value | Why |
| --- | --- | --- |
| `gpuTypeIds` | `["NVIDIA H200"]` | RunPod's **SXM** H200 SKU (141 GB). |
| Not | `NVIDIA H200 NVL` | Different card. Tests fail if a recipe uses it. |
| `gpuCount` | `8` | The node you asked for. |
| `cloudType` | `SECURE` | SXM inventory lives here. |
| `interruptible` | `false` | An 8-GPU spot preemption is expensive. |

## How to automate (three layers)

1. **Local (always, free)**
   ```bash
   uv run lmm ft-plan --recipe 7b_lora
   uv run lmm ft-launch --dry-run --recipe 7b_lora
   ```
   Prints the exact REST body. No GPU, no bill.

2. **Cursor MCP (this is the command from the RunPod banner)**
   On your laptop, in Cursor:
   ```bash
   npx @runpod/mcp-server@latest add
   ```
   Sign in with RunPod. Then you can ask the agent to create the pod
   using the JSON from `lmm ft-launch --dry-run`. This cloud session
   does **not** currently have that MCP connected, so it cannot rent
   GPUs for you from here.

3. **REST (CI / scripts)**
   ```bash
   export RUNPOD_API_KEY=...
   uv run lmm ft-launch --confirm --recipe 7b_lora --git-url https://github.com/zivzancoeli-commits/llm-training-stack.git
   ```
   Requires a clone URL because the pod bootstrap `git clone`s this repo,
   runs pytest, then `python -m fine_tune.train`.

## Cost brake

8x H200 is not a laptop. `ft-launch` without `--confirm` never POSTs.
The bootstrap starts in **smoke** mode (10 steps) unless you pass `--full`.
