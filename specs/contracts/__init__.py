"""Pure mathematical contracts used by tests and by class skeletons."""

from specs.contracts.attention_shapes import (
    AttentionBoundaryShapes,
    attention_boundary_shapes,
    hidden_size,
    validate_head_config,
)
from specs.contracts.initialization import (
    InitStdProfile,
    attention_logit_scale,
    embedding_std,
    gpt2_residual_out_std,
    init_std_profile,
    mup_linear_std,
)
from specs.contracts.memory import (
    H100_80GB_BYTES,
    H200_141GB_BYTES,
    RUNPOD_H200_NVL_GPU_TYPE_ID,
    RUNPOD_H200_SXM_GPU_TYPE_ID,
    MemoryEstimate,
    cluster_usable_bytes,
    flash_attention_workspace_bytes,
    lora_cluster_bytes,
    lora_trainable_params,
    naive_attention_score_bytes,
    parameter_bytes,
    project_training_footprint,
    would_oom,
    would_oom_cluster,
)

__all__ = [
    "AttentionBoundaryShapes",
    "H100_80GB_BYTES",
    "H200_141GB_BYTES",
    "InitStdProfile",
    "MemoryEstimate",
    "RUNPOD_H200_NVL_GPU_TYPE_ID",
    "RUNPOD_H200_SXM_GPU_TYPE_ID",
    "attention_boundary_shapes",
    "attention_logit_scale",
    "cluster_usable_bytes",
    "embedding_std",
    "flash_attention_workspace_bytes",
    "gpt2_residual_out_std",
    "hidden_size",
    "init_std_profile",
    "lora_cluster_bytes",
    "lora_trainable_params",
    "mup_linear_std",
    "naive_attention_score_bytes",
    "parameter_bytes",
    "project_training_footprint",
    "validate_head_config",
    "would_oom",
    "would_oom_cluster",
]
