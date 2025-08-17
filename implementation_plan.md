# Implementation Plan

[Overview]
Unify the codebase under a single Python package namespace (interview_workbook) for consistency across CLI, tests, and the Flask dashboard, and add Merge Sort and Heap Sort visualizations.

This plan standardizes imports to a single top-level namespace and removes duplication between src/* modules and the root-level interview_workbook/* directory. It defines a precise file move strategy, configuration updates, import rewrites, and test changes to ensure a clean, maintainable structure. The dashboard will be updated to map discovered demos to the new package path, and the sorting visualization module will gain Merge and Heap algorithm frames. The plan also outlines a roadmap to expand common DSA coverage (trees, stacks/queues, additional patterns) while preserving current behavior and test coverage.

[Types]
Centralize common type aliases for reuse across modules.

Create a small types module to keep shared aliases:
- File: src/interview_workbook/types.py
- Definitions:
  - from collections.abc import Hashable, Sequence, Iterable, Callable
  - Graph = dict[Hashable, list[Hashable]]
  - WeightedGraph = dict[Hashable, list[tuple[Hashable, int]]]
  - Index = int
  - Pair = tuple[int, int]
  - Comparable = object (note: Python typing lacks a direct Comparable bound; we’ll rely on runtime comparisons)
Validation rules:
- Graph/WeightedGraph keys must be hashable; adjacency lists must contain only hashable nodes.
- Edge weights (int) are non-negative where algorithms assume Dijkstra; Bellman-Ford may accept negatives but not negative cycles unless explicitly stated.

[Files]
Restructure modules under a single package, update configs, and clean duplicates.

New files to be created:
- src/interview_workbook/__init__.py (expose high-level subpackages)
- src/interview_workbook/types.py (common aliases)
- src/interview_workbook/algorithms/__init__.py (moved from src/algorithms/__init__.py)
- src/interview_workbook/algorithms/sorting/__init__.py (moved)
- src/interview_workbook/algorithms/searching/__init__.py (moved)
- src/interview_workbook/data_structures/__init__.py (moved)
- src/interview_workbook/graphs/__init__.py (moved)
- src/interview_workbook/strings/__init__.py (moved)
- src/interview_workbook/dp/__init__.py (moved)
- src/interview_workbook/patterns/__init__.py (moved)
- src/interview_workbook/math_utils/__init__.py (moved)
- src/interview_workbook/systems/__init__.py (moved)
- src/interview_workbook/utils/__init__.py (moved)

Existing files to be moved (non-exhaustive, pattern-driven):
- src/algorithms/... ➜ src/interview_workbook/algorithms/...
- src/data_structures/... ➜ src/interview_workbook/data_structures/...
- src/graphs/... ➜ src/interview_workbook/graphs/...
- src/dp/... ➜ src/interview_workbook/dp/...
- src/strings/... ➜ src/interview_workbook/strings/...
- src/math_utils/... ➜ src/interview_workbook/math_utils/...
- src/patterns/... ➜ src/interview_workbook/patterns/...
- src/systems/... ➜ src/interview_workbook/systems/...
- src/utils/... ➜ src/interview_workbook/utils/...
- src/main.py remains in src/, but its DEMOS mapping will import interview_workbook.* modules.

Files to be modified:
- pyproject.toml:
  - [tool.setuptools.packages.find] include ➜ ["interview_workbook*"]
  - Keep package-dir {"" = "src"}
- tests/test_*.py:
  - Update imports to interview_workbook.* (e.g., from algorithms.sorting.merge_sort ➜ from interview_workbook.algorithms.sorting.merge_sort)
  - Update utils import to from interview_workbook.utils.check_sorted import is_sorted
- tests/conftest.py:
  - Likely unchanged (still adds src to sys.path). Remove any legacy comments pointing to top-level modules if needed.
- src/main.py:
  - Update DEMOS mapping module paths to interview_workbook.algorithms..., interview_workbook.graphs..., etc. Keep CLI keys (e.g., "sorting.merge_sort") stable for user ergonomics.
- flask_app/app.py:
  - SORTING_VIZ_MAP keys updated to "interview_workbook.algorithms.sorting.bubble_sort", etc.
  - Visualization module imports remain under flask_app/visualizations (unchanged).
  - discover_demos() will now find modules as "interview_workbook...." via src scan; no logic change required.
- flask_app/templates/index.html:
  - No template logic change; relies on updated sorting_viz_map and discovered IDs.
- flask_app/visualizations/sorting_viz.py:
  - Add merge_sort_frames and heap_sort_frames
  - Add entries to ALGORITHMS: "merge", "heap"

Files to be deleted or moved:
- Root-level interview_workbook/ directory (duplicate implementation set):
  - Action: audit for divergences; if files contain unique additions not present in src/, merge meaningful differences into src/interview_workbook/ equivalents; then remove the root-level interview_workbook/ to avoid ambiguity.
  - Interim: optionally move to docs/legacy/ for reference if differences exist (non-installed).
- Any leftover top-level package shims (src/algorithms, etc.) after migration: remove directories once imports and tests are green.

Configuration file updates:
- pyproject.toml changes as above
- Optional: add mypy config later (deferred)

[Functions]
Introduce visualization frames and update module registries; no algorithmic behavior changes otherwise.

New functions:
- merge_sort_frames(arr: list[int], max_steps: int = 40000) -> list[dict[str, Any]]
  - File: flask_app/visualizations/sorting_viz.py
  - Purpose: Visualization frames for Merge Sort; show comparisons, merges, and final array.
- heap_sort_frames(arr: list[int], max_steps: int = 40000) -> list[dict[str, Any]]
  - File: flask_app/visualizations/sorting_viz.py
  - Purpose: Visualization frames for Heap Sort; show heapify and extraction steps.

Modified functions:
- src/main.py: run_demo and DEMOS mapping updated to new module paths (interview_workbook.*)
- flask_app/app.py:
  - SORTING_VIZ_MAP content updated to interview_workbook.* module IDs
  - No signature changes; only mapping and discovered IDs alignment
- flask_app/visualizations/sorting_viz.py:
  - visualize() to route "merge" and "heap" keys

Removed functions:
- None

[Classes]
No immediate new classes for the A-priority item; tree/DSA expansions are staged next.

Future (deferred, part of “more common DSA” expansion):
- New classes:
  - BinaryTreeNode (src/interview_workbook/data_structures/trees.py)
    - Fields: val: int | T, left: BinaryTreeNode | None, right: BinaryTreeNode | None
    - Methods: inorder, preorder, postorder, level_order, insert_bst, search_bst, delete_bst
- Modified classes:
  - None in migration phase
- Removed classes:
  - None

[Dependencies]
No new runtime dependencies are required.

- Keep Flask>=3.0.0 for dashboard.
- Dev tools unchanged (ruff, pytest, pre-commit).
- Consider mypy in a future PR (deferred).

[Testing]
Adapt tests to the new namespace and add basic visualization checks.

- Update all tests to import from interview_workbook.*
- Add lightweight tests for visualization functions (optional but recommended):
  - For sorting_viz.merge_sort_frames and heap_sort_frames:
    - Generate small arrays (n=5)
    - Assert last frame is sorted
    - Assert frames are non-empty and respect max_steps
- Run existing suite to ensure parity:
  - pytest -q
- CI remains unchanged; ensure pre-commit and ruff run clean.

[Implementation Order]
Migrate namespace first, then add visualizations, then de-duplicate and cleanup.

1. Create new package skeleton under src/interview_workbook/ with __init__.py and types.py.
2. Move modules from src/* into src/interview_workbook/* (algorithms, data_structures, graphs, dp, strings, patterns, math_utils, systems, utils). Keep relative filenames.
3. Update pyproject.toml packages.find include=["interview_workbook*"].
4. Rewrite imports across the repo to interview_workbook.* in:
   - tests/**/*.py
   - src/main.py DEMOS mapping module paths
   - flask_app/app.py SORTING_VIZ_MAP keys
5. Run ruff check --fix and ruff format to normalize imports; run pytest -q; fix any misses.
6. Implement merge_sort_frames and heap_sort_frames in flask_app/visualizations/sorting_viz.py; register in ALGORITHMS with keys "merge" and "heap".
7. Verify UI:
   - Start Flask app; confirm discovered IDs show interview_workbook.* and visualization page includes Merge/Heap.
   - Validate API endpoints return frames for the new algorithms.
8. De-duplication:
   - Diff root-level interview_workbook/** vs src/interview_workbook/**.
   - Merge any unique content; remove root-level interview_workbook/ directory (or move to docs/legacy/).
9. Final cleanup:
   - Remove any now-empty top-level src/algorithms, src/graphs, etc.
   - Re-run tests, update README import examples to interview_workbook.*.
   - Commit with clear migration notes.
