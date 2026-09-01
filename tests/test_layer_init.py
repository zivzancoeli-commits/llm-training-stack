"""Layer initialization stds from GPT-2 residual scaling and µP width scaling."""

from __future__ import annotations

import math

import pytest

from model.transformer_block import BlockConfig, TransformerBlock
from specs.contracts.initialization import (
    attention_logit_scale,
    embedding_std,
    gpt2_residual_out_std,
    mup_linear_std,
)

pytestmark = pytest.mark.init


def test_embedding_std_is_base() -> None:
    assert embedding_std() == pytest.approx(0.02)
    assert embedding_std(0.01) == pytest.approx(0.01)


def test_residual_out_std_shrinks_with_depth() -> None:
    proxy = gpt2_residual_out_std(12)
    seven = gpt2_residual_out_std(32)
    seventy = gpt2_residual_out_std(80)
    two_hundred = gpt2_residual_out_std(82)
    assert proxy == pytest.approx(0.02 / math.sqrt(24))
    assert seven < proxy
    assert seventy < seven
    # 82 vs 80 is a small step; still strictly smaller.
    assert two_hundred < seventy


def test_mup_linear_std_is_fan_in_scaled() -> None:
    narrow = mup_linear_std(768)
    wide = mup_linear_std(14336)
    assert narrow == pytest.approx(1.0 / math.sqrt(768))
    assert wide == pytest.approx(1.0 / math.sqrt(14336))
    assert wide < narrow


def test_attention_logit_scale_is_inv_sqrt_head_dim() -> None:
    assert attention_logit_scale(64) == pytest.approx(1.0 / 8.0)
    assert attention_logit_scale(128) == pytest.approx(1.0 / math.sqrt(128))


def test_block_profile_uses_residual_scaling_on_output_projections(
    block: TransformerBlock,
) -> None:
    profile = block.init_stds()
    expected_residual = gpt2_residual_out_std(block.config.n_layers)
    assert profile.attn_out == pytest.approx(expected_residual)
    assert profile.mlp_down == pytest.approx(expected_residual)
    # Input-side matrices follow µP, not the residual rule.
    assert profile.qkv == pytest.approx(mup_linear_std(block.config.hidden_size))
    assert profile.mlp_up == pytest.approx(mup_linear_std(block.config.hidden_size))
    assert profile.mlp_gate == pytest.approx(profile.mlp_up)
    assert profile.embedding == pytest.approx(0.02)
    assert profile.attention_logit_scale == pytest.approx(
        attention_logit_scale(block.config.head_dim)
    )


def test_deeper_block_has_smaller_output_std_than_proxy() -> None:
    proxy = TransformerBlock(
        BlockConfig(
            layer_index=0,
            n_layers=12,
            n_heads=12,
            n_kv_heads=12,
            head_dim=64,
            intermediate_size=2048,
        )
    )
    deep = TransformerBlock(
        BlockConfig(
            layer_index=0,
            n_layers=80,
            n_heads=64,
            n_kv_heads=8,
            head_dim=128,
            intermediate_size=28672,
        )
    )
    assert deep.init_stds().attn_out < proxy.init_stds().attn_out
    # Width also moves qkv std down (µP) from 768 → 8192.
    assert deep.init_stds().qkv < proxy.init_stds().qkv


def test_rejects_non_positive_depth() -> None:
    with pytest.raises(ValueError):
        gpt2_residual_out_std(0)
    with pytest.raises(ValueError):
        mup_linear_std(0)
