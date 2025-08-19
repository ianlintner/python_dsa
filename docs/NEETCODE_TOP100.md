# NeetCode Top 100 LeetCode Problems

This document provides an index of the curated NeetCode Top 100 problems implemented in this repository.

## Overview

The LeetCode problem collection is organized into 17 categories based on algorithmic patterns. Each problem includes:

- **Solution class** with canonical method signatures
- **Comprehensive test cases** with edge cases
- **Demo function** for CLI and Flask integration
- **Educational content** including complexity analysis, pitfalls, and follow-ups
- **Problem metadata** with difficulty, tags, and LeetCode links

## Access Methods

### CLI
```bash
python3 src/main.py --list                    # List all available demos
python3 src/main.py --demo leetcode.arrays_hashing.two_sum
```

### Flask Web Interface
```bash
python3 -m flask --app flask_app.app run
```
Then navigate to http://localhost:5000 to explore problems interactively.

### Python API
```python
from interview_workbook.leetcode import get_all, by_category
from interview_workbook.leetcode._types import Category

# Get all problems
problems = get_all()

# Get problems by category
arrays_problems = by_category(Category.ARRAYS_HASHING)
```

## Problem Categories

### Arrays & Hashing (10 problems)
Focus on array manipulation and hash table usage patterns.

**Implemented:**
- [x] `two_sum` - Two Sum (Easy)

**Planned:**
- [ ] `contains_duplicate` - Contains Duplicate (Easy)
- [ ] `valid_anagram` - Valid Anagram (Easy)
- [ ] `group_anagrams` - Group Anagrams (Medium)
- [ ] `top_k_frequent_elements` - Top K Frequent Elements (Medium)
- [ ] `product_of_array_except_self` - Product of Array Except Self (Medium)
- [ ] `valid_sudoku` - Valid Sudoku (Medium)
- [ ] `longest_consecutive_sequence` - Longest Consecutive Sequence (Medium)
- [ ] `encode_and_decode_strings` - Encode and Decode Strings (Medium)
- [ ] `longest_common_prefix` - Longest Common Prefix (Easy)

### Two Pointers (6 problems)
Problems solved using two-pointer technique with opposite or same direction pointers.

**Implemented:**
- [x] `valid_palindrome` - Valid Palindrome (Easy)

**Planned:**
- [ ] `two_sum_ii` - Two Sum II - Input Array Is Sorted (Easy)
- [ ] `three_sum` - 3Sum (Medium)
- [ ] `three_sum_closest` - 3Sum Closest (Medium)
- [ ] `container_with_most_water` - Container With Most Water (Medium)
- [ ] `move_zeroes` - Move Zeroes (Easy)

### Sliding Window (8 problems)
Problems using sliding window technique with fixed or variable window sizes.

**Implemented:**
- [x] `best_time_to_buy_sell_stock` - Best Time to Buy and Sell Stock (Easy)

**Planned:**
- [ ] `longest_substring_without_repeating` - Longest Substring Without Repeating Characters (Medium)
- [ ] `minimum_window_substring` - Minimum Window Substring (Hard)
- [ ] `longest_repeating_character_replacement` - Longest Repeating Character Replacement (Medium)
- [ ] `permutation_in_string` - Permutation in String (Medium)
- [ ] `find_all_anagrams_in_string` - Find All Anagrams in a String (Medium)
- [ ] `sliding_window_maximum` - Sliding Window Maximum (Hard)
- [ ] `subarray_product_less_than_k` - Subarray Product Less Than K (Medium)

### Stack (7 problems)
Problems utilizing stack data structure for parsing, validation, and computation.

**Planned:**
- [ ] `valid_parentheses` - Valid Parentheses (Easy)
- [ ] `min_stack` - Min Stack (Easy)
- [ ] `evaluate_reverse_polish_notation` - Evaluate Reverse Polish Notation (Medium)
- [ ] `generate_parentheses` - Generate Parentheses (Medium)
- [ ] `daily_temperatures` - Daily Temperatures (Medium)
- [ ] `car_fleet` - Car Fleet (Medium)
- [ ] `largest_rectangle_in_histogram` - Largest Rectangle in Histogram (Hard)

