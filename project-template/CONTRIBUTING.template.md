# Contributing to {{PROJECT_NAME}}

How a change goes from an idea to merged. Keep this identical across repos so the
workflow is muscle memory, not a per-project puzzle.

## Before you start

- Read [ARCHITECTURE.md](ARCHITECTURE.md) if you're touching more than one component.
- Get it running via [docs/development.md](docs/development.md).
- For anything non-trivial, open an issue / align on approach first. Cheaper than
  a rejected PR.

## Branching

<!-- FILL: your convention. Suggested default below. -->

- Branch off `main`: `type/short-description` (e.g. `feat/csv-export`, `fix/null-user`).
- Keep branches short-lived and focused on one change.

## Commits

<!-- FILL: your convention. Conventional Commits is a common default. -->

- Present tense, explains the *why* not just the *what*.
- One logical change per commit where practical.

## Pull requests

- Small and reviewable beats big and comprehensive. Split when you can.
- PR description says: what changed, why, and how you verified it.
- Green CI (tests + lint) before requesting review — see [docs/testing.md](docs/testing.md).
- Link the issue it closes.

## Review

<!-- FILL: how many approvals, who owns which areas (CODEOWNERS?), expected
     turnaround. Set the norm so review isn't a black hole. -->

## Recording decisions

If your change makes an architectural choice someone might later question, add an
ADR — copy `docs/adr/0000-adr-template.md` to the next number and fill it in.
Future-you will thank present-you.
