"""RunPod REST payload + optional create. Dry-run by default.

This cloud agent does **not** have the RunPod MCP connected. The same
JSON body is what the MCP ``create-pod`` tool would send. Launching a
real 8x H200 pod requires ``RUNPOD_API_KEY`` and ``--confirm``.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable

from data_pipeline.github_sources import DEFAULT_DATASET_GIT_URL
from fine_tune.planner import FineTunePlan
from fine_tune.recipes import H200_SXM_GPU_COUNT, H200_SXM_GPU_TYPE_ID

RUNPOD_PODS_URL = "https://rest.runpod.io/v1/pods"

# CUDA 12.4+ image so H200 SXM (Hopper/HBM3e) is usable.
DEFAULT_IMAGE = "runpod/pytorch:2.8.0-py3.11-cuda12.8.1-devel-ubuntu22.04"


def bootstrap_command(
    *,
    git_url: str,
    recipe: str,
    smoke: bool,
    job: str = "ft",
    dataset_git_url: str = "",
) -> list[str]:
    """What the pod runs on boot. Clones the repo, then smoke-trains."""
    smoke_flag = "--smoke" if smoke else "--full"
    clone_fn = r"""clone_github() {
  url="$1"
  dest="$2"
  if [ -n "${GITHUB_TOKEN:-}" ]; then
    case "$url" in
      https://*) url="https://x-access-token:${GITHUB_TOKEN}@${url#https://}" ;;
    esac
  fi
  git clone --depth 1 "$url" "$dest"
}
"""
    if job == "scratch":
        extras = "python -m pip install deepspeed"
        checks = (
            "python -m pytest tests/test_scratch_pretrain.py "
            "tests/test_token_budget.py tests/test_profiles.py -q"
        )
        train = (
            f"deepspeed --num_gpus 8 -m pretrain.train --recipe {recipe} {smoke_flag}"
        )
        ds_url = dataset_git_url or DEFAULT_DATASET_GIT_URL
        dataset_steps = f"""
if [ ! -d /workspace/llm-dataset/.git ]; then
  clone_github "{ds_url}" /workspace/llm-dataset || echo "WARN: could not clone dataset repo (private 404?). Using in-repo corpus."
fi
python -c "from pathlib import Path; from data_pipeline.import_zip import find_takehome_zip, import_takehome_zip
root=Path('/workspace/llm-dataset')
try:
    z=find_takehome_zip(root)
    print(import_takehome_zip(z))
except Exception as e:
    print('WARN: zip import skipped:', e)
"
"""
    else:
        extras = "python -m pip install transformers peft datasets accelerate"
        checks = (
            "python -m pytest tests/test_finetune_plan.py "
            "tests/test_runpod_dry_run.py tests/test_profiles.py -q"
        )
        train = f"python -m fine_tune.train --recipe {recipe} {smoke_flag}"
        dataset_steps = ""
    script = f"""set -euo pipefail
{clone_fn}
cd /workspace
if [ ! -f /workspace/pyproject.toml ]; then
  clone_github "{git_url}" /workspace/lmm-training-stack
  cd /workspace/lmm-training-stack
