"""
Non Overlapping Intervals

Problem: Non-overlapping Intervals
LeetCode link: https://leetcode.com/problems/non-overlapping-intervals/
Description: Given an array of intervals, return the minimum number of intervals to remove to make the rest non-overlapping.
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        """
        Non-overlapping Intervals: Minimum to remove to avoid overlap.
        """
        if not intervals:
            return 0
        intervals.sort(key=lambda x: x[1])
        count = 0
        prev_end = intervals[0][1]
        for i in range(1, len(intervals)):
            if intervals[i][0] < prev_end:
                count += 1
            else:
                prev_end = intervals[i][1]
        return count


# Example test cases
test_cases = [
    TestCase(([[1, 2], [2, 3], [3, 4], [1, 3]],), 1, "Remove [1,3] to avoid overlap"),
    TestCase(([[1, 2], [1, 2], [1, 2]],), 2, "Remove 2 duplicate intervals"),
    TestCase(([[1, 2], [2, 3]],), 0, "Already non-overlapping"),
    TestCase(([[1, 100], [11, 22], [1, 11], [2, 12]],), 2, "One long interval overlaps many"),
]


def demo() -> str:
    """Run test cases for Non-overlapping Intervals."""
    sol = Solution()
    outputs = []
    outputs.append("Non-overlapping Intervals | LeetCode 435")
    outputs.append("=" * 50)
    outputs.append("Time: O(n log n) | Space: O(1)")
    outputs.append("Technique: Greedy - sort by end time, count overlaps\n")

    for case in test_cases:
        intervals = [list(x) for x in case.input_args[0]]  # Copy
        res = sol.eraseOverlapIntervals(intervals)
        passed = res == case.expected
        status = "✓ PASS" if passed else "✗ FAIL"
        outputs.append(f"Test Case: {case.description}")
        outputs.append(f"  Input: intervals={case.input_args[0]}")
        outputs.append(f"  Output: {res}")
        outputs.append(f"  Expected: {case.expected}")
        outputs.append(f"  {status}\n")

    result = "\n".join(outputs)
    print(result)
    return result


register_problem(
    id=435,
    slug="non_overlapping_intervals",
    title="Non-overlapping Intervals",
    category=Category.INTERVALS,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "dynamic_programming", "greedy", "sorting"],
    url="https://leetcode.com/problems/non-overlapping-intervals/",
    notes="",
)
