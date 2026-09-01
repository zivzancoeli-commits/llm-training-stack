"""Typed fine-tune recipes. YAML under ``recipes/`` is the human copy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from specs.contracts.memory import (
    A40_48GB_BYTES,
    H200_141GB_BYTES,
    RUNPOD_H200_SXM_GPU_TYPE_ID,
    cluster_usable_bytes,
    lora_cluster_bytes,
    lora_trainable_params,
    parameter_bytes,
    would_oom_cluster,
)

Method = Literal["lora", "full"]
PRETRAIN_CONTEXT = 5120
RECIPE_DIR = Path(__file__).resolve().parent / "recipes"

# RunPod's SXM H200 SKU id. "NVIDIA H200 NVL" is a different card.
H200_SXM_GPU_TYPE_ID = RUNPOD_H200_SXM_GPU_TYPE_ID
H200_SXM_GPU_COUNT = 8
H200_SXM_GIB = 141
A40_GPU_TYPE_ID = "NVIDIA A40"
A40_QLORA_GPU_COUNTS = (2, 3)


@dataclass(frozen=True)
class FineTuneRecipe:
    """One fine-tune job. Context stays 5,120 — this is not Phase 5."""

    name: str
    base_model: str
    n_params: int
    n_layers: int
    hidden_size: int
    method: Method
    context_length: int = PRETRAIN_CONTEXT
    gpu_type_id: str = H200_SXM_GPU_TYPE_ID
    gpu_count: int = H200_SXM_GPU_COUNT
    zero_stage: int = 2
    lora_rank: int = 16
    learning_rate: float = 2.0e-4
    smoke_steps: int = 10
    max_steps: int = 500
    micro_batch_size: int = 1
    grad_accum: int = 8
    notes: str = ""
    weight_bits: int = 16

    def device_bytes(self) -> int:
        if self.gpu_type_id == H200_SXM_GPU_TYPE_ID:
            return H200_141GB_BYTES
        if self.gpu_type_id == A40_GPU_TYPE_ID:
            return A40_48GB_BYTES
        raise ValueError(f"unsupported gpu_type_id {self.gpu_type_id!r}")

    def trainable_params(self) -> int:
        if self.method == "full":
            return self.n_params
        return lora_trainable_params(
            n_layers=self.n_layers,
            hidden_size=self.hidden_size,
            rank=self.lora_rank,
        )

    def cluster_bytes(self) -> int:
        if self.method == "lora":
            return lora_cluster_bytes(
                n_params=self.n_params,
                n_trainable=self.trainable_params(),
                dtype_bytes=self.weight_bits / 8,
            )
        # Full FT: bf16 weights + AdamW fp32 moments (12 bytes / param) sharded.
        return parameter_bytes(n_params=self.n_params, dtype_bytes=2) + self.n_params * 12

    def fits_node(self) -> bool:
        return not would_oom_cluster(
            self.cluster_bytes(),
            n_gpus=self.gpu_count,
            device_bytes=self.device_bytes(),
        )

    def waste_warning(self) -> str | None:
        """7B LoRA on 8x H200 is valid but oversized — say so before launch."""
        usable = cluster_usable_bytes(self.gpu_count, device_bytes=self.device_bytes())
        used = self.cluster_bytes()
        if used < 0.15 * usable and self.method == "lora" and self.n_params < 20_000_000_000:
            return (
                f"{self.name} uses ~{used / 1024**3:.1f} GiB of "
                f"{usable / 1024**3:.0f} GiB usable on 8x H200. "
                "That is fine, but 1x H200 would also fit. "
                "Use recipe 7b_full or 70b_lora if you want these GPUs busy."
            )
        return None


def _load_yaml(path: Path) -> dict[str, Any]:
    import yaml

    with path.open() as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def recipe_from_mapping(data: dict[str, Any]) -> FineTuneRecipe:
    return FineTuneRecipe(
        name=str(data["name"]),
        base_model=str(data["base_model"]),
        n_params=int(data["n_params"]),
        n_layers=int(data["n_layers"]),
        hidden_size=int(data["hidden_size"]),
        method=data["method"],
        context_length=int(data.get("context_length", PRETRAIN_CONTEXT)),
        gpu_type_id=str(data.get("gpu_type_id", H200_SXM_GPU_TYPE_ID)),
        gpu_count=int(data.get("gpu_count", H200_SXM_GPU_COUNT)),
        zero_stage=int(data.get("zero_stage", 2)),
        lora_rank=int(data.get("lora_rank", 16)),
        learning_rate=float(data.get("learning_rate", 2.0e-4)),
        smoke_steps=int(data.get("smoke_steps", 10)),
        max_steps=int(data.get("max_steps", 500)),
        micro_batch_size=int(data.get("micro_batch_size", 1)),
        grad_accum=int(data.get("grad_accum", 8)),
        notes=str(data.get("notes") or "").strip(),
        weight_bits=int(data.get("weight_bits", 16)),
    )


def list_recipe_names() -> list[str]:
    return sorted(p.stem for p in RECIPE_DIR.glob("*.yaml"))


def load_recipe(name: str) -> FineTuneRecipe:
    path = RECIPE_DIR / f"{name}.yaml"
    if not path.is_file():
        known = ", ".join(list_recipe_names()) or "(none)"
        raise FileNotFoundError(f"unknown recipe {name!r}. known: {known}")
    recipe = recipe_from_mapping(_load_yaml(path))
    if recipe.context_length != PRETRAIN_CONTEXT:
        raise ValueError(
            f"recipe {name} has context_length={recipe.context_length}; "
            f"fine-tunes stay at {PRETRAIN_CONTEXT} until Phase 5"
        )
    if recipe.gpu_type_id == "NVIDIA H200 NVL":
        raise ValueError("this stack pins H200 SXM, not H200 NVL")
    if recipe.gpu_type_id == H200_SXM_GPU_TYPE_ID:
        if recipe.gpu_count != H200_SXM_GPU_COUNT:
            raise ValueError(f"H200 recipes pin {H200_SXM_GPU_COUNT}x H200 SXM")
        if recipe.weight_bits != 16:
            raise ValueError("H200 recipes stay bf16 (weight_bits=16)")
    elif recipe.gpu_type_id == A40_GPU_TYPE_ID:
        if recipe.gpu_count not in A40_QLORA_GPU_COUNTS:
            raise ValueError("A40 QLoRA recipes pin 2x or 3x NVIDIA A40")
        if recipe.method != "lora" or recipe.weight_bits != 4:
            raise ValueError("A40 recipes are 4-bit LoRA (QLoRA), not full FT")
    else:
        raise ValueError(f"unsupported gpu_type_id {recipe.gpu_type_id!r}")
    if recipe.method not in ("lora", "full"):
        raise ValueError(f"unsupported method {recipe.method!r}")
    return recipe
