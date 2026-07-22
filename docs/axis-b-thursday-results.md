# Axis B Thursday — Property-Based Testing Pilot Results

**Date:** 2026-07-22  
**Ticket:** Pilot property-based testing on 5–10 student-repository functions (#1)  
**Branch:** `axis-b-wednesday-pbt-setup`  
**Scope:** Axis B only (Hypothesis on locked Python functions). Not Axis A/C, not RQ3, not AI-log correlation.

## One-sentence outcome

End-to-end Hypothesis/pytest properties for all **10** locked functions ran green (**20** tests, **0** failures); no genuine student-code bugs found in this pilot.

## E2E run command

```bash
cd /Users/joshuacao/cse15
source pbt-venv/bin/activate
# Optional: set JWT_SECRET yourself. If unset, tests/pbt/conftest.py uses a local dummy
# (anything except empty / Wayfinder's "change-me-in-production" placeholder).
pytest tests/pbt/ -v
```

## Recorded suite output (full run)

```
platform darwin -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
hypothesis profile 'default'
plugins: hypothesis-6.160.0

collected 20 items

tests/pbt/test_alexandria_similarity.py::test_normalize_nonzero_unit_l2_and_shape PASSED
tests/pbt/test_alexandria_similarity.py::test_normalize_stack_preserves_shape_and_unit_rows PASSED
tests/pbt/test_alexandria_similarity.py::test_compute_cos_sim_diff_identical_near_zero PASSED
tests/pbt/test_alexandria_similarity.py::test_compute_cos_sim_diff_orthogonal_near_one PASSED
tests/pbt/test_alexandria_similarity.py::test_compute_cos_sim_diff_range PASSED
tests/pbt/test_alexandria_similarity.py::test_similarity_matrix_shape_diag_symmetric PASSED
tests/pbt/test_lens_helpers.py::test_lens2_ratio_none_or_rounded PASSED
tests/pbt/test_lens_helpers.py::test_month_end_last_day_same_year_month PASSED
tests/pbt/test_wayfinder_misc.py::test_format_nights_none PASSED
tests/pbt/test_wayfinder_misc.py::test_format_nights_one PASSED
tests/pbt/test_wayfinder_misc.py::test_format_nights_plural PASSED
tests/pbt/test_wayfinder_misc.py::test_score_to_level_threshold_bands PASSED
tests/pbt/test_wayfinder_misc.py::test_normalize_travelrisk_severity_known PASSED
tests/pbt/test_wayfinder_misc.py::test_normalize_travelrisk_severity_case_whitespace PASSED
tests/pbt/test_wayfinder_misc.py::test_normalize_travelrisk_severity_unknown_defaults_low PASSED
tests/pbt/test_wayfinder_travel.py::test_validate_trip_date_range_accepts_valid PASSED
tests/pbt/test_wayfinder_travel.py::test_validate_trip_date_range_end_before_start PASSED
tests/pbt/test_wayfinder_travel.py::test_validate_trip_date_range_too_long PASSED
tests/pbt/test_wayfinder_travel.py::test_validate_trip_date_range_none_required PASSED
tests/pbt/test_wayfinder_travel.py::test_iter_trip_dates_length_sorted_endpoints PASSED

============================== 20 passed in 5.90s ==============================
```

Environment notes from the run:
- Hypothesis fell back to an in-memory example database (default `.hypothesis/examples` path unusable in this environment). Does not affect pass/fail.
- Student trees under `repos/` treated as read-only; tests live under `tests/pbt/` in cse15.

## Results by function

| # | Repo | Function | Properties exercised | Result | Minimal failing example | Triage |
|---|------|----------|----------------------|--------|-------------------------|--------|
| 1 | Alexandria | `normalize` | Non-zero → L2 ≈ 1; shape preserved (vector + stack) | PASS | — | — |
| 2 | Alexandria | `compute_cos_sim_diff` | Identical ≈ 0; orthogonal ≈ 1; range ∈ [0, 2] | PASS | — | — |
| 3 | Alexandria | `_similarity_matrix` | Shape `(n,n)`; diagonal ≈ 1; symmetric | PASS | — | — |
| 4 | Wayfinder | `validate_trip_date_range` | Valid OK; end&lt;start / too long (&gt;14) / None → `ValueError` | PASS | — | — |
| 5 | Wayfinder | `iter_trip_dates` | Length = inclusive span; sorted; endpoints match | PASS | — | — |
| 6 | Wayfinder | `_format_nights` | `None` → `""`; `1` → `"1 Night"`; else `"{n} Nights"` | PASS | — | — |
| 7 | Wayfinder | `score_to_level` | Threshold bands match source (`3.5`/`2.5`/`1.5`) | PASS | — | — |
| 8 | Wayfinder | `normalize_travelrisk_severity` | Known map; unknown → `"low"`; case/whitespace tolerant | PASS | — | — |
| 9 | Lens | `_lens2_ratio` | `None` when inapplicable or victim=0; else rounded ratio | PASS | — | — |
| 10 | Lens | `_month_end` | Last day of month; year/month unchanged | PASS | — | — |

**Summary:** 10/10 functions PASS · 0 genuine code bugs · 0 invalid/over-strong tests that failed · 0 setup/import failures in the recorded run.

## Test layout

```
tests/pbt/
  conftest.py                 # Alexandria namespace load; JWT_SECRET env/dummy; app.* purge for Wayfinder vs Lens
  test_alexandria_similarity.py
  test_wayfinder_travel.py
  test_wayfinder_misc.py
  test_lens_helpers.py
```

Import strategy (honors Wednesday caveats):
1. **Alexandria** — namespace-package stub for `alexandria` / `alexandria.ir` so package `__init__` (tiktoken) is never imported.
2. **Wayfinder** — `JWT_SECRET` from the environment (or a local dummy via `setdefault`); functions extracted then `app.*` purged from `sys.modules`.
3. **Lens** — same purge/load pattern so Wayfinder and Lens can share one pytest process despite both using `app.*`.

## Triage notes

No failures to triage. Pre-run setup risks that were **avoided** (and must not be reported as student bugs if they reappear):

| Symptom | Likely cause | Classification |
|---------|--------------|----------------|
| Hang / network on Alexandria import | `import alexandria` pulls tiktoken encodings | **setup/import** — use namespace load |
| `JWT_SECRET` validation error on Wayfinder import | Placeholder secret rejected by Settings | **setup/import** — set `JWT_SECRET` env (or rely on conftest dummy) |
| Wrong helpers / missing symbols after collecting both Wayfinder + Lens | Shared `app` package name collision | **setup/import** — purge `app.*` between loads (handled in `conftest.py`) |

## Acceptance criteria map

| Criterion | Status |
|-----------|--------|
| 5–10 functions documented | Done (Wednesday `docs/axis-b-wednesday.md`) |
| Tools configured | Done (`pbt-venv` + Hypothesis/pytest) |
| Tests execute successfully | Done — `pytest tests/pbt/ -v` → 20 passed |
| Pass/fail recorded | Done — this document |
| E2E run demonstrated | Done — full suite log above |
| Scaling limitations documented | Done — section below |

## Scaling limitations + next steps

### What this pilot does **not** prove yet

1. **Function selection cost** — Finding 10 importable pure-ish helpers took manual inspection + dropped candidates (network-bound, framework-coupled, circular imports). Scaling to “all student functions” needs automation for purity / import graph filtering.
2. **Import isolation tax** — Shared package names (`app`), Settings side effects, and package `__init__` downloads are per-repo hazards. A multi-repo harness needs a standard loader (path + env + module purge), not ad-hoc test imports.
3. **Property authoring cost** — Properties here mirrored obvious contracts from source. Ambiguous or I/O-heavy code will need oracles, mocks, or differential tests — Hypothesis alone does not invent expected behavior.
4. **False confidence on green** — All 10 PASS does not mean the student repos are correct overall; only that these properties hold for the sampled inputs. Zero-vector / NaN / empty-embedding edges were intentionally constrained for `normalize` / cosine helpers.
5. **Language coverage** — Pilot is Python-only. TypeScript / fast-check was deferred until Python is green (now green) — next expansion can add a TS slice without blocking Axis B.
6. **No AI-log correlation** — Out of scope this week (Luna/Asin). Failures here are not yet linked to chat prompts or commit tasks.
7. **Not a benchmark unit** — Axis B tests functions in place; RQ3 packaging (pre-commit + prompt + outcome + tests) remains separate.

### Recommended next steps (after Issue #1)

1. Codify the loader helpers from `tests/pbt/conftest.py` into a small reusable harness module.
2. Add a second wave of functions (still Python) with slightly less “pure” surface (e.g. pydantic validators in situ) to measure property-writing friction.
3. Optionally pilot one TS function with fast-check now that Python E2E is proven.
4. Keep student repos read-only; continue housing pilot tests under cse15.
5. Defer AI-log ↔ failure correlation until Axis B reporting format is stable.

## Done definition (Thursday)

- [x] Hypothesis `@given` properties for all 10 locked functions  
- [x] Full suite run recorded  
- [x] Failures triaged (none; setup pitfalls documented)  
- [x] `docs/axis-b-thursday-results.md` completes Issue #1 Thursday deliverable  
