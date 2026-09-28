from __future__ import annotations

from collections.abc import Hashable, Iterable
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)

class UnionFind(Generic[K]):
    """Disjoint-set with path compression and union by rank.

    Complexity: find/union O(α(n)) amortized. Space O(n).
    """

    def __init__(self, items: Iterable[K] = ()) -> None:
        self._parent: dict[K, K] = {}
        self._rank: dict[K, int] = {}
        self._count = 0
        for x in items:
            self.add(x)

    def add(self, x: K) -> None:
        if x not in self._parent:
            self._parent[x] = x
            self._rank[x] = 0
            self._count += 1

    def find(self, x: K) -> K:
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != root:          # path compression
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a: K, b: K) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self._rank[ra] < self._rank[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        if self._rank[ra] == self._rank[rb]:
            self._rank[ra] += 1
        self._count -= 1
        return True

    def connected(self, a: K, b: K) -> bool:
        return self.find(a) == self.find(b)

    def __len__(self) -> int:
        return self._count                       # number of components

    def __contains__(self, x: object) -> bool:
        return x in self._parent
