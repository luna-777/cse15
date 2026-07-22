"""Property-based tests for Lens helper functions."""

from __future__ import annotations

from calendar import monthrange
from datetime import date

from hypothesis import given, settings
from hypothesis import strategies as st

_DATES = st.dates(min_value=date(1900, 1, 1), max_value=date(2100, 12, 31))
_COUNTS = st.integers(min_value=0, max_value=10_000)


@given(
    officer=_COUNTS,
    victim=_COUNTS,
    applicable=st.booleans(),
)
@settings(max_examples=100)
def test_lens2_ratio_none_or_rounded(lens, officer, victim, applicable):
    result = lens["_lens2_ratio"](officer, victim, applicable)
    if not applicable or victim == 0:
        assert result is None
    else:
        assert result == round(officer / victim * 100, 1)


@given(d=_DATES)
@settings(max_examples=80)
def test_month_end_last_day_same_year_month(lens, d):
    result = lens["_month_end"](d)
    last = monthrange(d.year, d.month)[1]
    assert result == date(d.year, d.month, last)
    assert result.year == d.year
    assert result.month == d.month
    assert result.day == last
