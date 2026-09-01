"""Tensor views and parallel-layout records (no real device buffers)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


DTypeName = Literal["fp32", "fp16", "bf16"]

_DTYPE_BYTES: dict[DTypeName, int] = {"fp32": 4, "fp16": 2, "bf16": 2}


@dataclass(frozen=True)
class TensorView:
    """Shape-only stand-in for a torch/numpy tensor.

    Tests and skeletons use this so CI never allocates GPU memory.
    """

    shape: tuple[int, ...]
    dtype: DTypeName = "bf16"

    @property
    def dtype_bytes(self) -> int:
        return _DTYPE_BYTES[self.dtype]

    @property
    def ndim(self) -> int:
        return len(self.shape)

    def nbytes(self) -> int:
        n = 1
        for dim in self.shape:
            n *= dim
        return n * self.dtype_bytes


@dataclass(frozen=True)
class ParallelLayout:
    """How one training rank sits on the (TP, PP) grid."""

    tensor_parallel_size: int = 1
    pipeline_parallel_size: int = 1
    tensor_rank: int = 0
    pipeline_stage: int = 0

    def __post_init__(self) -> None:
        if self.tensor_parallel_size <= 0 or self.pipeline_parallel_size <= 0:
            raise ValueError("parallel sizes must be positive")
        if not 0 <= self.tensor_rank < self.tensor_parallel_size:
            raise ValueError("tensor_rank out of range")
        if not 0 <= self.pipeline_stage < self.pipeline_parallel_size:
            raise ValueError("pipeline_stage out of range")


Partition = Literal["column", "row", "replicated"]


@dataclass(frozen=True)
class LayerMap:
    """Decoupled model-parallel / pipeline-parallel placement for one block.

    Attention and MLP partitions are stored separately so Megatron-style
    column/row pairing can be filled in later without rewriting the block.
    """

    layer_index: int
    pipeline_stage: int
    is_first_stage: bool
    is_last_stage: bool
    attention_qkv_partition: Partition
    attention_out_partition: Partition
    mlp_up_partition: Partition
    mlp_down_partition: Partition
