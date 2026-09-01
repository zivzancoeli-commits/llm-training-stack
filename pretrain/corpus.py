"""Load markdown bodies and stop at the token budget (1M preferred, 2.5M hard)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from data_pipeline.token_budget import (
    HARD_TOKEN_CAP,
    PREFERRED_TOKEN_BUDGET,
    bucket_for_category,
    heuristic_tokens,
    require_token_budget,
    select_round_robin,
)
from data_pipeline.tokenization.bpe import Tokenizer, pack_ids, train_bpe

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASETS = (
    ROOT / "data_pipeline" / "datasets" / "scratch70b_v0",
    ROOT / "data_pipeline" / "datasets" / "scratch70b_sft_2p5m",
)
SKIP_NAMES = frozenset(
    {"README.md", "SCHEMA.md", "WRITER.md", "TAKE_HOME.md", "MIX_PLAN.md"}
)


@dataclass(frozen=True)
class CorpusDoc:
    path: Path
    category: str
    bucket: str
    text: str

    def heuristic_tokens(self) -> int:
        return heuristic_tokens(self.text)


def iter_corpus_docs(roots: tuple[Path, ...] = DEFAULT_DATASETS) -> list[CorpusDoc]:
    docs: list[CorpusDoc] = []
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            if path.name in SKIP_NAMES:
                continue
            raw = path.read_text(encoding="utf-8")
            text = _strip_frontmatter(raw)
            if not text:
                continue
            category = path.parent.name
            docs.append(
                CorpusDoc(
                    path=path,
                    category=category,
                    bucket=bucket_for_category(category),
                    text=text,
                )
            )
    on_disk = sum(d.heuristic_tokens() for d in docs)
    if on_disk > HARD_TOKEN_CAP:
        raise ValueError(
            f"on-disk corpus is {on_disk} heuristic tokens; "
            f"hard cap is {HARD_TOKEN_CAP}. Stop generating."
        )
    return docs


def iter_markdown_bodies(roots: tuple[Path, ...] = DEFAULT_DATASETS) -> list[str]:
    return [doc.text for doc in iter_corpus_docs(roots)]


def _strip_frontmatter(raw: str) -> str:
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return raw.strip()


def select_texts(texts: list[str], max_tokens: int = PREFERRED_TOKEN_BUDGET) -> list[str]:
    """Keep documents until the heuristic token budget is hit."""
    require_token_budget(max_tokens)
    chosen: list[str] = []
    used = 0
    for text in texts:
        if not text:
            continue
        cost = heuristic_tokens(text)
        if chosen and used + cost > max_tokens:
            break
        chosen.append(text)
        used += cost
        if used >= max_tokens:
            break
    return chosen


def select_corpus_docs(
    docs: list[CorpusDoc],
    max_tokens: int = PREFERRED_TOKEN_BUDGET,
) -> list[CorpusDoc]:
    """Round-robin mix so a 1M cap does not become chat-only."""
    return select_round_robin(
        docs,
        bucket_of=lambda doc: doc.bucket,
        tokens_of=lambda doc: doc.heuristic_tokens(),
        max_tokens=max_tokens,
    )


def tokenize_and_pack(
    texts: list[str],
    *,
    vocab_size: int,
    seq_len: int,
    max_tokens: int = PREFERRED_TOKEN_BUDGET,
    tokenizer: Tokenizer | None = None,
    docs: list[CorpusDoc] | None = None,
) -> tuple[Tokenizer, list[list[int]]]:
    require_token_budget(max_tokens)
    if docs is not None:
        chosen = [doc.text for doc in select_corpus_docs(docs, max_tokens=max_tokens)]
    else:
        chosen = select_texts(texts, max_tokens=max_tokens)
    if tokenizer is None:
        # Byte-level plus a small merge table trained on a cap of chars so
        # CPU encode stays usable. Unused embedding rows are fine.
        tokenizer = Tokenizer(train_bpe(chosen, vocab_size=vocab_size, max_chars=400_000))
    stream: list[int] = []
    for text in chosen:
        stream.extend(tokenizer.encode(text))
        if len(stream) >= max_tokens:
            stream = stream[:max_tokens]
            break
    rows = pack_ids(stream, seq_len=seq_len, pad_id=tokenizer.pad_id)
    return tokenizer, rows
