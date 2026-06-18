"""1.3 Normalizer — the load-bearing component.

Strong-model structured extraction from the deterministic ExtractedDocument into
the typed ``StructuredState``. This is the only place the raw document is turned
into the shared contract; every writer downstream trusts this output and never
re-parses source.

Confidence-aware extraction: entities whose expansion cannot be confirmed are
emitted into ``unresolved_entities`` as placeholders rather than guessed.
"""
from __future__ import annotations

from ..config import RunConfig
from ..models import get_model
from ..state import ExtractedDocument, GraphState, StructuredState

NORMALIZER_SYSTEM = """\
You are the Normalizer for a Business Process Analysis generator. Convert the
extracted document into a single typed StructuredState object. Rules:

- Extract every system, data store, tool, licensed software item, role, and named
  individual that the source actually names. Preserve source vocabulary exactly;
  do not expand acronyms unless the source confirms the full form.
- Decompose the process into ordered Steps {who, what, how, timing, decision_points}.
  The source_document_type hint tells you how the steps are organized:
    * ppt / pdf_procedure -> steps follow the document's own ordering
    * pdf_meeting         -> reconstruct ordered steps from discussion; attribute
                             who/what carefully and mark sequence you inferred.
- Confidence-aware: if you cannot confirm an entity or an acronym expansion, do NOT
  guess. Add a Placeholder to unresolved_entities with the rendered form
  "[<thing>: exact value to be confirmed with system owner]" and leave the value out.
- Only populate timing_data with quantitative values the source states. Never invent.
- Return data that validates against the StructuredState schema exactly.
"""


def normalizer(state: GraphState, config: RunConfig) -> GraphState:
    extracted: ExtractedDocument = state["extracted"]
    model = get_model("normalize", config).with_structured_output(StructuredState)
    structured: StructuredState = model.invoke(
        [
            ("system", NORMALIZER_SYSTEM),
            (
                "human",
                f"source_document_type: {extracted.source_document_type.value}\n\n"
                f"EXTRACTED DOCUMENT TEXT:\n\n{extracted.text}",
            ),
        ]
    )
    # Keep the classifier's sub-type authoritative.
    structured = structured.model_copy(
        update={"source_document_type": extracted.source_document_type}
    )
    return {"structured_state": structured}
