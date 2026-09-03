"""Byte-level BPE and from-scratch token budget."""

from __future__ import annotations

from pathlib import Path

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
    for name in ("100m_scratch", "5b_mac_scratch", "7b_scratch", "70b_scratch"):
        recipe = load_scratch_recipe(name)
        assert recipe.max_tokens == 1_000_000
        assert recipe.max_tokens <= ScratchRecipe.HARD_TOKEN_CAP
        plan = plan_scratch(recipe)
        assert plan.init == "random"
        assert plan.base_model is None
        assert plan.fits_node is True


def test_70b_scratch_is_200k_with_cpu_offload() -> None:
    recipe = load_scratch_recipe("70b_scratch")
    assert recipe.context_length == 200_000
    assert recipe.cpu_offload is True
    for name in ("100m_scratch", "7b_scratch"):
        small = load_scratch_recipe(name)
        assert small.context_length == 5120
        assert small.cpu_offload is False
    recipe = load_scratch_recipe("70b_scratch")
    assert recipe.zero_stage == 3
    assert recipe.n_params >= 70_000_000_000
    assert recipe.fits_node()


def test_5b_mac_scratch_is_cpu_ssd_offload() -> None:
    recipe = load_scratch_recipe("5b_mac_scratch")
    assert 5_000_000_000 <= recipe.n_params < 6_000_000_000
    assert recipe.context_length == 5120
    assert recipe.gpu_type_id == "CPU"
    assert recipe.disk_offload is True
    assert recipe.cpu_offload is False
    assert recipe.gpu_count == 1
    assert recipe.zero_stage == 0
    assert recipe.checkpoint_every == 10
    plan = plan_scratch(recipe)
    assert plan.fits_node is True
    assert plan.init == "random"


def test_cpu_disk_offload_is_available_without_cuda() -> None:
    pytest.importorskip("torch")
    from pretrain.train import _accelerator_available

    assert _accelerator_available("CPU") is True


def test_70b_scratch_refuses_single_process_launch() -> None:
    from pretrain.runtime import require_distributed_70b

    require_distributed_70b(100_000_000, 2, env={})
    with pytest.raises(RuntimeError, match="deepspeed --num_gpus 8 --module"):
        require_distributed_70b(70_000_000_000, 3, env={})
    require_distributed_70b(70_000_000_000, 3, env={"LOCAL_RANK": "0"})


def test_70b_long_context_chunks_mlp_attention_and_logits() -> None:
    src = (Path(__file__).resolve().parents[1] / "pretrain" / "llama.py").read_text()
    assert "SEQ_CHUNK = 512" in src
    assert "x.split(chunk, dim=1)" in src
    assert "_tiled_causal_attn" in src
    assert "_ChunkedTiledAttn" in src
    assert "_sdpa_gqa" not in src
    assert "scaled_dot_product_attention" not in src
    assert "cpu_checkpointing" in (
        Path(__file__).resolve().parents[1] / "pretrain" / "runtime.py"
    ).read_text()
    assert 'reduction="sum"' in src
    assert "self.lm_head(pred[:, i : i + chunk])" in src
    # Full-seq SwiGLU (the first 8× H200 OOM) must not be the only path.
    assert "for sl in x.split(chunk, dim=1)" in src
    runtime_src = (Path(__file__).resolve().parents[1] / "pretrain" / "runtime.py").read_text()
    assert "run_disk_offload" in runtime_src


def test_disk_offload_store_trains_one_step_and_resumes(tmp_path: Path) -> None:
    torch = pytest.importorskip("torch")
    from pretrain.disk_offload import (
        DiskLayerStore,
        apply_adam,
        stream_microbatch,
    )
    from pretrain.llama import LlamaBuild, llama_parts

    spec = LlamaBuild(
        n_layers=2,
        hidden_size=32,
        n_heads=4,
        n_kv_heads=2,
        head_dim=8,
        intermediate_size=64,
        vocab_size=17,
        context_length=16,
    )
    parts = llama_parts(spec)
    store = DiskLayerStore(tmp_path / "offload", spec)
    store.initialize(parts)
    assert store.block_path(0).is_file()
    assert store.block_path(1).is_file()
    assert store.embed_path().is_file()
    before = store.load_tensor_tree(store.embed_path())["weight"].clone()
    ids = torch.randint(1, spec.vocab_size, (1, spec.context_length))
    loss = stream_microbatch(store, spec, parts, ids, ids.clone())
    assert torch.isfinite(torch.tensor(loss))
    apply_adam(
        store,
        spec,
        parts,
        lr=1e-3,
        weight_decay=0.1,
        opt_step=1,
        grad_scale=1.0,
    )
    after = store.load_tensor_tree(store.embed_path())["weight"]
    assert not torch.equal(before, after)
    store.save_counters(1, 1)
    step, opt_step = DiskLayerStore(tmp_path / "offload", spec).load_counters()
    assert step == 1
    assert opt_step == 1
    resumed = DiskLayerStore(tmp_path / "offload", spec)
    embed = resumed.load_embed()
    assert torch.equal(embed.weight.detach(), after)


def test_zero3_init_offloads_70b_to_cpu() -> None:
    from pretrain.runtime import build_zero3_config, zero_init_kwargs

    recipe = load_scratch_recipe("70b_scratch")
    cfg = build_zero3_config(recipe, world=8)
    zero = cfg["zero_optimization"]
    assert zero["stage"] == 3
    assert zero["overlap_comm"] is False
    assert zero["stage3_param_persistence_threshold"] == 0
    assert zero["offload_param"]["device"] == "cpu"
    assert zero["offload_optimizer"]["device"] == "cpu"
    assert cfg["activation_checkpointing"]["cpu_checkpointing"] is True
    kwargs = zero_init_kwargs(recipe, cfg)
    assert kwargs["remote_device"] == "cpu"
    assert kwargs["pin_memory"] is True
    assert kwargs["config_dict_or_path"] is cfg
    runtime_src = (Path(__file__).resolve().parents[1] / "pretrain" / "runtime.py").read_text()
    assert "deepspeed.zero.Init(dtype=torch.bfloat16)" not in runtime_src


def test_tiny_chunked_causal_lm_loss_is_finite() -> None:
    torch = pytest.importorskip("torch")
    from pretrain.llama import SEQ_CHUNK, LlamaBuild, build_llama

    spec = LlamaBuild(
        n_layers=1,
        hidden_size=32,
        n_heads=4,
        n_kv_heads=2,
        head_dim=8,
        intermediate_size=64,
        vocab_size=17,
        context_length=SEQ_CHUNK * 2,
    )
    model = build_llama(spec)
    model.train()
    seq = SEQ_CHUNK + 8
    ids = torch.randint(1, spec.vocab_size, (1, seq))
    _, loss = model(ids, ids)
    assert loss is not None
    assert torch.isfinite(loss)
    loss.backward()
    assert any(p.grad is not None and p.grad.abs().sum() > 0 for p in model.parameters())
