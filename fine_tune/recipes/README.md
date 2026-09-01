# fine_tune/recipes/

Human-editable fine-tune jobs. All three pin **8x NVIDIA H200 (SXM)** and
**5,120** context. Change a number, then:

```bash
uv run pytest tests/test_finetune_plan.py tests/test_runpod_dry_run.py
uv run lmm ft-plan --recipe 7b_lora
```

| File | When to use |
| --- | --- |
| `7b_lora.yaml` | Cheapest. Under-uses 8x H200; good first smoke. |
| `7b_full.yaml` | Uses the 8 GPUs. Default if you really want this node busy on a small model. |
| `70b_lora.yaml` | Why 8x 141GB exists. |
| `70b_qlora_a40.yaml` | 4-bit LoRA on 2x A40 48GB. Not for `lmm ft-launch`. |
| `70b_qlora_a40_3x.yaml` | Same, 3x A40 if 2x OOMs. |

`base_model` is a public Qwen instruct checkpoint so you are not blocked on
Llama license click-through. Swap the Hugging Face id if you already have
weights — keep `n_params` / `hidden_size` honest or the OOM tests lie.
