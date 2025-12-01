"""
Meeting Rooms

Problem: Meeting Rooms
LeetCode link: https://leetcode.com/problems/meeting-rooms/
Description: Given an array of meeting time intervals, determine if a person can attend all meetings.
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def canAttendMeetings(self, intervals: list[list[int]]) -> bool:
        """
        Meeting Rooms: Check if a person can attend all meetings.
        """
        intervals.sort(key=lambda x: x[0])
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                return False
        return True


# Example test cases
test_cases = [
    TestCase(([[0, 30], [5, 10], [15, 20]],), False, "Overlapping meetings"),
    TestCase(([[7, 10], [2, 4]],), True, "Non-overlapping meetings"),
    TestCase(([[1, 5], [5, 10]],), True, "Adjacent meetings (no overlap)"),
    TestCase(([],), True, "Empty intervals"),
]


def demo() -> str:
    """Run test cases for Meeting Rooms."""
    sol = Solution()
    outputs = []
    outputs.append("Meeting Rooms | LeetCode 252")
    outputs.append("=" * 50)
    outputs.append("Time: O(n log n) | Space: O(1)")
    outputs.append("Technique: Sort by start time, check overlaps\n")

    for case in test_cases:
        intervals = [list(x) for x in case.input_args[0]]  # Copy
        res = sol.canAttendMeetings(intervals)
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
    id=252,
    slug="meeting_rooms",
    title="Meeting Rooms",
    category=Category.INTERVALS,
    difficulty=Difficulty.EASY,
    tags=["array", "sorting"],
    url="https://leetcode.com/problems/meeting-rooms/",
    notes="",
)
