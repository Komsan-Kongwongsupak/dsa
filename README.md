# dsa

A from-scratch, pure-Python library of classic data structures and algorithms, built for computer science and AI/ML study and referenced against Cormen, Leiserson, Rivest & Stein's *Introduction to Algorithms* (CLRS).

The goal is a single, well-tested, fully-typed source to import from across coursework and projects, rather than re-implementing the same structures every time. Correctness is checked against trusted references (`sorted`, `networkx`, `scipy`, `scikit-learn`) using property-based testing.

## Status

Early and actively growing. Currently implemented:

**Structures**

- `UnionFind` — disjoint-set with path compression and union by rank

**Algorithms**

- `insertion_sort` / `insertion_sort_inplace` — CLRS Section 2.1
- `merge` — CLRS Section 2.3.1 (merge sort building block)

More structures and algorithms are added incrementally; see [Roadmap](#roadmap).

## Installation

This project isn't published to PyPI. Install it locally in editable mode:

```bash
git clone <your-repo-url>
cd dsa
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev,numeric]"
```

To use `dsa` from another project or notebook, install it into that environment the same way, pointing at this project's path:

```bash
pip install -e /path/to/dsa
```

## Usage

```python
from dsa import UnionFind, insertion_sort

uf = UnionFind(range(5))
uf.union(0, 1)
uf.union(1, 2)
uf.connected(0, 2)  # True
len(uf)  # 3 (number of components)

insertion_sort([5, 2, 4, 6, 1, 3])
# [1, 2, 3, 4, 5, 6]

insertion_sort(["banana", "fig", "apple"], key=len)
# ['fig', 'apple', 'banana']
```

## Project layout

```
dsa/
├── pyproject.toml
├── src/dsa/
│   ├── __init__.py          # public API
│   ├── _types.py            # shared TypeVars, Protocols
│   ├── structures/          # heap, union-find, trie, graph, ...
│   ├── algorithms/          # sorting, searching, graph algorithms, DP, ...
│   ├── ml/                  # autodiff, k-means, decision tree, ...
│   └── utils/
├── tests/                   # mirrors the src/ layout
├── benchmarks/
├── docs/
└── examples/
```

Everything importable lives under `src/dsa/` and is re-exported from `dsa/__init__.py`. Names prefixed with `_` are internal and may change without notice.

## Design principles

- **Typed and generic.** Structures and algorithms use `TypeVar`/`Generic` and accept `key=`/`reverse=` the way Python's built-ins do, so they work with any comparable or keyed type.
- **Protocol-based interfaces.** Algorithms depend on structural protocols (e.g. a `WeightedGraph` protocol) rather than concrete classes, so they work with this library's own structures or with adapters over others.
- **Faithful to CLRS.** Pseudocode is translated directly, with deviations (like 0-indexing or dropping `∞` sentinels) called out in docstrings.
- **Tested against trusted oracles.** Every algorithm has property-based tests (via `hypothesis`) checked against `sorted()`, `networkx`, `scipy`, or `scikit-learn` where applicable.
- **Documented complexity.** Every public function/class states time and space complexity in its docstring.
- **Dependency-free core.** The core has no required dependencies; NumPy lives behind the optional `numeric` extra.

## Development

```bash
pip install -e ".[dev,numeric]"

pytest                  # run tests
ruff check . --fix      # lint + autofix
ruff format .           # format
mypy src                # type-check
```

All four should pass cleanly before a commit.

## Roadmap

- [ ] Merge sort, heapsort, quicksort
- [ ] `MinHeap` / priority queue
- [ ] `Trie`
- [ ] `Graph` (adjacency list) + BFS, DFS, Dijkstra, A*, MST
- [ ] Dynamic programming (LCS, edit distance, knapsack, Viterbi)
- [ ] `KDTree`, k-means, decision tree
- [ ] Reverse-mode autodiff (micro-autograd)
- [ ] Optional Rust-backed extensions for performance-critical structures

## Reference

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. *Introduction to Algorithms* (3rd or 4th ed.). MIT Press.

## License

Add a license (e.g. MIT) before sharing this publicly. See `LICENSE`.
