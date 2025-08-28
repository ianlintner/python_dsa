"""
LeetCode 435: Non-overlapping Intervals
https://leetcode.com/problems/non-overlapping-intervals/

Given an array of intervals where intervals[i] = [start_i, end_i],
return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.
"""

from .._runner import TestCase, run_test_cases
from .._registry import register_problem
from .._types import Category, Difficulty


class Solution:
    def eraseOverlapIntervals_greedy_end_time(self, intervals: list[list[int]]) -> int:
        """
        Greedy approach: Always keep the interval with the earliest end time.

        Strategy:
        1. Sort intervals by end time
        2. Iterate through sorted intervals
        3. Keep intervals that don't overlap with previously kept interval
        4. Count intervals that need to be removed

        Time: O(n log n) - sorting dominates
        Space: O(1) - excluding input
        """
        if len(intervals) <= 1:
            return 0

        # Sort by end time - greedy choice
        intervals.sort(key=lambda x: x[1])

        kept_count = 1  # Always keep first interval
        last_end = intervals[0][1]

        for i in range(1, len(intervals)):
            current_start = intervals[i][0]

            # If current interval doesn't overlap with last kept interval
            if current_start >= last_end:
                kept_count += 1
                last_end = intervals[i][1]
            # Else: current interval overlaps, remove it (don't increment kept_count)

        return len(intervals) - kept_count

    def eraseOverlapIntervals_greedy_start_time(self, intervals: list[list[int]]) -> int:
        """
        Alternative greedy approach: Sort by start time, prefer earlier end time.

        Time: O(n log n) - sorting
        Space: O(1) - excluding input
        """
        if len(intervals) <= 1:
            return 0

        # Sort by start time, then by end time
        intervals.sort(key=lambda x: (x[0], x[1]))

        removed_count = 0
        prev_end = intervals[0][1]

        for i in range(1, len(intervals)):
            current_start, current_end = intervals[i]

            if current_start < prev_end:
                # Overlapping - remove the one with later end time
                removed_count += 1
                # Keep the interval with earlier end time
                prev_end = min(prev_end, current_end)
            else:
                # Non-overlapping - update prev_end
                prev_end = current_end

        return removed_count

    def eraseOverlapIntervals_dp(self, intervals: list[list[int]]) -> int:
        """
        Dynamic programming approach (less efficient but demonstrates concept).

        Time: O(n²) - for each interval, check all previous ones
        Space: O(n) - DP array
        """
        if len(intervals) <= 1:
            return 0

        # Sort by start time
        intervals.sort()
        n = len(intervals)

        # dp[i] = maximum number of non-overlapping intervals ending at or before i
        dp = [1] * n

        for i in range(1, n):
            # Option 1: don't include current interval
            dp[i] = dp[i - 1]

            # Option 2: include current interval
            max_prev = 0
            for j in range(i):
                # If interval j doesn't overlap with interval i
                if intervals[j][1] <= intervals[i][0]:
                    max_prev = max(max_prev, dp[j])

            # Include current interval
            dp[i] = max(dp[i], max_prev + 1)

        return n - dp[n - 1]

    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        """Main solution using greedy approach with end time sorting"""
        return self.eraseOverlapIntervals_greedy_end_time(intervals)


