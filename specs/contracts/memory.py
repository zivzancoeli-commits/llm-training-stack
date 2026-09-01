"""Mock-friendly memory contracts. No CUDA, no real allocations.

Used to fail a config in CI before it OOMs a rented node. Two attention
estimates are kept side by side on purpose:

- *Naive* score materialization is ``O(batch * heads * seq^2)`` and is the
  tripwire for 350k context.
- *FlashAttention-3* workspace is ``O(batch * heads * seq * head_dim)`` plus
  a small SRAM tile term. It is still not free at 350k — context-parallel
  / ring attention is required on top, which Phase 5 of the scaling
  manifest is for.
"""

from __future__ import annotations

from dataclasses import dataclass

# NVIDIA markets "80GB" H100/A100 as 80 GiB of HBM.
H100_80GB_BYTES = 80 * (1024**3)
# H200 SXM is 141 GB HBM3e. H200 NVL is a different SKU — do not mix them.
A40_48GB_BYTES = 48 * (1024**3)
H200_141GB_BYTES = 141 * (1024**3)
RUNPOD_H200_SXM_GPU_TYPE_ID = "NVIDIA H200"
RUNPOD_H200_NVL_GPU_TYPE_ID = "NVIDIA H200 NVL"

# Default safety margin: never plan to use more than 90% of device memory.
DEFAULT_SAFETY_MARGIN = 0.90


@dataclass(frozen=True)
class MemoryEstimate:
    """Byte-level breakdown of a *single-GPU* training step footprint."""

    parameters: int
    optimizer_states: int
    naive_attention_scores: int
    flash_workspace: int
    activations_checkpointed: int

    @property
    def naive_total(self) -> int:
        return (
            self.parameters
            + self.optimizer_states
            + self.naive_attention_scores
            + self.activations_checkpointed
        )

    @property
    def flash_total(self) -> int:
        return (
            self.parameters
            + self.optimizer_states
            + self.flash_workspace
            + self.activations_checkpointed
        )


def _numel(shape: tuple[int, ...]) -> int:
    n = 1
    for dim in shape:
        if dim <= 0:
            raise ValueError(f"invalid dim {dim} in {shape}")
        n *= dim
    return n


def naive_attention_score_bytes(
    *,
    batch: int,
    n_heads: int,
    seq: int,
    dtype_bytes: int = 2,
) -> int:
    """HBM cost of materializing the ``(B, H, S, S)`` score tensor."""
    return _numel((batch, n_heads, seq, seq)) * dtype_bytes


def flash_attention_workspace_bytes(
    *,
    batch: int,
    n_heads: int,
    seq: int,
    head_dim: int,
    dtype_bytes: int = 2,
    block_m: int = 128,
    block_n: int = 128,
) -> int:
    """Order-of-magnitude FA-3 HBM working set (Q/K/V + one output tile).

    This is a *contract*, not a vendor-accurate allocator. The block sizes
    match typical FA-3 SRAM tiles so tests can lock the O(seq) scaling.
    """
    qkv = _numel((batch, n_heads, seq, head_dim)) * dtype_bytes * 3
    # One output tile and a small stats buffer; independent of seq^2.
    tile = _numel((batch, n_heads, block_m, head_dim)) * dtype_bytes
    stats = _numel((batch, n_heads, seq)) * 4  # fp32 row max/sum
    _ = block_n  # reserved for a later more precise tile model
    return qkv + tile + stats


def parameter_bytes(*, n_params: int, dtype_bytes: float = 2) -> int:
    if n_params <= 0:
        raise ValueError("n_params must be positive")
    if dtype_bytes <= 0:
        raise ValueError("dtype_bytes must be positive")
    return int(n_params * dtype_bytes)


def project_training_footprint(
    *,
    n_params: int,
    batch: int,
    seq: int,
    n_layers: int,
    n_heads: int,
    head_dim: int,
    dtype_bytes: int = 2,
    optimizer_multiplier: float = 2.0,
    checkpointed_activation_bytes_per_token: int = 64,
) -> MemoryEstimate:
    """Project a single-rank training footprint.

    ``optimizer_multiplier`` defaults to 2.0 for AdamW in bf16 params +
    fp32 moments *sharded away* is *not* assumed here: this is the
    pessimistic single-GPU number. Parallel plans (ZeRO / TP / PP) must
    divide these totals explicitly in a later infra config.
    """
    params = parameter_bytes(n_params=n_params, dtype_bytes=dtype_bytes)
    opt = int(params * optimizer_multiplier)
    naive = naive_attention_score_bytes(
        batch=batch, n_heads=n_heads, seq=seq, dtype_bytes=dtype_bytes
    )
    flash = flash_attention_workspace_bytes(
        batch=batch,
        n_heads=n_heads,
        seq=seq,
        head_dim=head_dim,
        dtype_bytes=dtype_bytes,
    )
    activations = (
        batch * seq * n_layers * checkpointed_activation_bytes_per_token * dtype_bytes
    )
    return MemoryEstimate(
        parameters=params,
        optimizer_states=opt,
        naive_attention_scores=naive,
        flash_workspace=flash,
        activations_checkpointed=activations,
    )


def would_oom(
    requested_bytes: int,
    device_bytes: int = H100_80GB_BYTES,
    safety_margin: float = DEFAULT_SAFETY_MARGIN,
) -> bool:
    """True if a mock allocation should be rejected *before* touching the device."""
    if requested_bytes < 0:
        raise ValueError("requested_bytes must be non-negative")
    if not 0.0 < safety_margin <= 1.0:
        raise ValueError("safety_margin must be in (0, 1]")
    return requested_bytes > int(device_bytes * safety_margin)


def cluster_usable_bytes(
    n_gpus: int,
    device_bytes: int = H200_141GB_BYTES,
    safety_margin: float = DEFAULT_SAFETY_MARGIN,
) -> int:
    """Usable HBM across a node after the safety margin."""
    if n_gpus <= 0:
        raise ValueError("n_gpus must be positive")
    return int(device_bytes * safety_margin) * n_gpus


def would_oom_cluster(
    requested_bytes: int,
    *,
    n_gpus: int,
    device_bytes: int = H200_141GB_BYTES,
    safety_margin: float = DEFAULT_SAFETY_MARGIN,
) -> bool:
    """True if a sharded job does not fit the node."""
    return requested_bytes > cluster_usable_bytes(
        n_gpus, device_bytes=device_bytes, safety_margin=safety_margin
    )


def lora_trainable_params(
    *,
    n_layers: int,
    hidden_size: int,
    rank: int,
    n_projections: int = 4,
) -> int:
    """Adapter params for Q/K/V/O (or Q/V/…) LoRA: ``2 * hidden * rank`` each."""
    if min(n_layers, hidden_size, rank, n_projections) <= 0:
        raise ValueError("LoRA dimensions must be positive")
    return n_layers * n_projections * 2 * hidden_size * rank


def lora_cluster_bytes(
    *,
    n_params: int,
    n_trainable: int,
    dtype_bytes: float = 2,
    optimizer_bytes_per_trainable: int = 12,
) -> int:
    """Frozen weights (bf16) plus AdamW moments on adapters only."""
    frozen = parameter_bytes(n_params=n_params, dtype_bytes=dtype_bytes)
    opt = n_trainable * optimizer_bytes_per_trainable
    return frozen + opt
