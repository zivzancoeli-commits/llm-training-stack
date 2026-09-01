"""Byte-level BPE and from-scratch token budget."""

from __future__ import annotations

import pytest

from data_pipeline.tokenization.bpe import Tokenizer, pack_ids, train_bpe
from data_pipeline.token_budget import HARD_TOKEN_CAP, PREFERRED_TOKEN_BUDGET
from pretrain.corpus import select_texts
from pretrain.planner import plan_scratch
from pretrain.recipes import ScratchRecipe, load_scratch_recipe


def test_bpe_roundtrip_and_pack() -> None:
    vocab = train_bpe(["hello world hello", "world hello"], vocab_size=300, max_chars=200)
    tok = Tokenizer(vocab)
    ids = tok.encode("hello")
    assert ids[0] == tok.bos_id
    assert ids[-1] == tok.eos_id
    rows = pack_ids([1, 2, 3, 4, 5], seq_len=4, pad_id=0)
    assert rows[0] == [1, 2, 3, 4]
    assert rows[1] == [5, 0, 0, 0]


def test_select_texts_prefers_one_million() -> None:
    docs = ["word " * 800 for _ in range(4000)]
    chosen = select_texts(docs, max_tokens=PREFERRED_TOKEN_BUDGET)
    used = int(sum(len(t.split()) * 1.3 for t in chosen))
    assert used <= PREFERRED_TOKEN_BUDGET + 2000
    assert used > 500_000
    assert PREFERRED_TOKEN_BUDGET == 1_000_000
    assert HARD_TOKEN_CAP == 2_500_000


def test_scratch_recipes_are_random_init_and_capped() -> None:
    for name in ("100m_scratch", "7b_scratch", "70b_scratch"):
        recipe = load_scratch_recipe(name)
        assert recipe.max_tokens == 1_000_000
        assert recipe.max_tokens <= ScratchRecipe.HARD_TOKEN_CAP
        plan = plan_scratch(recipe)
        assert plan.init == "random"
        assert plan.base_model is None
        assert plan.fits_node is True


def test_70b_scratch_fits_8x_h200() -> None:
    recipe = load_scratch_recipe("70b_scratch")
    assert recipe.zero_stage == 3
    assert recipe.n_params >= 70_000_000_000
    assert recipe.fits_node()


def test_70b_scratch_refuses_single_process_launch() -> None:
    from pretrain.runtime import require_distributed_70b

    require_distributed_70b(100_000_000, 2, env={})
    with pytest.raises(RuntimeError, match="deepspeed --num_gpus 8"):
        require_distributed_70b(70_000_000_000, 3, env={})
    require_distributed_70b(70_000_000_000, 3, env={"LOCAL_RANK": "0"})
