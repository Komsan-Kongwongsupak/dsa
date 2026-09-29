from hypothesis import given
from hypothesis import strategies as st

from dsa import insertion_sort, insertion_sort_inplace


def test_examples():
    assert insertion_sort([]) == []
    assert insertion_sort([1]) == [1]
    assert insertion_sort([5, 2, 4, 6, 1, 3]) == [1, 2, 3, 4, 5, 6]


@given(st.lists(st.integers()))
def test_matches_sorted(xs):
    assert insertion_sort(xs) == sorted(xs)


@given(st.lists(st.integers()))
def test_reverse_matches_sorted(xs):
    assert insertion_sort(xs, reverse=True) == sorted(xs, reverse=True)


@given(st.lists(st.tuples(st.integers(0, 5), st.integers())))
def test_key_and_stability(pairs):
    # Sorting by the first field only: equal keys must keep original order,
    # which is exactly what sorted() guarantees too.
    assert insertion_sort(pairs, key=lambda p: p[0]) == sorted(
        pairs, key=lambda p: p[0]
    )


@given(st.lists(st.integers()))
def test_inplace_mutates_and_input_untouched_by_copy_version(xs):
    original = list(xs)
    insertion_sort(xs)
    assert xs == original  # the copying version doesn't mutate
    insertion_sort_inplace(xs)
    assert xs == sorted(original)  # the in-place version does
