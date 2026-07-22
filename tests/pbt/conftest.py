"""Shared fixtures and import loaders for Axis B property-based tests.

Student repos are treated as read-only. Import caveats from docs/axis-b-wednesday.md:
- Alexandria: avoid `import alexandria` (tiktoken download); use namespace-package load.
- Wayfinder: set non-placeholder JWT_SECRET before Settings-touching imports.
- Wayfinder and Lens both ship `app.*` — load functions, then purge `app` from sys.modules
  so a single pytest process can exercise both.
"""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
REPOS = REPO_ROOT / "repos"

# Wayfinder Settings rejects empty / "change-me-in-production". Prefer a real
# JWT_SECRET from the environment; otherwise use this clearly local dummy.
_LOCAL_JWT_DUMMY = "pbt-local-dummy"


def _ensure_jwt_secret() -> None:
    os.environ.setdefault("JWT_SECRET", _LOCAL_JWT_DUMMY)


def _purge_app_modules() -> None:
    for name in list(sys.modules):
        if name == "app" or name.startswith("app."):
            del sys.modules[name]


def _load_alexandria_similarity():
    """Load similarity helpers without triggering alexandria package __init__."""
    root = REPOS / "alexandria" / "src" / "alexandria"
    if "alexandria" not in sys.modules:
        pkg = types.ModuleType("alexandria")
        pkg.__path__ = [str(root)]
        sys.modules["alexandria"] = pkg
    if "alexandria.ir" not in sys.modules:
        ir = types.ModuleType("alexandria.ir")
        ir.__path__ = [str(root / "ir")]
        sys.modules["alexandria.ir"] = ir
    from alexandria.ir.similarity import (  # noqa: WPS433
        _similarity_matrix,
        compute_cos_sim_diff,
        normalize,
    )

    return {
        "normalize": normalize,
        "compute_cos_sim_diff": compute_cos_sim_diff,
        "_similarity_matrix": _similarity_matrix,
    }


def _load_wayfinder_fns():
    _ensure_jwt_secret()
    backend = str(REPOS / "wayfinder" / "backend")
    _purge_app_modules()
    sys.path.insert(0, backend)
    try:
        from app.providers.travelrisk import normalize_travelrisk_severity
        from app.schemas.travel import iter_trip_dates, validate_trip_date_range
        from app.services.favorites import _format_nights
        from app.services.safety import score_to_level

        return {
            "validate_trip_date_range": validate_trip_date_range,
            "iter_trip_dates": iter_trip_dates,
            "_format_nights": _format_nights,
            "score_to_level": score_to_level,
            "normalize_travelrisk_severity": normalize_travelrisk_severity,
        }
    finally:
        _purge_app_modules()
        if backend in sys.path:
            sys.path.remove(backend)


def _load_lens_fns():
    backend = str(REPOS / "Lens" / "backend")
    _purge_app_modules()
    sys.path.insert(0, backend)
    try:
        from app.api.lens import _lens2_ratio, _month_end

        return {
            "_lens2_ratio": _lens2_ratio,
            "_month_end": _month_end,
        }
    finally:
        _purge_app_modules()
        if backend in sys.path:
            sys.path.remove(backend)


@pytest.fixture(scope="session")
def alexandria():
    return _load_alexandria_similarity()


@pytest.fixture(scope="session")
def wayfinder():
    return _load_wayfinder_fns()


@pytest.fixture(scope="session")
def lens():
    return _load_lens_fns()
