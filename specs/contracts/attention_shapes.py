"""Shape contracts across a Llama-like self-attention boundary.

These tuples are the only "implementation" allowed at scaffold time: they
define what every later kernel (FlashAttention-3, a PyTorch SDPA fallback,
Megatron fused attention) must accept and return.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AttentionBoundaryShapes:
    """Named shapes at each hop of pre-attention → scores → context → output.

    Layout is ``(batch, heads, seq, head_dim)`` for Q/K/V/context and
    ``(batch, seq, hidden)`` for the residual-stream projection.
    """

    q: tuple[int, int, int, int]
    k: tuple[int, int, int, int]
    v: tuple[int, int, int, int]
    q_after_gqa_repeat: tuple[int, int, int, int]
    k_after_gqa_repeat: tuple[int, int, int, int]
    v_after_gqa_repeat: tuple[int, int, int, int]
    scores_if_materialized: tuple[int, int, int, int]
    context: tuple[int, int, int, int]
    projected: tuple[int, int, int]


def validate_head_config(*, n_heads: int, n_kv_heads: int, head_dim: int) -> None:
    """Reject GQA / MHA configs that cannot legally tile."""
    if n_heads <= 0 or n_kv_heads <= 0 or head_dim <= 0:
        raise ValueError("n_heads, n_kv_heads, and head_dim must be positive")
    if n_heads % n_kv_heads != 0:
        raise ValueError(
            f"n_heads ({n_heads}) must be divisible by n_kv_heads ({n_kv_heads}) for GQA"
        )
    if head_dim % 8 != 0:
        raise ValueError("head_dim should be a multiple of 8 for FlashAttention alignment")


def hidden_size(*, n_heads: int, head_dim: int) -> int:
    return n_heads * head_dim


def attention_boundary_shapes(
    *,
    batch: int,
    seq: int,
    n_heads: int,
    n_kv_heads: int,
    head_dim: int,
) -> AttentionBoundaryShapes:
    """Return every tensor shape that crosses the self-attention boundary.

    Grouped-query attention keeps K/V on ``n_kv_heads`` until a repeat
    (or an implicit FA-3 GQA path) expands them to ``n_heads``. FlashAttention-3
    must not change ``seq`` or ``head_dim``.
    """
    validate_head_config(n_heads=n_heads, n_kv_heads=n_kv_heads, head_dim=head_dim)
    if batch <= 0 or seq <= 0:
        raise ValueError("batch and seq must be positive")

    hidden = hidden_size(n_heads=n_heads, head_dim=head_dim)
    q = (batch, n_heads, seq, head_dim)
    k = (batch, n_kv_heads, seq, head_dim)
    v = (batch, n_kv_heads, seq, head_dim)
    k_rep = (batch, n_heads, seq, head_dim)
    v_rep = (batch, n_heads, seq, head_dim)
    scores = (batch, n_heads, seq, seq)
    context = (batch, n_heads, seq, head_dim)
    projected = (batch, seq, hidden)
    return AttentionBoundaryShapes(
        q=q,
        k=k,
        v=v,
        q_after_gqa_repeat=q,
        k_after_gqa_repeat=k_rep,
        v_after_gqa_repeat=v_rep,
        scores_if_materialized=scores,
        context=context,
        projected=projected,
    )
