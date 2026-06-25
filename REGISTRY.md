# agent-skills registry

Distribute these skills, agent personas, and commands the same way you install shadcn/ui
components — `npx shadcn add` copies the source files into your project, where you own
and can edit them.

> Generated from each `SKILL.md` / agent / command. The `registryDependencies` graph is
> derived from the cross-references in the skill bodies ("Use the X skill", "see X"), so the
> repo's "reference, don't duplicate" convention becomes an installable dependency edge.

## Install

```bash
# one capability (pulls its registryDependencies automatically)
npx shadcn add @agent-skills//code-review-and-quality

# the whole skill library (the meta-skill depends on every skill)
npx shadcn add @agent-skills//using-agent-skills
```

Each item installs into conventional Claude Code locations:

| kind | installs to |
|------|-------------|
| skill | `.claude/skills/<name>/SKILL.md` |
| agent | `.claude/agents/<name>.md` |
| command | `.claude/commands/<name>.md` |
| reference | `.claude/skills/_shared/references/<name>.md` |

## How it maps

- **`name` / `description`** come verbatim from the item's YAML frontmatter.
- **`files[].target`** is where the file lands in the consumer's repo (the runtime contract — this only works if they use Claude Code's `.claude/` layout).
- **`registryDependencies`** are the other items this one references. Installing a skill pulls in the skills, personas, commands, and reference checklists it points to.

There is no `overrides` field in the schema: the override story is simply that the files now
live in *your* repo, so you edit them in place (or add a local companion the skill references).

## Catalog

### Skills
| item | what it does | depends on |
|------|--------------|------------|
| `api-and-interface-design` | Guides stable API and interface design. | `deprecation-and-migration` |
| `browser-testing-with-devtools` | Tests in real browsers via Chrome DevTools MCP. | — |
| `ci-cd-and-automation` | Automates CI/CD pipeline setup. | `debugging-and-error-recovery` |
| `code-review-and-quality` | Conducts multi-axis code review. | `security-and-hardening`, `performance-optimization`, `security-checklist`, `performance-checklist` |
| `code-simplification` | Simplifies code for clarity. | — |
| `context-engineering` | Optimizes agent context setup. | — |
| `debugging-and-error-recovery` | Guides systematic root-cause debugging. | — |
| `deprecation-and-migration` | Manages deprecation and migration. | — |
| `documentation-and-adrs` | Records decisions and documentation. | — |
| `doubt-driven-development` | Subjects every non-trivial decision to a fresh-context adversarial review before it stands. | `code-review-and-quality`, `source-driven-development`, `test-driven-development`, `debugging-and-error-recovery`, `orchestration-patterns`, `review` |
| `frontend-ui-engineering` | Builds production-quality UIs. | `accessibility-checklist` |
| `git-workflow-and-versioning` | Structures git workflow practices. | `code-review-and-quality` |
| `idea-refine` | Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. | — |
| `incremental-implementation` | Delivers changes incrementally. | `git-workflow-and-versioning` |
| `interview-me` | Extracts what the user actually wants instead of what they think they should want. | `idea-refine`, `spec-driven-development`, `doubt-driven-development`, `planning-and-task-breakdown`, `source-driven-development` |
| `observability-and-instrumentation` | Instruments code so production behavior is visible and diagnosable. | `debugging-and-error-recovery`, `performance-optimization`, `shipping-and-launch`, `security-and-hardening` |
| `performance-optimization` | Optimizes application performance. | `performance-checklist` |
| `planning-and-task-breakdown` | Breaks work into ordered tasks. | — |
| `security-and-hardening` | Hardens code against vulnerabilities. | `security-checklist` |
| `shipping-and-launch` | Prepares production launches. | `security-checklist`, `performance-checklist`, `accessibility-checklist` |
| `source-driven-development` | Grounds every implementation decision in official documentation. | — |
| `spec-driven-development` | Creates specs before coding. | `incremental-implementation`, `test-driven-development`, `context-engineering` |
| `test-driven-development` | Drives development with tests. | `browser-testing-with-devtools`, `testing-patterns` |
| `using-agent-skills` | Discovers and invokes agent skills. | `api-and-interface-design`, `browser-testing-with-devtools`, `ci-cd-and-automation`, `code-review-and-quality`, `code-simplification`, `context-engineering`, `debugging-and-error-recovery`, `deprecation-and-migration`, `documentation-and-adrs`, `doubt-driven-development`, `frontend-ui-engineering`, `git-workflow-and-versioning`, `idea-refine`, `incremental-implementation`, `interview-me`, `observability-and-instrumentation`, `performance-optimization`, `planning-and-task-breakdown`, `security-and-hardening`, `shipping-and-launch`, `source-driven-development`, `spec-driven-development`, `test-driven-development` |

