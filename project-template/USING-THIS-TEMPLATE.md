# Using this project template

This directory is a **repo skeleton** — the standard set of files every new
project starts from, so the things that are easy to forget on a fresh repo
(architecture, how to build, how to test, how to run it locally) are captured
by default instead of reinvented each time.

## What's in here

| File | What it answers | Rename to |
| --- | --- | --- |
| `README.template.md` | What is this, who's it for, how do I start it? | `README.md` |
| `ARCHITECTURE.template.md` | How is it built? What are the pieces and why? | `ARCHITECTURE.md` |
| `CONTRIBUTING.template.md` | How do we work: branches, commits, reviews, PRs | `CONTRIBUTING.md` |
| `docs/development.template.md` | **How do we dev?** The local loop: run, debug, iterate | `docs/development.md` |
| `docs/testing.template.md` | **How do we test?** Layers, commands, expectations | `docs/testing.md` |
| `docs/build-and-release.template.md` | **How do we build/ship?** CI/CD, envs, versioning | `docs/build-and-release.md` |
| `docs/adr/0000-adr-template.md` | Record a decision so future-you knows *why* | `docs/adr/0001-<slug>.md` |

## How to instantiate a new repo from this

1. Copy the contents of `project-template/` into the new repo root.
2. Strip the `.template` suffix from each file (`README.template.md` → `README.md`).
3. Do a find-and-replace on the placeholders:
   - `{{PROJECT_NAME}}` — the repo/product name
   - `{{ONE_LINER}}` — one sentence: what it does and for whom
   - `{{OWNER}}` — team or person responsible
   - Anything in `<!-- FILL: ... -->` comments — replace the comment with real content, then delete the marker.
4. Delete this `USING-THIS-TEMPLATE.md` from the new repo.
5. Delete any section that genuinely doesn't apply — but **delete it deliberately**,
   don't just leave the placeholder. An empty "Testing" section reads as "we don't test."

## Design intent

- **One universal core, extended per project type.** These files apply to *any*
  project. Language/framework-specific bits live behind `<!-- FILL -->` markers so
  a Python service and a TypeScript app share the same skeleton and only differ in
  the filled-in details. (If we later want per-type variants — e.g. `service`,
  `library`, `cli`, `web-app` — they should be thin overlays on top of this core,
  not forks of it.)
- **Every "how do we…?" question has exactly one home.** If you're not sure where
  something goes, it goes in the doc named after the question.
- **Templates are scaffolds, not essays.** Keep them skimmable. A section that
  can't be filled in a few lines probably wants its own doc under `docs/`.

## Principles worth keeping (baked into these files)

These conventions — drawn from repos worth imitating (`wshobson/agents`,
`addyosmani/agent-skills`) — are the *why* behind the template's shape. Keep them
as you fill it in:

- **Single source of truth.** Author content in one place; generate everything
  else from it. Never hand-edit generated artifacts. (`ARCHITECTURE.md` §Invariants)
- **Progressive disclosure.** Entry docs stay short and point outward; detail
  lives in `docs/` and is read on demand. If `README.md` or `ARCHITECTURE.md`
  stops being skimmable, move detail down, don't pad up.
- **Mechanical enforcement with fix-hints.** Prefer a check over a guideline, and
  make every check print its concrete remediation, not just "invalid".
  (`docs/testing.md`, `CONTRIBUTING.md`)
- **One canonical entrypoint per task.** `make test` / `make validate` — CI and
  humans call the same command, so "how do I run this?" has exactly one answer.
- **Invariants first.** Lead the architecture doc with the non-negotiable rules,
  then map the components. A reader should learn what *can't* change before how it
  works.
