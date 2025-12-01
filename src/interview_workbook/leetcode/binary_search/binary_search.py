"""
Binary Search

Problem: Binary Search
LeetCode link: https://leetcode.com/problems/binary-search/
Description: Given a sorted array and a target, return the index of target if found, else -1.
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase


class Solution:
    def search(self, nums: list[int], target: int) -> int:
        """Standard binary search implementation."""
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1


# Example test cases
test_cases = [
    TestCase(([-1, 0, 3, 5, 9, 12], 9), 4, "Target in middle"),
    TestCase(([-1, 0, 3, 5, 9, 12], 2), -1, "Target not found"),
    TestCase(([5], 5), 0, "Single element found"),
    TestCase(([2, 5], 2), 0, "Target at start"),
    TestCase(([2, 5], 5), 1, "Target at end"),
]


def demo() -> str:
    """Run test cases for Binary Search."""
    sol = Solution()
    outputs = []
    outputs.append("Binary Search | LeetCode 704")
    outputs.append("=" * 50)
    outputs.append("Time: O(log n) | Space: O(1)")
    outputs.append("Technique: Classic binary search\n")

    for case in test_cases:
        nums, target = case.input_args
        res = sol.search(list(nums), target)
        passed = res == case.expected
        status = "✓ PASS" if passed else "✗ FAIL"
        outputs.append(f"Test Case: {case.description}")
        outputs.append(f"  Input: nums={list(nums)}, target={target}")
        outputs.append(f"  Output: {res}")
        outputs.append(f"  Expected: {case.expected}")
        outputs.append(f"  {status}\n")

    result = "\n".join(outputs)
    print(result)
    return result


# Register the problem with correct parameters
register_problem(
    id=704,
    slug="binary_search",
    title="Binary Search",
    category="binary_search",
    difficulty="Medium",
    tags=["binary-search"],
    url="https://leetcode.com/problems/binary-search/",
    notes="Classic binary search implementation.",
)
