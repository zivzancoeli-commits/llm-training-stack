"""Llama-like graph, layer hooks, and tensor-parallel maps.

No attention kernel lives here yet. `TransformerBlock` exposes shapes,
init stds, and MP/PP layer maps so tests can lock those before CUDA.
"""
