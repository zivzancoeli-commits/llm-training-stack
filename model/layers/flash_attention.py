"""FlashAttention-3 *hooks* — call signatures, not the kernel.

A later CUDA/Triton implementation must satisfy ``FlashAttention3Hook``
and must preserve the shapes in ``specs.contracts.attention_shapes``.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from model.tensor_config import TensorView


@runtime_checkable
class FlashAttention3Hook(Protocol):
    """Drop-in attention kernel with GQA + causal masking.

    Implementations must:

    - accept Q at ``(B, H, S, D)`` and K/V at ``(B, H_kv, S, D)``
    - return context at ``(B, H, S, D)`` (same as Q)
    - never return a materialized ``(B, H, S, S)`` score tensor
    """

    def __call__(
        self,
        q: TensorView,
        k: TensorView,
        v: TensorView,
        *,
        causal: bool = True,
    ) -> TensorView: ...


class FlashAttention3NotImplemented:
    """Default hook installed on every ``TransformerBlock`` in this scaffold."""

    def __call__(
        self,
        q: TensorView,
        k: TensorView,
        v: TensorView,
        *,
        causal: bool = True,
    ) -> TensorView:
        del k, v, causal
        raise NotImplementedError(
            "FlashAttention-3 kernel is not part of this scaffold. "
            "Swap in a hook that returns a TensorView with shape == q.shape."
        )
