"""
Contains Duplicate

Given an integer array `nums`, return True if any value appears
at least twice in the array, and return False if every element
is distinct.
"""


class Solution:
    def solve(self, nums: list[int]) -> bool:
        """Check if the array contains any duplicates."""
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False


def demo():
    """Demonstration of Contains Duplicate problem."""
    nums = [1, 2, 3, 1]
    solver = Solution()
    result = solver.solve(nums)
    return f"Input: {nums} -> Contains Duplicate: {result}"


from src.interview_workbook.leetcode._types import Category, Difficulty
from src.interview_workbook.leetcode._registry import register_problem

register_problem(
    id=217,
    slug="contains_duplicate",
    title="Contains Duplicate",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.EASY,
    tags=["array", "hashmap", "sorting"],
    url="https://leetcode.com/problems/contains-duplicate/",
    notes="Basic duplicate check using set."
)
