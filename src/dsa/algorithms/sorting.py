from __future__ import annotations

from collections.abc import Callable, Iterable, MutableSequence
from typing import Any, TypeVar

T = TypeVar("T")


def _identity(x: Any) -> Any:
    return x


def insertion_sort_inplace(
    a: MutableSequence[T],
    *,
    key: Callable[[T], Any] | None = None,
    reverse: bool = False,
) -> None:
    """Sort ``a`` in place using insertion sort.

    Stable: equal elements keep their original relative order.

    Complexity:
        Time:  O(n^2) worst/average, O(n) best (already sorted).
        Space: O(1) extra.

    Note: ``key`` is called repeatedly on elements during comparisons
    (O(n^2) calls worst case), unlike ``sorted``, which calls it once
    per element.
    """
    k = key or _identity
    for j in range(1, len(a)):
        item = a[j]
        item_key = k(item)
        # Insert a[j] into the sorted sequence a[0 .. j-1]
        i = j - 1
        while i >= 0 and (k(a[i]) < item_key if reverse else k(a[i]) > item_key):
            a[i + 1] = a[i]
            i -= 1
        a[i + 1] = item


def insertion_sort(
    iterable: Iterable[T],
    *,
    key: Callable[[T], Any] | None = None,
    reverse: bool = False,
) -> list[T]:
    """Return a new sorted list from ``iterable`` (like ``sorted``).

    Complexity: O(n^2) time, O(n) space (the copy).
    """
    result = list(iterable)
    insertion_sort_inplace(result, key=key, reverse=reverse)
    return result


def merge(
    a: MutableSequence[T],
    p: int,
    q: int,
    r: int,
    *,
    key: Callable[[T], Any] | None = None,
    reverse: bool = False,
) -> None:
    """Merge sorted ``a[p..q]`` and ``a[q+1..r]`` (inclusive) in place.

    Precondition: both subarrays are already sorted under the same
    ``key``/``reverse`` settings. Postcondition: ``a[p..r]`` is sorted.

    Stable: on ties, elements from the left half come first.

    Complexity:
        Time:  Θ(n) where n = r - p + 1.
        Space: Θ(n) for the two temporary copies.
    """
    if not 0 <= p <= q <= r < len(a):
        raise ValueError(f"need 0 <= p <= q <= r < len(a); got {p=}, {q=}, {r=}")

    k = key or _identity
    n1 = q - p + 1
    n2 = r - q

    left = [a[p + i] for i in range(n1)]
    right = [a[q + 1 + j] for j in range(n2)]
    left_keys = [k(x) for x in left]  # key called once per element
    right_keys = [k(x) for x in right]

    i = j = 0
    for m in range(p, r + 1):
        # Take from the left unless the right element strictly precedes it.
        # Using a strict comparison on the right is what keeps the merge stable.
        if i < n1 and (
            j >= n2
            or not (
                right_keys[j] > left_keys[i]
                if reverse
                else right_keys[j] < left_keys[i]
            )
        ):
            a[m] = left[i]
            i += 1
        else:
            a[m] = right[j]
            j += 1


def merge_sort_inplace(
    a: MutableSequence[T],
    p: int = 0,
    r: int | None = None,
    *,
    key: Callable[[T], Any] | None = None,
    reverse: bool = False,
) -> None:
    """Sort ``a[p..r]`` (inclusive) in place using merge sort.

    ``r`` defaults to ``len(a) - 1`` so it can be called as
    ``merge_sort_inplace(a)`` on the whole sequence.

    Stable: ties keep their original relative order (inherited from
    ``merge``).

    Complexity:
        Time:  Θ(n log n) always.
        Space: Θ(n) auxiliary (from ``merge``'s temporary copies).
    """
    if r is None:
        r = len(a) - 1
    if p < r:
        q = (p + r) // 2
        merge_sort_inplace(a, p, q, key=key, reverse=reverse)
        merge_sort_inplace(a, q + 1, r, key=key, reverse=reverse)
        merge(a, p, q, r, key=key, reverse=reverse)


def merge_sort(
    iterable: Iterable[T],
    *,
    key: Callable[[T], Any] | None = None,
    reverse: bool = False,
) -> list[T]:
    """Return a new sorted list from ``iterable`` (like ``sorted``).

    Complexity: Θ(n log n) time, Θ(n) space.
    """
    result = list(iterable)
    merge_sort_inplace(result, key=key, reverse=reverse)
    return result
