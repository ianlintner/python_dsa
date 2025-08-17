# Python Interview Algorithms Workbook

Clean, idiomatic Python implementations for senior/staff-level interview prep with complexity notes, pitfalls, demos, and tests.

This repo uses a src/ layout. Tests import modules directly from src/ via `tests/conftest.py`, so you can run and explore without packaging.

## Quickstart

Install (editable) and run tests:
```
python -m pip install -U pip
python -m pip install -e .
pytest -q
```

Run demos:
```
python src/main.py --list
python src/main.py --demo sorting.merge_sort
python src/main.py --demo searching.binary_search
python src/main.py --demo dp.lcs
python src/main.py --demo graphs.scc
```

Tip: If you see an import error when running a demo, run from the repo root (so `./src` is on `sys.path` via our launcher).

## Modules Overview

- algorithms/sorting
  - comparison: merge, quick (standard/3-way/iterative), heap, insertion, selection, bubble
  - non-comparison: counting, radix
- algorithms/searching
  - binary search family: classic, bounds, range, 2D
  - advanced: rotated, rotated-with-duplicates, exponential, unknown-size accessor
  - selection: quickselect (median, kth)
  - linear search (for unsorted/small inputs)
- data_structures
  - Union-Find (DSU), Trie, LRU/LFU caches, Fenwick tree, Segment tree, heap patterns
- graphs
  - BFS/DFS, Topological sort, Dijkstra, A*, Bellman-Ford, Floyd-Warshall, MST (Kruskal/Prim), SCC (Tarjan)
- dp
  - Fibonacci, coin change, LIS, knapsack, edit distance, bitmask TSP, state compression grid, LCS (longest common subsequence)
- strings
  - KMP, Rabin-Karp, Z-algorithm, Manacher, suffix array/LCP
- math_utils
  - sieve, gcd/lcm, extended GCD, modular inverse (Fermat/ExtGCD), fast power, prefix sums (1D/2D), difference array
- patterns
  - sliding window, monotonic stack/queue, two pointers, backtracking, meet-in-the-middle, binary search on answer
- systems/concurrency
  - reservoir sampling, rate limiters, sharded BFS (concept), consensus notes; concurrency intro

Each implementation includes:
- Time/space complexity analysis
- Common pitfalls and interviewer follow-ups
- Clean, production-ready code
- Demo functions for quick experimentation

## How to use in your own code

Import directly from src/ packages (tests do the same):

- Sorting (stable baseline)
```
from interview_workbook.algorithms.sorting.insertion_sort import insertion_sort
print(insertion_sort([3, 1, 2]))  # [1, 2, 3]
```

- Sorting (faster average case)
```
from interview_workbook.algorithms.sorting.quick_sort import quick_sort
print(quick_sort([5, 2, 8, 1]))
```

- Searching (sorted array)
```
from interview_workbook.algorithms.searching.binary_search import binary_search, lower_bound, upper_bound
arr = [1, 2, 2, 3, 5]
print(binary_search(arr, 3))     # 3
print(lower_bound(arr, 2))       # 1
print(upper_bound(arr, 2))       # 3 (first index > 2)
```

- Searching (unsorted/small)
```
from interview_workbook.algorithms.searching.linear_search import linear_search
print(linear_search(["b", "a", "c"], "a"))  # 1
```

- DP (LCS)
```
from interview_workbook.dp.lcs import lcs_length, lcs_reconstruct
print(lcs_length("abcde", "ace"))     # 3
print(lcs_reconstruct("abcde", "ace"))# "ace"
```

- Graphs (SCC)
```
from interview_workbook.graphs.scc import tarjan_scc
g = {0:[1],1:[2],2:[0,3],3:[4],4:[5],5:[3]}
print(tarjan_scc(g))  # e.g., [[0,2,1],[3,5,4]]
```

## Study guide and interview prep plan

A structured 2–3 week plan with checkpoints, must-know problems, and exercises is provided here:
- docs/LEARNING_PATH.md

Highlights:
- Day 1–3: Sorting/bounds/2-pointer patterns; implement insertion/selection/bubble to build fundamentals; graduate to quick/merge/heap
- Day 4–6: Binary search family, rotated/infinite array, sliding window and monotonic structures
- Day 7–9: Graphs (BFS/DFS, topo, Dijkstra), MST, SCC; practice classic questions
- Day 10–12: DP (knapsack, coin change, LIS, edit distance, LCS); practice transitions and state design
- Strings/math as needed (KMP, Z, Rabin-Karp, prefix sums), plus systems/concurrency notes

## Running and extending tests

- Run all tests: `pytest -q`
- Add your own tests under `tests/test_*.py`
- See `tests/test_sorting.py` and `tests/test_searching.py` for structure
- This PR adds tests for the new sorts and linear search to ensure parity with existing implementations

## Repo layout

- src/…: All implementation modules grouped by domain (algorithms, data_structures, graphs, dp, strings, math_utils, patterns, systems)
- src/main.py: CLI to list and run demos
- tests/…: Pytest suite; `tests/conftest.py` places `src/` on the module path

## Contributing

- Keep implementations clean, iterative where appropriate, with clear docstrings
- Include complexity, pitfalls, and a small `demo()` if practical
- Extend tests to cover edge cases (empty, single, sorted/reverse, duplicates, random, large)

## Development (linting & formatting)

Local setup (editable install + dev tools):
```
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

One-time Git hook setup (runs on commit):
```
pre-commit install
```

Manual formatting and linting:
```
# Format code (Ruff formatter)
ruff format .

# Lint code (Ruff rules E,F,I,B,UP etc.)
ruff check .

# Auto-fix simple issues
ruff check --fix
```

Run all pre-commit hooks on the whole repo:
```
pre-commit run --all-files --show-diff-on-failure --color=always
```

CI runs:
- Install with extras: `pip install -e ".[dev]"`
- Run pre-commit hooks (format + lint + misc checks)
- Run tests via `pytest -q`
