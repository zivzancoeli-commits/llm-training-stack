"""Random-init pretrain recipes. No Hugging Face base checkpoint."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from data_pipeline.token_budget import HARD_TOKEN_CAP as TOKEN_HARD_CAP
from data_pipeline.token_budget import PREFERRED_TOKEN_BUDGET
from specs.contracts.memory import (
    H200_141GB_BYTES,
    cluster_usable_bytes,
    parameter_bytes,
    would_oom_cluster,
)
from specs.profiles import load_profile

RECIPE_DIR = Path(__file__).resolve().parent / "recipes"
H200_SXM_GPU_TYPE_ID = "NVIDIA H200"
H200_SXM_GPU_COUNT = 8
CPU_GPU_TYPE_ID = "CPU"
PRETRAIN_CONTEXT = 5120
# 70b_scratch only. 100M/7B stay at 5,120. This is still not Phase-5 350k.
LONG_SCRATCH_CONTEXT = 200_000


@dataclass(frozen=True)
class ScratchRecipe:
    name: str
    profile: str
    n_params: int
    n_layers: int
    hidden_size: int
    n_heads: int
    n_kv_heads: int
    head_dim: int
    intermediate_size: int
    vocab_size: int
    context_length: int
    lr: float
    gpu_type_id: str
    gpu_count: int
    zero_stage: int
    smoke_steps: int
    max_steps: int
    micro_batch_size: int
    grad_accum: int
    notes: str
    weight_decay: float = 0.1
    max_tokens: int = PREFERRED_TOKEN_BUDGET
    cpu_offload: bool = False
    disk_offload: bool = False
    checkpoint_every: int = 0
    HARD_TOKEN_CAP: ClassVar[int] = TOKEN_HARD_CAP

    def cluster_bytes(self) -> int:
        # bf16 weights + AdamW fp32 moments, ZeRO-sharded across the node.
        return parameter_bytes(n_params=self.n_params, dtype_bytes=2) + self.n_params * 12

    def fits_node(self) -> bool:
        return not would_oom_cluster(
            self.cluster_bytes(),
            n_gpus=self.gpu_count,
            device_bytes=H200_141GB_BYTES,
        )

    def waste_warning(self) -> str | None:
        usable = cluster_usable_bytes(self.gpu_count, device_bytes=H200_141GB_BYTES)
        used = self.cluster_bytes()
        if self.n_params < 1_000_000_000 and used < 0.05 * usable:
            return (
                f"{self.name} is a 100M-class from-scratch smoke. "
                "It does not need 8x H200; 1x GPU is enough. "
                "Use 70b_scratch only when you intend to occupy the node."
            )
        return None


def _load_yaml(path: Path) -> dict[str, Any]:
    import yaml

    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def list_scratch_recipe_names() -> list[str]:
    return sorted(p.stem for p in RECIPE_DIR.glob("*.yaml"))


def load_scratch_recipe(name: str) -> ScratchRecipe:
    path = RECIPE_DIR / f"{name}.yaml"
    if not path.is_file():
        known = ", ".join(list_scratch_recipe_names()) or "(none)"
        raise FileNotFoundError(f"unknown scratch recipe {name!r}. known: {known}")
    data = _load_yaml(path)
    if str(data.get("init", "random")) != "random":
        raise ValueError(f"{name} must use init: random (from-scratch)")
    if data.get("base_model"):
        raise ValueError(f"{name} is from-scratch; do not set base_model")
    profile = load_profile(str(data["profile"]))
    recipe = ScratchRecipe(
        name=str(data["name"]),
        profile=str(data["profile"]),
        n_params=int(profile["params"]),
        n_layers=int(profile["n_layers"]),
        hidden_size=int(profile["hidden_size"]),
        n_heads=int(profile["n_heads"]),
        n_kv_heads=int(profile["n_kv_heads"]),
        head_dim=int(profile["head_dim"]),
        intermediate_size=int(profile["intermediate_size"]),
        vocab_size=int(profile["vocab_size"]),
        context_length=int(data.get("context_length", profile["context_length"])),
        lr=float(data.get("lr", profile.get("lr", 3.0e-4))),
        gpu_type_id=str(data.get("gpu_type_id", H200_SXM_GPU_TYPE_ID)),
        gpu_count=int(data.get("gpu_count", H200_SXM_GPU_COUNT)),
        zero_stage=int(data.get("zero_stage", 2)),
        smoke_steps=int(data.get("smoke_steps", 10)),
        max_steps=int(data.get("max_steps", 500)),
        micro_batch_size=int(data.get("micro_batch_size", 1)),
        grad_accum=int(data.get("grad_accum", 8)),
        notes=str(data.get("notes") or "").strip(),
        weight_decay=float(data.get("weight_decay", profile.get("weight_decay", 0.1))),
        max_tokens=int(data.get("max_tokens", PREFERRED_TOKEN_BUDGET)),
        cpu_offload=bool(data.get("cpu_offload", False)),
        disk_offload=bool(data.get("disk_offload", False)),
        checkpoint_every=int(data.get("checkpoint_every", 0)),
    )
    if recipe.max_tokens > ScratchRecipe.HARD_TOKEN_CAP:
        raise ValueError(
            f"{name} max_tokens={recipe.max_tokens} exceeds the "
            f"{ScratchRecipe.HARD_TOKEN_CAP} hard cap; "
            f"preferred budget is {PREFERRED_TOKEN_BUDGET} or less"
        )
    if recipe.max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    if recipe.name == "70b_scratch":
        if recipe.context_length != LONG_SCRATCH_CONTEXT:
            raise ValueError(
                "70b_scratch is pinned to 200,000 context (CPU offload). "
                f"got {recipe.context_length}"
            )
        if not recipe.cpu_offload:
            raise ValueError("70b_scratch requires cpu_offload: true at 200k context")
    elif recipe.context_length != PRETRAIN_CONTEXT:
        raise ValueError(
            f"{name} stays at 5,120 context; only 70b_scratch uses 200k"
        )
    is_cpu = recipe.gpu_type_id == CPU_GPU_TYPE_ID
    if is_cpu:
        if not recipe.disk_offload:
            raise ValueError("CPU scratch recipes require disk_offload: true")
        if recipe.gpu_count != 1 or recipe.zero_stage != 0:
            raise ValueError("CPU SSD offload recipes require gpu_count: 1 and zero_stage: 0")
        if recipe.cpu_offload:
            raise ValueError("disk_offload is layer-wise SSD streaming, not DeepSpeed cpu_offload")
    elif recipe.disk_offload:
        raise ValueError("disk_offload requires gpu_type_id: CPU")
    elif recipe.gpu_type_id != H200_SXM_GPU_TYPE_ID or recipe.gpu_count != H200_SXM_GPU_COUNT:
        raise ValueError("scratch recipes must target 8x NVIDIA H200 SXM or 1x CPU with disk_offload")
    if recipe.checkpoint_every < 0:
        raise ValueError("checkpoint_every cannot be negative")
    if not is_cpu and not recipe.fits_node():
        raise ValueError(
            f"{recipe.name} does not fit {recipe.gpu_count}x H200 "
            f"({recipe.cluster_bytes()} bytes)"
        )
    return recipe
