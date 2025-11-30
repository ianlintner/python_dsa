"""
Permutations (LeetCode 46)

Given a collection of distinct numbers, return all possible permutations.
"""

from typing import List

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []

        def backtrack(start=0):
            if start == len(nums):
                res.append(nums[:])
                return
            for i in range(start, len(nums)):
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                nums[start], nums[i] = nums[i], nums[start]

        backtrack()
        return res


# Example test cases
test_cases = [
    TestCase(
        ([1, 2, 3],),
        [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]],
        "Three elements",
    ),
    TestCase(([0, 1],), [[0, 1], [1, 0]], "Two elements"),
    TestCase(([1],), [[1]], "Single element"),
]


def demo() -> str:
    """Run test cases for Permutations."""
    sol = Solution()
    outputs = []
    outputs.append("Permutations | LeetCode 46")
    outputs.append("=" * 50)
    outputs.append("Time: O(n! * n) | Space: O(n)")
    outputs.append("Technique: Backtracking with in-place swapping\n")

    for case in test_cases:
        res = sol.permute(list(case.input_args[0]))  # Copy to avoid mutation
        # Sort for comparison since order may vary
        res_sorted = sorted([tuple(x) for x in res])
        expected_sorted = sorted([tuple(x) for x in case.expected])
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
    id=46,
    slug="permutations",
    title="Permutations",
    category=Category.BACKTRACKING,
    difficulty=Difficulty.MEDIUM,
    tags=["backtracking"],
    url="https://leetcode.com/problems/permutations/",
    notes="",
)
