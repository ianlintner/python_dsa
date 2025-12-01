"""
Find Median From Data Stream

Problem: Find Median from Data Stream
LeetCode link: https://leetcode.com/problems/find-median-from-data-stream/
Description: Design a data structure that supports adding numbers and finding the median in O(log n) time.
"""

import heapq

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    """Maintain two heaps to find streaming median in O(log n) time."""

    def __init__(self) -> None:
        self.small = []  # max-heap (store as negative values)
        self.large = []  # min-heap

    def add_num(self, num: int) -> None:
        # Push onto max-heap
        heapq.heappush(self.small, -num)

        # Balance so that every num in small <= every num in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Rebalance sizes
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0


def demo() -> str:
    """Run test cases for Find Median from Data Stream."""
    outputs = []
    outputs.append("Find Median from Data Stream | LeetCode 295")
    outputs.append("=" * 50)
    outputs.append("Time: O(log n) add, O(1) find | Space: O(n)")
    outputs.append("Technique: Two heaps (max-heap for lower half, min-heap for upper)\n")

    # Test Case 1: Standard sequence
    outputs.append("Test Case: Streaming median updates")
    outputs.append("  Operations: addNum(1), addNum(2), findMedian(), addNum(3), findMedian()")
    mf = Solution()
    mf.add_num(1)
    mf.add_num(2)
    med1 = mf.find_median()
    mf.add_num(3)
    med2 = mf.find_median()
    outputs.append(f"  After [1,2] -> median={med1} (expected 1.5)")
    outputs.append(f"  After [1,2,3] -> median={med2} (expected 2.0)")
    passed = med1 == 1.5 and med2 == 2.0
    outputs.append(f"  {'✓ PASS' if passed else '✗ FAIL'}\n")

    # Test Case 2: All same numbers
    outputs.append("Test Case: All same numbers")
    mf2 = Solution()
    for n in [5, 5, 5, 5]:
        mf2.add_num(n)
    med3 = mf2.find_median()
    outputs.append(f"  After [5,5,5,5] -> median={med3} (expected 5.0)")
    passed2 = med3 == 5.0
    outputs.append(f"  {'✓ PASS' if passed2 else '✗ FAIL'}\n")

    # Test Case 3: Larger sequence
    outputs.append("Test Case: Larger stream")
    mf3 = Solution()
    nums = [41, 35, 62, 4, 97, 108]
    for n in nums:
        mf3.add_num(n)
    med4 = mf3.find_median()
    outputs.append(f"  Stream: {nums}")
    outputs.append(f"  Final median: {med4} (expected 51.5)")
    passed3 = med4 == 51.5
    outputs.append(f"  {'✓ PASS' if passed3 else '✗ FAIL'}\n")

    result = "\n".join(outputs)
    print(result)
    return result


register_problem(
    id=295,
    slug="find_median_from_data_stream",
    title="Find Median from Data Stream",
    category=Category.HEAP,
    difficulty=Difficulty.HARD,
    tags=["heap", "design"],
    url="https://leetcode.com/problems/find-median-from-data-stream/",
    notes="",
)

if __name__ == "__main__":
    print(demo())
