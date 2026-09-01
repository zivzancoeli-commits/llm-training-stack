# megatron/

Placeholder for Megatron-LM / Megatron-Core arguments:

- tensor parallel size
- pipeline parallel size
- sequence / context parallel (Phase 5 only)
- activation checkpointing

`model.TransformerBlock.parallel_layer_map` is the Python-side sketch of
the same grid.
