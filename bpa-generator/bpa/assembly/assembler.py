"""Assembler — reducer-merged state in, artifacts out. Deterministic.

Orders the section drafts by their roster position, renders the branded BPA
document via Jinja2, and (when enabled) the BPMN sidecar from the same state.
"""
from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..config import RunConfig
from ..state import GraphState, SectionDraft, StructuredState
from ..writers.sections import SECTIONS_BY_ID
from .bpmn import render_bpmn

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=select_autoescape(enabled_extensions=()),
    trim_blocks=True,
    lstrip_blocks=True,
)


def _ordered(sections: dict[str, SectionDraft]) -> list[SectionDraft]:
    return sorted(
        sections.values(),
        key=lambda d: SECTIONS_BY_ID[d.section_id].order
        if d.section_id in SECTIONS_BY_ID
        else 999,
    )


def assembler(state: GraphState, config: RunConfig) -> GraphState:
    structured: StructuredState = state["structured_state"]
    sections = _ordered(state.get("sections", {}))

    bpa_md = _env.get_template("bpa.md.j2").render(state=structured, sections=sections)

    artifacts: dict = {"bpa_md": bpa_md}
    if config.enable_bpmn:
        artifacts["bpmn_xml"] = render_bpmn(structured)

    # Persist.
    out = Path(config.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    slug = structured.process_name.lower().replace(" ", "-").replace("/", "-") or "bpa"
    paths: dict[str, str] = {}
    md_path = out / f"{slug}.bpa.md"
    md_path.write_text(bpa_md)
    paths["bpa_md"] = str(md_path)
    if config.enable_bpmn:
        bpmn_path = out / f"{slug}.bpmn"
        bpmn_path.write_text(artifacts["bpmn_xml"])
        paths["bpmn"] = str(bpmn_path)
    artifacts["paths"] = paths

    return {"artifacts": artifacts}
