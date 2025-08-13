# Python Interview Algorithms Workbook

Clean, idiomatic Python implementations for senior/staff-level interview prep with complexity notes, pitfalls, and demo CLI.

## Installation and Usage

Install (editable) and run tests:
```bash
python -m pip install -U pip
python -m pip install -e .
pytest -q
```

Run demos:
```bash
python interview_workbook/main.py --list
python interview_workbook/main.py --demo sorting.merge_sort
python interview_workbook/main.py --demo graphs.dijkstra
```

## Modules Overview

- **algorithms/sorting**: merge, quick, heap, counting, radix
- **algorithms/searching**: binary search, bounds, rotated, infinite, quickselect
- **data_structures**: Union-Find, Trie, LRU/LFU, Fenwick, SegmentTree
- **graphs**: BFS/DFS, topo sort, Dijkstra, A*, Bellman-Ford, Floyd-Warshall, Kruskal, Prim
- **dp**: Fibonacci, coin change, LIS, knapsack, edit distance, bitmask TSP, state compression
- **strings**: KMP, Rabin-Karp, Z, Manacher, suffix array/LCP
- **math**: sieve, fast power, gcd/lcm, modular inverse, prefix sums (1D/2D)
- **concurrency**: threading, multiprocessing, asyncio, futures, producer-consumer
- **systems**: sliding window max, reservoir sampling, rate limiters, sharded BFS (concept), consensus notes
- **patterns**: backtracking, sudoku, meet-in-the-middle, binary search on answer, two-pointer, monotonic stack/queue

Each implementation includes:
- Time/space complexity analysis
- Common pitfalls and interviewer follow-ups
- Clean, production-ready code
- Demo functions for testing
