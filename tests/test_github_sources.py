"""GitHub clone URLs the pod actually uses."""

from data_pipeline.github_sources import (
    DEFAULT_DATASET_GIT_URL,
    DEFAULT_TRAINING_GIT_URL,
    authed_clone_url,
)


def test_dataset_repo_is_the_one_the_user_pushed() -> None:
    assert DEFAULT_DATASET_GIT_URL == (
        "https://github.com/zivzancoeli-commits/llm-dataset.git"
    )
    assert DEFAULT_TRAINING_GIT_URL == (
        "https://github.com/zivzancoeli-commits/llm-training-stack.git"
    )


def test_authed_clone_url_inserts_pat() -> None:
    raw = DEFAULT_DATASET_GIT_URL
    assert authed_clone_url(raw, None) == raw
    assert authed_clone_url(raw, "ghp_x") == (
        "https://x-access-token:ghp_x@github.com/zivzancoeli-commits/llm-dataset.git"
    )
