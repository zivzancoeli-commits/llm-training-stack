"""Import a take-home zip into ``data_pipeline/datasets/``."""

from __future__ import annotations

import zipfile
from pathlib import Path

from data_pipeline.github_sources import TAKEHOME_ZIP_NAMES

ROOT = Path(__file__).resolve().parents[1]
DATASETS = ROOT / "data_pipeline" / "datasets"
DATASET_FOLDERS = ("scratch70b_v0", "scratch70b_sft_2p5m")
SKIP_PARTS = frozenset({"__pycache__", "export", ".git", "__MACOSX"})
SKIP_FILES = frozenset({"review_decisions.json", ".DS_Store"})
SKIP_MD = frozenset(
    {"README.md", "SCHEMA.md", "WRITER.md", "TAKE_HOME.md", "MIX_PLAN.md"}
)


def find_takehome_zip(root: Path) -> Path:
    """Return the take-home zip under ``root`` (file or cloned repo).

    The reviewed mix lives at the root of
    ``zivzancoeli-commits/llm--dataset`` as ``scratch70b_1m_takehome.zip``.
    An older Mac upload on ``llm-dataset`` used
    ``scratch70b_1m_takehome 2.zip``.
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


def import_takehome_zip(
    zip_path: Path,
    dest_root: Path = DATASETS,
    *,
    replace: bool = True,
) -> dict[str, int]:
    """Copy markdown (and sidecars) from a take-home zip into the dataset dirs.

    Understands ``scratch70b_1m_takehome.zip`` (two dataset folders) and a
    bare ``scratch70b_v0/`` or ``scratch70b_sft_2p5m/`` tree inside the zip.

    ``replace=True`` (default) deletes existing training markdown in each
    folder the zip contains, so leftover chats from an older clone do not
    stay in the mix.
    """
    zip_path = zip_path.expanduser().resolve()
    if not zip_path.is_file():
        raise FileNotFoundError(f"zip not found: {zip_path}")
    copied = {name: 0 for name in DATASET_FOLDERS}
    members: list[tuple[zipfile.ZipInfo, str, Path]] = []
    folders_in_zip: set[str] = set()
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            mapped = _map_member(info.filename)
            if mapped is None:
                continue
            folder, rel = mapped
            folders_in_zip.add(folder)
            members.append((info, folder, rel))
        if replace:
            for folder in folders_in_zip:
                _clear_training_markdown(dest_root / folder)
        for info, folder, rel in members:
            dest = dest_root / folder / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(zf.read(info))
            if dest.suffix == ".md" and dest.name not in SKIP_MD:
                copied[folder] += 1
    if sum(copied.values()) == 0:
        raise ValueError(
            f"{zip_path.name} has no scratch70b_v0 or scratch70b_sft_2p5m "
            "markdown. Unzip and check the folder names."
        )
    _rename_mismatched_ids(dest_root)
    return copied


def _clear_training_markdown(folder: Path) -> None:
    if not folder.is_dir():
        return
    for path in folder.rglob("*.md"):
        if path.name in SKIP_MD or path.name.startswith("._"):
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        path.unlink()


def _rename_mismatched_ids(dest_root: Path) -> None:
    """Finder sometimes saves ``chat-0.md`` whose frontmatter id is ``chat-0625``."""
    for folder in DATASET_FOLDERS:
        chat_dir = dest_root / folder / "chat"
        if not chat_dir.is_dir():
            continue
        for path in sorted(chat_dir.glob("*.md")):
            if path.name in SKIP_MD or path.name.startswith("._"):
                continue
            doc_id = _frontmatter_id(path.read_text(encoding="utf-8"))
            if not doc_id or path.stem == doc_id:
                continue
            target = path.with_name(f"{doc_id}.md")
            if target.exists() and target.resolve() != path.resolve():
                raise ValueError(
                    f"{path.name} has id {doc_id!r} but {target.name} already exists"
                )
            path.rename(target)


def _frontmatter_id(raw: str) -> str | None:
    if not raw.startswith("---"):
        return None
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return None
    for line in parts[1].splitlines():
        stripped = line.strip()
        if stripped.startswith("id:"):
            return stripped.split(":", 1)[1].strip().strip("'\"")
    return None


def _map_member(filename: str) -> tuple[str, Path] | None:
    parts = [p for p in Path(filename).parts if p not in (".",)]
    if not parts or parts[-1] in SKIP_FILES or parts[-1].startswith("._"):
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
