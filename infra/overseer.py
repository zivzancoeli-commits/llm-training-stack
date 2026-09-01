"""Cluster health, heartbeats, and InfiniBand integrity (skeleton).

This is a template you run beside the training job, not inside the
model graph. It stores heartbeats in process memory so tests can inject
faults without Slurm, Prometheus, or `ibstat`.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# If a node misses a beat longer than this, it is stale.
DEFAULT_HEARTBEAT_TIMEOUT_S = 30.0
# HDR InfiniBand is 200 Gbit/s per direction; we treat < 100 as degraded.
MIN_HEALTHY_IB_GBPS = 100.0


@dataclass(frozen=True)
class NodeHeartbeat:
    """One sample from one rank/node."""

    node_id: str
    timestamp_s: float
    gpu_ok: bool
    cpu_util: float
    ib_link_up: bool
    ib_link_gbps: float | None
    notes: str = ""


@dataclass
class InfraOverseer:
    """Track node health so hardware decay is caught before a 256-GPU job.

    Parameters
    ----------
    heartbeat_timeout_s:
        A node is stale if ``now - last_beat`` exceeds this.
    min_ib_gbps:
        Link speed below this (while the link is 'up') still counts as
        degraded — silent CRC / lane-down faults look like this.
    """

    heartbeat_timeout_s: float = DEFAULT_HEARTBEAT_TIMEOUT_S
    min_ib_gbps: float = MIN_HEALTHY_IB_GBPS
    _beats: dict[str, NodeHeartbeat] = field(default_factory=dict, repr=False)

    def record_heartbeat(self, beat: NodeHeartbeat) -> None:
        """Upsert the latest sample for ``beat.node_id``."""
        if beat.timestamp_s < 0:
            raise ValueError("timestamp_s must be non-negative")
        if not 0.0 <= beat.cpu_util <= 1.0:
            raise ValueError("cpu_util must be in [0, 1]")
        self._beats[beat.node_id] = beat

    def last_heartbeat(self, node_id: str) -> NodeHeartbeat | None:
        return self._beats.get(node_id)

    def ib_link_integrity(self, beat: NodeHeartbeat) -> bool:
        """True only if the IB link is up *and* at a healthy data rate."""
        if not beat.ib_link_up:
            return False
        if beat.ib_link_gbps is None:
            return False
        return beat.ib_link_gbps >= self.min_ib_gbps

    def is_stale(self, node_id: str, now_s: float) -> bool:
        beat = self._beats.get(node_id)
        if beat is None:
            return True
        return (now_s - beat.timestamp_s) > self.heartbeat_timeout_s

    def degraded_nodes(self, now_s: float) -> list[str]:
        """Node ids that are stale, GPU-unhealthy, or IB-degraded."""
        bad: list[str] = []
        for node_id, beat in sorted(self._beats.items()):
            if self.is_stale(node_id, now_s):
                bad.append(node_id)
                continue
            if not beat.gpu_ok:
                bad.append(node_id)
                continue
            if not self.ib_link_integrity(beat):
                bad.append(node_id)
        return bad

    def should_halt_job(self, now_s: float) -> bool:
        """Halt if *any* known node is degraded. Empty roster is not a halt.

        An empty roster means the overseer has not been wired up yet —
        that is a scaffold state, not a cluster incident.
        """
        if not self._beats:
            return False
        return len(self.degraded_nodes(now_s)) > 0
