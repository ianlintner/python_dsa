# Implementation Plan

[Overview]
Add a curated “Top 100” coding interview problem set (based on NeetCode 150 core) into this repository with consistent structure, metadata, demos, and tests.

This implementation integrates a new leetcode-style problem package under src/interview_workbook/leetcode organized by canonical categories (arrays, two_pointers, sliding_window, stack, binary_search, linked_list, trees, tries, heap, backtracking, graphs, intervals, greedy, 1d_dp, 2d_dp, bit_manip, math_geometry). Each problem will be a self-contained module with Solution class and a demo() entrypoint for both CLI and Flask app discovery. A central registry provides metadata (id, title, category, difficulty, tags, slug) and enables index pages, demo discovery, and automated sanity checks.

This fills a practical gap: the repo already contains algorithmic building blocks (sorting/searching, DS, DP, graphs) but lacks a curated leetcode-problem suite. The new layer cross-links patterns to problems, provides runnable demos for each, and preserves the repository’s style of clear docstrings, complexity, pitfalls, and interviewer follow-ups.

[Types]  
Define canonical metadata and enums to index and validate the curated set.

Types to add (in a new module src/interview_workbook/leetcode/_types.py):
- Difficulty: Enum
  - fields: EASY, MEDIUM, HARD
- Category: Enum
  - fields: ARRAYS_HASHING, TWO_POINTERS, SLIDING_WINDOW, STACK, BINARY_SEARCH, LINKED_LIST, TREES, TRIES, HEAP, BACKTRACKING, GRAPHS, INTERVALS, GREEDY, DP_1D, DP_2D, BIT_MANIP, MATH_GEOMETRY
- Tag: Enum (optional, string enum)
  - examples: “hashmap”, “prefix_sum”, “monotonic_stack”, “union_find”, “dijkstra”, “topo”, “greedy”, etc.
- ProblemMeta: TypedDict
  - id: int | None (LeetCode ID when applicable)
  - slug: str (filesystem-safe, e.g., “two_sum”)
  - title: str (“Two Sum”)
  - category: Category
  - difficulty: Difficulty
  - tags: list[str] (Tag labels as strings for flexibility)
  - module: str (full dotted path to module, e.g., “interview_workbook.leetcode.arrays.two_sum”)
  - url: str | None (LeetCode link if available)
  - notes: str | None (short description)
Validation rules:
- slug matches module filename, lowercase, underscores.
- module path matches category/slug file location.
- category must match parent directory category.
- difficulty ∈ {EASY, MEDIUM, HARD}.

[Files]
Create the leetcode problem suite files and a registry, modify the CLI to dynamically discover demos, and leave Flask discovery unchanged (it already scans for demo()).

New files to be created:
- src/interview_workbook/leetcode/__init__.py
  - Purpose: Package init.
- src/interview_workbook/leetcode/_types.py
  - Purpose: Types (Difficulty, Category, Tag, ProblemMeta).
- src/interview_workbook/leetcode/_registry.py
  - Purpose: PROBLEMS: list[ProblemMeta], and helpers:
    - get_all() -> list[ProblemMeta]
    - by_category(cat: Category) -> list[ProblemMeta]
    - by_slug(slug: str) -> ProblemMeta | None
    - validate_registry() -> None (assert paths/types)
- src/interview_workbook/leetcode/_runner.py
  - Purpose: Common runner to execute sample tests for a problem’s Solution; used by demos.
  - Provides:
    - run_samples(problem: ProblemMeta) -> str (pretty-printed outputs)
- src/interview_workbook/leetcode/<category>/__init__.py for each category
  - Purpose: namespace.
- src/interview_workbook/leetcode/<category>/<slug>.py
  - Purpose: Single-problem module with:
    - docstring containing Title, URL, Difficulty, Category, Patterns, Complexity, Pitfalls, Follow-ups
    - class Solution with canonical method signature(s)
    - demo() that uses _runner.run_samples with in-file sample cases.

New docs:
- docs/NEETCODE_TOP100.md
  - Purpose: Human-readable index linking titles -> file paths, category, and brief notes. (Optional; the code registry is ground truth.)

Existing files to be modified:
- src/main.py
  - Change: add dynamic discovery (merge static DEMOS with discovered demo()-bearing modules under src/), so new “leetcode.*” demos appear in CLI.
  - Functions to add/modify:
    - discover_demos() -> dict[str, tuple[str, str]] mapping keys to (module, “demo”)
    - list_demos(): list from merged DEMOS
    - run_demo(): unchanged behavior, but keys now include dynamically discovered entries.
