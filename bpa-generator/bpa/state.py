"""Typed state — the single contract every node reads from and writes to.

Two layers live here:

1. ``StructuredState`` and its sub-models: the normalized, source-of-truth
   representation produced by the Normalizer. Field set transcribed from the
   PRD's section 6.1 table; sub-model fields below the snippet cutoff are marked
   ``# RECONSTRUCTED`` and should be reconciled against the full schema.

2. The LangGraph channel state (``GraphState``) plus reducers that let the nine
   writer+evaluator pairs write section drafts concurrently without clobbering
   each other.
"""
from __future__ import annotations

from enum import Enum
from typing import Annotated, Optional, TypedDict

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------- #
# Enums
# --------------------------------------------------------------------------- #
class SourceDocumentType(str, Enum):
    ppt = "ppt"
    pdf_procedure = "pdf_procedure"
    pdf_meeting = "pdf_meeting"


# --------------------------------------------------------------------------- #
# Component sub-models  (PRD 6.1)
# --------------------------------------------------------------------------- #
class System(BaseModel):
    """An in-house system that participates in the process."""

    name: str
    description: Optional[str] = None
    alt_names: list[str] = Field(default_factory=list)   # RECONSTRUCTED
    owner: Optional[str] = None                          # RECONSTRUCTED


class DataStore(BaseModel):
    name: str
    path: Optional[str] = None
    notes: Optional[str] = None


class Tool(BaseModel):
    name: str
    category: Optional[str] = None  # drives the Tools subsection label
    notes: Optional[str] = None     # RECONSTRUCTED


class Software(BaseModel):
    """Licensed / third-party software."""

    name: str
    vendor: Optional[str] = None    # RECONSTRUCTED
    notes: Optional[str] = None     # RECONSTRUCTED


class Person(BaseModel):
    name: str
    role: Optional[str] = None      # RECONSTRUCTED
    title: Optional[str] = None     # RECONSTRUCTED


class Role(BaseModel):
    name: str
    alt_names: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    named_individuals: list[Person] = Field(default_factory=list)


class Placeholder(BaseModel):
    """Confidence-aware unresolved entity.

    When both candidate expansions score below the extraction threshold the
    Normalizer emits ``rendered = "(Unspecified ...)"`` rather than guessing.
    """

    label: str
    candidates: list[str] = Field(default_factory=list)   # RECONSTRUCTED
    confidence: float = 0.0
    rendered: str  # e.g. "[<thing>: exact value to be confirmed with system owner]"


class DecisionPoint(BaseModel):
    """A branch in the process flow. Feeds both the prose and the BPMN gateway."""

    condition: str
    branches: dict[str, str] = Field(default_factory=dict)  # label -> outcome step
    notes: Optional[str] = None                             # RECONSTRUCTED


class Step(BaseModel):
    """One ordered action in the process (PRD: Step{who, what, how, timing, ...})."""

    id: str
    who: str                       # role / actor performing the action
    what: str                      # the action
    how: Optional[str] = None      # mechanism / system used
    timing: Optional[str] = None   # references timing_data when quantitative
    decision_points: list[DecisionPoint] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)    # RECONSTRUCTED
    outputs: list[str] = Field(default_factory=list)   # RECONSTRUCTED
    systems: list[str] = Field(default_factory=list)   # RECONSTRUCTED


class TimingDatum(BaseModel):
    """A single quantitative timing fact. Writers may ONLY cite values from here."""

    label: str
    value: float
    unit: str
    source: Optional[str] = None  # where in the source document this came from


# --------------------------------------------------------------------------- #
# StructuredState — the normalized source of truth
# --------------------------------------------------------------------------- #
class StructuredState(BaseModel):
    """Single source of truth. Specialists read from it; none re-parse source."""

    process_name: str
    process_description: str
    source_document_type: SourceDocumentType

    systems: list[System] = Field(default_factory=list)
    data_stores: list[DataStore] = Field(default_factory=list)
    tools: list[Tool] = Field(default_factory=list)
    licensed_software: list[Software] = Field(default_factory=list)

    roles: list[Role] = Field(default_factory=list)
    named_individuals: list[Person] = Field(default_factory=list)        # optional
    unresolved_entities: list[Placeholder] = Field(default_factory=list)  # optional

    steps: list[Step] = Field(default_factory=list)
    timing_data: list[TimingDatum] = Field(default_factory=list)


# --------------------------------------------------------------------------- #
# Ingestion intermediate models
# --------------------------------------------------------------------------- #
class GateDecision(BaseModel):
    is_procedure: bool
    reason: str
    confidence: float


class ExtractedDocument(BaseModel):
    """Deterministic extractor output, pre-normalization."""

    source_document_type: SourceDocumentType
    text: str
    # PPT carries slides; PDF carries page text. Kept loose on purpose.
    blocks: list[dict] = Field(default_factory=list)


# --------------------------------------------------------------------------- #
# Writer / evaluator I/O
# --------------------------------------------------------------------------- #
class SectionDraft(BaseModel):
    """What a writer emits for its section slot."""

    section_id: str
    title: str
    markdown: str
    structured: dict = Field(default_factory=dict)  # optional machine-readable payload
    revision: int = 0


class Critique(BaseModel):
    """Evaluator verdict against a section's conformance criteria."""

    section_id: str
    passes: bool
    issues: list[str] = Field(default_factory=list)
    guidance: str = ""  # concrete revision instructions when passes is False


# --------------------------------------------------------------------------- #
# LangGraph channel state + reducers
# --------------------------------------------------------------------------- #
def merge_sections(
    left: dict[str, SectionDraft] | None,
    right: dict[str, SectionDraft] | None,
) -> dict[str, SectionDraft]:
    """Reducer: concurrent writers each contribute one section key."""
    out = dict(left or {})
    out.update(right or {})
    return out


def merge_critiques(
    left: dict[str, Critique] | None,
    right: dict[str, Critique] | None,
) -> dict[str, Critique]:
    out = dict(left or {})
    out.update(right or {})
    return out


class GraphState(TypedDict, total=False):
    """The LangGraph channel state threaded through every node."""

    input_path: str
    raw_text: str
    gate: GateDecision
    rejected: bool
    rejection_reason: str
    extracted: ExtractedDocument
    structured_state: StructuredState
    # Parallel writer/evaluator writes are reducer-merged:
    sections: Annotated[dict[str, SectionDraft], merge_sections]
    critiques: Annotated[dict[str, Critique], merge_critiques]
    artifacts: dict  # {"bpa_md": str, "bpmn_xml": str, "paths": {...}}
