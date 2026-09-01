"""RunPod launcher must not spend money unless confirm + API key."""

from __future__ import annotations

import json

import pytest

from fine_tune.planner import plan_job
from fine_tune.recipes import load_recipe
from fine_tune.runpod import launch_pod, pod_create_body
from specs.contracts.memory import RUNPOD_H200_SXM_GPU_TYPE_ID


GIT = "https://github.com/example/lmm-training-stack.git"


def _plan(name: str = "7b_lora"):
    return plan_job(load_recipe(name), smoke=True)


def test_pod_body_is_8x_h200_sxm_not_nvl() -> None:
    body = pod_create_body(_plan(), git_url=GIT)
    assert body["gpuTypeIds"] == [RUNPOD_H200_SXM_GPU_TYPE_ID]
    assert "NVL" not in body["gpuTypeIds"][0]
    assert body["gpuCount"] == 8
    assert body["cloudType"] == "SECURE"
    assert body["interruptible"] is False
    assert body["env"]["LMM_RECIPE"] == "7b_lora"
    assert body["env"]["LMM_SMOKE"] == "1"
    cmd = body["dockerStartCmd"]
    assert cmd[0] == "bash"
    joined = " ".join(cmd)
    assert "fine_tune.train" in joined
    assert "pytest" in joined
    assert "llm-dataset" not in joined


def test_dry_run_never_posts() -> None:
    def boom(url: str, body: dict, key: str) -> dict:
        raise AssertionError(f"HTTP should not run in dry-run: {url}")

    result = launch_pod(
        _plan(),
        git_url=GIT,
        confirm=False,
        dry_run=True,
        api_key="should-not-be-used",
        post=boom,
    )
    assert result.dry_run is True
    assert result.pod_id is None


def test_confirm_without_key_refuses() -> None:
    with pytest.raises(RuntimeError, match="RUNPOD_API_KEY"):
        launch_pod(
            _plan(),
            git_url=GIT,
            confirm=True,
            dry_run=False,
            api_key="",
        )


def test_confirm_with_key_posts_once() -> None:
    calls: list[tuple[str, dict, str]] = []

    def fake_post(url: str, body: dict, key: str) -> dict:
        calls.append((url, body, key))
        return {"id": "pod-test-1"}

    result = launch_pod(
        _plan("70b_lora"),
        git_url=GIT,
        confirm=True,
        dry_run=False,
        api_key="rp_test",
        post=fake_post,
    )
    assert result.dry_run is False
    assert result.pod_id == "pod-test-1"
    assert len(calls) == 1
    assert calls[0][2] == "rp_test"
    assert calls[0][1]["gpuCount"] == 8
    json.dumps(calls[0][1])  # REST body must be JSON-serializable
