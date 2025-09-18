"""
Meeting Rooms Ii

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """
        Meeting Rooms II: Minimum meeting rooms required.
        Args:
            intervals (List[List[int]])
        Returns:
            int
        """
        (intervals,) = args
        if not intervals:
            return 0
        starts = sorted([i[0] for i in intervals])
        ends = sorted([i[1] for i in intervals])
        s = e = 0
        rooms = available = 0
        while s < len(intervals):
            if starts[s] < ends[e]:
                if available == 0:
                    rooms += 1
                else:
                    available -= 1
                s += 1
            else:
                available += 1
                e += 1
        return rooms


def demo():
    """Run a simple demonstration for Meeting Rooms II problem."""
    s = Solution()
    intervals1 = [[0, 30], [5, 10], [15, 20]]
    intervals2 = [[7, 10], [2, 4]]
    result1 = s.solve(intervals1)
    result2 = s.solve(intervals2)
    return f"{intervals1} -> {result1}; {intervals2} -> {result2}"


register_problem(
    id=253,
    slug="meeting_rooms_ii",
    title="Meeting Rooms II",
    category=Category.INTERVALS,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "two_pointers", "greedy", "sorting", "heap"],
    url="https://leetcode.com/problems/meeting-rooms-ii/",
    notes="",
)
