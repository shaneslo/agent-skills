"""Writer+evaluator pair node.

Each pair runs as ONE graph node so the fan-out stays a clean parallel map and
the revision loop is structurally bounded (it cannot become a graph cycle):

    writer drafts -> evaluator critiques -> writer revises once if needed -> emit

When ``config.enable_evaluators`` is False this degrades to the specv1 behaviour:
a single writer pass with no critique and no revision.
"""
from __future__ import annotations

from typing import Callable

from ..config import RunConfig
from ..models import get_model
from ..state import Critique, GraphState, SectionDraft, StructuredState
from ..style import STYLE_BLOCK
from .sections import SECTIONS_BY_ID, SectionConfig


def _writer_messages(cfg: SectionConfig, state_json: str, critique: Critique | None):
    system = (
        f"You are the {cfg.title} writer for a Business Process Analysis generator.\n\n"
        f"{STYLE_BLOCK}\n"
        f"SECTION TASK:\n{cfg.writer_instructions}\n\n"
        "You are given the full StructuredState as JSON. Read from it only; do not "
        "invent entities or numbers. Output Markdown for your section body (no top-level "
        "heading — the assembler adds it)."
    )
    human = f"StructuredState JSON:\n\n{state_json}"
    msgs = [("system", system), ("human", human)]
    if critique is not None and not critique.passes:
        msgs.append(
            (
                "human",
                "Your draft did not pass review. Revise it once to address:\n"
                + "\n".join(f"- {i}" for i in critique.issues)
                + (f"\n\nGuidance: {critique.guidance}" if critique.guidance else ""),
            )
        )
    return msgs


def _evaluator_critique(
    cfg: SectionConfig, draft_md: str, state_json: str, config: RunConfig
) -> Critique:
    system = (
        f"You are the evaluator for the {cfg.title} section of a Business Process "
        "Analysis. Critique the draft strictly against the conformance criteria. "
        "Pass it only if it fully complies.\n\n"
        f"CONFORMANCE CRITERIA:\n{cfg.conformance_criteria}\n\n"
        f"STYLE RULES THE DRAFT MUST OBEY:\n{STYLE_BLOCK}"
    )
    human = (
        f"StructuredState JSON:\n\n{state_json}\n\n"
        f"--- DRAFT ---\n{draft_md}\n--- END DRAFT ---\n\n"
        "Return passes/issues/guidance."
    )
    model = get_model("evaluate", config).with_structured_output(Critique)
    critique: Critique = model.invoke([("system", system), ("human", human)])
    return critique.model_copy(update={"section_id": cfg.id})


def make_writer_evaluator_node(config: RunConfig) -> Callable[[GraphState], GraphState]:
    """Return the node that handles whichever section a Send dispatches to it."""

    def node(state: GraphState) -> GraphState:
        # Model is fetched lazily (get_model caches), so building the graph never
        # requires a live provider client.
        writer_model = get_model("write", config)
        cfg = SECTIONS_BY_ID[state["section_id"]]  # type: ignore[typeddict-item]
        structured: StructuredState = state["structured_state"]
        state_json = structured.model_dump_json(indent=2)

        # 1) draft
        draft_md = writer_model.invoke(_writer_messages(cfg, state_json, None)).content
        draft = SectionDraft(
            section_id=cfg.id, title=cfg.title, markdown=draft_md, revision=0
        )
        critiques: dict[str, Critique] = {}

        # 2) critique + bounded revision (specv2 only)
        if config.enable_evaluators:
            for attempt in range(config.max_revisions):
                critique = _evaluator_critique(cfg, draft.markdown, state_json, config)
                critiques[cfg.id] = critique
                if critique.passes:
                    break
                revised = writer_model.invoke(
                    _writer_messages(cfg, state_json, critique)
                ).content
                draft = draft.model_copy(
                    update={"markdown": revised, "revision": attempt + 1}
                )

        return {"sections": {cfg.id: draft}, "critiques": critiques}

    return node
