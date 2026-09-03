"""CPU + SSD training that never materializes the full model in RAM.

16GB DDR3 cannot hold 5B weights plus AdamW. This trainer keeps one
transformer block (and the current residual) in RAM, and writes
everything else — remaining layers, Adam moments, layer-boundary
activations, and gradient accumulators — to disk.

This is extremely slow and wears the SSD. It is the only way a 5B
random-init run at 5,120 context can proceed on an Intel Mac with 16GB.
"""

from __future__ import annotations

import gc
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from pretrain.llama import SEQ_CHUNK, LlamaBuild, llama_parts
from pretrain.planner import ScratchPlan

BETA1 = 0.9
BETA2 = 0.95
ADAM_EPS = 1e-8
INIT_STD = 0.02


def _torch_load(torch: Any, path: Path) -> Any:
    try:
        return torch.load(path, map_location="cpu", weights_only=False)
    except TypeError:
        return torch.load(path, map_location="cpu")


class DiskLayerStore:
    """Per-layer shards under ``root``. Safe to resume a partial init."""

    def __init__(self, root: Path, spec: LlamaBuild) -> None:
        self.root = Path(root)
        self.spec = spec
        self.layers = self.root / "layers"
        self.adam = self.root / "adam"
        self.grads = self.root / "grads"
        self.acts = self.root / "activations"
        self.meta_path = self.root / "meta.json"
        self.state_path = self.root / "trainer_state.json"

    def prepare(self) -> None:
        for directory in (self.layers, self.adam, self.grads, self.acts):
            directory.mkdir(parents=True, exist_ok=True)

    def save_tensor_tree(self, obj: Any, path: Path) -> None:
        import torch

        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".tmp")
        torch.save(obj, temporary)
        temporary.replace(path)

    def load_tensor_tree(self, path: Path) -> Any:
        import torch

        return _torch_load(torch, path)

    def block_path(self, index: int) -> Path:
        return self.layers / f"block_{index:03d}.pt"

    def embed_path(self) -> Path:
        return self.layers / "embed.pt"

    def norm_path(self) -> Path:
        return self.layers / "norm.pt"

    def adam_path(self, key: str) -> Path:
        return self.adam / f"{key}.pt"

    def grad_path(self, key: str) -> Path:
        return self.grads / f"{key}.pt"

    def act_path(self, index: int) -> Path:
        return self.acts / f"h_{index:03d}.pt"

    def _meta(self) -> dict[str, Any]:
        if not self.meta_path.is_file():
            return {}
        return json.loads(self.meta_path.read_text())

    def _write_meta(self, done: set[str], *, complete: bool = False) -> None:
        payload = {
            "initialized": sorted(done),
            "n_layers": self.spec.n_layers,
            "hidden_size": self.spec.hidden_size,
            "complete": complete,
        }
        temporary = self.meta_path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(payload, indent=2) + "\n")
        temporary.replace(self.meta_path)

    def initialize(self, parts: Any) -> None:
        """Random-init each shard to SSD. Re-runs skip shards already on disk."""
        from torch import nn

        self.prepare()
        done = set(self._meta().get("initialized") or [])
        if "embed" not in done:
            embed = nn.Embedding(self.spec.vocab_size, self.spec.hidden_size)
            nn.init.normal_(embed.weight, mean=0.0, std=INIT_STD)
            self.save_tensor_tree(embed.state_dict(), self.embed_path())
            self._init_adam("embed", embed)
            del embed
            _release()
            done.add("embed")
            self._write_meta(done)
            print("disk-offload init embed", flush=True)
        for index in range(self.spec.n_layers):
            key = f"block_{index}"
            if key in done:
                continue
            block = parts.Block()
            for module in block.modules():
                if isinstance(module, nn.Linear):
                    nn.init.normal_(module.weight, mean=0.0, std=INIT_STD)
            self.save_tensor_tree(block.state_dict(), self.block_path(index))
            self._init_adam(key, block)
            del block
            _release()
            done.add(key)
            self._write_meta(done)
            print(
                f"disk-offload init block {index + 1}/{self.spec.n_layers}",
                flush=True,
            )
        if "norm" not in done:
            norm = parts.RMSNorm(self.spec.hidden_size)
            self.save_tensor_tree(norm.state_dict(), self.norm_path())
            self._init_adam("norm", norm)
            del norm
            _release()
            done.add("norm")
            self._write_meta(done)
            print("disk-offload init norm", flush=True)
        self._write_meta(done, complete=True)

    def _init_adam(self, key: str, module: Any) -> None:
        import torch

        state = {
            name: {
                "m": torch.zeros_like(param, dtype=torch.float32),
                "v": torch.zeros_like(param, dtype=torch.float32),
            }
            for name, param in module.named_parameters()
        }
        self.save_tensor_tree(state, self.adam_path(key))

    def load_embed(self) -> Any:
        from torch import nn

        embed = nn.Embedding(self.spec.vocab_size, self.spec.hidden_size)
        embed.load_state_dict(self.load_tensor_tree(self.embed_path()))
        embed.train()
        return embed

    def load_block(self, parts: Any, index: int) -> Any:
        block = parts.Block()
        block.load_state_dict(self.load_tensor_tree(self.block_path(index)))
        block.train()
        return block

    def load_norm(self, parts: Any) -> Any:
        norm = parts.RMSNorm(self.spec.hidden_size)
        norm.load_state_dict(self.load_tensor_tree(self.norm_path()))
        norm.train()
        return norm

    def save_module(self, key: str, module: Any) -> None:
        if key == "embed":
            path = self.embed_path()
        elif key == "norm":
            path = self.norm_path()
        elif key.startswith("block_"):
            path = self.block_path(int(key.split("_", 1)[1]))
        else:
            raise KeyError(key)
        self.save_tensor_tree(module.state_dict(), path)

    def save_act(self, index: int, tensor: Any) -> None:
        self.save_tensor_tree(tensor.detach().contiguous().cpu(), self.act_path(index))

    def load_act(self, index: int, *, requires_grad: bool = False) -> Any:
        tensor = self.load_tensor_tree(self.act_path(index))
        if requires_grad:
            tensor = tensor.detach().requires_grad_(True)
        return tensor

    def clear_acts(self) -> None:
        for path in self.acts.glob("h_*.pt"):
            path.unlink()

    def add_grads(self, key: str, module: Any) -> None:
        path = self.grad_path(key)
        acc: dict[str, Any] = self.load_tensor_tree(path) if path.is_file() else {}
        for name, param in module.named_parameters():
            if param.grad is None:
                continue
            grad = param.grad.detach().cpu()
            acc[name] = acc[name] + grad if name in acc else grad.clone()
        self.save_tensor_tree(acc, path)

    def clear_grads(self) -> None:
        for path in self.grads.glob("*.pt"):
            path.unlink()

    def adamw_step(
        self,
        key: str,
        module: Any,
        *,
        lr: float,
        weight_decay: float,
        opt_step: int,
        grad_scale: float,
    ) -> None:
        adam = self.load_tensor_tree(self.adam_path(key))
        grads_path = self.grad_path(key)
        grads = self.load_tensor_tree(grads_path) if grads_path.is_file() else {}
        if opt_step < 1:
            raise ValueError("opt_step must be 1-based for Adam bias correction")
        for name, param in module.named_parameters():
            grad = grads.get(name)
            if grad is None:
                continue
            grad = grad.float() * grad_scale
            if weight_decay and param.ndim >= 2:
                param.data.mul_(1.0 - lr * weight_decay)
            slot = adam[name]
            slot["m"].mul_(BETA1).add_(grad, alpha=1.0 - BETA1)
            slot["v"].mul_(BETA2).addcmul_(grad, grad, value=1.0 - BETA2)
            mhat = slot["m"] / (1.0 - BETA1**opt_step)
            vhat = slot["v"] / (1.0 - BETA2**opt_step)
            param.data.addcdiv_(mhat, vhat.sqrt().add(ADAM_EPS), value=-lr)
        self.save_tensor_tree(adam, self.adam_path(key))
        self.save_module(key, module)

    def load_counters(self) -> tuple[int, int]:
        if not self.state_path.is_file():
            return 0, 0
        data = json.loads(self.state_path.read_text())
        return int(data.get("step", 0)), int(data.get("opt_step", 0))

    def save_counters(self, step: int, opt_step: int) -> None:
        temporary = self.state_path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps({"step": step, "opt_step": opt_step}, indent=2) + "\n"
        )
        temporary.replace(self.state_path)


