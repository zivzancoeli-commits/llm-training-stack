# layers/

Placeholder package for kernels that do not exist yet.

- `flash_attention.py` — Protocol + NotImplemented stub
- `rope.py` — config only; no `cos/sin` cache

When a kernel lands, it must pass `tests/test_attention_shapes.py` without
changing those expected tuples.
