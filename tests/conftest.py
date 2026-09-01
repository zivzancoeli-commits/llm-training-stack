"""Shared Llama-like fixtures. No GPU, no torch."""

from __future__ import annotations

import pytest

from model.tensor_config import TensorView
from model.transformer_block import BlockConfig, TransformerBlock


# (name, n_layers, n_heads, n_kv_heads, head_dim, intermediate, context)
_PROFILES = {
    "100m": dict(
        n_layers=12,
        n_heads=12,
        n_kv_heads=12,
        head_dim=64,
        intermediate_size=2048,
        context_length=5120,
    ),
    "7b": dict(
        n_layers=32,
        n_heads=32,
        n_kv_heads=8,
        head_dim=128,
        intermediate_size=11008,
        context_length=5120,
    ),
    "70b": dict(
        n_layers=80,
        n_heads=64,
        n_kv_heads=8,
        head_dim=128,
        intermediate_size=28672,
        context_length=5120,
    ),
    "200b": dict(
        n_layers=82,
        n_heads=112,
        n_kv_heads=8,
        head_dim=128,
        intermediate_size=35840,
        context_length=5120,
    ),
}


@pytest.fixture(params=list(_PROFILES))
def profile_name(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture
def block_config(profile_name: str) -> BlockConfig:
    kwargs = dict(_PROFILES[profile_name])
    return BlockConfig(layer_index=0, **kwargs)


@pytest.fixture
def block(block_config: BlockConfig) -> TransformerBlock:
    return TransformerBlock(block_config)


class EchoFlashAttention:
    """Mock FA-3: returns a TensorView with Q's shape, no scores."""

    def __call__(
        self,
        q: TensorView,
        k: TensorView,
        v: TensorView,
        *,
        causal: bool = True,
    ) -> TensorView:
        del k, v, causal
        return TensorView(shape=q.shape, dtype=q.dtype)