### Agent personas
| item | what it does | depends on |
|------|--------------|------------|
| `code-reviewer` | Senior code reviewer that evaluates changes across five dimensions — correctness, readability, architecture, security, and performance. | `review`, `ship`, `security-auditor`, `test-engineer` |
| `security-auditor` | Security engineer focused on vulnerability detection, threat modeling, and secure coding practices. | `code-reviewer`, `test-engineer`, `ship` |
| `test-engineer` | QA engineer specialized in test strategy, test writing, and coverage analysis. | `test`, `ship`, `code-reviewer`, `security-auditor` |
| `web-performance-auditor` | Web performance engineer focused on Core Web Vitals, loading, rendering, and network optimization. | `browser-testing-with-devtools`, `performance-optimization`, `code-reviewer`, `ship`, `webperf`, `performance-checklist` |

### Commands
| item | what it does | depends on |
|------|--------------|------------|
| `build` | Implement tasks incrementally — build, test, verify, commit. | `incremental-implementation`, `test-driven-development`, `planning-and-task-breakdown`, `debugging-and-error-recovery`, `doubt-driven-development`, `spec`, `plan` |
| `code-simplify` | Simplify code for clarity and maintainability — reduce complexity without changing behavior. | `code-simplification`, `code-review-and-quality` |
| `plan` | Break work into small verifiable tasks with acceptance criteria and dependency ordering. | `planning-and-task-breakdown` |
| `review` | Conduct a five-axis code review — correctness, readability, architecture, security, performance. | `code-review-and-quality`, `security-and-hardening`, `performance-optimization` |
| `ship` | Run the pre-launch checklist via parallel fan-out to specialist personas, then synthesize a go/no-go decision. | `shipping-and-launch`, `code-reviewer`, `security-auditor`, `test-engineer`, `orchestration-patterns` |
| `spec` | Start spec-driven development — write a structured specification before writing code. | `spec-driven-development` |
| `test` | Run TDD workflow — write failing tests, implement, verify. | `test-driven-development`, `browser-testing-with-devtools` |
| `webperf` | Run a web performance audit via the web-performance-auditor persona. | `web-performance-auditor` |

### Reference checklists
| item | what it does | depends on |
|------|--------------|------------|
| `accessibility-checklist` | WCAG-oriented accessibility checklist covering semantics, keyboard navigation, ARIA, color contrast, and screen-reader support.. | — |
| `orchestration-patterns` | Multi-agent orchestration patterns — fan-out/gather, pipelines, judge panels, and verification loops for coordinating specialist agents.. | — |
| `performance-checklist` | Performance review checklist covering Core Web Vitals, rendering, network, bundle size, and runtime hot paths.. | — |
| `security-checklist` | Security review checklist covering input validation, authentication, secrets, data handling, and third-party integration risks.. | — |
| `testing-patterns` | Testing patterns and anti-patterns — unit, integration, and end-to-end strategies, fixtures, and coverage guidance.. | — |

---

Root manifest: [`registry.json`](./registry.json) · 41 items, 96 dependency edges.
Per-skill manifests live next to each skill at `skills/<name>/registry.json`.