def create_demo_output() -> str:
    """Generate demonstration output for Non-overlapping Intervals problem"""

    examples = [
        {
            "input": [[1, 2], [2, 3], [3, 4], [1, 3]],
            "description": "Standard case with one overlapping interval to remove",
        },
        {"input": [[1, 2], [1, 2], [1, 2]], "description": "Multiple identical intervals"},
        {"input": [[1, 2], [2, 3]], "description": "Adjacent intervals (no removal needed)"},
        {
            "input": [[1, 100], [11, 22], [1, 11], [2, 12]],
            "description": "Complex overlapping scenario",
        },
        {
            "input": [[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]],
            "description": "Chain of overlapping intervals",
        },
    ]

    output = ["=== Non-overlapping Intervals (LeetCode 435) ===\n"]
    output.append("Find minimum number of intervals to remove to make rest non-overlapping\n")

    solution = Solution()

    for i, example in enumerate(examples, 1):
        original_intervals = example["input"][:]

        output.append(f"Example {i}: {example['description']}")
        output.append(f"Original intervals: {original_intervals}")

        # Test greedy end time approach
        intervals_copy1 = [interval[:] for interval in original_intervals]
        result1 = solution.eraseOverlapIntervals_greedy_end_time(intervals_copy1)
        output.append(f"Greedy (end time) result: {result1} intervals to remove")

        # Show which intervals would be kept
        intervals_copy_demo = [interval[:] for interval in original_intervals]
        intervals_copy_demo.sort(key=lambda x: x[1])
        kept = [intervals_copy_demo[0]]
        last_end = intervals_copy_demo[0][1]
        for interval in intervals_copy_demo[1:]:
            if interval[0] >= last_end:
                kept.append(interval)
                last_end = interval[1]
        kept.sort()  # Sort for display
        output.append(f"Kept intervals: {kept}")

        # Test greedy start time approach
        intervals_copy2 = [interval[:] for interval in original_intervals]
        result2 = solution.eraseOverlapIntervals_greedy_start_time(intervals_copy2)
        output.append(f"Greedy (start time) result: {result2} (should match)")

        # Test DP approach (for smaller examples)
        if len(original_intervals) <= 10:
            intervals_copy3 = [interval[:] for interval in original_intervals]
            result3 = solution.eraseOverlapIntervals_dp(intervals_copy3)
            output.append(f"DP result: {result3} (should match)")

        output.append("")

    # Algorithm comparison
    output.append("=== Algorithm Analysis ===")
    output.append("1. Greedy (End Time Sort):")
    output.append("   - Time: O(n log n), Space: O(1)")
    output.append("   - Optimal: always keep interval with earliest end")
    output.append("   - Intuition: leaves most room for future intervals")

    output.append("2. Greedy (Start Time Sort):")
    output.append("   - Time: O(n log n), Space: O(1)")
    output.append("   - Works but less intuitive")
    output.append("   - Must carefully handle overlapping cases")

    output.append("3. Dynamic Programming:")
    output.append("   - Time: O(n²), Space: O(n)")
    output.append("   - Shows the problem structure clearly")
    output.append("   - Not optimal but demonstrates DP approach")

    output.append("\nKey Insight: Classic greedy interval scheduling")
    output.append("Pattern: Sort by end time, greedily select non-overlapping")

    # Greedy proof intuition
    output.append("\n=== Greedy Algorithm Correctness ===")
    output.append("Why sorting by end time works:")
    output.append("1. Earlier end time leaves maximum room for future intervals")
    output.append("2. If we have optimal solution, we can always replace intervals")
    output.append("   with same-or-better choices sorted by end time")
    output.append("3. This is the classic 'activity selection' problem")

    return "\n".join(output)


# Test cases
TEST_CASES = [
    TestCase(
        input_data=[[1, 2], [2, 3], [3, 4], [1, 3]],
        expected=1,
        description="Remove [1,3] to make non-overlapping",
    ),
    TestCase(
        input_data=[[1, 2], [1, 2], [1, 2]],
        expected=2,
        description="Keep only one of three identical intervals",
    ),
    TestCase(
        input_data=[[1, 2], [2, 3]], expected=0, description="Adjacent intervals don't overlap"
    ),
    TestCase(input_data=[[1, 2]], expected=0, description="Single interval"),
    TestCase(input_data=[], expected=0, description="Empty input"),
    TestCase(
        input_data=[[1, 100], [11, 22], [1, 11], [2, 12]],
        expected=2,
        description="Complex overlapping scenario",
    ),
    TestCase(
        input_data=[[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]],
        expected=2,
        description="Chain of overlapping intervals",
    ),
    TestCase(
        input_data=[[-1, 0], [0, 1], [1, 2]],
        expected=0,
        description="Adjacent intervals with negative start",
    ),
]


def test_solution():
    """Test function for Non-overlapping Intervals"""
    solution = Solution()

    def test_erase_overlap_intervals(intervals, expected, description):
        # Create copy to avoid modifying original
        intervals_copy = [interval[:] for interval in intervals]
        result = solution.eraseOverlapIntervals(intervals_copy)
        return result == expected

    test_cases_formatted = [
        TestCase(input_data=tc.input_data, expected=tc.expected, description=tc.description)
        for tc in TEST_CASES
    ]

    return run_test_cases(test_erase_overlap_intervals, test_cases_formatted)


# Register the problem
register_problem(
    slug="non_overlapping_intervals",
    leetcode_num=435,
    title="Non-overlapping Intervals",
    difficulty=Difficulty.MEDIUM,
    category=Category.INTERVALS,
    solution_func=Solution().eraseOverlapIntervals,
    test_func=test_solution,
    demo_func=create_demo_output,
)
