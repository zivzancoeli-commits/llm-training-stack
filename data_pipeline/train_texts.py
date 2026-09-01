"""Load packed training texts from the repo, a zip, a folder, or JSONL."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from data_pipeline.token_budget import PREFERRED_TOKEN_BUDGET
from pretrain.corpus import CorpusDoc, iter_corpus_docs, select_corpus_docs


def load_training_texts(
    source: str | Path | None = None,
    *,
    max_tokens: int = PREFERRED_TOKEN_BUDGET,
) -> list[str]:
    """Return document bodies packed at the 1M preferred budget (2.5M hard).

    ``source`` may be omitted (repo datasets), a take-home zip, a folder
    that contains ``scratch70b_v0`` / ``scratch70b_sft_2p5m``, or a JSONL
    file with a ``text`` or ``body`` field.
    """
    if source is None or str(source).strip() == "":
        docs = select_corpus_docs(iter_corpus_docs(), max_tokens=max_tokens)
        return [doc.text for doc in docs]

    path = Path(source).expanduser()
    if path.suffix.lower() == ".zip":
        return _from_zip(path, max_tokens=max_tokens)
    if path.suffix.lower() == ".jsonl":
        return _from_jsonl(path, max_tokens=max_tokens)
    if path.is_dir():
        docs = select_corpus_docs(
            iter_corpus_docs(_dataset_roots(path)), max_tokens=max_tokens
        )
        return [doc.text for doc in docs]
    raise FileNotFoundError(f"cannot load training texts from {path}")


def _dataset_roots(path: Path) -> tuple[Path, ...]:
    found: list[Path] = []
    for name in ("scratch70b_v0", "scratch70b_sft_2p5m"):
        candidate = path / name
        if candidate.is_dir():
            found.append(candidate)
        found.extend(p for p in path.glob(f"*/{name}") if p.is_dir())
    if not found:
        return (path,)
    seen: set[Path] = set()
    out: list[Path] = []
    for item in found:
        resolved = item.resolve()
        if resolved not in seen:
            seen.add(resolved)
            out.append(resolved)
    return tuple(out)


def _from_jsonl(path: Path, *, max_tokens: int) -> list[str]:
    texts: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if isinstance(row, dict) and row.get("text"):
            texts.append(str(row["text"]))
        elif isinstance(row, dict) and row.get("body"):
            texts.append(str(row["body"]))
        else:
            texts.append(str(row))
    wrapped = [
        CorpusDoc(path=path, category="chat", bucket="speech", text=text)
        for text in texts
        if text.strip()
    ]
    return [doc.text for doc in select_corpus_docs(wrapped, max_tokens=max_tokens)]


def _from_zip(path: Path, *, max_tokens: int) -> list[str]:
    from data_pipeline.import_zip import import_takehome_zip

    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        import_takehome_zip(path, dest_root=dest)
        docs = select_corpus_docs(
            iter_corpus_docs(_dataset_roots(dest)), max_tokens=max_tokens
        )
        return [doc.text for doc in docs]
