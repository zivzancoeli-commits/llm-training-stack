"""Import a take-home zip into ``data_pipeline/datasets/``."""

from __future__ import annotations

import zipfile
from pathlib import Path

from data_pipeline.github_sources import TAKEHOME_ZIP_NAMES

ROOT = Path(__file__).resolve().parents[1]
DATASETS = ROOT / "data_pipeline" / "datasets"
DATASET_FOLDERS = ("scratch70b_v0", "scratch70b_sft_2p5m")
SKIP_PARTS = frozenset({"__pycache__", "export", ".git", "__MACOSX"})
SKIP_FILES = frozenset({"review_decisions.json"})


def find_takehome_zip(root: Path) -> Path:
    """Return the take-home zip under ``root`` (file or cloned repo).

    GitHub web upload saved the Mac duplicate name
    ``scratch70b_1m_takehome 2.zip`` at the repo root of
    ``zivzancoeli-commits/llm-dataset``.
    """
    root = root.expanduser().resolve()
    if root.is_file():
        if root.suffix.lower() != ".zip":
            raise FileNotFoundError(f"not a zip: {root}")
        return root
    if not root.is_dir():
        raise FileNotFoundError(f"zip not found: {root}")
    for name in TAKEHOME_ZIP_NAMES:
        hit = root / name
        if hit.is_file():
            return hit
    matches = [
        path
        for path in sorted(root.rglob("*.zip"))
        if "takehome" in path.name.lower() and "__MACOSX" not in path.parts
    ]
    if len(matches) == 1:
        return matches[0]
    if matches:
        named = [p for p in matches if p.name in TAKEHOME_ZIP_NAMES]
        if named:
            return named[0]
        return matches[0]
    raise FileNotFoundError(
        f"no take-home zip under {root}. Expected one of {TAKEHOME_ZIP_NAMES}."
    )


def import_takehome_zip(zip_path: Path, dest_root: Path = DATASETS) -> dict[str, int]:
    """Copy markdown (and sidecars) from a take-home zip into the dataset dirs.

    Understands ``scratch70b_1m_takehome.zip`` (two dataset folders) and a
    bare ``scratch70b_v0/`` or ``scratch70b_sft_2p5m/`` tree inside the zip.
    """
    zip_path = zip_path.expanduser().resolve()
    if not zip_path.is_file():
        raise FileNotFoundError(f"zip not found: {zip_path}")
    copied = {name: 0 for name in DATASET_FOLDERS}
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            mapped = _map_member(info.filename)
            if mapped is None:
                continue
            folder, rel = mapped
            dest = dest_root / folder / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(zf.read(info))
            if dest.suffix == ".md" and dest.name not in {
                "README.md",
                "SCHEMA.md",
                "WRITER.md",
                "TAKE_HOME.md",
            }:
                copied[folder] += 1
    if sum(copied.values()) == 0:
        raise ValueError(
            f"{zip_path.name} has no scratch70b_v0 or scratch70b_sft_2p5m "
            "markdown. Unzip and check the folder names."
        )
    return copied


def _map_member(filename: str) -> tuple[str, Path] | None:
    parts = [p for p in Path(filename).parts if p not in (".",)]
    if not parts or parts[-1] in SKIP_FILES:
        return None
    if any(p in SKIP_PARTS or p.endswith(".pyc") for p in parts):
        return None
    for folder in DATASET_FOLDERS:
        if folder in parts:
            idx = parts.index(folder)
            rel = Path(*parts[idx + 1 :])
            if not rel.parts:
                return None
            return folder, rel
    return None
