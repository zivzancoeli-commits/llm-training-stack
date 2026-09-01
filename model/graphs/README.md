# graphs/

Placeholder for the full Llama-like stack:

`embed → dropout? → [TransformerBlock × L] → rmsnorm → lm_head`

No graph compiler (torch.compile / CUDA graphs / Megatron schedule) until
Phase 0 needs a real forward. The block-level contracts in
`transformer_block.py` are the unit of test until then.
