"""
Kth Largest Element

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


import heapq
import random


class Solution:
    """Find the kth largest element in an unsorted list using a heap."""

    def solve(self, nums: list[int], k: int) -> int:
        """Return the kth largest element."""
        if not nums or k < 1 or k > len(nums):
            return None
        heap = nums[:k]
        heapq.heapify(heap)
        for n in nums[k:]:
            if n > heap[0]:
                heapq.heapreplace(heap, n)
        return heap[0]


def demo() -> str:
    """Demo for Kth Largest Element."""
    random.seed(0)
    nums = [3, 2, 1, 5, 6, 4]
    k = 2
    s = Solution()
    result = s.solve(nums, k)
    return f"{k}th largest in {nums} is {result}"


register_problem(
    id=215,
    slug="kth_largest_element",
    title="Kth Largest Element in an Array",
    category=Category.HEAP,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "heap", "divide_conquer", "sorting"],
    url="https://leetcode.com/problems/kth-largest-element-in-an-array/",
    notes="",
)
