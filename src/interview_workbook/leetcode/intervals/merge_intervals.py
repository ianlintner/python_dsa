"""
Merge Intervals

Problem: Merge Intervals
LeetCode link: https://leetcode.com/problems/merge-intervals/
Description: Given an array of intervals where intervals[i] = [start, end], merge all overlapping intervals and return an array of non-overlapping intervals covering all the input intervals.
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """
        Merge Intervals: Merge overlapping intervals.
        Args:
            intervals (List[List[int]])
        Returns:
            List[List[int]]
        """
        (intervals,) = args
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


def demo():
    """Run a simple demonstration for Merge Intervals problem."""
    s = Solution()
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    result = s.solve(intervals)
    print(f"Initial intervals: {intervals}, Merged intervals: {result}")
    return f"{intervals} -> {result}"


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
