"""Turn a recipe into a launch plan (no network)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from fine_tune.recipes import FineTuneRecipe


@dataclass(frozen=True)
class FineTunePlan:
    recipe: FineTuneRecipe
    fits_node: bool
    cluster_bytes: int
    trainable_params: int
    waste_warning: str | None
    smoke: bool

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["recipe"] = asdict(self.recipe)
        return payload


def plan_job(recipe: FineTuneRecipe, *, smoke: bool = True) -> FineTunePlan:
    if recipe.context_length != 5120:
        raise ValueError("fine-tune context must stay 5120")
    if not recipe.fits_node():
        raise ValueError(
            f"{recipe.name} does not fit {recipe.gpu_count}x {recipe.gpu_type_id} "
            f"({recipe.cluster_bytes()} bytes requested)"
        )
    return FineTunePlan(
        recipe=recipe,
        fits_node=True,
        cluster_bytes=recipe.cluster_bytes(),
        trainable_params=recipe.trainable_params(),
        waste_warning=recipe.waste_warning(),
        smoke=smoke,
    )
