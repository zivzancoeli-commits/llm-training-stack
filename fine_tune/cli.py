"""``lmm tour`` / ``lmm check`` / ``lmm ft-plan`` / ``lmm ft-launch``."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOUR_STEPS = (
    ("README.md", "What this repo is (and what it is not)."),
    ("WALKTHROUGH.md", "How to edit one file and prove it with pytest."),
    ("SCALING_MANIFEST.md", "100M → 200B phases, 5,120 vs 350k context."),
    ("DECISIONS.md", "Defaults we picked so work was not blocked."),
    ("specs/hyperparameter_profiles/", "YAML knobs. Change these first."),
    ("specs/contracts/", "Shape / init / OOM math the tests lock."),
    ("data_pipeline/loader.py", "Streaming worker skeleton."),
    ("model/transformer_block.py", "Llama-like block + FA-3 hook + PP map."),
    ("infra/overseer.py", "Heartbeat + InfiniBand halt."),
    ("pretrain/recipes/", "From-scratch 100M/7B/70B. Random init. 1M token cap."),
    ("fine_tune/recipes/", "Optional Qwen FT (not the from-scratch path)."),
    ("data_pipeline/datasets/scratch70b_v0/", "70B-from-scratch seed corpus (review this)."),
    ("infra/runpod/", "Pod payload + MCP notes. Dry-run until --confirm."),
    ("tests/", "The only gate before spending GPU money."),
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lmm",
        description="Local tour, pytest gate, and dry-run 8x H200 fine-tune launcher.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("tour", help="Print the map of the repo and how to check edits.")
    chk = sub.add_parser("check", help="Run pytest. Extra args go to pytest (e.g. lmm check -q).")
    chk.add_argument("pytest_args", nargs=argparse.REMAINDER)

    plan = sub.add_parser("ft-plan", help="Print the 8x H200 fine-tune plan.")
    plan.add_argument("--recipe", default="7b_lora")
    plan.add_argument("--full", action="store_true")

    launch = sub.add_parser(
        "ft-launch",
        help="Build (and optionally POST) the RunPod 8x H200 SXM pod.",
    )
    launch.add_argument("--recipe", default="7b_lora")
    launch.add_argument("--full", action="store_true")
    launch.add_argument(
        "--git-url",
        default="",
        help="Repo the pod should clone. Required for a real launch.",
    )
    launch.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Print JSON, do not create a pod (default).",
    )
    launch.add_argument(
        "--confirm",
        action="store_true",
        help="Spend money: POST to RunPod. Requires RUNPOD_API_KEY.",
    )
    launch.add_argument("--name", default="")

    sub.add_parser("data-export", help="Validate scratch70b_v0 and write JSONL + catalog.")
    imp = sub.add_parser("data-import", help="Import a take-home zip into the dataset folders.")
    imp.add_argument("zip_path", help="Path to scratch70b_1m_takehome.zip (macOS ' 2' name is fine).")
    review = sub.add_parser("data-review", help="Serve the dataset review UI (port 43147).")
    review.add_argument("--host", default="127.0.0.1")
    review.add_argument("--port", type=int, default=43147)

    splan = sub.add_parser("scratch-plan", help="Print a from-scratch (random init) plan.")
    splan.add_argument("--recipe", default="100m_scratch")
    splan.add_argument("--full", action="store_true")
    strain = sub.add_parser("scratch-train", help="From-scratch train. Dry-run without CUDA.")
    strain.add_argument("--recipe", default="100m_scratch")
    strain.add_argument("--full", action="store_true")
    strain.add_argument("--dry-run", action="store_true")
    slaunch = sub.add_parser(
        "scratch-launch",
        help="Build (and optionally POST) an 8x H200 SXM from-scratch pod.",
    )
    slaunch.add_argument("--recipe", default="70b_scratch")
    slaunch.add_argument("--full", action="store_true")
    slaunch.add_argument(
        "--git-url",
        default="",
        help="Training-stack clone URL. Dry-run defaults to "
        "github.com/zivzancoeli-commits/llm-training-stack. "
        "Required for --confirm.",
    )
    slaunch.add_argument(
        "--dataset-git-url",
        default="",
        help="Dataset clone URL. Default: "
        "github.com/zivzancoeli-commits/llm-dataset",
    )
    slaunch.add_argument("--dry-run", action="store_true", default=True)
    slaunch.add_argument("--confirm", action="store_true")
    slaunch.add_argument("--name", default="")
    return parser


def cmd_tour() -> int:
    print("LMM stack — where things live")
    print("================================")
    print()
    print("Start at WALKTHROUGH.md. Edit YAML, then pytest. GPU is last.")
    print()
    for i, (path, why) in enumerate(TOUR_STEPS, start=1):
        mark = "ok" if (ROOT / path).exists() else "MISSING"
        print(f"  {i:2d}. [{mark}] {path}")
        print(f"      {why}")
    print()
    print("Small-change loop")
    print("-----------------")
    print("  1. Edit one YAML in specs/hyperparameter_profiles/ or fine_tune/recipes/")
    print("  2. uv run lmm check tests/test_profiles.py tests/test_finetune_plan.py")
    print("  3. uv run lmm check")
    print("  4. uv run lmm scratch-plan --recipe 100m_scratch")
    print("  5. uv run lmm scratch-plan --recipe 70b_scratch")
    print("  6. uv run lmm data-review     # seed corpus")
    print()
    print("From-scratch uses random weights and a 1M-token cap (2.5M hard).")
    print("Prefer 1M or less; do not generate toward the 2.5M hard cap.")
    print("Qwen LoRA (`lmm ft-launch`) is optional and separate.")
    print("8x H200 SXM is not billed until `lmm ft-launch --confirm` (FT) or")
    print("a real `scratch-train` on a CUDA node.")
    print("RunPod MCP (optional, FT pods): npx @runpod/mcp-server@latest add")
    return 0
    return 0


def cmd_check(pytest_args: list[str]) -> int:
    cmd = [sys.executable, "-m", "pytest", *pytest_args]
    print("+", " ".join(cmd), flush=True)
    return subprocess.call(cmd, cwd=ROOT)


def cmd_ft_plan(recipe: str, full: bool) -> int:
    from fine_tune.planner import plan_job
    from fine_tune.recipes import load_recipe

    plan = plan_job(load_recipe(recipe), smoke=not full)
    print(json.dumps(plan.to_dict(), indent=2))
    if plan.waste_warning:
        print(plan.waste_warning, file=sys.stderr)
    return 0


def cmd_ft_launch(
    *,
    recipe: str,
    full: bool,
    git_url: str,
    dry_run: bool,
    confirm: bool,
    name: str,
) -> int:
    from fine_tune.planner import plan_job
    from fine_tune.recipes import H200_SXM_GPU_TYPE_ID, load_recipe
    from fine_tune.runpod import launch_pod

    recipe = load_recipe(recipe)
    if recipe.gpu_type_id != H200_SXM_GPU_TYPE_ID:
        print(
            "lmm ft-launch only builds 8x H200 SXM pods. "
            f"{recipe.name} is {recipe.gpu_count}x {recipe.gpu_type_id} — "
            "run fine_tune/train.py on that machine instead.",
            file=sys.stderr,
        )
        return 2

    # --confirm is the only way off the dry-run path.
    effective_dry = dry_run and not confirm
    if confirm and not git_url:
        print("Refusing --confirm without --git-url (the pod has to clone this repo).", file=sys.stderr)
        return 2
    url = git_url or "https://example.invalid/your-fork.git"
    plan = plan_job(recipe, smoke=not full)
    result = launch_pod(
        plan,
        git_url=url,
        confirm=confirm,
        dry_run=effective_dry,
        name=name or None,
    )
    print(json.dumps({"dry_run": result.dry_run, "pod_id": result.pod_id, "body": result.body}, indent=2))
    if result.dry_run:
        print(
            "Dry-run only. No pod was created. "
            "Connect RunPod MCP (`npx @runpod/mcp-server@latest add`) or "
            "export RUNPOD_API_KEY and re-run with --confirm --git-url …",
            file=sys.stderr,
        )
    return 0


def cmd_data_export() -> int:
    from data_pipeline.datasets.scratch70b_v0.catalog import load_all, mix_counts, write_export

    docs = load_all()
    dest = write_export(docs)
    mix = mix_counts(docs)
    print(f"wrote {len(docs)} docs to {dest}")
    print(json.dumps({"n_docs": len(docs), "mix": mix}, indent=2))
    return 0


def cmd_data_import(zip_path: str) -> int:
    from data_pipeline.import_zip import import_takehome_zip

    copied = import_takehome_zip(Path(zip_path))
    print(json.dumps({"imported": copied}, indent=2))
    return 0


def cmd_scratch_launch(
    *,
    recipe: str,
    full: bool,
    git_url: str,
    dry_run: bool,
    confirm: bool,
    name: str,
    dataset_git_url: str = "",
) -> int:
    from data_pipeline.github_sources import (
        DEFAULT_DATASET_GIT_URL,
        DEFAULT_TRAINING_GIT_URL,
    )
    from fine_tune.runpod import launch_scratch_pod
    from pretrain.planner import plan_scratch
    from pretrain.recipes import load_scratch_recipe

    recipe_obj = load_scratch_recipe(recipe)
    effective_dry = dry_run and not confirm
    if confirm and not git_url:
        print("Refusing --confirm without --git-url (the pod has to clone this repo).", file=sys.stderr)
        return 2
    url = git_url or DEFAULT_TRAINING_GIT_URL
    plan = plan_scratch(recipe_obj, smoke=not full)
    result = launch_scratch_pod(
        plan,
        git_url=url,
        confirm=confirm,
        dry_run=effective_dry,
        name=name or None,
        dataset_git_url=dataset_git_url or DEFAULT_DATASET_GIT_URL,
    )
    print(json.dumps({"dry_run": result.dry_run, "pod_id": result.pod_id, "body": result.body}, indent=2))
    if result.dry_run:
        print(
            "Dry-run only. No pod was created. "
            "export RUNPOD_API_KEY and re-run with --confirm --git-url …",
            file=sys.stderr,
        )
    return 0


def cmd_data_review(host: str, port: int) -> int:
    from data_pipeline.datasets.scratch70b_v0.review_server import serve

    serve(host, port)
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # `lmm check -q` must not be eaten by this parser; pytest owns the flags.
    if argv and argv[0] == "check":
        return cmd_check(argv[1:])
    args = build_parser().parse_args(argv)
    if args.cmd == "tour":
        return cmd_tour()
    if args.cmd == "check":
        return cmd_check(args.pytest_args)
    if args.cmd == "ft-plan":
        return cmd_ft_plan(args.recipe, args.full)
    if args.cmd == "ft-launch":
        return cmd_ft_launch(
            recipe=args.recipe,
            full=args.full,
            git_url=args.git_url,
            dry_run=args.dry_run,
            confirm=args.confirm,
            name=args.name,
        )
    if args.cmd == "data-export":
        return cmd_data_export()
    if args.cmd == "data-import":
        return cmd_data_import(args.zip_path)
    if args.cmd == "data-review":
        return cmd_data_review(args.host, args.port)
    if args.cmd == "scratch-plan":
        return cmd_scratch_plan(args.recipe, args.full)
    if args.cmd == "scratch-train":
        return cmd_scratch_train(args.recipe, args.full, args.dry_run)
    if args.cmd == "scratch-launch":
        return cmd_scratch_launch(
            recipe=args.recipe,
            full=args.full,
            git_url=args.git_url,
            dry_run=args.dry_run,
            confirm=args.confirm,
            name=args.name,
            dataset_git_url=getattr(args, "dataset_git_url", ""),
        )
    raise AssertionError(args.cmd)


def cmd_scratch_plan(recipe: str, full: bool) -> int:
    from pretrain.planner import plan_scratch
    from pretrain.recipes import load_scratch_recipe

    plan = plan_scratch(load_scratch_recipe(recipe), smoke=not full)
    print(json.dumps(plan.to_dict(), indent=2))
    if plan.waste_warning:
        print(plan.waste_warning, file=sys.stderr)
    return 0


def cmd_scratch_train(recipe: str, full: bool, dry_run: bool) -> int:
    from pretrain.train import main as scratch_main

    argv = ["--recipe", recipe]
    if full:
        argv.append("--full")
    if dry_run:
        argv.append("--dry-run")
    return scratch_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
