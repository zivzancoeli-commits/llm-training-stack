# Recorded defaults (so this scaffold is not blocked)

The original brief said to stop and ask at every ambiguous architecture
choice. This file records the **cheap default** we took so the repo can
exist. Override these before Phase 1 if you care; none of them require
rewriting tests except vocab size and head counts.

| Topic | Default | Cheap to change until |
| --- | --- | --- |
| Framework | **PyTorch** (Llama/DeepSpeed/Megatron ecosystem). Not JAX. | Phase 0 |
| 70B vs 200B goal | Original prompt said 70B-from-scratch. **200B is the goal**; 70B is a systems probe. | already reflected |
| Context | **5,120** until Phase 5; **350,208** only then | locked |
| Tokenizer | 32k slot byte-level BPE (`data_pipeline/tokenization/bpe.py`) | Phase 1 |
| From-scratch token budget | **1M preferred (or less), 2.5M hard cap** | now |
| Fine-tune base | Optional Qwen2.5 instruct — **not** the from-scratch path | now |
| Small-model quality | Reasoning **data mix**, not long context | Phase 0 YAML |
| ≤7B runtime | DeepSpeed ZeRO-2 | Phase 2 |
| 70B / 200B runtime | Megatron-LM TP+PP | Phase 3 |
| Pretrain scheduler | Slurm first; K8s folder stays empty | Phase 3 |
| GPU vendor | **8x H200 SXM** for from-scratch 70B ZeRO-3 and optional FT | now |
| Fine-tune cluster | **RunPod 8x `NVIDIA H200` (SXM)**, dry-run until `--confirm` | now |
| Fine-tune base | Qwen2.5 instruct (7B / 72B), not our untrained 200B | now |
| Precision | bf16 compute, fp32 reduction | Phase 0 |
| Logging | Local JSON via the overseer; no W&B required | Phase 1 |
| 200B shape | 82L × 14336d × 112 heads — a **proposal** | Phase 4 freeze |

If you want JAX, a 128k tokenizer, AMD GPUs, or Kubernetes-first, say so
before we write a kernel. The tests are framework-agnostic on purpose
(`TensorView` is a shape tuple, not a `torch.Tensor`).
