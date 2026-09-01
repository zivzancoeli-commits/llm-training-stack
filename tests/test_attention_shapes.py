"""Shape contracts across the self-attention boundary.

These tests mock FlashAttention-3. They never allocate an (S, S) score
tensor. If a future kernel returns the wrong rank, this file is the
failure you want *before* a cluster job.
"""

from __future__ import annotations

import pytest

from model.layers.flash_attention import FlashAttention3NotImplemented
from model.tensor_config import TensorView
from model.transformer_block import BlockConfig, TransformerBlock
from specs.contracts.attention_shapes import attention_boundary_shapes
from tests.conftest import EchoFlashAttention

pytestmark = pytest.mark.shape


def test_qkv_ranks_match_gqa_contract(block: TransformerBlock) -> None:
    shapes = block.attention_boundary_shapes(batch=2)
    cfg = block.config
    assert shapes.q == (2, cfg.n_heads, cfg.context_length, cfg.head_dim)
    assert shapes.k == (2, cfg.n_kv_heads, cfg.context_length, cfg.head_dim)
    assert shapes.v == shapes.k


def test_gqa_repeat_expands_kv_heads_only(block: TransformerBlock) -> None:
    shapes = block.attention_boundary_shapes(batch=1)
    assert shapes.k[1] == block.config.n_kv_heads
    assert shapes.k_after_gqa_repeat[1] == block.config.n_heads
    assert shapes.k_after_gqa_repeat[2] == shapes.k[2]  # seq unchanged
    assert shapes.k_after_gqa_repeat[3] == shapes.k[3]  # head_dim unchanged


def test_materialized_scores_are_square_in_seq(block: TransformerBlock) -> None:
    shapes = block.attention_boundary_shapes(batch=1, seq=5120)
    b, h, s, s2 = shapes.scores_if_materialized
    assert b == 1
    assert h == block.config.n_heads
    assert s == s2 == 5120


def test_projected_output_rejoins_residual_stream(block: TransformerBlock) -> None:
    batch = 3
    shapes = block.attention_boundary_shapes(batch=batch)
    residual = block.residual_stream_shape(batch)
    assert shapes.projected == residual
    assert residual[2] == block.config.n_heads * block.config.head_dim


def test_context_length_only_changes_seq_axis(block: TransformerBlock) -> None:
    short = block.attention_boundary_shapes(batch=1, seq=5120)
    # 350k is illegal for Phases 0–4 *training*, but the shape function
    # must still be consistent: only the seq axis moves.
    long = block.attention_boundary_shapes(batch=1, seq=350208)
    assert short.q[0] == long.q[0]
    assert short.q[1] == long.q[1]
    assert short.q[3] == long.q[3]
    assert short.q[2] == 5120
    assert long.q[2] == 350208
    assert long.scores_if_materialized[2:] == (350208, 350208)


def test_mock_fa3_preserves_q_shape_and_never_returns_scores(
    block_config: BlockConfig,
) -> None:
    block = TransformerBlock(block_config, flash_attn_3=EchoFlashAttention())
    # seq must not equal head_dim, or (B,H,S,S) scores alias (B,H,S,D) context.
    expected = block.attention_boundary_shapes(batch=2, seq=256)
    q = TensorView(expected.q)
    k = TensorView(expected.k)
    v = TensorView(expected.v)
    out = block.apply_attention(q, k, v, causal=True)
    assert out.shape == expected.context
    assert out.shape[2:] == (256, block_config.head_dim)
    assert expected.scores_if_materialized[2:] == (256, 256)
    assert out.shape != expected.scores_if_materialized
    assert out.ndim == 4


def test_apply_attention_rejects_wrong_kv_rank(block_config: BlockConfig) -> None:
    block = TransformerBlock(block_config, flash_attn_3=EchoFlashAttention())
    expected = block.attention_boundary_shapes(batch=1, seq=64)
    q = TensorView(expected.q)
    # Wrong seq on K (works for both MHA and GQA).
    bad_k = TensorView((expected.k[0], expected.k[1], expected.k[2] + 1, expected.k[3]))
    v = TensorView(expected.v)
    with pytest.raises(ValueError, match="K shape"):
        block.apply_attention(q, bad_k, v)


def test_default_fa3_hook_is_explicitly_unimplemented(block: TransformerBlock) -> None:
    assert isinstance(block.flash_attn_3, FlashAttention3NotImplemented)
    expected = block.attention_boundary_shapes(batch=1, seq=16)
    with pytest.raises(NotImplementedError, match="FlashAttention-3"):
        block.apply_attention(
            TensorView(expected.q),
            TensorView(expected.k),
            TensorView(expected.v),
        )


def test_n_heads_must_divide_into_kv_heads() -> None:
    with pytest.raises(ValueError, match="divisible"):
        BlockConfig(
            layer_index=0,
            n_layers=4,
            n_heads=12,
            n_kv_heads=5,
            head_dim=64,
            intermediate_size=256,
        )


def test_free_function_matches_block_method() -> None:
    cfg = BlockConfig(
        layer_index=3,
        n_layers=32,
        n_heads=32,
        n_kv_heads=8,
        head_dim=128,
        intermediate_size=11008,
        context_length=5120,
    )
    block = TransformerBlock(cfg)
    via_block = block.attention_boundary_shapes(batch=4, seq=256)
    via_spec = attention_boundary_shapes(
        batch=4, seq=256, n_heads=32, n_kv_heads=8, head_dim=128
    )
    assert via_block == via_spec
