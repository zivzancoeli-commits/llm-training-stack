"""CLI tour / check / ft-plan stay free of torch and of RunPod."""

from __future__ import annotations

import json

import pytest

from fine_tune.cli import main


def test_tour_lists_walkthrough(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["tour"]) == 0
    out = capsys.readouterr().out
    assert "WALKTHROUGH.md" in out
    assert "8x H200" in out
    assert "npx @runpod/mcp-server@latest add" in out


def test_scratch_plan_is_random_init(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["scratch-plan", "--recipe", "70b_scratch"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["init"] == "random"
    assert payload["base_model"] is None
    assert payload["max_tokens"] == 1_000_000
    assert payload["preferred_tokens"] == 1_000_000
    assert payload["hard_token_cap"] == 2_500_000
    assert payload["recipe"]["gpu_count"] == 8
    assert payload["recipe"]["context_length"] == 200000
    assert payload["recipe"]["cpu_offload"] is True


def test_ft_plan_json(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["ft-plan", "--recipe", "7b_lora"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["recipe"]["gpu_count"] == 8
    assert payload["recipe"]["context_length"] == 5120


def test_ft_launch_default_is_dry_run(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["ft-launch", "--recipe", "7b_full"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["dry_run"] is True
    assert payload["pod_id"] is None
    assert payload["body"]["gpuCount"] == 8


def test_ft_launch_rejects_a40_recipe(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["ft-launch", "--recipe", "70b_qlora_a40"]) == 2
    err = capsys.readouterr().err
    assert "H200" in err
    assert "A40" in err


def test_ft_launch_confirm_without_git_url_fails() -> None:
    assert main(["ft-launch", "--confirm", "--recipe", "7b_lora"]) == 2


def test_scratch_launch_default_is_dry_run_and_deepspeed(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["scratch-launch", "--recipe", "70b_scratch"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["dry_run"] is True
    assert payload["pod_id"] is None
    assert payload["body"]["gpuCount"] == 8
    assert payload["body"]["containerDiskInGb"] == 100
    assert payload["body"]["volumeInGb"] == 300
    joined = " ".join(payload["body"]["dockerStartCmd"])
    assert "pretrain.train" in joined
    assert "deepspeed" in joined
    assert "fine_tune.train" not in joined
    assert "github.com/zivzancoeli-commits/llm--dataset" in joined
    assert "find_takehome_zip" in joined
    assert payload["body"]["env"]["LMM_GIT_URL"] == (
        "https://github.com/zivzancoeli-commits/llm-training-stack.git"
    )


def test_scratch_launch_confirm_without_git_url_fails() -> None:
    assert main(["scratch-launch", "--confirm", "--recipe", "70b_scratch"]) == 2


def test_find_takehome_zip_macos_duplicate_name(tmp_path) -> None:
    from data_pipeline.import_zip import find_takehome_zip

    zipped = tmp_path / "scratch70b_1m_takehome 2.zip"
    zipped.write_bytes(b"PK\x03\x04")
    assert find_takehome_zip(tmp_path) == zipped.resolve()
    assert find_takehome_zip(zipped) == zipped.resolve()


def test_data_import_takehome_zip(tmp_path, monkeypatch, capsys: pytest.CaptureFixture[str]) -> None:
    from data_pipeline.import_zip import import_takehome_zip

    zip_path = tmp_path / "tiny.zip"
    src = tmp_path / "scratch70b_1m_takehome" / "scratch70b_v0" / "math"
    src.mkdir(parents=True)
    (src / "math-001.md").write_text(
        "---\nid: math-001\ncategory: math\ndifficulty: easy\n"
        "source_model: cursor-grok\ntitle: Tiny\napprox_words: 200\n"
        "skills: [worked-solution]\n---\n" + ("word " * 200)
    )
    import zipfile

    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(src / "math-001.md", arcname="scratch70b_1m_takehome/scratch70b_v0/math/math-001.md")
    dest = tmp_path / "datasets"
    leftover = dest / "scratch70b_v0" / "math" / "math-999.md"
    leftover.parent.mkdir(parents=True)
    leftover.write_text("# leftover\n")
    copied = import_takehome_zip(zip_path, dest_root=dest)
    assert copied["scratch70b_v0"] == 1
    assert (dest / "scratch70b_v0" / "math" / "math-001.md").is_file()
    assert not leftover.is_file()


def test_data_import_renames_chat_zero_to_frontmatter_id(tmp_path) -> None:
    from data_pipeline.import_zip import import_takehome_zip

    zip_path = tmp_path / "tiny.zip"
    src = tmp_path / "scratch70b_sft_2p5m" / "chat"
    src.mkdir(parents=True)
    body = "word " * 200
    (src / "chat-0.md").write_text(
        "---\nid: chat-0625\ncategory: chat\nsubcategory: everyday-dialogue\n"
        "difficulty: easy\nsource_model: cursor-grok\ntitle: Tiny\n"
        "approx_words: 200\nskills: [conversational]\n---\n" + body
    )
    import zipfile

    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(src / "chat-0.md", arcname="scratch70b_sft_2p5m/chat/chat-0.md")
    dest = tmp_path / "datasets"
    leftover = dest / "scratch70b_sft_2p5m" / "chat" / "chat-0628.md"
    leftover.parent.mkdir(parents=True)
    leftover.write_text("# leftover\n")
    copied = import_takehome_zip(zip_path, dest_root=dest)
    assert copied["scratch70b_sft_2p5m"] == 1
    assert (dest / "scratch70b_sft_2p5m" / "chat" / "chat-0625.md").is_file()
    assert not (dest / "scratch70b_sft_2p5m" / "chat" / "chat-0.md").is_file()
    assert not leftover.is_file()


def test_check_forwards_pytest_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[list[str]] = []

    def fake_call(cmd: list[str], cwd=None) -> int:
        seen.append(list(cmd))
        return 0

    monkeypatch.setattr("fine_tune.cli.subprocess.call", fake_call)
    assert main(["check", "-q", "tests/test_profiles.py"]) == 0
    assert seen[0][-2:] == ["-q", "tests/test_profiles.py"]