def _release() -> None:
    gc.collect()


def _chunked_tied_loss(weight: Any, hidden: Any, labels: Any, vocab_size: int) -> Any:
    import torch
    from torch.nn import functional as F

    pred = hidden[:, :-1, :]
    tgt = labels[:, 1:]
    total = hidden.new_zeros(())
    for start in range(0, pred.size(1), SEQ_CHUNK):
        logits = F.linear(pred[:, start : start + SEQ_CHUNK], weight)
        total = total + F.cross_entropy(
            logits.reshape(-1, vocab_size),
            tgt[:, start : start + SEQ_CHUNK].reshape(-1),
            ignore_index=0,
            reduction="sum",
        )
    ntok = (tgt != 0).sum().to(dtype=total.dtype).clamp(min=1)
    return total / ntok


def stream_microbatch(
    store: DiskLayerStore,
    spec: LlamaBuild,
    parts: Any,
    input_ids: Any,
    labels: Any,
) -> float:
    """One forward+backward. Grads accumulate on disk. Activations are freed."""
    import torch

    embed = store.load_embed()
    with torch.no_grad():
        hidden = embed(input_ids)
    store.save_act(0, hidden)
    del embed, hidden
    _release()

    for index in range(spec.n_layers):
        block = store.load_block(parts, index)
        hidden = store.load_act(index)
        with torch.no_grad():
            hidden = block(hidden)
        store.save_act(index + 1, hidden)
        del block, hidden
        _release()
        print(f"  fwd layer {index + 1}/{spec.n_layers}", flush=True)

    hidden = store.load_act(spec.n_layers, requires_grad=True)
    norm = store.load_norm(parts)
    embed = store.load_embed()
    loss = _chunked_tied_loss(
        embed.weight, norm(hidden), labels, spec.vocab_size
    )
    loss.backward()
    store.add_grads("norm", norm)
    store.add_grads("embed", embed)
    residual_grad = hidden.grad.detach().contiguous()
    loss_value = float(loss.detach())
    del norm, embed, hidden, loss
    _release()

    for index in range(spec.n_layers - 1, -1, -1):
        block = store.load_block(parts, index)
        h_in = store.load_act(index, requires_grad=True)
        h_out = block(h_in)
        h_out.backward(residual_grad)
        store.add_grads(f"block_{index}", block)
        residual_grad = h_in.grad.detach().contiguous()
        del block, h_in, h_out
        _release()
        print(f"  bwd layer {index + 1}/{spec.n_layers}", flush=True)

    embed = store.load_embed()
    h0 = embed(input_ids)
    h0.backward(residual_grad)
    store.add_grads("embed", embed)
    del embed, h0, residual_grad
    _release()
    store.clear_acts()
    return loss_value


