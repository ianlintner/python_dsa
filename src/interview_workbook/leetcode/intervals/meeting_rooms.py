"""
Meeting Rooms

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """
        Meeting Rooms: Check if a person can attend all meetings.
        Args:
            intervals (List[List[int]])
        Returns:
            bool
        """
        (intervals,) = args
        intervals.sort(key=lambda x: x[0])
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                return False
        return True


def demo():
    """Run a simple demonstration for Meeting Rooms problem."""
    s = Solution()
    intervals1 = [[0, 30], [5, 10], [15, 20]]
    intervals2 = [[7, 10], [2, 4]]
    result1 = s.solve(intervals1)
    result2 = s.solve(intervals2)
    return f"{intervals1} -> {result1}; {intervals2} -> {result2}"


register_problem(
    id=252,
    slug="meeting_rooms",
    title="Meeting Rooms",
    category=Category.INTERVALS,
    difficulty=Difficulty.EASY,
    tags=["array", "sorting"],
    url="https://leetcode.com/problems/meeting-rooms/",
    notes="",
)
