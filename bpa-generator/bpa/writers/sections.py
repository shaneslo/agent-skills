"""The fixed roster of nine section specialists (W1..W9).

Each entry pairs a *writer* instruction with the *conformance criteria* its
dedicated evaluator checks against. Writer instructions follow the section
semantics named in specv2; the detailed criteria below the snippet cutoff are
marked RECONSTRUCTED and should be reconciled against the full spec.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SectionConfig:
    id: str           # stable slot key, also the assembly ordering key
    order: int
    title: str
    writer_instructions: str
    conformance_criteria: str


SECTIONS: list[SectionConfig] = [
    SectionConfig(
        id="executive_summary",
        order=1,
        title="Executive Summary",
        writer_instructions=(
            "Write a prose executive summary (no bullets) of the process: what it "
            "is, who owns it, what it produces, and why it matters operationally. "
            "Draw only on process_name, process_description, roles, and steps."
        ),
        conformance_criteria=(  # RECONSTRUCTED
            "Prose only; 1-3 short paragraphs; names the process and its end state; "
            "no invented metrics; no marketing language; unknowns rendered as "
            "explicit placeholders."
        ),
    ),
    SectionConfig(
        id="components",
        order=2,
        title="Components",
        writer_instructions=(
            "Enumerate the process components grouped under subsections: Systems, "
            "Data Stores, Tools (label the subsection by tool.category when present), "
            "and Licensed Software. Use bullets. Include paths/notes when the state "
            "carries them."
        ),
        conformance_criteria=(  # RECONSTRUCTED
            "Every component traces to a state entry; no component invented; Tools "
            "subsection label reflects tool.category; placeholders preserved verbatim."
        ),
    ),
    SectionConfig(
        id="process_overview",
        order=3,
        title="Process Overview",
        writer_instructions=(
            "Produce TWO renders. (1) A flat narrative summary of the end-to-end "
            "flow in prose. (2) A detailed, numbered Steps list where each step "
            "shows who / what / how / timing and notes any decision points. Put the "
            "flat summary first under a '### Summary' heading, then '### Steps'."
        ),
        conformance_criteria=(  # RECONSTRUCTED
            "Both renders present; Steps ordered and consistent with state.steps; "
            "timing values only from timing_data; decision points surfaced; the two "
            "renders do not contradict each other."
        ),
    ),
    SectionConfig(
        id="roles",
        order=4,
        title="Roles & Responsibilities",
        writer_instructions=(
            "Produce TWO renders. (1) Detailed Roles: for each role give its name, "
            "alternate names, and responsibilities; surface named_individuals when "
            "present. (2) A flat Responsibilities list aggregating responsibilities "
            "across roles. Use '### Roles' then '### Responsibilities'."
        ),
        conformance_criteria=(  # RECONSTRUCTED
            "Every role from state present; alt names preserved; named individuals "
            "only shown when populated; flat list is a faithful union of role "
            "responsibilities."
        ),
    ),
    SectionConfig(
        id="common_patterns",
        order=5,
        title="Common Patterns",
        writer_instructions=(
            "Identify recurring operational patterns in the process (e.g. repeated "
            "review loops, manual reconciliation, hand-offs between teams). Classify "
            "each pattern and cite the steps that exhibit it."
        ),
        conformance_criteria=(  # RECONSTRUCTED
            "Each pattern grounded in specific steps; no pattern asserted without "
            "supporting steps; concise classification labels."
        ),
    ),
    SectionConfig(
        id="quantitative",
        order=6,
        title="Quantitative Analysis",
        writer_instructions=(
            "Report quantitative findings using ONLY values present in "
            "timing_data (or computed from them: totals, ranges, bottleneck steps). "
            "If timing_data is empty, state that no quantitative data was available "
            "and emit a placeholder. Never estimate."
        ),
        conformance_criteria=(  # RECONSTRUCTED
            "Zero numbers that are not in timing_data or derived from it; arithmetic "
            "correct; empty-data case handled with an explicit placeholder."
        ),
    ),
    SectionConfig(
        id="decision_points",
        order=7,
        title="Decision Points",
        writer_instructions=(
            "Summarize every decision point in the process: the condition, its "
            "branches and outcomes, and which step it governs. Aggregate from "
            "state.steps[*].decision_points."
        ),
        conformance_criteria=(  # RECONSTRUCTED
            "All decision points from state represented; each shows condition and "
            "branches; branch outcomes map to real steps."
        ),
    ),
    SectionConfig(
        id="automation_recommendations",
        order=8,
        title="Automation Recommendations",
        writer_instructions=(
            "Recommend where the process could be automated. For each "
            "recommendation give the target step(s), the rationale, and the expected "
            "operational effect. Ground every recommendation in a real step; do not "
            "promise metrics."
        ),
        conformance_criteria=(  # RECONSTRUCTED
            "Each recommendation cites specific steps; rationale is operational, not "
            "marketing; no fabricated savings figures."
        ),
    ),
    SectionConfig(
        id="genai_fit",
        order=9,
        title="GenAI Fit",
        writer_instructions=(
            "Evaluate where generative AI is and is not a fit within this process. "
            "For each candidate step assess suitability, the failure mode if misused, "
            "and the guardrail required. Be conservative and audit-aware."
        ),
        conformance_criteria=(  # RECONSTRUCTED
            "Balanced (names non-fits, not only fits); each assessment tied to a step; "
            "states a guardrail; no overstated capability claims."
        ),
    ),
]

SECTIONS_BY_ID: dict[str, SectionConfig] = {s.id: s for s in SECTIONS}
