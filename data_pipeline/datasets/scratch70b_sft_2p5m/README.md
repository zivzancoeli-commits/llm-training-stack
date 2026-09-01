# scratch70b_sft_2p5m — from-scratch mix (1M tokens preferred)

**Status: cap locked.** Target **1 million** heuristic tokens or less
(1.3 × words). Hard cap **2.5 million**. Folder name is historical.

Do **not** generate toward 2.5M. The packer in `pretrain/corpus.py`
stops at `max_tokens` (recipes: 1M). On-disk files may be fewer than
1M; that is the intended “or less.”

This is **pretrain prose** for a **random-init** model, not a Qwen
fine-tune.

```bash
uv run lmm scratch-plan --recipe 100m_scratch
uv run lmm scratch-plan --recipe 70b_scratch
```

1M tokens will not make a 70B generally fluent. It is the cheap
from-scratch budget. Writers stop once the catalog nears 1M tokens.
