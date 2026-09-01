"""From-scratch token budget: 1M preferred, 2.5M hard cap.

Packing and recipes default to the preferred budget. Writers must not
keep filling toward the hard cap. Training on 1M tokens (or fewer) is a
systems smoke, not a Chinchilla run.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Callable, TypeVar

PREFERRED_TOKEN_BUDGET = 1_000_000
HARD_TOKEN_CAP = 2_500_000
TOKENS_PER_WORD = 1.3
DOC_OVERHEAD_TOKENS = 32

SPEECH_CATEGORIES = frozenset({"chat"})
REASONING_CATEGORIES = frozenset(
    {"math", "code", "science", "logic", "reasoning_habits"}
)
KNOWLEDGE_CATEGORIES = frozenset({"world", "how_things_work"})

# ~35% speech / ~50% reasoning / ~15% knowledge when the packer has to cut.
MIX_SCHEDULE = ("speech",) * 7 + ("reasoning",) * 10 + ("knowledge",) * 3

T = TypeVar("T")


def require_token_budget(max_tokens: int) -> int:
    if max_tokens > HARD_TOKEN_CAP:
        raise ValueError(
            f"max_tokens {max_tokens} exceeds the {HARD_TOKEN_CAP} hard cap; "
            f"preferred budget is {PREFERRED_TOKEN_BUDGET} or less"
        )
    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    return max_tokens


def heuristic_tokens(text: str) -> int:
    return int(len(text.split()) * TOKENS_PER_WORD) + DOC_OVERHEAD_TOKENS


def bucket_for_category(category: str) -> str:
    if category in SPEECH_CATEGORIES:
        return "speech"
    if category in REASONING_CATEGORIES:
        return "reasoning"
    if category in KNOWLEDGE_CATEGORIES:
        return "knowledge"
    return "reasoning"


def select_round_robin(
    items: list[T],
    *,
    bucket_of: Callable[[T], str],
    tokens_of: Callable[[T], int],
    max_tokens: int,
) -> list[T]:
    """Keep a mix while staying at or under ``max_tokens`` (1M or less)."""
    max_tokens = require_token_budget(max_tokens)
    by_bucket: dict[str, deque[T]] = defaultdict(deque)
    for item in items:
        by_bucket[bucket_of(item)].append(item)
    chosen: list[T] = []
    used = 0
    while True:
        progressed = False
        for bucket in MIX_SCHEDULE:
            queue = by_bucket.get(bucket)
            if not queue:
                continue
            item = queue[0]
            cost = tokens_of(item)
            if chosen and used + cost > max_tokens:
                queue.popleft()
                progressed = True
                continue
            queue.popleft()
            chosen.append(item)
            used += cost
            progressed = True
            if used >= max_tokens:
                return chosen
        if not progressed:
            return chosen
