"""Property-based tests for Wayfinder formatting / severity helpers."""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

_SEVERITY_MAP = {
    "critical": "extreme",
    "high": "high",
    "medium": "moderate",
    "moderate": "moderate",
    "low": "low",
}


@given(nights=st.none())
@settings(max_examples=5)
def test_format_nights_none(wayfinder, nights):
    assert wayfinder["_format_nights"](nights) == ""


@given(nights=st.just(1))
@settings(max_examples=5)
def test_format_nights_one(wayfinder, nights):
    assert wayfinder["_format_nights"](nights) == "1 Night"


@given(nights=st.integers().filter(lambda n: n != 1))
@settings(max_examples=60)
def test_format_nights_plural(wayfinder, nights):
    assert wayfinder["_format_nights"](nights) == f"{nights} Nights"


@given(
    score=st.floats(
        allow_nan=False,
        allow_infinity=False,
        width=64,
        min_value=-1e6,
        max_value=1e6,
    )
)
@settings(max_examples=100)
def test_score_to_level_threshold_bands(wayfinder, score):
    level = wayfinder["score_to_level"](score)
    if score >= 3.5:
        assert level == "extreme"
    elif score >= 2.5:
        assert level == "high"
    elif score >= 1.5:
        assert level == "moderate"
    else:
        assert level == "low"


@given(key=st.sampled_from(list(_SEVERITY_MAP)))
@settings(max_examples=20)
def test_normalize_travelrisk_severity_known(wayfinder, key):
    assert wayfinder["normalize_travelrisk_severity"](key) == _SEVERITY_MAP[key]


@given(
    key=st.sampled_from(list(_SEVERITY_MAP)),
    prefix=st.text(alphabet=" \t", max_size=3),
    suffix=st.text(alphabet=" \t", max_size=3),
    upper=st.booleans(),
)
@settings(max_examples=40)
def test_normalize_travelrisk_severity_case_whitespace(wayfinder, key, prefix, suffix, upper):
    raw = f"{prefix}{key.upper() if upper else key}{suffix}"
    assert wayfinder["normalize_travelrisk_severity"](raw) == _SEVERITY_MAP[key]


@given(
    value=st.one_of(
        st.none(),
        st.text().filter(lambda s: s.strip().lower() not in _SEVERITY_MAP),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
    )
)
@settings(max_examples=60)
def test_normalize_travelrisk_severity_unknown_defaults_low(wayfinder, value):
    assert wayfinder["normalize_travelrisk_severity"](value) == "low"
