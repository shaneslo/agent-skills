"""1.1 Gate Evaluator — first contact with the input.

Decides whether the document describes a procedure worth normalizing. A bad
gate decision is unrecoverable downstream, so it errs toward rejection: below
the confidence floor, ``is_procedure`` is forced False.
"""
from __future__ import annotations

from pathlib import Path

from ..config import RunConfig
from ..models import get_model
from ..state import GateDecision, GraphState

# System prompt transcribed verbatim from specv2 §1.1.
GATE_SYSTEM = """\
You are a gate evaluator for a Business Process Analysis (BPA) generator. Your only
job is to decide whether the input document describes a procedure or business process.

A valid procedure or business process has:
- Named roles, actors, or teams who perform actions
- Step-like sequences of actions (verbs, transitions, decisions)
- Identifiable artifacts, systems, or files involved
- A definable end state or outcome

INVALID inputs include: marketing decks, research reports, policy memos without
procedural content, generic training materials, organizational announcements.

Examine the provided text snippet. Output structured JSON:
{
  "is_procedure": true | false,
  "reason": "<one sentence explaining your call>",
  "confidence": <0.0 to 1.0>
}

If confidence is below 0.6, set is_procedure to false and explain why the input is
ambiguous. The downstream pipeline cannot recover from a bad gate decision; err
toward rejection when uncertain.
"""


def _read_snippet(path: str, limit: int = 2000) -> str:
    """Best-effort first-2000-chars snippet for the gate (full extract comes later)."""
    p = Path(path)
    if p.suffix.lower() in {".txt", ".md"}:
        return p.read_text(errors="replace")[:limit]
    # For binary formats the orchestrator may pre-populate raw_text; fall back to
    # a deterministic peek so the gate always has something to judge.
    try:
        return p.read_bytes()[:limit].decode("latin-1", "replace")
    except OSError:
        return ""


def gate_evaluator(state: GraphState, config: RunConfig) -> GraphState:
    snippet = state.get("raw_text") or _read_snippet(state["input_path"])
    model = get_model("gate", config).with_structured_output(GateDecision)
    decision: GateDecision = model.invoke(
        [
            ("system", GATE_SYSTEM),
            ("human", f"Document text snippet (first 2000 chars):\n\n{snippet}"),
        ]
    )

    # Enforce the confidence floor: ambiguity is rejection.
    if decision.confidence < config.gate_confidence_floor:
        decision = decision.model_copy(update={"is_procedure": False})

    if not decision.is_procedure:
        return {
            "gate": decision,
            "rejected": True,
            "rejection_reason": decision.reason,
        }
    return {"gate": decision, "rejected": False, "raw_text": snippet}
