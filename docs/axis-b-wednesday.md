# Axis B Wednesday — Function Selection + Hypothesis Setup

**Date:** 2026-07-22  
**Goal:** Finalize ~10 pure-ish Python functions and configure a working Hypothesis/pytest pilot environment.  
**Out of scope today:** writing `@given` properties, generating cases, or recording pass/fail results (Thursday).

## Repos cloned

| Repo | URL | Local path |
|------|-----|------------|
| Alexandria | https://github.com/ucsc-cse115a-alexandria/alexandria | `repos/alexandria/` |
| Wayfinder | https://github.com/juansant-cmyk/wayfinder | `repos/wayfinder/` |
| Lens | https://github.com/jacobluanjohnston/Lens | `repos/Lens/` |

Note: sources were fetched as GitHub `main` tarballs (sandbox blocked writing `.git/` during `git clone`). Contents match the shortlisted remotes.

## Final selected functions (10)

| # | Repo | Function | Path | Language | Why kept | Import smoke |
|---|------|----------|------|----------|----------|--------------|
| 1 | Alexandria | `normalize` | `src/alexandria/ir/similarity.py` | Python | Pure L2-normalize over numpy vectors; clear I/O | PASS |
| 2 | Alexandria | `compute_cos_sim_diff` | `src/alexandria/ir/similarity.py` | Python | Pure cosine-distance helper; clear float output | PASS |
| 3 | Alexandria | `_similarity_matrix` | `src/alexandria/ir/similarity.py` | Python | Pure bytes→matrix transform; original candidate | PASS |
| 4 | Wayfinder | `validate_trip_date_range` | `backend/app/schemas/travel.py` | Python | Pure date-range validation; no I/O | PASS |
| 5 | Wayfinder | `iter_trip_dates` | `backend/app/schemas/travel.py` | Python | Deterministic date list from range | PASS |
| 6 | Wayfinder | `_format_nights` | `backend/app/services/favorites.py` | Python | Pure int→label formatting | PASS |
| 7 | Wayfinder | `score_to_level` | `backend/app/services/safety.py` | Python | Pure float→severity bucket mapping | PASS |
| 8 | Wayfinder | `normalize_travelrisk_severity` | `backend/app/providers/travelrisk.py` | Python | Pure string normalization map | PASS |
| 9 | Lens | `_lens2_ratio` | `backend/app/api/lens.py` | Python | Pure arithmetic with None edge cases | PASS |
| 10 | Lens | `_month_end` | `backend/app/api/lens.py` | Python | Pure calendar end-of-month | PASS |

Alexandria note: preliminary candidates `target_round` / merger helpers were missing or network-bound. Kept nearby pure helpers from `similarity.py` instead (still Alexandria, same IR surface).

## Dropped candidates

| Repo | Function | Path | Why dropped |
|------|----------|------|-------------|
| Alexandria | `target_round` | `src/alexandria/ir/contracts.py` | Not present in current `main` tree |
| Alexandria | `default_merger` | `src/alexandria/utils/merger.py` | Factory for OpenAI client; network/API side effects |
| Alexandria | `merge_candidates_to_target` | `src/alexandria/utils/merger.py` | Instance method that calls OpenAI |
| Alexandria | `_apply_prune_prefix` | `src/alexandria/ops/features/target.py` | Needs full `Document` IR construction / heavy mocking |
| Alexandria | `_serialize_embedding` | `src/alexandria/ir/document.py` | Pydantic `@field_serializer` method, not a free function |
| Wayfinder | `_distance_key` | `backend/app/services/hotel_sort.py` | Circular import via providers on module load; not needed for 10 |
| Wayfinder | `normalize_country_codes` | `backend/app/services/geocode.py` | Importable with JWT, but cut for headroom (pycountry lookup) |
| Lens | `_parse_year_month` | `backend/app/api/lens.py` | Importable; raises `HTTPException` (framework-coupled); cut for headroom |
| Lens | `_norm_category` | `pipeline/adapters/sf/ingest.py` | Importable; pandas-coupled; cut for headroom |
| Lens | `_norm_resolution` | `pipeline/adapters/sf/ingest.py` | Importable; pandas-coupled; cut for headroom |

## Pilot environment

| Item | Value |
|------|-------|
| Python | 3.13 (`/usr/local/bin/python3.13`) |
| Virtualenv | `pbt-venv/` (gitignored; `.venv/` is blocked in this environment) |
| Requirements | [`requirements-pbt.txt`](../requirements-pbt.txt) — Hypothesis, pytest, plus minimal import deps |
| Hypothesis | 6.160.0 |
| pytest | 9.1.1 |

### Activate

```bash
cd /Users/joshuacao/cse15
source pbt-venv/bin/activate
```

### Import smoke commands (no property runs)

```bash
# Tools
pbt-venv/bin/python -c "import hypothesis, pytest; print(hypothesis.__version__, pytest.__version__)"

# Alexandria (avoid package __init__, which downloads tiktoken encodings)
pbt-venv/bin/python -c "
import sys, types
from pathlib import Path
root = Path('repos/alexandria/src/alexandria')
pkg = types.ModuleType('alexandria'); pkg.__path__=[str(root)]; sys.modules['alexandria']=pkg
ir = types.ModuleType('alexandria.ir'); ir.__path__=[str(root/'ir')]; sys.modules['alexandria.ir']=ir
from alexandria.ir.similarity import normalize, compute_cos_sim_diff, _similarity_matrix
print('ok')
"

# Wayfinder (Settings requires a non-default JWT secret)
JWT_SECRET='wednesday-pbt-pilot-not-for-production-use-abcdefghijklmnopqrstuvwxyz' \
PYTHONPATH=repos/wayfinder/backend pbt-venv/bin/python -c "
from app.schemas.travel import validate_trip_date_range, iter_trip_dates
from app.services.favorites import _format_nights
from app.services.safety import score_to_level
from app.providers.travelrisk import normalize_travelrisk_severity
print('ok')
"

# Lens
PYTHONPATH=repos/Lens/backend pbt-venv/bin/python -c "
from app.api.lens import _lens2_ratio, _month_end
print('ok')
"
```

### Setup caveats for Thursday

1. **Alexandria package import:** `import alexandria` pulls ops + tiktoken encoding download. Prefer the namespace-package load above (or install encodings offline) when writing tests.
2. **Wayfinder Settings:** set `JWT_SECRET` to a non-placeholder value before importing modules that load `app.core.config`.
3. **Shared `app` package name:** Wayfinder and Lens both use `app.*` — import them in separate processes or clear `sys.modules` between repos.
4. **No `@given` tests yet** — property writing and pass/fail recording are Thursday work.

## Thursday preview

Write Hypothesis properties for the 10 kept functions, run them, record pass/fail + minimal failing examples, separate real bugs from bad tests/setup, and note scaling limits.
