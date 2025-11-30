"""
Insert Interval

Problem: Insert Interval
LeetCode link: https://leetcode.com/problems/insert-interval/
Description: Insert a new interval into a list of non-overlapping intervals, merging if necessary.
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        """
        Insert Interval: Given intervals and a new interval, insert and merge.
        """
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


# Example test cases
test_cases = [
    TestCase(
        ([[1, 3], [6, 9]], [2, 5]),
        [[1, 5], [6, 9]],
        "Merge with first interval",
    ),
    TestCase(
        ([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]),
        [[1, 2], [3, 10], [12, 16]],
        "Merge multiple intervals",
    ),
    TestCase(([], [5, 7]), [[5, 7]], "Empty intervals list"),
    TestCase(([[1, 5]], [2, 3]), [[1, 5]], "New interval inside existing"),
]


def demo() -> str:
    """Run test cases for Insert Interval."""
    sol = Solution()
    outputs = []
    outputs.append("Insert Interval | LeetCode 57")
    outputs.append("=" * 50)
    outputs.append("Time: O(n) | Space: O(n)")
    outputs.append("Technique: Linear scan with merge\n")

    for case in test_cases:
        intervals, new_int = case.input_args
        # Copy to avoid mutation
        intervals_copy = [list(x) for x in intervals]
        new_int_copy = list(new_int)
        res = sol.insert(intervals_copy, new_int_copy)
        passed = res == case.expected
        status = "✓ PASS" if passed else "✗ FAIL"
        outputs.append(f"Test Case: {case.description}")
        outputs.append(f"  Input: intervals={intervals}, newInterval={new_int}")
        outputs.append(f"  Output: {res}")
        outputs.append(f"  Expected: {case.expected}")
        outputs.append(f"  {status}\n")

    result = "\n".join(outputs)
    print(result)
    return result


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
