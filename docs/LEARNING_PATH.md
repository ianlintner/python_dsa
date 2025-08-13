# Learning Path and Study Guide

This guide is a structured plan to learn and practice algorithms and data structures using this repository. It emphasizes problem patterns, implementation drills, and interview-style reasoning.

Audience: mid/senior/staff engineers preparing for interviews or solidifying fundamentals.

Time: 2–3 weeks at ~1.5–2 hours/day (adjust as needed).

## How to use this repo effectively

- Explore implementations under `src/` and run `demo()` functions via `python src/main.py --demo ...`
- Read docstrings for complexity, pitfalls, and follow-up questions.
- Use tests as templates for your own TDD-style practice under `tests/`.
- Create small kata sessions: re-implement a function from scratch, compare with provided code, add your notes.

Helpful commands:
- List available demos: `python src/main.py --list`
- Run a demo, e.g.: `python src/main.py --demo sorting.quick_sort`
- Run all tests: `pytest -q`

## High-level plan

- Week 1: Sorting, searching, patterns (sliding window, two pointers), basic graph traversal
- Week 2: Graphs (shortest paths, MST, SCC), DP core problems, strings
- Week 3: Practice sets, mixed interviews, systems/concurrency notes, number theory/prefix sums

Each day below includes goals, reading/implementations, and practice prompts.

---

## Week 1

Day 1: Sorting Fundamentals
- Read: `algorithms/sorting/insertion_sort.py`, `selection_sort.py`, `bubble_sort.py`
- Compare properties: stability, complexity, use cases
- Implement from scratch: insertion sort (stable), selection sort (not stable)
- Practice:
  - Prove insertion sort stability using adjacent swaps argument
  - When would you switch to insertion sort within quick/merge?

Day 2: Quicksort Variants
- Read: `algorithms/sorting/quick_sort.py` (standard, 3-way, iterative)
- Key topics: pivot strategies, 3-way partitioning for duplicates, worst-case avoidance
- Implement from scratch: 3-way partition quicksort
- Practice:
  - Explain worst-case triggers and mitigations
  - Why 3-way partitioning helps on low-entropy inputs

Day 3: Merge Sort and Heap Sort
- Read: `algorithms/sorting/merge_sort.py`, `heap_sort.py`
- Implement from scratch: merge step; discuss in-place merge tradeoffs
- Practice:
  - When is stable sort required?
  - Compare heap sort vs quicksort in practice

Day 4: Binary Search Family
- Read: `algorithms/searching/binary_search.py` and bounds/range, 2D
- Implement from scratch: `lower_bound`, `upper_bound`, `binary_search_range`
- Practice:
  - Common off-by-one pitfalls; overflow-safe mid
  - Use bounds to count occurrences

Day 5: Advanced Search
- Read: `algorithms/searching/advanced_search.py`
- Implement from scratch: rotated array search, exponential search, unknown-size accessor search
- Practice:
  - Why duplicates degrade rotated search to O(n)?
  - Design `get(i)` for unknown-sized arrays

Day 6: Sliding Window and Two Pointers
- Read: `patterns/sliding_window.py`, `two_pointers.py`, `monotonic_stack.py`
- Implement from scratch: fixed/variable window, monotonic queue for max-in-window
- Practice:
  - LeetCode-style: longest substring without repeat, min window substring outline
  - Max of each subarray of size k (monotonic deque)

Day 7: Review and Mixed Drills
- Run demos and tests; add 2 new tests for each module you studied
- Pick 3 problems and implement in under 30 minutes each:
  - Find first/last occurrence, search rotated array, sort colors (Dutch flag)
- Reflect: document your pitfalls and fixes in a personal notes file

---

## Week 2

Day 8: Graph Traversal
- Read: `graphs/bfs_dfs.py`, `graphs/topological_sort.py`
- Implement from scratch: BFS, DFS, topo with Kahn’s algorithm
- Practice:
  - Detect cycles in directed graph (topo vs DFS back-edges)

