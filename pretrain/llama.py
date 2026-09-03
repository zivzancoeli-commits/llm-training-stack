"""Llama-like causal LM. Torch is imported only when a trainer asks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pretrain.recipes import ScratchRecipe

# 200k × 28,672 bf16 is ~11 GiB per MLP tensor; 200k × 32k logits ~12.8 GiB;
# expanding GQA K/V to 64 heads is another ~3 GiB each. Chunk the sequence
# and keep native GQA so 8× H200 can hold a training step.
SEQ_CHUNK = 512


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
    chunk = SEQ_CHUNK
    # 200k scratch uses a larger RoPE base so positions do not wrap as fast
    # as theta=10k. This is not YaRN / Phase-5 350k scaling.
    rope_base = 1_000_000.0 if spec.context_length >= 200_000 else 10_000.0

    class RMSNorm(nn.Module):
        def __init__(self, dim: int, eps: float = 1e-6):
            super().__init__()
            self.eps = eps
            self.weight = nn.Parameter(torch.ones(dim))

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            norm = x.pow(2).mean(dim=-1, keepdim=True).add(self.eps).rsqrt()
            return self.weight * x * norm

    def _apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
        x1 = x[..., ::2]
        x2 = x[..., 1::2]
        cos = cos[None, :, None, :]
        sin = sin[None, :, None, :]
        out = torch.stack((x1 * cos - x2 * sin, x1 * sin + x2 * cos), dim=-1)
        return out.flatten(-2)

    def _tiled_causal_attn(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
        """Causal GQA in 512×512 tiles. No SDPA (FLASH/GQA/Lq≠Lk has no kernel on H200)."""
        _, _, tq, d = q.shape
        tk = k.size(2)
        scale = d ** -0.5
        q_start = tk - tq
        qf = q.float()
        out = torch.zeros_like(qf)
        m = q.new_full((*q.shape[:3], 1), -1e9, dtype=torch.float32)
        denom = torch.zeros_like(m)
        q_idx = torch.arange(q_start, q_start + tq, device=q.device)
        for t0 in range(0, min(tk, q_start + tq), chunk):
            t1 = min(t0 + chunk, tk)
            kt = k[:, :, t0:t1]
            vt = v[:, :, t0:t1]
            if n_rep > 1:
                kt = kt.repeat_interleave(n_rep, dim=1)
                vt = vt.repeat_interleave(n_rep, dim=1)
            scores = torch.matmul(qf, kt.float().transpose(-2, -1)) * scale
            k_idx = torch.arange(t0, t1, device=q.device)
            scores = scores.masked_fill(k_idx > q_idx[:, None], float("-inf"))
            block_m = scores.amax(dim=-1, keepdim=True)
            new_m = torch.maximum(m, block_m)
            alpha = torch.exp(m - new_m)
            exp_s = torch.exp(scores - new_m)
            out = out * alpha + torch.matmul(exp_s, vt.float())
            denom = denom * alpha + exp_s.sum(dim=-1, keepdim=True)
            m = new_m
        return (out / denom.clamp(min=1e-6)).to(dtype=q.dtype)

    def _linear_chunks(linear: nn.Linear, x: torch.Tensor) -> torch.Tensor:
        if x.size(1) <= chunk:
            return linear(x)
        return torch.cat([linear(sl) for sl in x.split(chunk, dim=1)], dim=1)

    class _ChunkedFlashAttn(torch.autograd.Function):
        """One saved K/V; flash per query chunk. Avoids 391 SDPA graphs and math scores."""

        @staticmethod
        def forward(ctx, k, v, x, w_q, cos, sin):
            ctx.save_for_backward(k, v, x, w_q, cos, sin)
            b, _, s, _ = k.shape
            y = k.new_empty(b, spec.n_heads, s, spec.head_dim)
            with torch.no_grad():
                start = 0
                while start < s:
                    end = min(start + chunk, s)
                    q = F.linear(x[:, start:end], w_q).view(
                        b, end - start, spec.n_heads, spec.head_dim
                    )
                    q = _apply_rope(q, cos[start:end], sin[start:end]).transpose(1, 2)
                    y[:, :, start:end] = _tiled_causal_attn(q, k[:, :, :end], v[:, :, :end])
                    start = end
            return y

        @staticmethod
        def backward(ctx, dy):
            k, v, x, w_q, cos, sin = ctx.saved_tensors
            k = k.detach().requires_grad_(True)
            v = v.detach().requires_grad_(True)
            x = x.detach().requires_grad_(True)
            w_q = w_q.detach().requires_grad_(True)
            b, _, s, _ = k.shape
            start = 0
            while start < s:
                end = min(start + chunk, s)
                q = F.linear(x[:, start:end], w_q).view(
                    b, end - start, spec.n_heads, spec.head_dim
                )
                q = _apply_rope(q, cos[start:end], sin[start:end]).transpose(1, 2)
                y_c = _tiled_causal_attn(q, k[:, :, :end], v[:, :, :end])
                y_c.backward(dy[:, :, start:end])
                start = end
            return k.grad, v.grad, x.grad, w_q.grad, None, None

    class Attention(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.q = nn.Linear(spec.hidden_size, spec.n_heads * spec.head_dim, bias=False)
            self.k = nn.Linear(spec.hidden_size, spec.n_kv_heads * spec.head_dim, bias=False)
            self.v = nn.Linear(spec.hidden_size, spec.n_kv_heads * spec.head_dim, bias=False)
            self.o = nn.Linear(spec.hidden_size, spec.hidden_size, bias=False)
            inv = 1.0 / (rope_base ** (torch.arange(0, spec.head_dim, 2).float() / spec.head_dim))
            self.register_buffer("inv_freq", inv, persistent=False)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            b, s, _ = x.shape
            t = torch.arange(s, device=x.device, dtype=self.inv_freq.dtype)
            freqs = torch.outer(t, self.inv_freq)
            cos = torch.cos(freqs).to(x.dtype)
            sin = torch.sin(freqs).to(x.dtype)
            k = _apply_rope(
                self.k(x).view(b, s, spec.n_kv_heads, spec.head_dim), cos, sin
            ).transpose(1, 2)
            v = self.v(x).view(b, s, spec.n_kv_heads, spec.head_dim).transpose(1, 2)
            y = _ChunkedFlashAttn.apply(k, v, x, self.q.weight, cos, sin)
            y = y.transpose(1, 2).contiguous().view(b, s, spec.hidden_size)
            return _linear_chunks(self.o, y)

    class SwiGLU(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.up = nn.Linear(spec.hidden_size, spec.intermediate_size, bias=False)
            self.gate = nn.Linear(spec.hidden_size, spec.intermediate_size, bias=False)
            self.down = nn.Linear(spec.intermediate_size, spec.hidden_size, bias=False)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            if x.size(1) <= chunk:
                return self.down(F.silu(self.gate(x)) * self.up(x))
            parts = [
                self.down(F.silu(self.gate(sl)) * self.up(sl))
                for sl in x.split(chunk, dim=1)
            ]
            return torch.cat(parts, dim=1)

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

    def _run_block(block: nn.Module, h: torch.Tensor) -> torch.Tensor:
        if spec.context_length < 200_000:
            return block(h)
        # Do not wrap DeepSpeed checkpoint in except-retry: a kernel error
        # inside the block was re-run a second time on the same GPUs.
        return torch.utils.checkpoint.checkpoint(block, h, use_reentrant=False)

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
                x = _run_block(block, x)
            hidden = self.norm(x)
            if labels is None:
                return _linear_chunks(self.lm_head, hidden), None
            pred = hidden[:, :-1, :]
            tgt = labels[:, 1:]
            total = hidden.new_zeros(())
            for i in range(0, pred.size(1), chunk):
                logits = self.lm_head(pred[:, i : i + chunk])
                chunk_tgt = tgt[:, i : i + chunk]
                total = total + F.cross_entropy(
                    logits.reshape(-1, spec.vocab_size),
                    chunk_tgt.reshape(-1),
                    ignore_index=0,
                    reduction="sum",
                )
            ntok = (tgt != 0).sum().to(dtype=total.dtype).clamp(min=1)
            return None, total / ntok

    _ = math  # kept for possible later μP scaling
    return LlamaLM()
