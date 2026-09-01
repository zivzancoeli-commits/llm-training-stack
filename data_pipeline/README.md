# data_pipeline/

CPU-side path from raw text to packed token batches. Nothing here should
import CUDA. The GPU must see a steady stream of ``(micro_batch, 5120)``
rows; if it waits, that is a bug in this folder, not in the model.

## Layout

| Path | Status | Role |
| --- | --- | --- |
| `loader.py` | skeleton | Multi-thread prefetch worker |
| `tokenization/` | placeholder | BPE / SentencePiece / tiktoken — **not chosen yet** |
| `streaming/` | placeholder | Memory-map / WebDataset / Mosaic streaming shards |
| `deduplication/` | placeholder | Exact + MinHash / Bloom near-dedup |
| `datasets/scratch70b_v0/` | seed corpus | 70B-from-scratch review set (5,120 ctx) |

## Contract the loader must keep

- Packed shape is ``(batch, context_length)``.
- Default ``context_length`` is **5,120** for every phase until 200B
  extension. The worker should refuse an accidental 350,208 pretrain mix.
- `prefetch_depth` batches sit on the CPU side so `starvation_ratio`
  stays near zero.
- Labels are next-token ids; packing may concatenate documents with an
  EOS separator (algorithm later).

## Reasoning mix (small models)

Dedup and mix weights are how 100M–7B stay *smart* without 350k context.
Target ratios live in `specs/hyperparameter_profiles/*.yaml`
(`reasoning_mix_ratio`). Implementation of the mixer is deferred; do not
silently fill the mix with Common Crawl.

## Tokenizer — recorded default, still cheap to change

Default we will start from unless you override it: **byte-level BPE with
a 32k vocab** (Llama-2-shaped) so the 100M proxy and the 200B share ids.
Not locked. If you prefer tiktoken-100k or Llama-3 128k, change the
profiles before Phase 1 — vocab size is a shape input to embeddings.