Day 9: Shortest Paths
- Read: `graphs/dijkstra.py`, `graphs/bellman_ford.py`, `graphs/floyd_warshall.py`, `graphs/a_star.py`
- Implement from scratch: Dijkstra with heap; Bellman-Ford (negative edges)
- Practice:
  - When to prefer Bellman-Ford or Floyd-Warshall
  - A* heuristics (admissible/consistent)

Day 10: MST
- Read: `graphs/mst.py`
- Implement from scratch: Kruskal (DSU), Prim (heap)
- Practice:
  - DSU optimizations (union by rank, path compression)
  - Differences between Kruskal and Prim in dense vs sparse

Day 11: SCC (Strongly Connected Components)
- Read: `graphs/scc.py` (Tarjan, Kosaraju)
- Implement from scratch: Tarjan’s algorithm
- Practice:
  - Explain low-link values and stack role
  - Condensation DAG properties

Day 12: Core DP
- Read: `dp/knapsack.py`, `dp/coin_change.py`, `dp/longest_increasing_subsequence.py`, `dp/edit_distance.py`, `dp/lcs.py`
- Implement from scratch: 0/1 knapsack, LIS (n log n version), Edit Distance, LCS (length + reconstruct)
- Practice:
  - State design: what dimensions and transitions?
  - Space optimization techniques (rolling arrays)

Day 13: Strings
- Read: `strings/kmp.py`, `strings/z_algorithm.py`, `strings/rabin_karp.py`, `strings/manacher.py`, `strings/suffix_array.py`
- Implement from scratch: KMP prefix function; Z algorithm; optionally Manacher
- Practice:
  - When to use Z vs KMP
  - Tradeoffs of hash-based search (collisions)

Day 14: Systems/Concurrency and Review
- Read: `systems/reservoir_sampling.py`, `systems/rate_limiter.py`, `systems/sharded_bfs.py`, `systems/consensus_basics.py`, `concurrency/intro.py`
- Practice:
  - Implement token bucket or leaky bucket in code and tests
  - Discuss parallel BFS and partitioning
  - Concurrency primitives and pitfalls

---

## Mixed Interview Sets (Week 3 or as time allows)

- Set A (45–60 min): lower/upper bound usage, rotated array search, sliding window (distinct at most K), LIS
- Set B: Dijkstra/Bellman-Ford scenario, MST edge cases, SCC on a real input, KMP/Z
- Set C: Edit distance variants (transpositions), coin change variations, knapsack with reconstruction, LCS
- Systems: streaming median design, rate limiting (distributed), sharded graph traversal

---

## Complexity quick reference

- Sorting:
  - Quick: average O(n log n), worst O(n^2), not stable; 3-way for duplicates
  - Merge: O(n log n), stable, O(n) extra; in-place is complex
  - Heap: O(n log n), not stable, in-place
  - Insertion: O(n^2), stable, great for small/nearly-sorted
- Searching:
  - Binary: O(log n); bounds/range queries; rotated/infinite patterns
  - Linear: O(n) for unsorted/small inputs
- Graphs:
  - BFS/DFS O(V+E)
  - Dijkstra O((V+E) log V), Bellman-Ford O(VE), Floyd-Warshall O(V^3)
  - MST (Kruskal/Prim) ≈ O(E log V)
  - SCC (Tarjan/Kosaraju) O(V+E)
- DP:
  - Knapsack O(nW), Coin Change O(n*amount)
  - LIS O(n log n)
  - Edit Distance O(nm), LCS O(nm)
- Strings:
  - KMP and Z: O(n + m)
  - Rabin-Karp average O(n + m), worst O(nm)
  - Manacher O(n)
- Math/Prefix:
  - Sieve O(n log log n), prefix sums O(n), 2D prefix sums O(nm)

---

## Tips for interviews

- Always state constraints and intent (time/space target, stable vs not, recursion vs iterative).
- Identify the pattern: sliding window? monotonic structure? binary search on answer? greedy with a proof?
- Validate edge cases (empty input, all duplicates, negative weights where applicable).
- Communicate tradeoffs: why choose a specific algorithm and what degrades its performance.
- Write small helper tests or print statements (demo functions here mimic that).

Good luck and keep iterating. Track your time and accuracy to build confidence.
