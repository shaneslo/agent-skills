"""Shared style block — injected verbatim into every writer's system prompt.

Voice consistency comes from this block plus the per-writer evaluator critique,
not from a post-generation editor agent. Transcribed from specv2.
"""

STYLE_BLOCK = """\
STYLE RULES (apply to all output):
- Voice: precise, operational, audit-aware. Write for a senior wealth management
  operations reviewer who will verify your output against source documents.
- Mark unknowns explicitly. When a fact cannot be confirmed from source, render
  "[<thing>: exact value to be confirmed with system owner]" rather than guessing.
- Preserve source vocabulary. Do not expand acronyms or rename systems unless the
  source confirms the full form. "3D" stays "3D" if that's what the source called it.
- No marketing language. Avoid "leverage", "streamline", "best-in-class", "robust",
  "seamless". Use plain operational verbs.
- Numbers: only render quantitative values that appear in `structured_state.timing_data`
  or are computed from it. Never invent metrics.
- Format: Markdown. Use bullets and sub-bullets when content is enumerable. Use prose
  for narrative summaries (executive summary, role descriptions).
"""
