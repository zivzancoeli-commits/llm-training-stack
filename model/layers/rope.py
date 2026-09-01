"""RoPE configuration hook (no rotation kernel).

5,120-context phases use the base theta below. The 200B 350k-context
phase must *not* silently reuse that theta; a YaRN / NTK-aware scale
belongs in a later implementation of ``extend_theta``.
"""

from __future__ import annotations

from dataclasses import dataclass

PRETRAIN_CONTEXT = 5120
LONG_CONTEXT = 350208
DEFAULT_THETA = 10_000.0


@dataclass(frozen=True)
class RopeConfig:
    head_dim: int
    context_length: int = PRETRAIN_CONTEXT
    theta: float = DEFAULT_THETA

    def __post_init__(self) -> None:
        if self.head_dim % 2 != 0:
            raise ValueError("RoPE head_dim must be even")
        if self.context_length <= 0:
            raise ValueError("context_length must be positive")
        if self.theta <= 0:
            raise ValueError("theta must be positive")

    def extend_theta(self, new_context_length: int) -> RopeConfig:
        """Return a config for a longer context.

        The scale rule is deferred. Calling this with ``350208`` during
        Phases 0–4 should be treated as a mistake by the training entry
        point (not implemented here).
        """
        raise NotImplementedError(
            "Long-context RoPE scaling (YaRN/NTK) is deferred to Phase 5"
        )
