"""Property-based tests for Wayfinder trip date helpers."""

from __future__ import annotations

from datetime import date, timedelta

import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

MAX_TRIP_INCLUSIVE_DAYS = 14

_DATES = st.dates(min_value=date(2020, 1, 1), max_value=date(2030, 12, 31))


@st.composite
def valid_trip_range(draw):
    start = draw(_DATES)
    span = draw(st.integers(min_value=1, max_value=MAX_TRIP_INCLUSIVE_DAYS))
    end = start + timedelta(days=span - 1)
    return start, end


@given(pair=valid_trip_range())
@settings(max_examples=80)
def test_validate_trip_date_range_accepts_valid(wayfinder, pair):
    start, end = pair
    wayfinder["validate_trip_date_range"](start, end)  # no raise


@given(start=_DATES, end=_DATES)
@settings(max_examples=60)
def test_validate_trip_date_range_end_before_start(wayfinder, start, end):
    assume(end < start)
    with pytest.raises(ValueError, match="on or after"):
        wayfinder["validate_trip_date_range"](start, end)


@given(start=_DATES)
@settings(max_examples=40)
def test_validate_trip_date_range_too_long(wayfinder, start):
    end = start + timedelta(days=MAX_TRIP_INCLUSIVE_DAYS)  # inclusive days = 15
    with pytest.raises(ValueError, match="at most"):
        wayfinder["validate_trip_date_range"](start, end)


@given(
    start=st.one_of(st.none(), _DATES),
    end=st.one_of(st.none(), _DATES),
)
@settings(max_examples=40)
def test_validate_trip_date_range_none_required(wayfinder, start, end):
    assume(start is None or end is None)
    with pytest.raises(ValueError, match="required"):
        wayfinder["validate_trip_date_range"](start, end)


@given(pair=valid_trip_range())
@settings(max_examples=80)
def test_iter_trip_dates_length_sorted_endpoints(wayfinder, pair):
    start, end = pair
    dates = wayfinder["iter_trip_dates"](start, end)
    expected_len = (end - start).days + 1
    assert len(dates) == expected_len
    assert dates == sorted(dates)
    assert dates[0] == start
    assert dates[-1] == end
    assert dates == [start + timedelta(days=i) for i in range(expected_len)]
