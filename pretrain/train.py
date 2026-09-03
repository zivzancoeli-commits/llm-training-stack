"""From-scratch pretrain entry. ``--dry-run`` never imports torch."""

from __future__ import annotations

import argparse
import json
import os
import sys

# Must be set before the first CUDA context (DeepSpeed ranks import torch here).
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

from pretrain.planner import plan_scratch
from pretrain.recipes import load_scratch_recipe


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="From-scratch pretrain (random init).")
    parser.add_argument("--recipe", default="100m_scratch")
    parser.add_argument("--smoke", action="store_true", default=True)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true", help="Resume outputs/<recipe>/latest.pt.")
    parser.add_argument("--local_rank", type=int, default=-1, help="Set by DeepSpeed.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args, _unknown = parser.parse_known_args(argv)
    recipe = load_scratch_recipe(args.recipe)
    plan = plan_scratch(recipe, smoke=not args.full)
    if args.dry_run or not _accelerator_available(recipe.gpu_type_id):
        json.dump(plan.to_dict(), sys.stdout, indent=2)
        sys.stdout.write("\n")
        if not args.dry_run:
            sys.stderr.write(
                "Requested accelerator unavailable: printed from-scratch plan only. "
                "This is not Qwen. Random init. Token budget "
                f"{recipe.max_tokens} preferred (hard cap 2.5M).\n"
            )
        if plan.waste_warning:
            sys.stderr.write(plan.waste_warning + "\n")
        return 0
    from pretrain.runtime import run_scratch

    return run_scratch(plan, resume=args.resume)


def _accelerator_available(gpu_type_id: str) -> bool:
    try:
        import torch
    except ImportError:
        return False
    if gpu_type_id == "CPU":
        return True
    mps = getattr(torch.backends, "mps", None)
    if gpu_type_id == "Apple MPS":
        return bool(mps is not None and mps.is_available())
    return bool(torch.cuda.is_available())


if __name__ == "__main__":
    raise SystemExit(main())
