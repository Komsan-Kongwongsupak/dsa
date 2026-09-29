import pytest
from hypothesis import given
from hypothesis import strategies as st

from dsa.algorithms.sorting import merge


def test_clrs_example():
    a = [2, 4, 5, 7, 1, 2, 3, 6]
    merge(a, 0, 3, 7)
    assert a == [1, 2, 2, 3, 4, 5, 6, 7]


def test_single_elements():
    a = [2, 1]
    merge(a, 0, 0, 1)
    assert a == [1, 2]


def test_invalid_indices():
    with pytest.raises(ValueError):
        merge([1, 2, 3], 2, 1, 2)
    with pytest.raises(ValueError):
        merge([1, 2, 3], 0, 1, 3)


@given(st.lists(st.integers()), st.lists(st.integers()))
def test_matches_sorted(xs, ys):
    xs, ys = sorted(xs), sorted(ys)
    if not xs:  # merge needs a non-empty left half
        return
    a = xs + ys
    merge(a, 0, len(xs) - 1, len(a) - 1)
    assert a == sorted(xs + ys)


@given(st.lists(st.integers()), st.lists(st.integers()))
def test_reverse(xs, ys):
    xs, ys = sorted(xs, reverse=True), sorted(ys, reverse=True)
    if not xs:
        return
    a = xs + ys
    merge(a, 0, len(xs) - 1, len(a) - 1, reverse=True)
    assert a == sorted(xs + ys, reverse=True)


@given(
    st.lists(st.integers()),
    st.lists(st.integers()),
    st.lists(st.integers(), max_size=5),
    st.lists(st.integers(), max_size=5),
)
def test_only_touches_range(xs, ys, before, after):
    xs, ys = sorted(xs), sorted(ys)
    if not xs:
        return
    a = before + xs + ys + after
    p = len(before)
    q = p + len(xs) - 1
    r = q + len(ys)
    merge(a, p, q, r)
    assert a[:p] == before
    assert a[r + 1 :] == after
    assert a[p : r + 1] == sorted(xs + ys)


@given(
    st.lists(st.tuples(st.integers(0, 3), st.integers())),
    st.lists(st.tuples(st.integers(0, 3), st.integers())),
)
def test_stability(xs, ys):
    first = lambda t: t[0]
    xs, ys = sorted(xs, key=first), sorted(ys, key=first)
    if not xs:
        return
    a = xs + ys
    merge(a, 0, len(xs) - 1, len(a) - 1, key=first)
    assert a == sorted(xs + ys, key=first)  # sorted() is stable too