fi
python -m pip install -U pip
python -m pip install pyyaml pytest
{extras}
{dataset_steps}
{checks}
{train}
"""
    return ["bash", "-lc", script]


def pod_create_body(
    plan: FineTunePlan,
    *,
    git_url: str,
    name: str | None = None,
    image_name: str = DEFAULT_IMAGE,
    hf_token: str | None = None,
    job: str = "ft",
) -> dict[str, Any]:
    recipe = plan.recipe
    if recipe.gpu_type_id != H200_SXM_GPU_TYPE_ID:
        raise ValueError("pod body is pinned to NVIDIA H200 (SXM), not NVL")
    if recipe.gpu_count != H200_SXM_GPU_COUNT:
        raise ValueError("pod body is pinned to 8 GPUs")
    return h200_pod_body(
        git_url=git_url,
        recipe_name=recipe.name,
        smoke=plan.smoke,
        job=job,
        name=name,
        image_name=image_name,
        hf_token=hf_token,
    )


def scratch_pod_create_body(
    plan: Any,
    *,
    git_url: str,
    name: str | None = None,
    image_name: str = DEFAULT_IMAGE,
    dataset_git_url: str = DEFAULT_DATASET_GIT_URL,
) -> dict[str, Any]:
    recipe = plan.recipe
    if recipe.gpu_type_id != H200_SXM_GPU_TYPE_ID or recipe.gpu_count != H200_SXM_GPU_COUNT:
        raise ValueError("from-scratch pods are pinned to 8x NVIDIA H200 SXM")
    return h200_pod_body(
        git_url=git_url,
        recipe_name=recipe.name,
        smoke=plan.smoke,
        job="scratch",
        name=name,
        image_name=image_name,
        hf_token=None,
        dataset_git_url=dataset_git_url,
    )


def h200_pod_body(
    *,
    git_url: str,
    recipe_name: str,
    smoke: bool,
    job: str,
    name: str | None = None,
    image_name: str = DEFAULT_IMAGE,
    hf_token: str | None = None,
    dataset_git_url: str = DEFAULT_DATASET_GIT_URL,
) -> dict[str, Any]:
    env: dict[str, str] = {
        "LMM_RECIPE": recipe_name,
        "LMM_SMOKE": "1" if smoke else "0",
        "LMM_GIT_URL": git_url,
        "LMM_JOB": job,
        "HF_HUB_ENABLE_HF_TRANSFER": "1",
    }
    if job == "scratch":
        env["LMM_DATASET_GIT_URL"] = dataset_git_url or DEFAULT_DATASET_GIT_URL
    if hf_token:
        env["HF_TOKEN"] = hf_token
        env["HUGGING_FACE_HUB_TOKEN"] = hf_token
    prefix = "scratch" if job == "scratch" else "ft"
    return {
        "name": name or f"lmm-{prefix}-{recipe_name}",
        "cloudType": "SECURE",
        "computeType": "GPU",
        "gpuTypeIds": [H200_SXM_GPU_TYPE_ID],
        "gpuTypePriority": "custom",
        "gpuCount": H200_SXM_GPU_COUNT,
        "imageName": image_name,
        "containerDiskInGb": 100,
        "volumeInGb": 300,
        "volumeMountPath": "/workspace",
        "minRAMPerGPU": 64,
        "minVCPUPerGPU": 8,
        "interruptible": False,
        "ports": ["22/tcp", "8888/http"],
        "env": env,
        "dockerStartCmd": bootstrap_command(
            git_url=git_url,
            recipe=recipe_name,
            smoke=smoke,
            job=job,
            dataset_git_url=dataset_git_url if job == "scratch" else "",
        ),
    }


@dataclass(frozen=True)
class LaunchResult:
    dry_run: bool
    body: dict[str, Any]
    pod_id: str | None
    raw: dict[str, Any] | None


def _post_json(url: str, body: dict[str, Any], api_key: str) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode() if exc.fp else ""
        raise RuntimeError(f"RunPod HTTP {exc.code}: {detail}") from exc


def launch_pod(
    plan: FineTunePlan,
    *,
    git_url: str,
    confirm: bool = False,
    dry_run: bool = True,
    api_key: str | None = None,
    hf_token: str | None = None,
    name: str | None = None,
    post: Callable[[str, dict[str, Any], str], dict[str, Any]] | None = None,
) -> LaunchResult:
    """Create an 8x H200 SXM pod. Refuses unless ``confirm`` and not ``dry_run``."""
    body = pod_create_body(plan, git_url=git_url, name=name, hf_token=hf_token)
    if dry_run or not confirm:
        return LaunchResult(dry_run=True, body=body, pod_id=None, raw=None)
    key = api_key if api_key is not None else os.environ.get("RUNPOD_API_KEY")
    if not key:
        raise RuntimeError(
            "Refusing to create an 8x H200 pod: RUNPOD_API_KEY is not set. "
            "Re-run with --dry-run, or export the key and pass --confirm."
        )
    poster = post or _post_json
    raw = poster(RUNPOD_PODS_URL, body, key)
    pod_id = None
    if isinstance(raw, dict):
        pod_id = raw.get("id") or raw.get("podId")
    return LaunchResult(dry_run=False, body=body, pod_id=pod_id, raw=raw)


def launch_scratch_pod(
    plan: Any,
    *,
    git_url: str,
    confirm: bool = False,
    dry_run: bool = True,
    api_key: str | None = None,
    name: str | None = None,
    dataset_git_url: str = DEFAULT_DATASET_GIT_URL,
    post: Callable[[str, dict[str, Any], str], dict[str, Any]] | None = None,
) -> LaunchResult:
    """Create an 8x H200 SXM from-scratch pod. Same confirm rules as FT."""
    body = scratch_pod_create_body(
        plan, git_url=git_url, name=name, dataset_git_url=dataset_git_url
    )
    if dry_run or not confirm:
        return LaunchResult(dry_run=True, body=body, pod_id=None, raw=None)
    key = api_key if api_key is not None else os.environ.get("RUNPOD_API_KEY")
    if not key:
        raise RuntimeError(
            "Refusing to create an 8x H200 pod: RUNPOD_API_KEY is not set. "
            "Re-run with --dry-run, or export the key and pass --confirm."
        )
    poster = post or _post_json
    raw = poster(RUNPOD_PODS_URL, body, key)
    pod_id = None
    if isinstance(raw, dict):
        pod_id = raw.get("id") or raw.get("podId")
    return LaunchResult(dry_run=False, body=body, pod_id=pod_id, raw=raw)
