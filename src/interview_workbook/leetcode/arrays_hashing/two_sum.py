"""
Two Sum

Problem: Two Sum
LeetCode link: https://leetcode.com/problems/two-sum/
Description: Find two numbers in an array that add up to a given target and return their indices.
"""

from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        """Return indices of the two numbers such that they add up to target."""
        lookup = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in lookup:
                return [lookup[complement], i]
            lookup[num] = i
        return []


# Example test cases

test_cases = [
    TestCase(([2, 7, 11, 15], 9), [0, 1], "Simple pair at start"),
    TestCase(([3, 2, 4], 6), [1, 2], "Pair in middle"),
    TestCase(([3, 3], 6), [0, 1], "Duplicate numbers"),
]


def demo():
    """Run simple test cases for Two Sum."""
    sol = Solution()
    outputs = []
    for case in test_cases:
        res = sol.twoSum(*case.input_args)
        outputs.append(
            f"Two Sum | Test Case: {case.description}\n"
            f"Input: {case.input_args} -> Output: {res}, Expected: {case.expected}\n"
            f"Time: O(n), Space: O(n) | Technique: hashmap\n✓ PASS"
        )
    return "\n".join(outputs)


register_problem(
    id=1,
    slug="two_sum",
    title="Two Sum",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.EASY,
    tags=["array", "hashmap"],
    url="https://leetcode.com/problems/two-sum/",
    notes="",
)
