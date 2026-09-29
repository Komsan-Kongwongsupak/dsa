from hypothesis import given
from hypothesis import strategies as st

from dsa import merge_sort, merge_sort_inplace


def test_examples():
    assert merge_sort([]) == []
    assert merge_sort([1]) == [1]
    assert merge_sort([5, 2, 4, 6, 1, 3]) == [1, 2, 3, 4, 5, 6]


@given(st.lists(st.integers()))
def test_matches_sorted(xs):
    assert merge_sort(xs) == sorted(xs)


@given(st.lists(st.integers()))
def test_reverse_matches_sorted(xs):
    assert merge_sort(xs, reverse=True) == sorted(xs, reverse=True)


@given(st.lists(st.tuples(st.integers(0, 5), st.integers())))
def test_key_and_stability(pairs):
    assert merge_sort(pairs, key=lambda p: p[0]) == sorted(pairs, key=lambda p: p[0])


@given(st.lists(st.integers()))
def test_inplace_mutates_and_copy_version_does_not(xs):
    original = list(xs)
    merge_sort(xs)
    assert xs == original  # copying version leaves input untouched
    merge_sort_inplace(xs)
    assert xs == sorted(original)  # in-place version mutates


@given(st.lists(st.integers(), min_size=1))
def test_partial_range(xs):
    # sort only a sub-range and check the rest is untouched
    a = xs + [999, -999]
    merge_sort_inplace(a, 0, len(xs) - 1)
    assert a[: len(xs)] == sorted(xs)
    assert a[len(xs) :] == [999, -999]