- Optionally, flask_app/app.py
  - No required changes; it already discovers modules by scanning src for demo(). If category prettification is desired, add a mapping to rewrite “interview_workbook/leetcode/…” to “leetcode/…”.

Files to be deleted or moved:
- None.

Configuration updates:
- None required (no new dependencies).

[Functions]
Introduce new helper functions for registry/discovery and maintain demo runner alignment.

New functions:
- src/interview_workbook/leetcode/_registry.py
  - get_all() -> list[ProblemMeta]
  - by_category(cat: Category) -> list[ProblemMeta]
  - by_slug(slug: str) -> ProblemMeta | None
  - validate_registry() -> None
- src/interview_workbook/leetcode/_runner.py
  - run_samples(problem: ProblemMeta) -> str
- src/main.py
  - discover_demos() -> dict[str, tuple[str, str]]
    - Scan src/ for python modules with a top-level demo(), build keys like “leetcode.arrays.two_sum” and return a mapping.
  - list_demos() (modified)
    - Merge static DEMOS + dynamic discover_demos(), unique-sort keys.

Modified functions:
- src/main.py
  - list_demos(): now includes dynamic registry.
  - main() / run_demo(): unchanged logic, but broader namespace support.

Removed functions:
- None.

[Classes]
Define one new enum set and maintain LeetCode-style Solution classes per problem.

New classes:
- src/interview_workbook/leetcode/_types.py
  - Enum Difficulty
  - Enum Category
  - (Optional) Enum Tag

Per-problem:
- class Solution:
  - Methods vary per problem; must match canonical signatures and include clear typing and docstrings.
  - demo() at module level uses Solution and in-file sample vectors.

Modified classes:
- None in existing codebase.

Removed classes:
- None.

[Dependencies]
No new third-party dependencies.

Everything is standard library; pytest remains used for tests; Flask stays for UI.

[Testing]
Add lightweight tests for the registry and a representative subset of problems to enforce structure and sample correctness.

Tests:
- tests/test_leetcode_registry.py
  - validate that PROBLEMS is non-empty, slugs map to files, metadata is consistent.
- tests/test_leetcode_samples.py
  - parametrize over a subset of problems (e.g., 15–20 spread across categories) and assert sample inputs match expected outputs from demo() or a dedicated sample_cases collection in each module.

Validation strategies:
- CI runs existing suite and new tests.
- Lint via Ruff as configured.
- Ensure demo() discovery works in both CLI and Flask.

[Implementation Order]
Implement foundation first (types/registry/runner), wire discovery, then add problems in batches by category with tests.

1. Create package skeleton: leetcode/__init__.py, _types.py, _registry.py, _runner.py, category __init__.py files.
2. Implement CLI discovery in src/main.py (discover_demos + list_demos merge).
3. Add initial seed problems (2–3 per category) to validate structure and UI integration; add tests for registry + samples.
4. Bulk-add remaining problems per curated list (below) in 4–6 batches; keep tests updated.
5. Optional: category name prettification in Flask UI.
6. Final: run full CI, update docs/NEETCODE_TOP100.md with coverage checklist.

--------------------------------
Curated NeetCode Core Top 100 Roster (by category -> slug “Title”)
Note: This anchors the registry ground truth. Each becomes a module at src/interview_workbook/leetcode/<category>/<slug>.py

Arrays & Hashing (10)
- two_sum “Two Sum”
- contains_duplicate “Contains Duplicate”
- valid_anagram “Valid Anagram”
- group_anagrams “Group Anagrams”
- top_k_frequent_elements “Top K Frequent Elements”
- product_of_array_except_self “Product of Array Except Self”
- valid_sudoku “Valid Sudoku”
- longest_consecutive_sequence “Longest Consecutive Sequence”
- encode_and_decode_strings “Encode and Decode Strings”
- longest_common_prefix “Longest Common Prefix”

Two Pointers (6)
- valid_palindrome “Valid Palindrome”
- two_sum_ii “Two Sum II - Input Array Is Sorted”
- three_sum “3Sum”
- three_sum_closest “3Sum Closest”
- container_with_most_water “Container With Most Water”
- move_zeroes “Move Zeroes”

Sliding Window (8)
- best_time_to_buy_sell_stock “Best Time to Buy and Sell Stock”
- longest_substring_without_repeating “Longest Substring Without Repeating Characters”
- minimum_window_substring “Minimum Window Substring”
- longest_repeating_character_replacement “Longest Repeating Character Replacement”
- permutation_in_string “Permutation in String”
- find_all_anagrams_in_string “Find All Anagrams in a String”
- sliding_window_maximum “Sliding Window Maximum”
- subarray_product_less_than_k “Subarray Product Less Than K”

