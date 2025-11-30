"""
Merge Intervals

Problem: Merge Intervals
LeetCode link: https://leetcode.com/problems/merge-intervals/
Description: Given an array of intervals where intervals[i] = [start, end], merge all overlapping intervals and return an array of non-overlapping intervals covering all the input intervals.
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        """
        Merge overlapping intervals.
        Args:
            intervals: List of [start, end] intervals
        Returns:
            List of merged non-overlapping intervals
        """
        if not intervals:
            return []
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]
        for start, end in intervals[1:]:
            if start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return merged


# Example test cases
test_cases = [
    TestCase(
        ([[1, 3], [2, 6], [8, 10], [15, 18]],),
        [[1, 6], [8, 10], [15, 18]],
        "Overlapping and non-overlapping intervals",
    ),
    TestCase(([[1, 4], [4, 5]],), [[1, 5]], "Adjacent intervals"),
    TestCase(([[1, 4], [0, 4]],), [[0, 4]], "Second interval starts before first"),
    TestCase(([[1, 4]],), [[1, 4]], "Single interval"),
]


def demo() -> str:
    """Run test cases for Merge Intervals."""
    sol = Solution()
    outputs = []
    outputs.append("Merge Intervals | LeetCode 56")
    outputs.append("=" * 50)
    outputs.append("Time: O(n log n) | Space: O(n)")
    outputs.append("Technique: Sort by start, merge overlapping\n")

    for case in test_cases:
        # Copy to avoid mutation
        intervals_copy = [list(x) for x in case.input_args[0]]
        res = sol.merge(intervals_copy)
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
    id=56,
    slug="merge_intervals",
    title="Merge Intervals",
    category=Category.INTERVALS,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "sorting"],
    url="https://leetcode.com/problems/merge-intervals/",
    notes="",
)
