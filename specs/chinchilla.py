"""Chinchilla compute/token constraints (Hoffmann et al., 2022).

We use the public rule of thumb ``tokens ≈ 20 * params`` as the *compute-optimal*
token count. This project deliberately **under-trains** the 70B and 200B runs
relative to that line so the ladder stays cheap until the 200B phase. Small
models spend their limited tokens on a reasoning-heavy mix instead of extra
web crawl (see SCALING_MANIFEST.md).
"""

from __future__ import annotations

# Hoffmann et al. compute-optimal ratio (tokens per parameter), rounded.
CHINCHILLA_TOKENS_PER_PARAM = 20

# FLOPs ≈ 6 * N * D for a dense transformer (Kaplan / Hoffmann approximation).
FLOPS_PER_PARAM_PER_TOKEN = 6


def chinchilla_tokens(n_params: int) -> int:
    if n_params <= 0:
        raise ValueError("n_params must be positive")
    return CHINCHILLA_TOKENS_PER_PARAM * n_params


def estimated_training_flops(n_params: int, n_tokens: int) -> int:
    if n_params <= 0 or n_tokens <= 0:
        raise ValueError("n_params and n_tokens must be positive")
    return FLOPS_PER_PARAM_PER_TOKEN * n_params * n_tokens


def tokens_vs_chinchilla(n_params: int, n_tokens: int) -> float:
    """Return ``planned_tokens / chinchilla_tokens``. <1 means under-trained."""
    return n_tokens / chinchilla_tokens(n_params)