Stack (7)
- valid_parentheses “Valid Parentheses”
- min_stack “Min Stack”
- evaluate_reverse_polish_notation “Evaluate Reverse Polish Notation”
- generate_parentheses “Generate Parentheses”
- daily_temperatures “Daily Temperatures”
- car_fleet “Car Fleet”
- largest_rectangle_in_histogram “Largest Rectangle in Histogram”

Binary Search (7)
- binary_search “Binary Search”
- search_in_rotated_sorted_array “Search in Rotated Sorted Array”
- find_min_in_rotated_sorted_array “Find Minimum in Rotated Sorted Array”
- search_2d_matrix “Search a 2D Matrix”
- find_kth_smallest_in_sorted_matrix “Kth Smallest Element in a Sorted Matrix”
- koko_eating_bananas “Koko Eating Bananas”
- find_peak_element “Find Peak Element”

Linked List (7)
- reverse_linked_list “Reverse Linked List”
- merge_two_sorted_lists “Merge Two Sorted Lists”
- reorder_list “Reorder List”
- remove_nth_node_from_end “Remove Nth Node From End of List”
- linked_list_cycle “Linked List Cycle”
- linked_list_cycle_ii “Linked List Cycle II”
- add_two_numbers “Add Two Numbers”

Trees (8)
- invert_binary_tree “Invert Binary Tree”
- max_depth_binary_tree “Maximum Depth of Binary Tree”
- diameter_of_binary_tree “Diameter of Binary Tree”
- balanced_binary_tree “Balanced Binary Tree”
- same_tree “Same Tree”
- subtree_of_another_tree “Subtree of Another Tree”
- validate_bst “Validate Binary Search Tree”
- binary_tree_level_order_traversal “Binary Tree Level Order Traversal”

Tries (2)
- implement_trie “Implement Trie (Prefix Tree)”
- add_and_search_word “Design Add and Search Words Data Structure”

Heap / Priority Queue (5)
- kth_largest_element “Kth Largest Element in an Array”
- top_k_frequent_words “Top K Frequent Words”
- find_median_from_data_stream “Find Median from Data Stream”
- task_scheduler “Task Scheduler”
- last_stone_weight “Last Stone Weight”

Backtracking (5)
- subsets “Subsets”
- subsets_ii “Subsets II”
- combination_sum “Combination Sum”
- combination_sum_ii “Combination Sum II”
- permutations “Permutations”

Graphs (7)
- number_of_islands “Number of Islands”
- clone_graph “Clone Graph”
- course_schedule “Course Schedule”
- course_schedule_ii “Course Schedule II”
- pacific_atlantic_water_flow “Pacific Atlantic Water Flow”
- surrounded_regions “Surrounded Regions”
- rotting_oranges “Rotting Oranges”

Intervals (5)
- merge_intervals “Merge Intervals”
- insert_interval “Insert Interval”
- non_overlapping_intervals “Non-overlapping Intervals”
- meeting_rooms “Meeting Rooms”
- meeting_rooms_ii “Meeting Rooms II”

Greedy (4)
- jump_game “Jump Game”
- jump_game_ii “Jump Game II”
- gas_station “Gas Station”
- partition_labels “Partition Labels”

1-D DP (6)
- climbing_stairs “Climbing Stairs”
- house_robber “House Robber”
- house_robber_ii “House Robber II”
- coin_change “Coin Change”
- longest_increasing_subsequence “Longest Increasing Subsequence”
- partition_equal_subset_sum “Partition Equal Subset Sum”

2-D DP (5)
- unique_paths “Unique Paths”
- longest_common_subsequence “Longest Common Subsequence”
- edit_distance “Edit Distance”
- word_break “Word Break”
- maximal_square “Maximal Square”

Bit Manipulation (4)
- single_number “Single Number”
- number_of_1_bits “Number of 1 Bits”
- counting_bits “Counting Bits”
- reverse_bits “Reverse Bits”

Math & Geometry (4)
- rotate_image “Rotate Image”
- spiral_matrix “Spiral Matrix”
- set_matrix_zeroes “Set Matrix Zeroes”
- happy_number “Happy Number”

Notes:
- Where implementations already exist (e.g., LIS, LCS, edit distance, coin change, trie) we will either reference the canonical approach or wrap existing functions into a LeetCode-style Solution while keeping docstrings aligned with problem expectations.
