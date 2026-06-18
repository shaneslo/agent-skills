# BPA Generator — Agentic Orchestration (LangGraph)

A clean-room LangGraph implementation of the **Business Process Analysis (BPA)
generator** described in `bpa-generator-orchestration-specv2`. It ingests a
PowerPoint or PDF describing a business process and emits a branded,
multi-section BPA document plus a sidecar BPMN diagram rendered from the same
typed state — so the prose and the diagram cannot diverge.

> **Provenance.** This package was generated from the orchestration spec (v2),
> the earlier spec (v1), and the rebuild PRD. Anywhere the spec text was below
> the source snippet cutoff, the code is marked `# RECONSTRUCTED` so it can be
> reconciled against the full document. Nothing in `timing_data` or any metric
> is invented at runtime — the writers surface explicit placeholders instead.

## Pipeline shape

```
Stage 1 — INGESTION (linear)
  raw input
    → Gate Evaluator        (cheap LLM: is this a procedure? else halt)
    → Format Extractor       (deterministic; +1 LLM classify call for PDFs)
    → Normalizer             (strong LLM, structured output → StructuredState)

Stage 2 — FAN-OUT (9 writer+evaluator pairs, concurrent over shared state)
  each pair: writer drafts → evaluator critiques → writer revises once → emit
    W1 Executive Summary   W2 Components          W3 Process Overview
    W4 Roles               W5 Common Patterns     W6 Quantitative
    W7 Decision Points     W8 Automation Rec.     W9 GenAI Fit

Stage 3 — ASSEMBLY (deterministic, no LLM)
  reducer-merged StructuredState
    ├── Jinja2 template → final BPA (.md)
    └── BPMN renderer   → sidecar diagram (.bpmn XML, drawio/Camunda importable)
```

## Layout

| Path | Role |
| --- | --- |
| `bpa/state.py` | Pydantic StructuredState + section I/O models + LangGraph reducers |
| `bpa/config.py` | Feature flags + tiered model-role configuration |
| `bpa/models.py` | Model-provider abstraction (AI Gateway / `init_chat_model`) |
| `bpa/style.py` | Shared style block injected into every writer |
| `bpa/ingestion/` | Gate evaluator, format extractors, normalizer |
| `bpa/writers/` | Writer+evaluator pair factory and the 9 section configs |
| `bpa/assembly/` | Deterministic assembler, Jinja2 template, BPMN renderer |
| `bpa/graph.py` | LangGraph `StateGraph` wiring (Send fan-out, MemorySaver) |
| `bpa/cli.py` | CLI entrypoint |

## Quick start

```bash
cd bpa-generator
pip install -r requirements.txt

# Point the model abstraction at your AI Gateway (Anthropic-compatible):
export AI_GATEWAY_BASE_URL="https://gateway.example/v1"
export AI_GATEWAY_API_KEY="..."

python -m bpa.cli path/to/process.pptx --out ./out
# → ./out/<process>.bpa.md   and   ./out/<process>.bpmn
```

To reproduce the v1 behaviour (writers only, no evaluator critique, no BPMN):

```bash
python -m bpa.cli path/to/process.pdf --no-evaluators --no-bpmn
```

## Design contracts

- **The state object is the contract.** Every writer reads from `StructuredState`;
  none re-parse the source document.
- **Bounded revision.** Each writer revises at most once after its evaluator's
  critique; the loop cannot spin.
- **Determinism at the edges.** Extraction and assembly are LLM-free; only
  ingestion-classification and the writer/evaluator layer call models.
- **Provider-agnostic.** Swap models per role via env without touching graph code.
