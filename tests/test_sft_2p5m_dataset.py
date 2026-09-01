"""sft mix documents must stay unique, tagged, and under 5,120 tokens."""

from __future__ import annotations

import json
from pathlib import Path

from data_pipeline.datasets.scratch70b_sft_2p5m.catalog import (
    CATEGORIES,
    MAX_TOKENS,
    TARGET_TOKENS,
    heuristic_token_total,
    load_all,
    mix_counts,
    select_for_budget,
    write_export,
)
from data_pipeline.datasets.scratch70b_sft_2p5m.generate_topics import (
    DOCS_PER_BATCH,
    QUOTAS,
    build_topics,
)
from data_pipeline.token_budget import HARD_TOKEN_CAP, PREFERRED_TOKEN_BUDGET


def test_topic_bank_hits_the_1m_doc_quota() -> None:
    topics = build_topics()
    assert len(topics) == sum(QUOTAS.values()) == 1056
    ids = [t["id"] for t in topics]
    assert len(ids) == len(set(ids))
    by_cat = {c: 0 for c in CATEGORIES}
    for t in topics:
        by_cat[str(t["category"])] += 1
    assert by_cat == QUOTAS
    assert len(topics) % DOCS_PER_BATCH == 0
    on_disk = Path(__file__).resolve().parents[1] / (
        "data_pipeline/datasets/scratch70b_sft_2p5m/topics.jsonl"
    )
    rows = [json.loads(line) for line in on_disk.read_text().splitlines() if line.strip()]
    assert len(rows) == 1056


def test_written_docs_validate_if_present(tmp_path) -> None:
    docs = load_all()
    ids = [d.id for d in docs]
    assert len(ids) == len(set(ids))
    for doc in docs:
        assert doc.source_model == "cursor-grok"
        assert doc.heuristic_tokens() <= 5120
    if docs:
        dest = write_export(docs, dest=tmp_path / "out.jsonl")
        assert dest.is_file()
        mix = mix_counts(docs)
        assert set(mix) == {"speech", "reasoning", "knowledge"}


def test_target_token_constant() -> None:
    assert TARGET_TOKENS == PREFERRED_TOKEN_BUDGET == 1_000_000
    assert MAX_TOKENS == HARD_TOKEN_CAP == 2_500_000
    assert TARGET_TOKENS < MAX_TOKENS


def test_on_disk_mix_stays_under_hard_cap_and_packs_at_or_under_1m(tmp_path) -> None:
    docs = load_all()
    assert heuristic_token_total(docs) <= MAX_TOKENS
    packed = select_for_budget(docs)
    assert heuristic_token_total(packed) <= TARGET_TOKENS
    dest = write_export(docs, dest=tmp_path / "out.jsonl")
    n_lines = sum(1 for line in dest.read_text(encoding="utf-8").splitlines() if line.strip())
    assert n_lines == len(packed)

