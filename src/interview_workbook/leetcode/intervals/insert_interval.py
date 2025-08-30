"""
Insert Interval

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """
        Insert Interval: Given intervals and a new interval, insert and merge.
        Args:
            intervals (List[List[int]]), newInterval (List[int])
        Returns:
            List[List[int]]
        """
        intervals, newInterval = args
        res = []
        i = 0
        n = len(intervals)
        # add all intervals ending before newInterval starts
        while i < n and intervals[i][1] < newInterval[0]:
            res.append(intervals[i])
            i += 1
        # merge overlapping intervals
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        res.append(newInterval)
        # add the rest
        while i < n:
            res.append(intervals[i])
            i += 1
        return res


def demo():
    """TODO: Implement demo function."""
    pass


register_problem(
    id=57,
    slug="insert_interval",
    title="Insert Interval",
    category=Category.INTERVALS,
    difficulty=Difficulty.MEDIUM,
    tags=["array"],
    url="https://leetcode.com/problems/insert-interval/",
    notes="",
)
