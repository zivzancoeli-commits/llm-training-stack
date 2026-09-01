"""YAML profiles are the knobs you should edit. These tests catch illegal edits."""

from __future__ import annotations

import pytest

from specs.contracts.attention_shapes import validate_head_config
from specs.profiles import LONG_CONTEXT, PRETRAIN_CONTEXT, load_all_profiles, load_profile


def test_all_pretrain_profiles_are_5k_context() -> None:
    profiles = load_all_profiles()
    assert set(profiles) >= {"100m", "1b", "7b", "70b", "200b"}
    for name, prof in profiles.items():
        assert prof["context_length"] == PRETRAIN_CONTEXT, name


def test_only_200b_declares_350k_extension() -> None:
    small = load_profile("7b")
    big = load_profile("200b")
    assert small.get("context_length_extension") in (None, "")
    assert big["context_length_extension"] == LONG_CONTEXT
    assert big["context_length"] == PRETRAIN_CONTEXT


def test_gqa_heads_divide(profile_stem: str) -> None:
    prof = load_profile(profile_stem)
    validate_head_config(
        n_heads=int(prof["n_heads"]),
        n_kv_heads=int(prof["n_kv_heads"]),
        head_dim=int(prof["head_dim"]),
    )


def test_reasoning_mix_is_present() -> None:
    for name in ("100m", "1b", "7b"):
        mix = float(load_profile(name)["reasoning_mix_ratio"])
        assert 0.2 <= mix <= 0.8, name


@pytest.fixture(params=["100m", "1b", "7b", "70b", "200b"])
def profile_stem(request: pytest.FixtureRequest) -> str:
    return request.param