def apply_adam(
    store: DiskLayerStore,
    spec: LlamaBuild,
    parts: Any,
    *,
    lr: float,
    weight_decay: float,
    opt_step: int,
    grad_scale: float,
) -> None:
    embed = store.load_embed()
    store.adamw_step(
        "embed",
        embed,
        lr=lr,
        weight_decay=weight_decay,
        opt_step=opt_step,
        grad_scale=grad_scale,
    )
    del embed
    _release()
    for index in range(spec.n_layers):
        block = store.load_block(parts, index)
        store.adamw_step(
            f"block_{index}",
            block,
            lr=lr,
            weight_decay=weight_decay,
            opt_step=opt_step,
            grad_scale=grad_scale,
        )
        del block
        _release()
        print(f"  adam layer {index + 1}/{spec.n_layers}", flush=True)
    norm = store.load_norm(parts)
    store.adamw_step(
        "norm",
        norm,
        lr=lr,
        weight_decay=weight_decay,
        opt_step=opt_step,
        grad_scale=grad_scale,
    )
    del norm
    _release()
    store.clear_grads()


def _warn_machine(spec: LlamaBuild, root: Path) -> None:
    threads = max(1, min(4, os.cpu_count() or 1))
    print(
        "disk-offload CPU training: one transformer block in RAM, "
        f"the rest on SSD under {root}. Intel 16GB DDR3 has no MPS. "
        "Expect hours to days per optimizer step, heavy SSD wear, and a "
        "machine that is barely usable until you stop the run.",
        flush=True,
    )
    if spec.n_layers >= 16 and spec.hidden_size >= 2048:
        free_gb = shutil.disk_usage(root).free / 1024**3
        print(f"disk-offload free_gb={free_gb:.1f} threads={threads}", flush=True)
        if free_gb < 80:
            sys.stderr.write(
                "Need about 80GB free for 5B fp32 weights + Adam moments. "
                f"Only {free_gb:.1f}GB is free.\n"
            )


def run_disk_offload(
    plan: ScratchPlan,
    packed_cls: type,
    tokenizer: Any,
    *,
    resume: bool = False,
) -> int:
    import torch
    from torch.utils.data import DataLoader

    recipe = plan.recipe
    spec = LlamaBuild.from_recipe(recipe)
    parts = llama_parts(spec)
    out = Path("outputs") / recipe.name
    store = DiskLayerStore(out / "offload", spec)
    store.prepare()
    _warn_machine(spec, store.root)
    torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))

    store.initialize(parts)
    step, opt_step = store.load_counters()
    if resume or step > 0:
        print(f"resumed step={step} opt_step={opt_step} from {store.root}", flush=True)

    steps = recipe.smoke_steps if plan.smoke else recipe.max_steps
    loader = DataLoader(packed_cls(), batch_size=recipe.micro_batch_size, shuffle=True)
    pending = 0
    while step < steps:
        for batch in loader:
            if step >= steps:
                break
            loss = stream_microbatch(
                store,
                spec,
                parts,
                batch["input_ids"],
                batch["labels"],
            )
            pending += 1
            step += 1
            store.save_counters(step, opt_step)
            print(f"step={step} loss={loss:.4f}", flush=True)
            flush = pending >= recipe.grad_accum or step >= steps
            if flush:
                opt_step += 1
                apply_adam(
                    store,
                    spec,
                    parts,
                    lr=recipe.lr,
                    weight_decay=recipe.weight_decay,
                    opt_step=opt_step,
                    grad_scale=1.0 / pending,
                )
                pending = 0
                store.save_counters(step, opt_step)
                if recipe.checkpoint_every and opt_step % recipe.checkpoint_every == 0:
                    print(
                        f"checkpoint opt_step={opt_step} shards under {store.root}",
                        flush=True,
                    )
    out.mkdir(parents=True, exist_ok=True)
    tokenizer.save(out / "tokenizer.json")
    store.save_counters(step, opt_step)
    return 0
