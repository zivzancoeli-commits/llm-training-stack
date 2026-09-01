# Hyperparameter profiles

One YAML file per scaling phase. These are **tracking records**, not
DeepSpeed configs. Change a number here first, then update tests if a
shape or memory contract breaks.

| File | Phase | Context |
| --- | --- | --- |
| `100m.yaml` | 0 proxy | 5,120 |
| `1b.yaml` | 1 reasoning-first | 5,120 |
| `7b.yaml` | 2 cheap 7B | 5,120 |
| `70b.yaml` | 3 systems probe | 5,120 |
| `200b.yaml` | 4 pretrain + 5 context extension | 5,120 then 350,208 |

Widths and depths are **proposals** to freeze after Phase 0. They exist so
shape and OOM tests have a concrete Llama-like graph to argue about.
