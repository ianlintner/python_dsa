"""
Subsets (LeetCode 78)

Given an integer array nums of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets, and the subsets may be returned in any order.
"""

from typing import List

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res: List[List[int]] = []

        def backtrack(start: int, path: List[int]) -> None:
            res.append(path[:])
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()

        backtrack(0, [])
        return res


# Example test cases
test_cases = [
    TestCase(
        ([1, 2, 3],),
        [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]],
        "Three elements",
    ),
    TestCase(([0],), [[], [0]], "Single element"),
]


def demo() -> str:
    """Run test cases for Subsets."""
    sol = Solution()
    outputs = []
    outputs.append("Subsets | LeetCode 78")
    outputs.append("=" * 50)
    outputs.append("Time: O(n * 2^n) | Space: O(n)")
    outputs.append("Technique: Backtracking to generate power set\n")

    for case in test_cases:
        res = sol.subsets(list(case.input_args[0]))
        # Sort for comparison since order may vary
        res_sorted = sorted([tuple(sorted(x)) for x in res])
        expected_sorted = sorted([tuple(sorted(x)) for x in case.expected])
        passed = res_sorted == expected_sorted
        status = "✓ PASS" if passed else "✗ FAIL"
        outputs.append(f"Test Case: {case.description}")
        outputs.append(f"  Input: nums={list(case.input_args[0])}")
        outputs.append(f"  Output: {res}")
        outputs.append(f"  Expected: {case.expected}")
        outputs.append(f"  {status}\n")

    result = "\n".join(outputs)
    print(result)
    return result


register_problem(
    id=78,
    slug="subsets",
    title="Subsets",
    category=Category.BACKTRACKING,
    difficulty=Difficulty.MEDIUM,
    tags=["backtracking"],
    url="https://leetcode.com/problems/subsets/",
    notes="",
)
