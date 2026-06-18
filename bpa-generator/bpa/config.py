"""Run configuration: feature flags and tiered model-role assignment.

The spec calls for "model provider abstraction through AI Gateway". We express
that as named *roles* (gate / classify / normalize / write / evaluate) so the
graph never hard-codes a model id. Swap any role via environment variable
without touching orchestration code.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field


# Default tier assignment. Cheap calls -> Haiku; the load-bearing Normalizer ->
# the strongest model; the writer/evaluator layer -> a mid-tier model.
_DEFAULT_MODELS: dict[str, str] = {
    "gate": "claude-haiku-4-5-20251001",
    "classify": "claude-haiku-4-5-20251001",
    "normalize": "claude-opus-4-8",
    "write": "claude-sonnet-4-6",
    "evaluate": "claude-sonnet-4-6",
}


@dataclass
class GatewayConfig:
    """Anthropic-compatible AI Gateway endpoint. The model layer reads these."""

    base_url: str | None = field(
        default_factory=lambda: os.getenv("AI_GATEWAY_BASE_URL")
    )
    api_key: str | None = field(
        default_factory=lambda: os.getenv("AI_GATEWAY_API_KEY")
        or os.getenv("ANTHROPIC_API_KEY")
    )


@dataclass
class RunConfig:
    """Per-run knobs. Defaults reproduce specv2; flags below recover specv1."""

    enable_evaluators: bool = True   # v1 == False (writers only, no critique)
    enable_bpmn: bool = True         # v1 == False (no sidecar diagram)
    max_revisions: int = 1           # spec: bounded to one revision cycle
    gate_confidence_floor: float = 0.6
    out_dir: str = "./out"

    gateway: GatewayConfig = field(default_factory=GatewayConfig)
    models: dict[str, str] = field(default_factory=lambda: dict(_DEFAULT_MODELS))

    def model_for(self, role: str) -> str:
        """Resolve a role to a model id, honouring BPA_MODEL_<ROLE> overrides."""
        env = os.getenv(f"BPA_MODEL_{role.upper()}")
        return env or self.models[role]
