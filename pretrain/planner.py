"""Plan a from-scratch job (no network, no torch)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from data_pipeline.token_budget import HARD_TOKEN_CAP, PREFERRED_TOKEN_BUDGET
from pretrain.recipes import ScratchRecipe


@dataclass(frozen=True)
class ScratchPlan:
    recipe: ScratchRecipe
    fits_node: bool
    cluster_bytes: int
    smoke: bool
    max_tokens: int
    waste_warning: str | None
    init: str = "random"
    base_model: None = None
    preferred_tokens: int = PREFERRED_TOKEN_BUDGET
    hard_token_cap: int = HARD_TOKEN_CAP

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["recipe"] = asdict(self.recipe)
        return payload


def plan_scratch(recipe: ScratchRecipe, *, smoke: bool = True) -> ScratchPlan:
    if not recipe.disk_offload and not recipe.fits_node():
        raise ValueError(f"{recipe.name} does not fit 8x H200")
    return ScratchPlan(
        recipe=recipe,
        fits_node=True,
        cluster_bytes=recipe.cluster_bytes(),
        smoke=smoke,
        max_tokens=recipe.max_tokens,
        waste_warning=recipe.waste_warning(),
        preferred_tokens=PREFERRED_TOKEN_BUDGET,
        hard_token_cap=HARD_TOKEN_CAP,
    )
