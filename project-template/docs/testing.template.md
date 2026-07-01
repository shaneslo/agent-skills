# Testing — how we test {{PROJECT_NAME}}

What we test, how to run it, and what "good enough to merge" means. The goal is
that anyone can run the suite in one command and trust a green result.

## How to run the tests

```bash
# FILL: the single command that runs everything. This must work from a clean
# checkout after setup. Add the narrower commands below it.
# all:
# one file/suite:
# with coverage:
# watch:
```

## What we test (and where)

<!-- FILL: name the layers this project actually uses; delete the ones it doesn't.
     The point is a shared vocabulary so "add a test" is never ambiguous. -->

| Layer | What it covers | Lives in | Mock boundary |
| --- | --- | --- | --- |
| Unit | pure logic, one module at a time | `<path>` | mock only external I/O |
| Integration | modules + real adapters (db, fs) | `<path>` | real deps, fake network |
| End-to-end | the system as a user hits it | `<path>` | nothing internal mocked |

## What to test — the bar for a change

<!-- FILL: your team's actual bar. Suggested default below; edit to taste. -->

- New behavior ships with a test that would fail without the change.
- Bug fixes start with a failing test that reproduces the bug (prove-it first).
- Test **behavior and contracts**, not implementation details — a passing suite
  should survive a safe refactor.
- Mock at boundaries only; never assert on things you can't control (wall-clock,
  network, generated text). Prefer deterministic inputs.

## Coverage expectations

<!-- FILL: a number only if you'll enforce it. An honest "we cover the core
     domain logic and the risky branches; we don't chase 100%" beats a vanity
     gate. State what's intentionally NOT covered and why. -->

## CI

<!-- FILL: which of these run on every PR vs nightly vs on-demand, and the link
     to the workflow. A test that CI doesn't run is documentation, not a safety
     net — say explicitly what is and isn't gated. -->
