"""From-scratch train loop. Imported only when CUDA (or --force-cpu) is on."""

from __future__ import annotations

import os
from pathlib import Path

from data_pipeline.token_budget import HARD_TOKEN_CAP
from pretrain.corpus import iter_corpus_docs, tokenize_and_pack
from pretrain.llama import LlamaBuild, build_llama
from pretrain.planner import ScratchPlan

DEEPSPEED_LAUNCH = (
    "deepspeed --num_gpus 8 -m pretrain.train --recipe 70b_scratch --smoke"
)


def require_distributed_70b(n_params: int, zero_stage: int, env: dict[str, str] | None = None) -> None:
    env = env if env is not None else dict(os.environ)
    if n_params >= 70_000_000_000 and zero_stage >= 3:
        if "LOCAL_RANK" not in env and "RANK" not in env:
            raise RuntimeError(
                "70b_scratch does not fit on one GPU. Launch with:\n  " + DEEPSPEED_LAUNCH
            )


def run_scratch(plan: ScratchPlan, *, data_roots: tuple[Path, ...] | None = None) -> int:
    try:
        import torch
        from torch.utils.data import DataLoader, Dataset
    except ImportError as exc:
        raise RuntimeError(
            "torch is required for from-scratch training. "
            "Locally use: uv run lmm scratch-train --dry-run"
        ) from exc

    recipe = plan.recipe
    if recipe.max_tokens > HARD_TOKEN_CAP:
        raise ValueError("token budget exceeds the 2.5M hard cap")
    require_distributed_70b(recipe.n_params, recipe.zero_stage)
    docs = iter_corpus_docs() if data_roots is None else iter_corpus_docs(data_roots)
    tokenizer, rows = tokenize_and_pack(
        [],
        vocab_size=recipe.vocab_size,
        seq_len=recipe.context_length,
        max_tokens=recipe.max_tokens,
        docs=docs,
    )

    class Packed(Dataset):
        def __len__(self) -> int:
            return len(rows)

        def __getitem__(self, idx: int) -> dict:
            ids = torch.tensor(rows[idx], dtype=torch.long)
            return {"input_ids": ids, "labels": ids.clone()}

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if recipe.n_params >= 70_000_000_000 and device.type != "cuda":
        raise RuntimeError("70b_scratch needs 8x H200 CUDA; this machine has none")

    if recipe.zero_stage >= 3 and device.type == "cuda":
        return _run_zero3(plan, Packed, tokenizer)

    model = build_llama(LlamaBuild.from_recipe(recipe))
    dtype = torch.bfloat16 if device.type == "cuda" else torch.float32
    model = model.to(device=device, dtype=dtype)
    opt = torch.optim.AdamW(model.parameters(), lr=recipe.lr, weight_decay=recipe.weight_decay)
    steps = recipe.smoke_steps if plan.smoke else recipe.max_steps
    loader = DataLoader(Packed(), batch_size=recipe.micro_batch_size, shuffle=True)
    model.train()
    step = 0
    while step < steps:
        for batch in loader:
            if step >= steps:
                break
            ids = batch["input_ids"].to(device)
            labels = batch["labels"].to(device)
            _, loss = model(ids, labels)
            (loss / recipe.grad_accum).backward()
            if (step + 1) % recipe.grad_accum == 0:
                opt.step()
                opt.zero_grad(set_to_none=True)
            step += 1
            print(f"step={step} loss={float(loss.detach()):.4f}", flush=True)
    out = Path("outputs") / recipe.name
    out.mkdir(parents=True, exist_ok=True)
    torch.save({"model": model.state_dict(), "step": step}, out / "scratch.pt")
    tokenizer.save(out / "tokenizer.json")
    return 0


def _run_zero3(plan: ScratchPlan, packed_cls, tokenizer) -> int:
    import torch
    from torch.utils.data import DataLoader

    try:
        import deepspeed
    except ImportError as exc:
        raise RuntimeError(
            "70b_scratch wants DeepSpeed ZeRO-3 on the 8x H200 node. "
            "pip install deepspeed, then: " + DEEPSPEED_LAUNCH
        ) from exc

    recipe = plan.recipe
    world = max(int(os.environ.get("WORLD_SIZE", "8")), 1)
    ds_config = {
        "train_micro_batch_size_per_gpu": recipe.micro_batch_size,
        "gradient_accumulation_steps": recipe.grad_accum,
        "train_batch_size": recipe.micro_batch_size * recipe.grad_accum * world,
        "bf16": {"enabled": True},
        "zero_optimization": {
            "stage": 3,
            "overlap_comm": True,
            "contiguous_gradients": True,
        },
        "optimizer": {
            "type": "AdamW",
            "params": {
                "lr": recipe.lr,
                "betas": [0.9, 0.95],
                "weight_decay": recipe.weight_decay,
            },
        },
        "gradient_clipping": 1.0,
        "steps_per_print": 1,
    }
    if recipe.cpu_offload:
        ds_config["zero_optimization"]["offload_param"] = {
            "device": "cpu",
            "pin_memory": True,
        }
        ds_config["zero_optimization"]["offload_optimizer"] = {
            "device": "cpu",
            "pin_memory": True,
        }
        ds_config["activation_checkpointing"] = {
            "partition_activations": True,
            "cpu_checkpointing": True,
            "contiguous_memory_optimization": True,
            "number_checkpoints": 16,
        }
    class _LossOnly(torch.nn.Module):
        def __init__(self, inner: torch.nn.Module):
            super().__init__()
            self.inner = inner

        def forward(self, input_ids: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
            _, loss = self.inner(input_ids, labels)
            assert loss is not None
            return loss

    with deepspeed.zero.Init(dtype=torch.bfloat16):
        model = _LossOnly(build_llama(LlamaBuild.from_recipe(recipe)))
    engine, _, _, _ = deepspeed.initialize(
        model=model,
        model_parameters=model.parameters(),
        config=ds_config,
    )
    steps = recipe.smoke_steps if plan.smoke else recipe.max_steps
    loader = DataLoader(
        packed_cls(),
        batch_size=recipe.micro_batch_size,
        shuffle=True,
    )
    engine.train()
    step = 0
    while step < steps:
        for batch in loader:
            if step >= steps:
                break
            ids = batch["input_ids"].to(engine.device)
            labels = batch["labels"].to(engine.device)
            loss = engine(ids, labels)
            engine.backward(loss)
            engine.step()
            step += 1
            if engine.local_rank == 0:
                print(f"step={step} loss={float(loss.detach()):.4f}", flush=True)
    if engine.local_rank == 0:
        out = Path("outputs") / recipe.name
        out.mkdir(parents=True, exist_ok=True)
        tokenizer.save(out / "tokenizer.json")
    engine.save_checkpoint(str(Path("outputs") / recipe.name / "ds"))
    return 0
