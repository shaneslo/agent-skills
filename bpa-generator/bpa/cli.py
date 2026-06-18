"""CLI entrypoint:  python -m bpa.cli process.pptx --out ./out"""
from __future__ import annotations

import argparse
import sys

from .config import RunConfig
from .graph import run


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="bpa", description="BPA Generator (LangGraph)")
    p.add_argument("input", help="Path to a .pptx or .pdf process document")
    p.add_argument("--out", default="./out", help="Output directory")
    p.add_argument(
        "--no-evaluators",
        action="store_true",
        help="Disable evaluator critique/revision (reproduces specv1)",
    )
    p.add_argument(
        "--no-bpmn", action="store_true", help="Skip the BPMN sidecar diagram"
    )
    p.add_argument("--thread-id", default="bpa-run", help="Checkpoint thread id")
    args = p.parse_args(argv)

    config = RunConfig(
        enable_evaluators=not args.no_evaluators,
        enable_bpmn=not args.no_bpmn,
        out_dir=args.out,
    )

    result = run(args.input, config=config, thread_id=args.thread_id)

    if result.get("rejected"):
        print(f"REJECTED by gate: {result.get('rejection_reason')}", file=sys.stderr)
        return 2

    paths = result.get("artifacts", {}).get("paths", {})
    print("Wrote:")
    for kind, path in paths.items():
        print(f"  {kind}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
