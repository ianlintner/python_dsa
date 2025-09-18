"""
Product Of Array Except Self

Given an integer array nums, return an array answer such that answer[i] is equal
to the product of all the elements of nums except nums[i].

The algorithm must run in O(n) time without using division.
"""

import random

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty

random.seed(0)


class Solution:
    def solve(self, nums: list[int]) -> list[int]:
        """Return array output where each index is product of all other elements."""
        n = len(nums)
        res = [1] * n

        prefix = 1
        for i in range(n):
            res[i] = prefix
            prefix *= nums[i]

        suffix = 1
        for i in range(n - 1, -1, -1):
            res[i] *= suffix
            suffix *= nums[i]

        return res


def demo():
    """Demonstrate product of array except self solution."""
    sol = Solution()
    result = sol.solve([1, 2, 3, 4])
    assert result == [24, 12, 8, 6]
    print(f"Final result: {result}")
    return "Product of Array Except Self demo passed."


register_problem(
    id=238,
    slug="product_of_array_except_self",
    title="Product Of Array Except Self",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags=["prefix-product", "array"],
    url="https://leetcode.com/problems/product-of-array-except-self/",
    notes="Computes prefix and suffix products in O(n) time without division.",
)
