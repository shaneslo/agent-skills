# Test Coverage Analysis

_An assessment of the current automated-test situation in this repository, with a
prioritized set of proposals for where new tests would buy the most safety._

## TL;DR

The repository ships **real executable code** — a ~1,100-line Python package
(`bpa-generator/bpa/`), a 230-line Node validator (`scripts/validate-skills.js`),
and six shell hooks — but the automated-test surface is almost empty:

- **Only two tests exist** (`hooks/session-start-test.sh`,
  `hooks/simplify-ignore-test.sh`), and **CI runs neither of them.**
- CI (`.github/workflows/test-plugin-install.yml`) runs only
  `node scripts/validate-skills.js` and `claude plugin validate` — there is no
  `pytest`, no JS unit runner, and no invocation of the existing bash harnesses.
- The `bpa-generator` Python package has **zero tests** and no test
  configuration (`pyproject.toml` / `pytest.ini` absent).
- `scripts/validate-skills.js`, the gate that protects every other PR, has **no
  tests of its own**.

The good news: most of the highest-risk code is **deterministic and pure**
(state→XML rendering, file dispatch, frontmatter parsing, config resolution), so
it is cheap to test well without mocking an LLM. The codebase is explicitly
designed around that ("determinism at the edges" — see
`bpa-generator/README.md`), which makes it unusually test-friendly.

---

## Current coverage map

| Area | LOC (approx) | Tests today | CI-enforced |
| --- | --- | --- | --- |
| `bpa-generator/bpa/` (Python pkg) | ~1,116 | none | no |
| `scripts/validate-skills.js` | ~230 | none | runs in CI, but untested itself |
| `hooks/session-start.sh` | 24 | `session-start-test.sh` | **no** |
| `hooks/simplify-ignore.sh` | 302 | `simplify-ignore-test.sh` | **no** |
| `hooks/sdd-cache-pre.sh` / `-post.sh` | 106 / 135 | none | no |
| `registry.json` + per-skill `registry.json` | data | none (not referenced anywhere) | no |
| `skills/**/SKILL.md` content | docs | structure-validated by `validate-skills.js` | yes |

The single biggest gap is that **the two tests that do exist never run** — they
can rot silently because nothing executes them.

---

## Proposed improvements (prioritized)

### P0 — Wire the existing tests into CI

Lowest effort, immediate value. Two working bash harnesses already exist but are
invisible to CI. Add a job to `.github/workflows/test-plugin-install.yml` that
runs them:

```yaml
  hook-tests:
    name: Hook unit tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bash hooks/session-start-test.sh
      - run: bash hooks/simplify-ignore-test.sh
```

Without this, every other testing investment below is also at risk of silently
not running. Make "tests run in CI" the baseline before adding more.

### P1 — Unit-test the deterministic core of `bpa-generator`

These modules contain branching logic, string assembly, and schema rules but **no
LLM calls**, so they can be tested directly with `pytest` and plain fixtures.
Highest value-per-test:

1. **`bpa/assembly/bpmn.py` → `render_bpmn`** — pure `StructuredState → XML`.
   Test: empty steps (start→end only), linear steps produce N tasks + N+1 flows,
   a step with `decision_points` injects an `exclusiveGateway`, and that
   `condition` / `who` / `what` strings containing `&`, `<`, `"` are XML-escaped
   (the code calls `escape()` — assert it actually holds). Well-formed-XML
   assertion via `xml.dom.minidom.parseString`.

2. **`bpa/ingestion/extractors.py` → `format_extractor`** — dispatch on file
   extension. Test: `.pptx`/`.ppt`/`.pdf` route correctly, and an unsupported
   suffix raises `ValueError` with the expected message. The `.pptx` and `.pdf`
   bodies can be covered with tiny real fixtures or by monkeypatching
   `_extract_ppt` / `_extract_pdf`.

3. **`bpa/config.py` → `RunConfig.model_for`** — env-override precedence. Test:
   `BPA_MODEL_<ROLE>` overrides defaults; unknown role raises `KeyError`;
   `GatewayConfig` reads `AI_GATEWAY_API_KEY` then falls back to
   `ANTHROPIC_API_KEY`. Use `monkeypatch.setenv`.

4. **`bpa/state.py` → `merge_sections` / `merge_critiques`** — the LangGraph
   reducers that let nine writers fan in without clobbering each other. Test:
   `None` operands, disjoint keys union, right-wins-on-conflict. This is exactly
   the concurrency-correctness logic that breaks subtly in production.

5. **`bpa/assembly/assembler.py` → `_ordered` + `assembler`** — sections sort by
   `SECTIONS_BY_ID[id].order`, unknown ids sink to `999`, the process-name slug
   is lowercased/space-and-slash-replaced, and `enable_bpmn=False` omits the
   `.bpmn` file. Drive `assembler` against a `tmp_path` out-dir and assert the
   written files and `artifacts["paths"]`.

