"""Multi-threaded tokenized streaming worker (skeleton).

No tokenizer, no disk format, no CUDA copies yet. The methods below pin
the *contract* a later implementation must keep: packed ``(batch, 5120)``
rows, a prefetch queue deep enough to hide CPU latency, and a starvation
counter the Infra Overseer can scrape.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


DEFAULT_CONTEXT_LENGTH = 5120


@dataclass(frozen=True)
class PackedBatch:
    """CPU-side packed token batch ready for a host-to-device copy.

    ``input_ids`` is stored as nested sequences so this scaffold has zero
    tensor-library dependency. A later implementation may swap in torch
    tensors without changing field names.
    """

    input_ids: Sequence[Sequence[int]]
    labels: Sequence[Sequence[int]]
    attention_mask: Sequence[Sequence[int]]
    seq_len: int
    n_tokens: int


@runtime_checkable
class TokenShard(Protocol):
    """A finite or infinite iterator of token ids from one data file."""

    def __iter__(self) -> Iterator[int]: ...


class TokenizedStreamingWorker:
    """Prefetch packed token batches on CPU threads.

    Design goal: the training step should almost never wait on data.
    ``prefetch_depth`` is the number of packed batches that must sit in
    the queue before ``starvation_ratio`` is allowed to be non-zero.

    Parameters
    ----------
    shards:
        Token iterators. Sharding across ranks is a later concern.
    context_length:
        Locked to 5,120 for every model until the 200B extension phase.
    batch_size:
        Sequences per packed batch (micro-batch).
    prefetch_depth:
        Target in-flight batches. Keep small on laptops; raise on the cluster.
    num_workers:
        CPU threads filling the queue.
    seed:
        Deterministic packing / shuffle seed.
    """

    def __init__(
        self,
        shards: Sequence[TokenShard],
        *,
        context_length: int = DEFAULT_CONTEXT_LENGTH,
        batch_size: int = 1,
        prefetch_depth: int = 4,
        num_workers: int = 2,
        seed: int = 0,
    ) -> None:
        if context_length <= 0 or batch_size <= 0:
            raise ValueError("context_length and batch_size must be positive")
        if prefetch_depth <= 0 or num_workers <= 0:
            raise ValueError("prefetch_depth and num_workers must be positive")
        self._shards = list(shards)
        self.context_length = context_length
        self.batch_size = batch_size
        self.prefetch_depth = prefetch_depth
        self.num_workers = num_workers
        self.seed = seed
        self._started = False

    def packed_batch_shape(self) -> tuple[int, int]:
        """``(batch_size, context_length)`` — the only legal packed shape."""
        return (self.batch_size, self.context_length)

    def prefetch_watermark(self) -> int:
        """Minimum queue depth we treat as 'GPU will not starve'."""
        return self.prefetch_depth

    def start(self) -> None:
        """Spin worker threads and fill the prefetch queue.

        Not implemented in this scaffold. A later change must keep
        ``packed_batch_shape()`` unchanged.
        """
        raise NotImplementedError(
            "Streaming runtime is deferred; see data_pipeline/README.md"
        )

    def stop(self) -> None:
        """Join workers and drain the queue."""
        raise NotImplementedError(
            "Streaming runtime is deferred; see data_pipeline/README.md"
        )

    def next_batch(self) -> PackedBatch:
        """Block until one packed batch is available (or raise starvation)."""
        raise NotImplementedError(
            "Streaming runtime is deferred; see data_pipeline/README.md"
        )

    def starvation_ratio(self) -> float:
        """Fraction of ``next_batch`` wall time spent with an empty queue.

        The Infra Overseer should halt a job if this stays above a small
        epsilon for a full step window — that is GPU data starvation.
        """
        raise NotImplementedError(
            "Streaming runtime is deferred; see data_pipeline/README.md"
        )

    def __iter__(self) -> Iterator[PackedBatch]:
        self.start()
        try:
            while True:
                yield self.next_batch()
        finally:
            self.stop()
