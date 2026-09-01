"""Byte-level BPE. No Hugging Face, no downloaded vocab."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

PAD, BOS, EOS, UNK = "<pad>", "<bos>", "<eos>", "<unk>"
SPECIAL = (PAD, BOS, EOS, UNK)
BYTE_OFFSET = len(SPECIAL)  # 0..3 specials, 4..259 bytes


@dataclass(frozen=True)
class BpeVocab:
    vocab_size: int
    merges: tuple[tuple[int, int], ...]
    token_to_id: dict[str, int]

    def to_json(self) -> dict:
        return {
            "vocab_size": self.vocab_size,
            "merges": [list(m) for m in self.merges],
            "token_to_id": self.token_to_id,
        }

    @classmethod
    def from_json(cls, data: dict) -> BpeVocab:
        merges = tuple((int(a), int(b)) for a, b in data["merges"])
        return cls(
            vocab_size=int(data["vocab_size"]),
            merges=merges,
            token_to_id={str(k): int(v) for k, v in data["token_to_id"].items()},
        )


def _pair_key(a: int, b: int) -> tuple[int, int]:
    return (a, b)


def train_bpe(texts: list[str], vocab_size: int = 32000, max_chars: int = 2_000_000) -> BpeVocab:
    """Train merges on UTF-8 bytes. ``vocab_size`` includes 4 specials + 256 bytes."""
    if vocab_size < BYTE_OFFSET + 256:
        raise ValueError("vocab_size must be at least 260 (specials + bytes)")
    blob = "\n".join(texts)
    raw = blob.encode("utf-8")[:max_chars]
    symbols = [BYTE_OFFSET + b for b in raw]
    merges: list[tuple[int, int]] = []
    next_id = BYTE_OFFSET + 256
    target_merges = vocab_size - next_id
    while len(merges) < target_merges and len(symbols) >= 2:
        counts: Counter[tuple[int, int]] = Counter()
        for i in range(len(symbols) - 1):
            counts[_pair_key(symbols[i], symbols[i + 1])] += 1
        if not counts:
            break
        pair, freq = counts.most_common(1)[0]
        if freq < 2:
            break
        merges.append(pair)
        symbols = _merge(symbols, pair, next_id)
        next_id += 1
    token_to_id = {name: i for i, name in enumerate(SPECIAL)}
    return BpeVocab(vocab_size=vocab_size, merges=tuple(merges), token_to_id=token_to_id)


def _merge(symbols: list[int], pair: tuple[int, int], new_id: int) -> list[int]:
    out: list[int] = []
    i = 0
    a, b = pair
    while i < len(symbols):
        if i < len(symbols) - 1 and symbols[i] == a and symbols[i + 1] == b:
            out.append(new_id)
            i += 2
        else:
            out.append(symbols[i])
            i += 1
    return out


class Tokenizer:
    def __init__(self, vocab: BpeVocab):
        self.vocab = vocab
        self.pad_id = vocab.token_to_id[PAD]
        self.bos_id = vocab.token_to_id[BOS]
        self.eos_id = vocab.token_to_id[EOS]
        self.unk_id = vocab.token_to_id[UNK]
        self._merge_ranks = {pair: i for i, pair in enumerate(vocab.merges)}

    def encode(self, text: str, *, add_special: bool = True) -> list[int]:
        ids = [BYTE_OFFSET + b for b in text.encode("utf-8")]
        ids = self._apply_merges(ids)
        if add_special:
            return [self.bos_id, *ids, self.eos_id]
        return ids

    def _apply_merges(self, ids: list[int]) -> list[int]:
        if not self._merge_ranks:
            return ids
        while True:
            best_i = -1
            best_rank = 10**18
            for i in range(len(ids) - 1):
                rank = self._merge_ranks.get((ids[i], ids[i + 1]))
                if rank is not None and rank < best_rank:
                    best_rank = rank
                    best_i = i
            if best_i < 0:
                return ids
            a, b = ids[best_i], ids[best_i + 1]
            new_id = BYTE_OFFSET + 256 + self._merge_ranks[(a, b)]
            ids = ids[:best_i] + [new_id] + ids[best_i + 2 :]

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.vocab.to_json(), indent=2) + "\n")

    @classmethod
    def load(cls, path: Path) -> Tokenizer:
        return cls(BpeVocab.from_json(json.loads(path.read_text())))


def pack_ids(ids: list[int], seq_len: int = 5120, pad_id: int = 0) -> list[list[int]]:
    """Split a stream into ``seq_len`` rows, padding the last row."""
    if seq_len <= 0:
        raise ValueError("seq_len must be positive")
    rows: list[list[int]] = []
    for start in range(0, len(ids), seq_len):
        chunk = ids[start : start + seq_len]
        if len(chunk) < seq_len:
            chunk = chunk + [pad_id] * (seq_len - len(chunk))
        rows.append(chunk)
    return rows or [[pad_id] * seq_len]
