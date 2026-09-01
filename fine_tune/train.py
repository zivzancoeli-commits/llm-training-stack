"""On-pod (or local dry-run) fine-tune entry.

Local ``--dry-run`` never imports torch. A real run on 8x H200 needs
``transformers`` + ``peft`` installed on the pod (the bootstrap script
does that).
"""

from __future__ import annotations

import argparse
import json
import sys

from fine_tune.planner import plan_job
from fine_tune.recipes import load_recipe


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fine-tune entry (dry-run safe).")
    parser.add_argument("--recipe", default="7b_lora")
    parser.add_argument("--smoke", action="store_true", default=True)
    parser.add_argument("--full", action="store_true", help="Disable smoke step cap.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the plan as JSON and exit. Default on machines without CUDA.",
    )
    parser.add_argument("--data", default="", help="Path or HF dataset id (pod only).")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    smoke = not args.full
    recipe = load_recipe(args.recipe)
    plan = plan_job(recipe, smoke=smoke)
    if args.dry_run or not _cuda_available():
        json.dump(plan.to_dict(), sys.stdout, indent=2)
        sys.stdout.write("\n")
        if not args.dry_run and not _cuda_available():
            sys.stderr.write(
                "No CUDA device: printed plan only. "
                "This is the local check. Real FT runs on the RunPod 8x H200 node.\n"
            )
        return 0
    from fine_tune.runtime import run_training

    return run_training(plan, data=args.data or None)


def _cuda_available() -> bool:
    try:
        import torch
    except ImportError:
        return False
    return bool(torch.cuda.is_available())


if __name__ == "__main__":
    raise SystemExit(main())
