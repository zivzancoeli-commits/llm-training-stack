"""1M preferred, 2.5M hard cap — packing never aims at the hard cap."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from data_pipeline.token_budget import (
    HARD_TOKEN_CAP,
    PREFERRED_TOKEN_BUDGET,
    heuristic_tokens,
    require_token_budget,
    select_round_robin,
)
from pretrain.corpus import (
    CorpusDoc,
    select_corpus_docs,
    select_texts,
)
from pretrain.recipes import ScratchRecipe, load_scratch_recipe


def test_preferred_is_one_million_or_less_and_hard_cap_is_2p5m() -> None:
    assert PREFERRED_TOKEN_BUDGET == 1_000_000
    assert HARD_TOKEN_CAP == 2_500_000
    assert PREFERRED_TOKEN_BUDGET < HARD_TOKEN_CAP
    assert ScratchRecipe.HARD_TOKEN_CAP == HARD_TOKEN_CAP


def test_require_token_budget_rejects_over_hard_cap() -> None:
    with pytest.raises(ValueError, match="hard cap"):
        require_token_budget(HARD_TOKEN_CAP + 1)
    assert require_token_budget(HARD_TOKEN_CAP) == HARD_TOKEN_CAP
    assert require_token_budget(PREFERRED_TOKEN_BUDGET) == PREFERRED_TOKEN_BUDGET


def test_select_texts_stays_at_or_under_preferred() -> None:
    docs = ["word " * 800 for _ in range(4000)]
    chosen = select_texts(docs, max_tokens=PREFERRED_TOKEN_BUDGET)
    used = sum(heuristic_tokens(t) for t in chosen)
    assert used <= PREFERRED_TOKEN_BUDGET + heuristic_tokens(docs[0])
    assert used > 500_000


def test_select_texts_rejects_over_hard_cap() -> None:
    with pytest.raises(ValueError, match="hard cap"):
        select_texts(["hello"], max_tokens=HARD_TOKEN_CAP + 1)


def test_round_robin_keeps_mix_under_a_small_budget() -> None:
    items = (
        [("speech", "chat " * 80)] * 40
        + [("reasoning", "math " * 80)] * 40
        + [("knowledge", "world " * 80)] * 20
    )
    chosen = select_round_robin(
        items,
        bucket_of=lambda item: item[0],
        tokens_of=lambda item: heuristic_tokens(item[1]),
        max_tokens=8_000,
    )
    used = sum(heuristic_tokens(text) for _, text in chosen)
    assert used <= 8_000
    buckets = Counter(bucket for bucket, _ in chosen)
    assert buckets["reasoning"] >= buckets["speech"]
    assert buckets["speech"] > buckets["knowledge"]
    assert buckets["knowledge"] > 0


def test_select_corpus_docs_does_not_fill_with_chat_only() -> None:
    docs = [
        CorpusDoc(
            path=Path(f"{bucket}-{i}.md"),
            category={"speech": "chat", "reasoning": "math", "knowledge": "world"}[bucket],
            bucket=bucket,
            text=("token " * 100),
        )
        for bucket, n in (("speech", 80), ("reasoning", 80), ("knowledge", 40))
        for i in range(n)
    ]
    chosen = select_corpus_docs(docs, max_tokens=20_000)
    used = sum(d.heuristic_tokens() for d in chosen)
    assert used <= 20_000
    buckets = Counter(d.bucket for d in chosen)
    assert buckets["reasoning"] >= buckets["speech"]
    assert buckets["knowledge"] > 0


def test_scratch_recipes_default_to_one_million_not_two_point_five() -> None:
    for name in ("100m_scratch", "7b_scratch", "70b_scratch"):
        recipe = load_scratch_recipe(name)
        assert recipe.max_tokens == PREFERRED_TOKEN_BUDGET
        assert recipe.max_tokens < ScratchRecipe.HARD_TOKEN_CAP
