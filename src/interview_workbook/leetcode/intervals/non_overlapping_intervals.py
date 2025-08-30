"""
Non Overlapping Intervals

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """
        Non-overlapping Intervals: Minimum to remove to avoid overlap.
        Args:
            intervals (List[List[int]])
        Returns:
            int
        """
        (intervals,) = args
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


def demo():
    """TODO: Implement demo function."""
    pass


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
