"""
LeetCode 56: Merge Intervals
https://leetcode.com/problems/merge-intervals/

Given an array of intervals where intervals[i] = [start_i, end_i],
merge all overlapping intervals, and return an array of the non-overlapping intervals
that cover all the intervals in the input.
"""

from .._runner import TestCase, run_test_cases
from .._registry import register_problem
from .._types import Category, Difficulty


class Solution:
    def merge_sort_and_merge(self, intervals: list[list[int]]) -> list[list[int]]:
        """
        Sort intervals by start time then merge overlapping ones.

        Strategy:
        1. Sort intervals by start time
        2. Iterate through sorted intervals
        3. If current interval overlaps with last merged, extend the end
        4. Otherwise, add current interval to result

        Time: O(n log n) - sorting dominates
        Space: O(1) - excluding output array
        """
        if not intervals:
            return []

        # Sort by start time
        intervals.sort(key=lambda x: x[0])

        merged = [intervals[0]]

        for current in intervals[1:]:
            last_merged = merged[-1]

            # Check if current overlaps with last merged interval
            if current[0] <= last_merged[1]:
                # Overlapping - merge by extending the end time
                last_merged[1] = max(last_merged[1], current[1])
            else:
                # No overlap - add current interval
                merged.append(current)

        return merged

    def merge_one_pass_optimized(self, intervals: list[list[int]]) -> list[list[int]]:
        """
        Optimized version with single pass after sorting.

        Time: O(n log n) - sorting
        Space: O(1) - excluding output
        """
        if not intervals:
            return []

        intervals.sort()
        result = []

        for interval in intervals:
            # If result is empty or no overlap with last interval
            if not result or result[-1][1] < interval[0]:
                result.append(interval)
            else:
                # Overlapping - merge by updating end time
                result[-1][1] = max(result[-1][1], interval[1])

        return result

    def merge_stack_based(self, intervals: list[list[int]]) -> list[list[int]]:
        """
        Stack-based approach for merging intervals.

        Time: O(n log n) - sorting
        Space: O(n) - stack storage
        """
        if not intervals:
            return []

        intervals.sort()
        stack = [intervals[0]]

        for i in range(1, len(intervals)):
            top = stack[-1]
            current = intervals[i]

            # If intervals don't overlap
            if top[1] < current[0]:
                stack.append(current)
            else:
                # Overlapping - merge intervals
                stack[-1] = [top[0], max(top[1], current[1])]

        return stack

    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        """Main solution using sort and merge approach"""
        return self.merge_sort_and_merge(intervals)


def create_demo_output() -> str:
    """Generate demonstration output for Merge Intervals problem"""

    examples = [
        {
            "input": [[1, 3], [2, 6], [8, 10], [15, 18]],
            "description": "Standard case with overlapping intervals",
        },
        {"input": [[1, 4], [4, 5]], "description": "Adjacent intervals that should merge"},
        {"input": [[1, 4], [0, 4]], "description": "Intervals with same end, different start"},
        {"input": [[1, 4], [2, 3]], "description": "One interval completely inside another"},
        {"input": [[1, 4], [5, 6]], "description": "Non-overlapping intervals"},
    ]

    output = ["=== Merge Intervals (LeetCode 56) ===\n"]
    output.append("Merge all overlapping intervals in a list\n")

    solution = Solution()

    for i, example in enumerate(examples, 1):
        original_intervals = example["input"][:]

        output.append(f"Example {i}: {example['description']}")
        output.append(f"Original intervals: {original_intervals}")

        # Test sort and merge approach
        intervals_copy1 = [interval[:] for interval in original_intervals]
        result1 = solution.merge_sort_and_merge(intervals_copy1)
        output.append(f"Sort & merge result: {result1}")

        # Test optimized approach
        intervals_copy2 = [interval[:] for interval in original_intervals]
        result2 = solution.merge_one_pass_optimized(intervals_copy2)
        output.append(f"Optimized result: {result2} (should match)")

        # Test stack approach
        intervals_copy3 = [interval[:] for interval in original_intervals]
        result3 = solution.merge_stack_based(intervals_copy3)
        output.append(f"Stack-based result: {result3} (should match)")
        output.append("")

    # Algorithm comparison
    output.append("=== Algorithm Analysis ===")
    output.append("1. Sort and Merge:")
    output.append("   - Time: O(n log n), Space: O(1)")
    output.append("   - Most straightforward and efficient")

    output.append("2. One-pass Optimized:")
    output.append("   - Time: O(n log n), Space: O(1)")
    output.append("   - Clean implementation, same complexity")

    output.append("3. Stack-based:")
    output.append("   - Time: O(n log n), Space: O(n)")
    output.append("   - Conceptually clear but uses extra space")

    output.append("\nKey Insight: Sorting by start time enables linear merge")
    output.append("Pattern: Sort then scan with merge condition")

    # Edge cases
    output.append("\n=== Edge Cases ===")
    edge_cases = [
        ([], "Empty array"),
        ([[1, 1]], "Single point interval"),
        ([[1, 2], [2, 3], [3, 4]], "Chain of adjacent intervals"),
        ([[1, 10], [2, 3], [4, 5], [6, 7]], "Multiple intervals inside one large interval"),
    ]

    for intervals, description in edge_cases:
        if intervals:
            result = solution.merge([interval[:] for interval in intervals])
            output.append(f"{description}: {intervals} -> {result}")
        else:
            output.append(f"{description}: [] -> []")

    return "\n".join(output)


# Test cases
TEST_CASES = [
    TestCase(
        input_data=[[1, 3], [2, 6], [8, 10], [15, 18]],
        expected=[[1, 6], [8, 10], [15, 18]],
        description="Standard overlapping intervals",
    ),
    TestCase(
        input_data=[[1, 4], [4, 5]], expected=[[1, 5]], description="Adjacent intervals that touch"
    ),
    TestCase(input_data=[], expected=[], description="Empty input"),
    TestCase(input_data=[[1, 4]], expected=[[1, 4]], description="Single interval"),
    TestCase(
        input_data=[[1, 4], [0, 4]], expected=[[0, 4]], description="Overlapping with same end"
    ),
    TestCase(
        input_data=[[1, 4], [2, 3]], expected=[[1, 4]], description="One interval inside another"
    ),
    TestCase(
        input_data=[[1, 4], [0, 0]],
        expected=[[0, 0], [1, 4]],
        description="Point interval separate from range",
    ),
    TestCase(
        input_data=[[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]],
        expected=[[1, 10]],
        description="One large interval contains all others",
    ),
]


def test_solution():
    """Test function for Merge Intervals"""
    solution = Solution()

    def test_merge(intervals, expected, description):
        # Test main merge method with copy to avoid modifying input
        intervals_copy = [interval[:] for interval in intervals]
        result = solution.merge(intervals_copy)
        return result == expected

    test_cases_formatted = [
        TestCase(input_data=tc.input_data, expected=tc.expected, description=tc.description)
        for tc in TEST_CASES
    ]

    return run_test_cases(test_merge, test_cases_formatted)


# Register the problem
register_problem(
    slug="merge_intervals",
    leetcode_num=56,
    title="Merge Intervals",
    difficulty=Difficulty.MEDIUM,
    category=Category.INTERVALS,
    solution_func=Solution().merge,
    test_func=test_solution,
    demo_func=create_demo_output,
)
