"""Parse and catalog scratch70b_v0 markdown documents."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

DATASET_DIR = Path(__file__).resolve().parent
CATEGORIES = (
    "math",
    "code",
    "science",
    "logic",
    "world",
    "how_things_work",
    "reasoning_habits",
)
DIFFICULTIES = ("easy", "medium", "hard")
SOURCE_MODELS = ("fable-5", "opus-5", "cursor-grok")
REASONING_CATEGORIES = frozenset(
    {"math", "code", "science", "logic", "reasoning_habits"}
)
KNOWLEDGE_CATEGORIES = frozenset({"world", "how_things_work"})
MAX_APPROX_WORDS = 1800
MAX_CONTEXT_TOKENS = 5120


@dataclass(frozen=True)
class Document:
    id: str
    category: str
    subcategory: str
    difficulty: str
    source_model: str
    title: str
    skills: tuple[str, ...]
    approx_words: int
    path: str
    body: str

    @property
    def bucket(self) -> str:
        if self.category in REASONING_CATEGORIES:
            return "reasoning"
        if self.category in KNOWLEDGE_CATEGORIES:
            return "knowledge"
        raise ValueError(f"uncategorized {self.category}")

    def to_record(self) -> dict[str, Any]:
        rec = asdict(self)
        rec["skills"] = list(self.skills)
        rec["bucket"] = self.bucket
        rec["text"] = f"# {self.title}\n\n{self.body.strip()}\n"
        return rec


def _parse_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    if not raw.startswith("---"):
        raise ValueError("document must start with YAML frontmatter")
    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise ValueError("unterminated frontmatter")
    import yaml

    meta = yaml.safe_load(parts[1]) or {}
    if not isinstance(meta, dict):
        raise ValueError("frontmatter must be a mapping")
    return meta, parts[2].lstrip("\n")


def parse_document(path: Path) -> Document:
    meta, body = _parse_frontmatter(path.read_text(encoding="utf-8"))
    skills = meta.get("skills") or []
    if isinstance(skills, str):
        skills = [skills]
    doc = Document(
        id=str(meta["id"]),
        category=str(meta["category"]),
        subcategory=str(meta.get("subcategory") or "general"),
        difficulty=str(meta["difficulty"]),
        source_model=str(meta["source_model"]),
        title=str(meta["title"]),
        skills=tuple(str(s) for s in skills),
        approx_words=int(meta.get("approx_words") or len(body.split())),
        path=str(path.relative_to(DATASET_DIR)),
        body=body,
    )
    validate_document(doc)
    return doc


def validate_document(doc: Document) -> None:
    if doc.category not in CATEGORIES:
        raise ValueError(f"{doc.id}: bad category {doc.category!r}")
    if doc.difficulty not in DIFFICULTIES:
        raise ValueError(f"{doc.id}: bad difficulty {doc.difficulty!r}")
    if doc.source_model not in SOURCE_MODELS:
        raise ValueError(f"{doc.id}: bad source_model {doc.source_model!r}")
    if not doc.title.strip():
        raise ValueError(f"{doc.id}: empty title")
    words = len(doc.body.split())
    if words < 120:
        raise ValueError(f"{doc.id}: body too short ({words} words)")
    if words > MAX_APPROX_WORDS:
        raise ValueError(f"{doc.id}: body too long ({words} words)")
    # Crude token ceiling: ~1.3 tokens/word plus title.
    if int(words * 1.3) + 32 > MAX_CONTEXT_TOKENS:
        raise ValueError(f"{doc.id}: would not fit in {MAX_CONTEXT_TOKENS} context")
    lowered = doc.body.lower()
    if "lorem ipsum" in lowered:
        raise ValueError(f"{doc.id}: placeholder lorem text")


def iter_document_paths(root: Path = DATASET_DIR) -> list[Path]:
    paths: list[Path] = []
    for category in CATEGORIES:
        folder = root / category
        if folder.is_dir():
            paths.extend(sorted(folder.glob("*.md")))
    return paths


def load_all(root: Path = DATASET_DIR) -> list[Document]:
    docs = [parse_document(path) for path in iter_document_paths(root)]
    ids = [d.id for d in docs]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate document ids")
    return docs


def mix_counts(docs: list[Document]) -> dict[str, int]:
    counts = {"reasoning": 0, "knowledge": 0}
    for doc in docs:
        counts[doc.bucket] += 1
    return counts


def write_export(docs: list[Document], dest: Path | None = None) -> Path:
    dest = dest or (DATASET_DIR / "export" / "scratch70b_v0.jsonl")
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8") as fh:
        for doc in docs:
            fh.write(json.dumps(doc.to_record(), ensure_ascii=False) + "\n")
    catalog = dest.with_suffix(".catalog.json")
    catalog.write_text(
        json.dumps(
            {
                "n_docs": len(docs),
                "mix": mix_counts(docs),
                "by_category": _by_category(docs),
                "docs": [
                    {
                        "id": d.id,
                        "category": d.category,
                        "title": d.title,
                        "difficulty": d.difficulty,
                        "source_model": d.source_model,
                        "path": d.path,
                        "words": len(d.body.split()),
                    }
                    for d in docs
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return dest


def _by_category(docs: list[Document]) -> dict[str, int]:
    out: dict[str, int] = {c: 0 for c in CATEGORIES}
    for doc in docs:
        out[doc.category] += 1
    return out
