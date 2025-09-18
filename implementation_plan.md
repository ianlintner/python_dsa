# Implementation Plan

[Overview]  
The goal is to complete the missing demos in `src/interview_workbook/algorithms/searching` by ensuring each algorithm module has a `demo()` function that runs sample inputs and prints results.

The searching algorithms already have core implementations (`binary_search`, `linear_search`, `quickselect`, `advanced_search`). Some files already contain a `demo()` function, but others are incomplete or inconsistent. This plan ensures all searching modules expose a consistent `demo()` entry point for testing and demonstration purposes. This will improve usability, testing coverage, and educational value of the repository.

[Types]  
No new type system changes are required.

All functions will continue to use Python type hints (`list[int]`, `Sequence[int]`, `Callable`, etc.) as already present in the codebase.

[Files]  
We will add or complete `demo()` functions in the following files:
- `src/interview_workbook/algorithms/searching/binary_search.py` (already has `demo()`, ensure coverage of all variants)
- `src/interview_workbook/algorithms/searching/linear_search.py` (already has `demo()`, expand with more cases)
- `src/interview_workbook/algorithms/searching/quickselect.py` (already has `demo()`, expand with median/kth examples)
- `src/interview_workbook/algorithms/searching/advanced_search.py` (already has `demo()`, expand with rotated array, exponential search, unknown size)

No files will be deleted or moved.  
No configuration changes are required.

[Functions]  
We will standardize and expand the `demo()` functions.

- **New/Expanded demo functions**:
  - `binary_search.py:demo()` → Show standard binary search, recursive, lower/upper bound, first/last occurrence, range search, 2D search, insert position.
  - `linear_search.py:demo()` → Show single match, multiple matches (`find_all`), and not-found case.
  - `quickselect.py:demo()` → Show kth smallest, kth largest, median, and randomized partitioning.
  - `advanced_search.py:demo()` → Show rotated array search, rotated with duplicates, exponential search, and unknown size search.

No core algorithm functions will be modified. Only demos will be added/expanded.

[Classes]  
No new classes are required.  
The only class-like structure is the helper `search_unknown_size` wrapper in `advanced_search.py`, which will be exercised in its demo.

[Dependencies]  
No new dependencies are required.  
We will continue using Python standard library only.

[Testing]  
We will extend `tests/test_demos.py` to ensure each `demo()` runs without error.  
- Add tests that call each `demo()` and assert no exceptions are raised.  
- Optionally capture stdout to verify expected substrings (e.g., "Found at index", "Median is").  

This ensures demos remain functional and educational.

[Implementation Order]  
1. Update `binary_search.py:demo()` to cover all variants.  
2. Update `linear_search.py:demo()` with multiple cases.  
3. Update `quickselect.py:demo()` with kth/median examples.  
4. Update `advanced_search.py:demo()` with rotated/exponential/unknown size examples.  
5. Add/expand tests in `tests/test_demos.py` to call all demos.  
6. Run pytest to confirm all demos pass.
