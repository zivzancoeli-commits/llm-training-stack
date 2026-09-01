# streaming/

Placeholder for shard readers (memory maps, object-store streams).

The worker in `loader.py` will iterate `TokenShard` objects from here.
Keep readers sequential and restartable; random access over 10B tokens is
how jobs become expensive.
