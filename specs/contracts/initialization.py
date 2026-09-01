"""Initialization standard deviations from modern residual-scaling practice.

References (formulas only, no kernels):

- GPT-2 residual-output scaling: ``std = base / sqrt(2 * n_layers)`` so the
  residual stream variance stays O(1) as depth grows.
- µP / tensor-program width scaling: linear weights ``~ 1/sqrt(fan_in)`` so
  a learning rate tuned on the 100M proxy can transfer toward 7B / 70B.
- Attention logits: ``1 / sqrt(head_dim)`` (scaled dot-product).
"""

from __future__ import annotations

import math
from dataclasses import dataclass


DEFAULT_EMBED_STD = 0.02
DEFAULT_BASE_LINEAR_STD = 0.02


@dataclass(frozen=True)
class InitStdProfile:
    """Per-matrix target standard deviations for one transformer block."""

    embedding: float
    qkv: float
    attn_out: float
    mlp_up: float
    mlp_gate: float
    mlp_down: float
    attention_logit_scale: float


def embedding_std(base: float = DEFAULT_EMBED_STD) -> float:
    return base


def gpt2_residual_out_std(n_layers: int, base: float = DEFAULT_BASE_LINEAR_STD) -> float:
    """Depth-scaled std for residual *output* projections (W_o, W_down)."""
    if n_layers <= 0:
        raise ValueError("n_layers must be positive")
    return base / math.sqrt(2.0 * n_layers)


def mup_linear_std(fan_in: int) -> float:
    """Width-scaled std for a linear map under maximal-update parameterization."""
    if fan_in <= 0:
        raise ValueError("fan_in must be positive")
    return 1.0 / math.sqrt(fan_in)


def attention_logit_scale(head_dim: int) -> float:
    if head_dim <= 0:
        raise ValueError("head_dim must be positive")
    return 1.0 / math.sqrt(head_dim)


def init_std_profile(
    *,
    n_layers: int,
    hidden_size: int,
    head_dim: int,
    intermediate_size: int,
    base: float = DEFAULT_BASE_LINEAR_STD,
) -> InitStdProfile:
    """Compose embedding, µP-width, and GPT-2 depth rules into one profile."""
    residual = gpt2_residual_out_std(n_layers, base=base)
    return InitStdProfile(
        embedding=embedding_std(base),
        qkv=mup_linear_std(hidden_size),
        attn_out=residual,
        mlp_up=mup_linear_std(hidden_size),
        mlp_gate=mup_linear_std(hidden_size),
        mlp_down=residual,
        attention_logit_scale=attention_logit_scale(head_dim),
    )
