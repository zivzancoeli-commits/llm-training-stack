"""Llama-like causal LM. Torch is imported only when a trainer asks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pretrain.recipes import ScratchRecipe


@dataclass(frozen=True)
class LlamaBuild:
    n_layers: int
    hidden_size: int
    n_heads: int
    n_kv_heads: int
    head_dim: int
    intermediate_size: int
    vocab_size: int
    context_length: int

    @classmethod
    def from_recipe(cls, recipe: ScratchRecipe) -> LlamaBuild:
        return cls(
            n_layers=recipe.n_layers,
            hidden_size=recipe.hidden_size,
            n_heads=recipe.n_heads,
            n_kv_heads=recipe.n_kv_heads,
            head_dim=recipe.head_dim,
            intermediate_size=recipe.intermediate_size,
            vocab_size=recipe.vocab_size,
            context_length=recipe.context_length,
        )


def build_llama(spec: LlamaBuild) -> Any:
    """Construct a randomly initialized causal LM. Requires torch."""
    import math

    import torch
    from torch import nn
    from torch.nn import functional as F

    if spec.hidden_size != spec.n_heads * spec.head_dim:
        raise ValueError("hidden_size must equal n_heads * head_dim")
    if spec.n_heads % spec.n_kv_heads != 0:
        raise ValueError("n_heads must be divisible by n_kv_heads")
    n_rep = spec.n_heads // spec.n_kv_heads

    class RMSNorm(nn.Module):
        def __init__(self, dim: int, eps: float = 1e-6):
            super().__init__()
            self.eps = eps
            self.weight = nn.Parameter(torch.ones(dim))

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            norm = x.pow(2).mean(dim=-1, keepdim=True).add(self.eps).rsqrt()
            return self.weight * x * norm

    class Attention(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.q = nn.Linear(spec.hidden_size, spec.n_heads * spec.head_dim, bias=False)
            self.k = nn.Linear(spec.hidden_size, spec.n_kv_heads * spec.head_dim, bias=False)
            self.v = nn.Linear(spec.hidden_size, spec.n_kv_heads * spec.head_dim, bias=False)
            self.o = nn.Linear(spec.hidden_size, spec.hidden_size, bias=False)
            inv = 1.0 / (10000 ** (torch.arange(0, spec.head_dim, 2).float() / spec.head_dim))
            self.register_buffer("inv_freq", inv, persistent=False)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            b, s, _ = x.shape
            q = self.q(x).view(b, s, spec.n_heads, spec.head_dim)
            k = self.k(x).view(b, s, spec.n_kv_heads, spec.head_dim)
            v = self.v(x).view(b, s, spec.n_kv_heads, spec.head_dim)
            t = torch.arange(s, device=x.device, dtype=self.inv_freq.dtype)
            freqs = torch.outer(t, self.inv_freq)
            cos = torch.cos(freqs).to(x.dtype)
            sin = torch.sin(freqs).to(x.dtype)
            q = _apply_rope(q, cos, sin)
            k = _apply_rope(k, cos, sin)
            if n_rep > 1:
                k = k.repeat_interleave(n_rep, dim=2)
                v = v.repeat_interleave(n_rep, dim=2)
            y = F.scaled_dot_product_attention(
                q.transpose(1, 2),
                k.transpose(1, 2),
                v.transpose(1, 2),
                dropout_p=0.0,
                is_causal=True,
            )
            y = y.transpose(1, 2).contiguous().view(b, s, spec.hidden_size)
            return self.o(y)

    def _apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
        x1 = x[..., ::2]
        x2 = x[..., 1::2]
        cos = cos[None, :, None, :]
        sin = sin[None, :, None, :]
        out = torch.stack((x1 * cos - x2 * sin, x1 * sin + x2 * cos), dim=-1)
        return out.flatten(-2)

    class SwiGLU(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.up = nn.Linear(spec.hidden_size, spec.intermediate_size, bias=False)
            self.gate = nn.Linear(spec.hidden_size, spec.intermediate_size, bias=False)
            self.down = nn.Linear(spec.intermediate_size, spec.hidden_size, bias=False)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.down(F.silu(self.gate(x)) * self.up(x))

    class Block(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.n1 = RMSNorm(spec.hidden_size)
            self.attn = Attention()
            self.n2 = RMSNorm(spec.hidden_size)
            self.mlp = SwiGLU()

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            x = x + self.attn(self.n1(x))
            x = x + self.mlp(self.n2(x))
            return x

    class LlamaLM(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.embed = nn.Embedding(spec.vocab_size, spec.hidden_size)
            self.blocks = nn.ModuleList(Block() for _ in range(spec.n_layers))
            self.norm = RMSNorm(spec.hidden_size)
            self.lm_head = nn.Linear(spec.hidden_size, spec.vocab_size, bias=False)
            self.lm_head.weight = self.embed.weight
            self._reset()

        def _reset(self) -> None:
            std = 0.02
            nn.init.normal_(self.embed.weight, mean=0.0, std=std)
            for block in self.blocks:
                for linear in block.modules():
                    if isinstance(linear, nn.Linear):
                        nn.init.normal_(linear.weight, mean=0.0, std=std)

        def forward(self, input_ids: torch.Tensor, labels: torch.Tensor | None = None):
            x = self.embed(input_ids)
            for block in self.blocks:
                x = block(x)
            logits = self.lm_head(self.norm(x))
            loss = None
            if labels is not None:
                loss = F.cross_entropy(
                    logits[:, :-1, :].contiguous().view(-1, spec.vocab_size),
                    labels[:, 1:].contiguous().view(-1),
                    ignore_index=0,
                )
            return logits, loss

    _ = math  # kept for possible later μP scaling
    return LlamaLM()
