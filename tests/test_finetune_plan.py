"""Fine-tune recipes must fit 8x H200 SXM at 5,120 context."""

from __future__ import annotations

import pytest

from fine_tune.planner import plan_job
from fine_tune.recipes import load_recipe
from specs.contracts.memory import (
    H200_141GB_BYTES,
    RUNPOD_H200_NVL_GPU_TYPE_ID,
    RUNPOD_H200_SXM_GPU_TYPE_ID,
    would_oom_cluster,
)


@pytest.mark.parametrize("name", ["7b_lora", "7b_full", "70b_lora"])
def test_recipe_pins_8x_h200_sxm_and_5k(name: str) -> None:
    recipe = load_recipe(name)
    assert recipe.gpu_type_id == RUNPOD_H200_SXM_GPU_TYPE_ID
    assert recipe.gpu_type_id != RUNPOD_H200_NVL_GPU_TYPE_ID
    assert recipe.gpu_count == 8
    assert recipe.context_length == 5120
    assert recipe.fits_node() is True
    plan = plan_job(recipe)
    assert plan.fits_node is True
    assert plan.trainable_params > 0


def test_7b_lora_warns_that_eight_gpus_are_oversized() -> None:
    warning = load_recipe("7b_lora").waste_warning()
    assert warning is not None
    assert "1x H200" in warning


def test_70b_lora_is_the_recipe_that_needs_the_node() -> None:
    recipe = load_recipe("70b_lora")
    assert recipe.waste_warning() is None
    assert recipe.method == "lora"
    assert recipe.trainable_params() < recipe.n_params / 10


def test_200b_full_ft_does_not_fit_8x_h200() -> None:
    # 200B × 2 bytes weights + 12 bytes Adam ≈ 2.6 TB. 8×141GB is ~1 TB usable.
    n_params = 200_000_000_000
    requested = n_params * 2 + n_params * 12
    assert would_oom_cluster(
        requested, n_gpus=8, device_bytes=H200_141GB_BYTES
    ) is True


def test_7b_full_fits_8x_h200() -> None:
    recipe = load_recipe("7b_full")
    assert recipe.method == "full"
    assert would_oom_cluster(
        recipe.cluster_bytes(), n_gpus=8, device_bytes=H200_141GB_BYTES
    ) is False


def test_70b_qlora_fits_2x_a40() -> None:
    recipe = load_recipe("70b_qlora_a40")
    assert recipe.gpu_type_id == "NVIDIA A40"
    assert recipe.gpu_count == 2
    assert recipe.weight_bits == 4
    assert recipe.fits_node() is True
    plan = plan_job(recipe)
    assert plan.fits_node is True


def test_70b_qlora_fits_3x_a40() -> None:
    recipe = load_recipe("70b_qlora_a40_3x")
    assert recipe.gpu_count == 3
    assert recipe.fits_node() is True
