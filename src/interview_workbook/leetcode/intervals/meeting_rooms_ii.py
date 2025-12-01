"""
Meeting Rooms II

Problem: Meeting Rooms II
LeetCode link: https://leetcode.com/problems/meeting-rooms-ii/
Description: Given an array of meeting time intervals, find the minimum number of conference rooms required.
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def minMeetingRooms(self, intervals: list[list[int]]) -> int:
        """
        Meeting Rooms II: Minimum meeting rooms required.
        """
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


# Example test cases
test_cases = [
    TestCase(([[0, 30], [5, 10], [15, 20]],), 2, "Overlapping meetings need 2 rooms"),
    TestCase(([[7, 10], [2, 4]],), 1, "Non-overlapping meetings need 1 room"),
    TestCase(([[1, 5], [5, 10], [10, 15]],), 1, "Sequential meetings"),
    TestCase(
        ([[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]],),
        4,
        "Complex overlapping",
    ),
]


def demo() -> str:
    """Run test cases for Meeting Rooms II."""
    sol = Solution()
    outputs = []
    outputs.append("Meeting Rooms II | LeetCode 253")
    outputs.append("=" * 50)
    outputs.append("Time: O(n log n) | Space: O(n)")
    outputs.append("Technique: Two-pointer on sorted start/end times\n")

    for case in test_cases:
        intervals = [list(x) for x in case.input_args[0]]  # Copy
        res = sol.minMeetingRooms(intervals)
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
    id=253,
    slug="meeting_rooms_ii",
    title="Meeting Rooms II",
    category=Category.INTERVALS,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "two_pointers", "greedy", "sorting", "heap"],
    url="https://leetcode.com/problems/meeting-rooms-ii/",
    notes="",
)
