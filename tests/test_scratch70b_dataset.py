"""scratch70b_v0 must stay reviewable, unique, and under 5,120 tokens."""

from __future__ import annotations

from collections import Counter

from data_pipeline.datasets.scratch70b_v0.catalog import (
    CATEGORIES,
    load_all,
    mix_counts,
    write_export,
)


def test_seed_has_full_id_coverage() -> None:
    docs = load_all()
    ids = {d.id for d in docs}
    expected = set()
    expected.update(f"math-{i:03d}" for i in range(1, 19))
    expected.update(f"code-{i:03d}" for i in range(1, 19))
    expected.update(f"science-{i:03d}" for i in range(1, 17))
    expected.update(f"logic-{i:03d}" for i in range(1, 15))
    expected.update(f"habits-{i:03d}" for i in range(1, 15))
    expected.update(f"world-{i:03d}" for i in range(1, 19))
    expected.update(f"how-{i:03d}" for i in range(1, 17))
    assert ids == expected


def test_reasoning_is_the_majority() -> None:
    docs = load_all()
    mix = mix_counts(docs)
    assert mix["reasoning"] > mix["knowledge"]
    assert mix["reasoning"] / len(docs) >= 0.60


def test_every_category_is_present() -> None:
    counts = Counter(d.category for d in load_all())
    for category in CATEGORIES:
        assert counts[category] >= 10, category


def test_export_roundtrip(tmp_path) -> None:
    dest = write_export(load_all(), dest=tmp_path / "out.jsonl")
    lines = dest.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 114
    catalog = dest.with_suffix(".catalog.json")
    assert catalog.is_file()
