"""Property-based tests for Alexandria similarity helpers."""

from __future__ import annotations

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

# Modest sizes keep matrix tests fast while still exploring shapes.
_DIM = st.integers(min_value=1, max_value=8)
_COUNT = st.integers(min_value=1, max_value=6)
_FLOATS = st.floats(
    min_value=-10.0,
    max_value=10.0,
    allow_nan=False,
    allow_infinity=False,
    width=32,
)


def _vector(dim: int) -> st.SearchStrategy[np.ndarray]:
    return st.lists(_FLOATS, min_size=dim, max_size=dim).map(
        lambda xs: np.asarray(xs, dtype=np.float32)
    )


def _nonzero_vector(dim: int) -> st.SearchStrategy[np.ndarray]:
    return _vector(dim).filter(lambda v: float(np.linalg.norm(v)) > 1e-6)


def _stack(n: int, dim: int) -> st.SearchStrategy[np.ndarray]:
    return st.lists(_vector(dim), min_size=n, max_size=n).map(
        lambda rows: np.asarray(rows, dtype=np.float32)
    )


def _nonzero_stack(n: int, dim: int) -> st.SearchStrategy[np.ndarray]:
    return st.lists(_nonzero_vector(dim), min_size=n, max_size=n).map(
        lambda rows: np.asarray(rows, dtype=np.float32)
    )


@given(dim=_DIM, vec=st.data())
@settings(max_examples=80)
def test_normalize_nonzero_unit_l2_and_shape(alexandria, dim, vec):
    normalize = alexandria["normalize"]
    v = vec.draw(_nonzero_vector(dim))
    out = normalize(v)
    assert out.shape == v.shape
    assert abs(float(np.linalg.norm(out)) - 1.0) < 1e-5


@given(n=_COUNT, dim=_DIM, data=st.data())
@settings(max_examples=60)
def test_normalize_stack_preserves_shape_and_unit_rows(alexandria, n, dim, data):
    normalize = alexandria["normalize"]
    stack = data.draw(_nonzero_stack(n, dim))
    out = normalize(stack)
    assert out.shape == stack.shape
    norms = np.linalg.norm(out, axis=-1)
    assert np.allclose(norms, 1.0, atol=1e-5)


@given(dim=_DIM, data=st.data())
@settings(max_examples=60)
def test_compute_cos_sim_diff_identical_near_zero(alexandria, dim, data):
    compute_cos_sim_diff = alexandria["compute_cos_sim_diff"]
    a = data.draw(_nonzero_vector(dim))
    assert abs(compute_cos_sim_diff(a, a.copy()) - 0.0) < 1e-5


@given(dim=_DIM, data=st.data())
@settings(max_examples=40)
def test_compute_cos_sim_diff_orthogonal_near_one(alexandria, dim, data):
    compute_cos_sim_diff = alexandria["compute_cos_sim_diff"]
    # Build an orthogonal pair in R^dim (dim>=2) via Gram-Schmidt-ish pick.
    if dim < 2:
        return
    a = data.draw(_nonzero_vector(dim))
    b = data.draw(_nonzero_vector(dim))
    # Project b off a; skip if residual collapses.
    proj = (float(a @ b) / float(a @ a)) * a
    b_orth = b - proj
    if float(np.linalg.norm(b_orth)) <= 1e-6:
        return
    b_orth = b_orth.astype(np.float32)
    diff = compute_cos_sim_diff(a, b_orth)
    assert abs(diff - 1.0) < 1e-4


@given(dim=_DIM, data=st.data())
@settings(max_examples=80)
def test_compute_cos_sim_diff_range(alexandria, dim, data):
    compute_cos_sim_diff = alexandria["compute_cos_sim_diff"]
    a = data.draw(_nonzero_vector(dim))
    b = data.draw(_nonzero_vector(dim))
    diff = compute_cos_sim_diff(a, b)
    # Cosine similarity in [-1, 1] ⇒ distance in [0, 2]
    assert 0.0 - 1e-5 <= diff <= 2.0 + 1e-5


@given(n=_COUNT, dim=_DIM, data=st.data())
@settings(max_examples=50)
def test_similarity_matrix_shape_diag_symmetric(alexandria, n, dim, data):
    _similarity_matrix = alexandria["_similarity_matrix"]
    embeddings = data.draw(_nonzero_stack(n, dim))
    matrix = _similarity_matrix(embeddings.tobytes(), embeddings.shape)
    assert matrix.shape == (n, n)
    assert np.allclose(np.diag(matrix), 1.0, atol=1e-5)
    assert np.allclose(matrix, matrix.T, atol=1e-5)
