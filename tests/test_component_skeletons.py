"""Structural tests for the three core skeletons (no algorithms)."""

from __future__ import annotations

import pytest

from data_pipeline.loader import TokenizedStreamingWorker
from infra.overseer import InfraOverseer, NodeHeartbeat
from model.tensor_config import ParallelLayout
from model.transformer_block import BlockConfig, TransformerBlock


def test_loader_packed_shape_is_batch_by_5k() -> None:
    worker = TokenizedStreamingWorker([], batch_size=4, context_length=5120)
    assert worker.packed_batch_shape() == (4, 5120)
    assert worker.prefetch_watermark() == 4


def test_loader_runtime_is_deferred() -> None:
    worker = TokenizedStreamingWorker([])
    with pytest.raises(NotImplementedError, match="Streaming runtime"):
        worker.start()


def test_pipeline_map_splits_layers_contiguously() -> None:
    cfg = BlockConfig(
        layer_index=17,
        n_layers=32,
        n_heads=32,
        n_kv_heads=8,
        head_dim=128,
        intermediate_size=11008,
    )
    block = TransformerBlock(cfg)
    layout = ParallelLayout(
        tensor_parallel_size=2,
        pipeline_parallel_size=4,
        tensor_rank=1,
        pipeline_stage=0,
    )
    layer_map = block.parallel_layer_map(layout)
    assert layer_map.pipeline_stage == 2  # 17 // (32/4) == 2
    assert layer_map.is_first_stage is False
    assert layer_map.is_last_stage is False
    assert layer_map.attention_qkv_partition == "column"
    assert layer_map.attention_out_partition == "row"
    assert layer_map.mlp_up_partition == "column"
    assert layer_map.mlp_down_partition == "row"


def test_first_and_last_pipeline_stages() -> None:
    first = TransformerBlock(
        BlockConfig(
            layer_index=0,
            n_layers=8,
            n_heads=8,
            n_kv_heads=2,
            head_dim=64,
            intermediate_size=256,
        )
    )
    last = TransformerBlock(
        BlockConfig(
            layer_index=7,
            n_layers=8,
            n_heads=8,
            n_kv_heads=2,
            head_dim=64,
            intermediate_size=256,
        )
    )
    layout = ParallelLayout(pipeline_parallel_size=4)
    assert first.parallel_layer_map(layout).is_first_stage is True
    assert last.parallel_layer_map(layout).is_last_stage is True


def test_overseer_halts_on_dead_infiniband() -> None:
    overseer = InfraOverseer()
    overseer.record_heartbeat(
        NodeHeartbeat(
            node_id="rank0",
            timestamp_s=10.0,
            gpu_ok=True,
            cpu_util=0.2,
            ib_link_up=False,
            ib_link_gbps=0.0,
        )
    )
    assert overseer.should_halt_job(now_s=11.0) is True
    assert overseer.degraded_nodes(now_s=11.0) == ["rank0"]


def test_overseer_halts_on_slow_ib_even_if_link_reports_up() -> None:
    overseer = InfraOverseer(min_ib_gbps=100.0)
    overseer.record_heartbeat(
        NodeHeartbeat(
            node_id="rank1",
            timestamp_s=1.0,
            gpu_ok=True,
            cpu_util=0.1,
            ib_link_up=True,
            ib_link_gbps=25.0,  # lane-down / degraded HDR
        )
    )
    assert overseer.ib_link_integrity(overseer.last_heartbeat("rank1")) is False
    assert overseer.should_halt_job(now_s=2.0) is True


def test_overseer_stale_heartbeat_is_degraded() -> None:
    overseer = InfraOverseer(heartbeat_timeout_s=30.0)
    overseer.record_heartbeat(
        NodeHeartbeat(
            node_id="rank2",
            timestamp_s=0.0,
            gpu_ok=True,
            cpu_util=0.0,
            ib_link_up=True,
            ib_link_gbps=200.0,
        )
    )
    assert overseer.is_stale("rank2", now_s=31.0) is True
    assert overseer.should_halt_job(now_s=31.0) is True
    assert overseer.should_halt_job(now_s=10.0) is False


def test_overseer_empty_roster_does_not_halt() -> None:
    assert InfraOverseer().should_halt_job(now_s=0.0) is False
