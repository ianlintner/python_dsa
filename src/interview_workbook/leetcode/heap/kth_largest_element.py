"""
Kth Largest Element

Problem: Kth Largest Element in an Array
LeetCode link: https://leetcode.com/problems/kth-largest-element-in-an-array/
Description: Find the kth largest element in an unsorted array.
"""

import heapq
import random

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    """Find the kth largest element in an unsorted list using a heap."""

    def findKthLargest(self, nums: list[int], k: int) -> int:
        """Return the kth largest element."""
        if not nums or k < 1 or k > len(nums):
            return None
        heap = nums[:k]
        heapq.heapify(heap)
        for n in nums[k:]:
            if n > heap[0]:
                heapq.heapreplace(heap, n)
        return heap[0]


# Example test cases
test_cases = [
    TestCase(([3, 2, 1, 5, 6, 4], 2), 5, "Standard case k=2"),
    TestCase(([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4, "Duplicates present"),
    TestCase(([1], 1), 1, "Single element"),
    TestCase(([7, 6, 5, 4, 3, 2, 1], 5), 3, "Sorted descending"),
]


def demo() -> str:
    """Run test cases for Kth Largest Element."""
    random.seed(0)
    sol = Solution()
    outputs = []
    outputs.append("Kth Largest Element | LeetCode 215")
    outputs.append("=" * 50)
    outputs.append("Time: O(n log k) | Space: O(k)")
    outputs.append("Technique: Min-heap of size k\n")

    for case in test_cases:
        nums, k = case.input_args
        res = sol.findKthLargest(list(nums), k)
        passed = res == case.expected
        status = "✓ PASS" if passed else "✗ FAIL"
        outputs.append(f"Test Case: {case.description}")
        outputs.append(f"  Input: nums={list(nums)}, k={k}")
        outputs.append(f"  Output: {res}")
        outputs.append(f"  Expected: {case.expected}")
        outputs.append(f"  {status}\n")

    result = "\n".join(outputs)
    print(result)
    return result


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

if __name__ == "__main__":
    print(demo())