6. **`bpa/ingestion/gate.py` → confidence floor + `_read_snippet`** — the
   business rule that "below `gate_confidence_floor`, `is_procedure` is forced
   False" is safety-critical and easy to regress. Inject a fake model (a stub
   exposing `.with_structured_output().invoke()`) returning a high-confidence
   `is_procedure=True` *and* a `confidence=0.3` case; assert the floor flips the
   second to rejected. Separately unit-test `_read_snippet` truncation and the
   `.txt`/binary branches against `tmp_path` files.

> A fake-model fixture (a small object with
> `with_structured_output(self, schema)` returning something whose `.invoke()`
> yields a canned pydantic object) unlocks `gate`, `normalizer`, and the
> writer/evaluator node **without any network or API key** — mock at the
> `get_model` boundary only, matching `references/testing-patterns.md`.

### P2 — Test the writer/evaluator control flow (not the prose)

`bpa/writers/base.py` contains the only real control flow in the LLM layer:
bounded revision. With a fake model you can assert behavior without judging text:

- `enable_evaluators=False` → exactly one writer call, no critique, `revision=0`.
- evaluator returns `passes=False` → writer is called again, `revision=1`, and
  the loop stops after `max_revisions` (it "cannot spin" — prove it).
- evaluator returns `passes=True` → no revision call.
- the returned `critique.section_id` is forced to `cfg.id` (`model_copy` update).

These are deterministic given a scripted fake model and protect the spec's
"bounded revision" contract.

### P3 — Test the CI gatekeeper: `scripts/validate-skills.js`

This script decides whether every other PR passes. It is logic-heavy
(frontmatter regex, exemption allowlist, dead-reference detection) and currently
trusts itself. Add a lightweight runner (`node --test` is built-in, zero deps)
covering:

- `parseFrontmatter`: CRLF vs LF, quoted vs unquoted values, missing block → `null`,
  keys with colons in the value.
- name/dir mismatch is an error; description > 1024 chars is an error.
- the **exemption-bypass guard**: a skill declaring `type: meta` while *not* in
  `SECTION_EXEMPT_SKILLS` must error (this is a security-relevant check — it
  stops contributors self-exempting).
- `extractSkillReferences` flags a dead cross-reference but ignores generic
  inline code.
- exit code is `1` when any error is present, `0` otherwise.

Run against fixture skill directories in a temp dir so it doesn't depend on the
live `skills/` tree.

### P4 — Validate `registry.json` against the real tree

`registry.json` and the per-skill `registry.json` files are referenced by **no**
script and **no** CI step, so they drift freely from `skills/`. Add a check that:

- every `files[].path` in `registry.json` exists on disk,
- every `skills/<name>/` directory has a corresponding registry item,
- `registryDependencies` point at items that actually exist.

This is pure data validation — fast, deterministic, high signal against the most
common rot in this repo (a skill added or renamed without updating the registry).

### P5 — Cover the remaining hooks + an end-to-end smoke test

- Add harnesses for `hooks/sdd-cache-pre.sh` / `sdd-cache-post.sh` mirroring the
  style of the two existing hook tests (cache hit/miss, hash stability).
- One **graph smoke test** for `bpa/graph.py` `run(...)` with all models faked:
  assert a gate-rejection short-circuits to `rejected=True` and that a happy path
  writes both artifacts. This guards the wiring (`Send` fan-out, conditional
  edges) that unit tests don't exercise.

---

## Suggested minimal test scaffolding

```
bpa-generator/
  pyproject.toml          # [tool.pytest.ini_options]; declares pytest + deps
  tests/
    conftest.py           # fake-model fixture, sample StructuredState factory
    test_bpmn.py          # P1.1
    test_extractors.py    # P1.2
    test_config.py        # P1.3
    test_reducers.py      # P1.4
    test_assembler.py     # P1.5
    test_gate.py          # P1.6
    test_writer_node.py   # P2
scripts/
  validate-skills.test.js # P3 (node --test)
  validate-registry.js    # P4 (new check) + its test
.github/workflows/
  test-plugin-install.yml # add: hook-tests, python-tests, js-tests jobs
```

## Guiding principles (consistent with this repo's own guidance)

- **Mock only at the `get_model` boundary** — never assert on generated prose;
  assert on control flow, schema conformance, and deterministic transforms
  (`references/testing-patterns.md`: "Mock at Boundaries Only").
- **Prioritize deterministic, branchy, safety-critical code** — the gate
  confidence floor, the revision bound, XML escaping, and the fan-in reducers are
  where a silent regression does real damage.
- **Make CI the source of truth** — a test that CI doesn't run (today's state) is
  documentation, not a safety net. P0 fixes that first.
