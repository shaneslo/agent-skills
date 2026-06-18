"""BPA Generator — agentic orchestration over a typed shared state.

Public entrypoints:
    build_graph()   -> compiled LangGraph application
    run(path, ...)  -> convenience wrapper returning the assembled artifacts
"""
from .graph import build_graph, run

__all__ = ["build_graph", "run"]
