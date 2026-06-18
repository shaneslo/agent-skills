"""LangGraph wiring.

    START
      → gate            (cheap LLM)         ── rejected ─▶ END
      → extract         (deterministic / 1 classify call)
      → normalize       (strong LLM → StructuredState)
      → [Send fan-out]  one writer+evaluator invocation per section (parallel)
      → assemble        (deterministic; runs once after the fan-out joins)
      → END

In-run checkpointing uses MemorySaver for resumability and step-level
inspection, matching the spec's memory model (no cross-run memory).
"""
from __future__ import annotations

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from .assembly import assembler
from .config import RunConfig
from .ingestion import format_extractor, gate_evaluator, normalizer
from .state import GraphState
from .writers import SECTIONS, make_writer_evaluator_node


def build_graph(config: RunConfig | None = None):
    """Compile the BPA orchestration graph for a given run configuration."""
    config = config or RunConfig()

    g = StateGraph(GraphState)

    # --- nodes (closures bind the RunConfig so node signatures stay (state,)) ---
    g.add_node("gate", lambda s: gate_evaluator(s, config))
    g.add_node("extract", lambda s: format_extractor(s, config))
    g.add_node("normalize", lambda s: normalizer(s, config))
    g.add_node("writer", make_writer_evaluator_node(config))
    g.add_node("assemble", lambda s: assembler(s, config))

    # --- ingestion (linear, with the hard gate branch) ---
    g.add_edge(START, "gate")
    g.add_conditional_edges(
        "gate",
        lambda s: "reject" if s.get("rejected") else "continue",
        {"reject": END, "continue": "extract"},
    )
    g.add_edge("extract", "normalize")

    # --- fan-out: one Send per section, all consuming the shared state ---
    def dispatch_writers(state: GraphState):
        return [
            Send(
                "writer",
                {
                    "section_id": cfg.id,
                    "structured_state": state["structured_state"],
                },
            )
            for cfg in SECTIONS
        ]

    g.add_conditional_edges("normalize", dispatch_writers, ["writer"])

    # --- fan-in: assemble runs once after every writer invocation completes ---
    g.add_edge("writer", "assemble")
    g.add_edge("assemble", END)

    return g.compile(checkpointer=MemorySaver())


def run(
    input_path: str,
    config: RunConfig | None = None,
    thread_id: str = "bpa-run",
) -> dict:
    """Run the pipeline end-to-end. Returns the final graph state.

    On success the assembled artifacts are in ``result["artifacts"]`` and have
    already been written to ``config.out_dir``. On gate rejection the result
    carries ``rejected = True`` and a ``rejection_reason``.
    """
    config = config or RunConfig()
    app = build_graph(config)
    return app.invoke(
        {"input_path": input_path},
        config={"configurable": {"thread_id": thread_id}},
    )