### Binary Search (7 problems)
Classic binary search and its variations on sorted arrays and search spaces.

**Planned:**
- [ ] `binary_search` - Binary Search (Easy)
- [ ] `search_in_rotated_sorted_array` - Search in Rotated Sorted Array (Medium)
- [ ] `find_min_in_rotated_sorted_array` - Find Minimum in Rotated Sorted Array (Medium)
- [ ] `search_2d_matrix` - Search a 2D Matrix (Medium)
- [ ] `find_kth_smallest_in_sorted_matrix` - Kth Smallest Element in a Sorted Matrix (Medium)
- [ ] `koko_eating_bananas` - Koko Eating Bananas (Medium)
- [ ] `find_peak_element` - Find Peak Element (Medium)

### Linked List (7 problems)
Fundamental linked list manipulation patterns and algorithms.

**Planned:**
- [ ] `reverse_linked_list` - Reverse Linked List (Easy)
- [ ] `merge_two_sorted_lists` - Merge Two Sorted Lists (Easy)
- [ ] `reorder_list` - Reorder List (Medium)
- [ ] `remove_nth_node_from_end` - Remove Nth Node From End of List (Medium)
- [ ] `linked_list_cycle` - Linked List Cycle (Easy)
- [ ] `linked_list_cycle_ii` - Linked List Cycle II (Medium)
- [ ] `add_two_numbers` - Add Two Numbers (Medium)

### Trees (8 problems)
Binary tree traversal, validation, and manipulation algorithms.

**Planned:**
- [ ] `invert_binary_tree` - Invert Binary Tree (Easy)
- [ ] `max_depth_binary_tree` - Maximum Depth of Binary Tree (Easy)
- [ ] `diameter_of_binary_tree` - Diameter of Binary Tree (Easy)
- [ ] `balanced_binary_tree` - Balanced Binary Tree (Easy)
- [ ] `same_tree` - Same Tree (Easy)
- [ ] `subtree_of_another_tree` - Subtree of Another Tree (Easy)
- [ ] `validate_bst` - Validate Binary Search Tree (Medium)
- [ ] `binary_tree_level_order_traversal` - Binary Tree Level Order Traversal (Medium)

### Tries (2 problems)
Prefix tree (trie) data structure implementation and applications.

**Planned:**
- [ ] `implement_trie` - Implement Trie (Prefix Tree) (Medium)
- [ ] `add_and_search_word` - Design Add and Search Words Data Structure (Medium)

### Heap / Priority Queue (5 problems)
Priority queue and heap-based algorithms for optimization problems.

**Planned:**
- [ ] `kth_largest_element` - Kth Largest Element in an Array (Medium)
- [ ] `top_k_frequent_words` - Top K Frequent Words (Medium)
- [ ] `find_median_from_data_stream` - Find Median from Data Stream (Hard)
- [ ] `task_scheduler` - Task Scheduler (Medium)
- [ ] `last_stone_weight` - Last Stone Weight (Easy)

### Backtracking (5 problems)
Recursive backtracking for combinatorial search problems.

**Planned:**
- [ ] `subsets` - Subsets (Medium)
- [ ] `subsets_ii` - Subsets II (Medium)
- [ ] `combination_sum` - Combination Sum (Medium)
- [ ] `combination_sum_ii` - Combination Sum II (Medium)
- [ ] `permutations` - Permutations (Medium)

### Graphs (7 problems)
Graph traversal, topological sorting, and connectivity algorithms.

**Planned:**
- [ ] `number_of_islands` - Number of Islands (Medium)
- [ ] `clone_graph` - Clone Graph (Medium)
- [ ] `course_schedule` - Course Schedule (Medium)
- [ ] `course_schedule_ii` - Course Schedule II (Medium)
- [ ] `pacific_atlantic_water_flow` - Pacific Atlantic Water Flow (Medium)
- [ ] `surrounded_regions` - Surrounded Regions (Medium)
- [ ] `rotting_oranges` - Rotting Oranges (Medium)

