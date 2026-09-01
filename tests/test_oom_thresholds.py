"""OOM tripwires via mock allocations. No CUDA, no real malloc of S×S scores."""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from specs.contracts.memory import (
    H100_80GB_BYTES,
    flash_attention_workspace_bytes,
    naive_attention_score_bytes,
    project_training_footprint,
    would_oom,
)

pytestmark = pytest.mark.oom

# 200B GQA head count from the Phase 4 profile.
HEADS_200B = 112
HEAD_DIM_200B = 128
SEQ_5K = 5120
SEQ_350K = 350208


@dataclass
class MockDevice:
    """Stand-in for a single 80GB GPU allocator."""

    capacity_bytes: int = H100_80GB_BYTES
    used: int = 0
    allocations: list[int] = field(default_factory=list)

    def alloc(self, n_bytes: int) -> None:
        if n_bytes < 0:
            raise ValueError("n_bytes must be non-negative")
        if would_oom(self.used + n_bytes, device_bytes=self.capacity_bytes):
            raise MemoryError(
                f"OOM: {self.used + n_bytes} bytes requested, "
                f"capacity={self.capacity_bytes}"
            )
        self.used += n_bytes
        self.allocations.append(n_bytes)


def test_would_oom_respects_ninety_percent_safety_margin() -> None:
    cap = H100_80GB_BYTES
    assert would_oom(int(cap * 0.90) + 1, device_bytes=cap) is True
    assert would_oom(int(cap * 0.90), device_bytes=cap) is False
    assert would_oom(0, device_bytes=cap) is False


def test_naive_350k_scores_trip_single_gpu_oom() -> None:
    """Materializing (B, H, 350208, 350208) bf16 scores must be refused."""
    bytes_350k = naive_attention_score_bytes(
        batch=1, n_heads=HEADS_200B, seq=SEQ_350K, dtype_bytes=2
    )
    device = MockDevice()
    with pytest.raises(MemoryError, match="OOM"):
        device.alloc(bytes_350k)
    # Sanity: this is hundreds of terabytes, not a rounding error.
    assert bytes_350k > 100 * H100_80GB_BYTES


def test_naive_5k_scores_fit_on_80gb_for_small_head_count() -> None:
    """5,120 context with a 100M-style 12 heads is the cheap path."""
    bytes_5k = naive_attention_score_bytes(batch=1, n_heads=12, seq=SEQ_5K, dtype_bytes=2)
    device = MockDevice()
    device.alloc(bytes_5k)  # must not raise
    assert device.used == bytes_5k
    assert would_oom(bytes_5k) is False


def test_flash_workspace_is_linear_in_seq_not_quadratic() -> None:
    short = flash_attention_workspace_bytes(
        batch=1, n_heads=HEADS_200B, seq=SEQ_5K, head_dim=HEAD_DIM_200B
    )
    long = flash_attention_workspace_bytes(
        batch=1, n_heads=HEADS_200B, seq=SEQ_350K, head_dim=HEAD_DIM_200B
    )
    naive_long = naive_attention_score_bytes(
        batch=1, n_heads=HEADS_200B, seq=SEQ_350K
    )
    ratio = long / short
    seq_ratio = SEQ_350K / SEQ_5K
    # Linear in seq: ratio ≈ 350208/5120 ≈ 68.4, not ≈ 68.4².
    assert ratio == pytest.approx(seq_ratio, rel=0.15)
    assert long < naive_long
    # Naive scores are ~ S/(3D) ≈ 900× the FA workspace at 350k / d=128.
    assert naive_long / long > 500


def test_flash_350k_workspace_fits_80gb_scores_path_alone() -> None:
    """FA-3 working set for QKV at 350k fits; naive scores do not.

    This does *not* claim a 200B training step fits on one GPU. It claims
    the attention *workspace* is no longer the seq² bomb. Parameter memory
    is tested separately.
    """
    flash = flash_attention_workspace_bytes(
        batch=1, n_heads=HEADS_200B, seq=SEQ_350K, head_dim=HEAD_DIM_200B
    )
    device = MockDevice()
    device.alloc(flash)  # must not raise
    assert would_oom(flash) is False


def test_200b_parameter_memory_alone_exceeds_one_80gb_gpu() -> None:
    """Forces TP/PP/ZeRO: 200B × 2 bytes = 400GB weights."""
    footprint = project_training_footprint(
        n_params=200_000_000_000,
        batch=1,
        seq=SEQ_5K,
        n_layers=82,
        n_heads=HEADS_200B,
        head_dim=HEAD_DIM_200B,
    )
    device = MockDevice()
    with pytest.raises(MemoryError):
        device.alloc(footprint.parameters)
    assert footprint.parameters == 200_000_000_000 * 2


def test_7b_flash_5k_microbatch_fits_80gb_under_pessimistic_single_rank() -> None:
    """7B + AdamW moments + FA workspace + checkpointed activations, 5k ctx.

    Pessimistic: optimizer states are *not* ZeRO-sharded in this estimate.
    7B × 2 bytes params + 2× that in moments still fits 80GB; this is why
    Phase 2 is allowed on 8×80GB with ZeRO-2 rather than Megatron TP.
    Stretching that same 7B to 350k with *naive* scores must still trip OOM
    — that is the cost argument for keeping 5,120 until 200B.
    """
    at_5k = project_training_footprint(
        n_params=7_000_000_000,
        batch=1,
        seq=SEQ_5K,
        n_layers=32,
        n_heads=32,
        head_dim=128,
    )
    at_350k = project_training_footprint(
        n_params=7_000_000_000,
        batch=1,
        seq=SEQ_350K,
        n_layers=32,
        n_heads=32,
        head_dim=128,
    )
    assert would_oom(at_5k.flash_total) is False
    assert would_oom(at_5k.naive_total) is False
    assert would_oom(at_350k.naive_total) is True
    assert would_oom(at_350k.flash_total) is False


def test_mock_allocator_records_successful_grants() -> None:
    device = MockDevice(capacity_bytes=1024)
    device.alloc(100)
    device.alloc(200)
    assert device.used == 300
    assert device.allocations == [100, 200]
    with pytest.raises(MemoryError):
        device.alloc(800)  # 300+800=1100 > 0.9*1024
