"""Load the human-editable YAML profiles so small edits are testable."""

from __future__ import annotations

from pathlib import Path
from typing import Any

PROFILE_DIR = Path(__file__).resolve().parent / "hyperparameter_profiles"

# Phases 0–4 stay at 5,120. Only the 200B *extension* field may be 350,208.
PRETRAIN_CONTEXT = 5120
LONG_CONTEXT = 350208


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - declared in pyproject
        raise RuntimeError("PyYAML is required to load hyperparameter profiles") from exc
    with path.open() as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def list_profile_paths() -> list[Path]:
    return sorted(PROFILE_DIR.glob("*.yaml"))


def load_profile(name: str) -> dict[str, Any]:
    """Load ``100m``, ``1b``, ``7b``, ``70b``, or ``200b``."""
    path = PROFILE_DIR / f"{name}.yaml"
    if not path.is_file():
        raise FileNotFoundError(path)
    return _load_yaml(path)


def load_all_profiles() -> dict[str, dict[str, Any]]:
    return {path.stem: _load_yaml(path) for path in list_profile_paths()}