### Intervals (5 problems)
Interval merging, scheduling, and overlap detection problems.

**Planned:**
- [ ] `merge_intervals` - Merge Intervals (Medium)
- [ ] `insert_interval` - Insert Interval (Medium)
- [ ] `non_overlapping_intervals` - Non-overlapping Intervals (Medium)
- [ ] `meeting_rooms` - Meeting Rooms (Easy)
- [ ] `meeting_rooms_ii` - Meeting Rooms II (Medium)

### Greedy (4 problems)
Greedy algorithmic approaches for optimization problems.

**Planned:**
- [ ] `jump_game` - Jump Game (Medium)
- [ ] `jump_game_ii` - Jump Game II (Medium)
- [ ] `gas_station` - Gas Station (Medium)
- [ ] `partition_labels` - Partition Labels (Medium)

### 1-D DP (6 problems)
One-dimensional dynamic programming patterns.

**Planned:**
- [ ] `climbing_stairs` - Climbing Stairs (Easy)
- [ ] `house_robber` - House Robber (Easy)
- [ ] `house_robber_ii` - House Robber II (Medium)
- [ ] `coin_change` - Coin Change (Medium)
- [ ] `longest_increasing_subsequence` - Longest Increasing Subsequence (Medium)
- [ ] `partition_equal_subset_sum` - Partition Equal Subset Sum (Medium)

### 2-D DP (5 problems)
Two-dimensional dynamic programming for grid and string problems.

**Planned:**
- [ ] `unique_paths` - Unique Paths (Medium)
- [ ] `longest_common_subsequence` - Longest Common Subsequence (Medium)
- [ ] `edit_distance` - Edit Distance (Hard)
- [ ] `word_break` - Word Break (Medium)
- [ ] `maximal_square` - Maximal Square (Medium)

### Bit Manipulation (4 problems)
Bitwise operations and bit manipulation techniques.

**Planned:**
- [ ] `single_number` - Single Number (Easy)
- [ ] `number_of_1_bits` - Number of 1 Bits (Easy)
- [ ] `counting_bits` - Counting Bits (Easy)
- [ ] `reverse_bits` - Reverse Bits (Easy)

### Math & Geometry (4 problems)
Mathematical algorithms and geometric problems.

**Planned:**
- [ ] `rotate_image` - Rotate Image (Medium)
- [ ] `spiral_matrix` - Spiral Matrix (Medium)
- [ ] `set_matrix_zeroes` - Set Matrix Zeroes (Medium)
- [ ] `happy_number` - Happy Number (Easy)

## Implementation Status

**Phase 1 Complete:** ✅
- [x] Foundation infrastructure (types, registry, runner)
- [x] CLI discovery enhancement
- [x] Seed problems (3 problems across 3 categories)
- [x] Test infrastructure

**Phase 2 - 4: In Progress** 🚧
- [ ] Batch implementations of remaining 97 problems
- [ ] Category completion across all 17 categories
- [ ] Documentation and cross-references

## Technical Architecture

### Registry System
All problems are registered in a central registry with metadata including:
- Problem ID and LeetCode URL
- Category and difficulty classification
- Tags for algorithmic patterns
- Module path for dynamic import

### Testing Framework
Each problem includes:
- Unit tests for Solution class methods
- Test cases covering edge cases and examples
- Integration tests for demo functions
- Registry validation tests

### Discovery System
Both CLI and Flask automatically discover new problems through:
- File system scanning for `demo()` functions
- Dynamic module import and execution
- Category-based organization and filtering

## Contributing

To add a new problem:

1. Create the problem module in the appropriate category directory
2. Implement the `Solution` class with canonical method signatures
3. Add comprehensive test cases and a `demo()` function
4. Register the problem using `register_problem()`
5. The problem will automatically appear in CLI and Flask interfaces

See existing implementations for examples and patterns to follow.
