"""Stage 2 — the nine writer+evaluator pairs over shared state."""
from .sections import SECTIONS, SectionConfig
from .base import make_writer_evaluator_node

__all__ = ["SECTIONS", "SectionConfig", "make_writer_evaluator_node"]
