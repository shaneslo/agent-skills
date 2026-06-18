"""Stage 1 — linear ingestion: gate -> extract -> normalize."""
from .gate import gate_evaluator
from .extractors import format_extractor
from .normalizer import normalizer

__all__ = ["gate_evaluator", "format_extractor", "normalizer"]
