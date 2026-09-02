"""Public GitHub clone URLs the RunPod bootstrap uses.

RunPod cannot clone a Cursor codebase page. It needs GitHub HTTPS.
These repos live under ``zivzancoeli-commits`` and are **public**, so a
pod can ``git clone`` them without a token.
"""

from __future__ import annotations

DATASET_OWNER = "zivzancoeli-commits"
# Double dash is the repo the reviewed zip was uploaded to (not llm-dataset).
DATASET_REPO = "llm--dataset"
TRAINING_STACK_REPO = "llm-training-stack"

DEFAULT_DATASET_GIT_URL = f"https://github.com/{DATASET_OWNER}/{DATASET_REPO}.git"
DEFAULT_TRAINING_GIT_URL = f"https://github.com/{DATASET_OWNER}/{TRAINING_STACK_REPO}.git"

# Canonical name plus the macOS duplicate-download name from GitHub web.
TAKEHOME_ZIP_NAMES = (
    "scratch70b_1m_takehome.zip",
    "scratch70b_1m_takehome 2.zip",
)


def authed_clone_url(https_url: str, token: str | None) -> str:
    """Insert a PAT so ``git clone`` works on a private GitHub repo."""
    token = (token or "").strip()
    if not token:
        return https_url
    prefix = "https://"
    if https_url.startswith(prefix):
        return f"{prefix}x-access-token:{token}@{https_url[len(prefix):]}"
    return https_url
