# Architecture — {{PROJECT_NAME}}

<!--
  STRUCTURE: this template follows the "invariants-first" architecture-doc style
  used in wshobson/agents — state the non-negotiable rules first, then map the
  components, then how correctness is mechanically enforced. Voice is prescriptive
  and reference-oriented: pair every high-level statement with a concrete path,
  command, or contract. This file is the MAP; deep detail offloads to docs/.
  Keep it skimmable — if a section can't stay tight, give it its own doc.
-->

## Invariants

<!-- The non-negotiable rules the system is built around. Write each as an
     imperative with a bold lead phrase. If one of these is violated, something is
     broken by definition — not a matter of taste. Aim for 3-6. The items below
     show the *shape*; replace them with this project's real rules. -->

1. **Single source of truth.** <!-- FILL: where authored/source content lives, and
   what is generated from it. State plainly what must never be hand-edited. -->
2. **One canonical {{THING}}.** <!-- FILL: the one config/context/entry file that
   everything else derives from or points at. -->
3. **{{BOUNDARY}} owns {{CONCERN}}; source stays portable.** <!-- FILL: what
   isolates environment/platform/harness specifics so the core stays clean. -->
4. **Mechanical enforcement with remediation hints.** <!-- FILL: how the rules are
   enforced automatically, and that every failure names its concrete fix. -->

## Component overview

<!-- An ASCII directory tree of the repo with aligned inline `#` comments marking
     what each path is and whether it is SOURCE or GENERATED. This is the single
     most useful artifact for a new engineer — keep it current with reality. -->

```
{{PROJECT_NAME}}/
├── README.md                 # User-facing entry point
├── ARCHITECTURE.md           # This file — the map
├── CONTRIBUTING.md           # Contributor entry point
├── {{SOURCE_DIR}}/           # SOURCE OF TRUTH — what authors edit
│   └── ...
├── {{GENERATED_DIR}}/        # GENERATED — do not hand-edit (gitignored, or
│                             #   committed only if it merely points at source)
├── {{CODE_OR_TOOLS_DIR}}/    # build / core logic / tooling
│   └── tests/                # where the tests live
└── docs/                     # Detailed reference docs (this file is the map)
```

<!-- Follow the tree with 2-4 sentences: what is committed vs generated, and any
     symlink/build relationships that aren't obvious from the tree alone. -->

## Core mechanics

<!-- The load-bearing mechanism of THIS system — the one thing that, if a reader
     doesn't understand it, nothing else makes sense. (In wshobson/agents this is
     the cross-harness adapter framework.) Prefer a table of the moving parts over
     prose; name the transform each part performs. -->

| Part | Input | Output | Responsibility / transform |
| --- | --- | --- | --- |
| | | | |

## Quality gates

<!-- The automated stages that enforce correctness before merge/release, as
     concrete commands. Say what each one checks and which run in CI. A rule that
     isn't mechanically enforced is a suggestion, not an invariant — so every
     invariant above should map to a gate here. -->

1. `{{VALIDATE_CMD}}` — <!-- what structural/lint rules it enforces -->
2. `{{TEST_CMD}}` — <!-- test scope + where the suite lives; see docs/testing.md -->
3. <!-- CI: which of the above gate a PR vs run on merge/tag; link the workflow -->

## Component / module model

<!-- The core building blocks and the contract each must satisfy: where they live,
     their required frontmatter / interface / public API, and how they are
     discovered or composed. Keep the contract here; push authoring detail to a
     dedicated docs/ guide. -->

## Model tiers

<!-- OPTIONAL — keep only for AI/agent projects that route work across models by
     complexity or cost. Delete this whole section otherwise. -->

| Tier | Model | Use for |
| --- | --- | --- |
| | | |

## See also

- [README.md](README.md) — what this is and how to start it
- [docs/development.md](docs/development.md) — the local dev loop
- [docs/testing.md](docs/testing.md) — how we test
- [docs/build-and-release.md](docs/build-and-release.md) — how we ship
- [docs/adr/](docs/adr/) — decision records (the *why* behind the above)
