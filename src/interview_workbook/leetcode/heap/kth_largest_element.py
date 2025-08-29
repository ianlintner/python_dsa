"""
Kth Largest Element

TODO: Add problem description
"""


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


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="kth_largest_element",
#     title="Kth Largest Element",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
