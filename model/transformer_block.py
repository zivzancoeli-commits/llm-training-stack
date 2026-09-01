"""Llama-like transformer block blueprint (skeleton).

Structure, in order (no kernels yet):

1. RMSNorm
2. QKV (GQA) + RoPE
3. FlashAttention-3 hook
4. Output projection + residual
5. RMSNorm
6. SwiGLU MLP + residual

Forward is intentionally unimplemented. Shape, init, and MP/PP map
methods are implemented because they are *contracts*, not algorithms.
"""

from __future__ import annotations

from dataclasses import dataclass

from model.layers.flash_attention import FlashAttention3Hook, FlashAttention3NotImplemented
from model.layers.rope import RopeConfig
from model.tensor_config import LayerMap, ParallelLayout, TensorView
from specs.contracts.attention_shapes import (
    AttentionBoundaryShapes,
    attention_boundary_shapes,
    hidden_size,
    validate_head_config,
)
from specs.contracts.initialization import InitStdProfile, init_std_profile


@dataclass(frozen=True)
class BlockConfig:
    layer_index: int
    n_layers: int
    n_heads: int
    n_kv_heads: int
    head_dim: int
    intermediate_size: int
    context_length: int = 5120

    @property
    def hidden_size(self) -> int:
        return hidden_size(n_heads=self.n_heads, head_dim=self.head_dim)

    def __post_init__(self) -> None:
        if self.layer_index < 0 or self.layer_index >= self.n_layers:
            raise ValueError("layer_index out of range")
        validate_head_config(
            n_heads=self.n_heads, n_kv_heads=self.n_kv_heads, head_dim=self.head_dim
        )
        if self.intermediate_size <= 0:
            raise ValueError("intermediate_size must be positive")
        if self.context_length <= 0:
            raise ValueError("context_length must be positive")


class TransformerBlock:
    """One Llama-like layer with FA-3 and MP/PP maps attached, no math.

    Parameters
    ----------
    config:
        Width / depth / GQA for this layer.
    flash_attn_3:
        Kernel hook. Defaults to a stub that raises ``NotImplementedError``.
    rope:
        RoPE config. Defaults to ``head_dim`` from ``config`` at 5,120.
    """

    def __init__(
        self,
        config: BlockConfig,
        *,
        flash_attn_3: FlashAttention3Hook | None = None,
        rope: RopeConfig | None = None,
    ) -> None:
        self.config = config
        self.flash_attn_3: FlashAttention3Hook = (
            flash_attn_3 if flash_attn_3 is not None else FlashAttention3NotImplemented()
        )
        self.rope = rope if rope is not None else RopeConfig(head_dim=config.head_dim)

    def residual_stream_shape(self, batch: int, seq: int | None = None) -> tuple[int, int, int]:
        """``(batch, seq, hidden)`` entering and leaving the block."""
        seq_len = self.config.context_length if seq is None else seq
        if batch <= 0 or seq_len <= 0:
            raise ValueError("batch and seq must be positive")
        return (batch, seq_len, self.config.hidden_size)

    def attention_boundary_shapes(
        self, batch: int, seq: int | None = None
    ) -> AttentionBoundaryShapes:
        """Shape tuple at every hop of self-attention (see specs.contracts)."""
        seq_len = self.config.context_length if seq is None else seq
        return attention_boundary_shapes(
            batch=batch,
            seq=seq_len,
            n_heads=self.config.n_heads,
            n_kv_heads=self.config.n_kv_heads,
            head_dim=self.config.head_dim,
        )

    def mlp_shapes(
        self, batch: int, seq: int | None = None
    ) -> dict[str, tuple[int, ...]]:
        """SwiGLU in/gate/up/down residual-stream shapes (no activation fn)."""
        stream = self.residual_stream_shape(batch, seq)
        hidden = self.config.hidden_size
        inter = self.config.intermediate_size
        b, s, _ = stream
        return {
            "rms_in": stream,
            "gate": (b, s, inter),
            "up": (b, s, inter),
            "down": stream,
            "w_gate": (inter, hidden),
            "w_up": (inter, hidden),
            "w_down": (hidden, inter),
        }

    def init_stds(self) -> InitStdProfile:
        """Depth- and width-aware init stds for this block's matrices."""
        return init_std_profile(
            n_layers=self.config.n_layers,
            hidden_size=self.config.hidden_size,
            head_dim=self.config.head_dim,
            intermediate_size=self.config.intermediate_size,
        )

    def parallel_layer_map(self, layout: ParallelLayout) -> LayerMap:
        """Place this block on a tensor-parallel × pipeline-parallel grid.

        Layers are split contiguously across PP stages. Attention QKV and
        MLP up/gate are column-parallel; output projections are row-parallel
        (Megatron pairing). No collectives are issued here.
        """
        n_layers = self.config.n_layers
        pp = layout.pipeline_parallel_size
        if n_layers % pp != 0:
            raise ValueError(
                f"n_layers ({n_layers}) must divide pipeline_parallel_size ({pp}) "
                "in this scaffold; uneven PP splits are a later feature"
            )
        layers_per_stage = n_layers // pp
        stage = self.config.layer_index // layers_per_stage
        return LayerMap(
            layer_index=self.config.layer_index,
            pipeline_stage=stage,
            is_first_stage=stage == 0,
            is_last_stage=stage == pp - 1,
            attention_qkv_partition="column",
            attention_out_partition="row",
            mlp_up_partition="column",
            mlp_down_partition="row",
        )

    def apply_attention(
        self,
        q: TensorView,
        k: TensorView,
        v: TensorView,
        *,
        causal: bool = True,
    ) -> TensorView:
        """Call the FA-3 hook after asserting the Q/K/V rank contract."""
        expected = self.attention_boundary_shapes(batch=q.shape[0], seq=q.shape[2])
        if q.shape != expected.q:
            raise ValueError(f"Q shape {q.shape} != {expected.q}")
        if k.shape != expected.k:
            raise ValueError(f"K shape {k.shape} != {expected.k}")
        if v.shape != expected.v:
            raise ValueError(f"V shape {v.shape} != {expected.v}")
        out = self.flash_attn_3(q, k, v, causal=causal)
        if out.shape != expected.context:
            raise ValueError(f"FA-3 output shape {out.shape} != {expected.context}")
        return out

    def forward(self, residual: TensorView) -> TensorView:
        """Full block. Deferred — would call RMSNorm, RoPE, FA-3, SwiGLU."""
        raise NotImplementedError(
            "TransformerBlock.forward is deferred; use attention_boundary_shapes "
            "and apply_attention in tests until a kernel exists"
        )
