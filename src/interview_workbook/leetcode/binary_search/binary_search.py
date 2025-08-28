"""
LeetCode 704: Binary Search

Given an array of integers nums which is sorted in ascending order, and an integer target,
write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4

Example 2:
Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1

URL: https://leetcode.com/problems/binary-search/
Difficulty: Easy
Category: Binary Search

Patterns:
- Classic binary search template
- Two pointers with mid calculation
- Divide and conquer approach

Complexity:
- Time: O(log n) - halve search space each iteration
- Space: O(1) - only use constant extra space

Pitfalls:
- Integer overflow when calculating mid (use left + (right - left) // 2)
- Off-by-one errors with boundary conditions
- Incorrect loop condition (should be left <= right)
- Wrong pointer updates (left = mid + 1, right = mid - 1)

Follow-ups:
- What if array contains duplicates? (find first/last occurrence)
- What if we need to find insertion point for target?
- How to handle rotated sorted arrays?
"""

from typing import List

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """
        Binary search for target in sorted array.

        Args:
            nums: Sorted array of integers in ascending order
            target: Target value to search for

        Returns:
            Index of target if found, -1 otherwise
        """
        left, right = 0, len(nums) - 1

        while left <= right:
            # Avoid integer overflow: use left + (right - left) // 2
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                # Target is in right half
                left = mid + 1
            else:
                # Target is in left half
                right = mid - 1

        # Target not found
        return -1


# Test cases
test_cases = [
    TestCase(([-1, 0, 3, 5, 9, 12], 9), 4, "Example 1: target exists"),
    TestCase(([-1, 0, 3, 5, 9, 12], 2), -1, "Example 2: target doesn't exist"),
    TestCase(([5], 5), 0, "Single element - found"),
    TestCase(([5], -5), -1, "Single element - not found"),
    TestCase(([-1, 0, 3, 5, 9, 12], -1), 0, "Target at beginning"),
    TestCase(([-1, 0, 3, 5, 9, 12], 12), 5, "Target at end"),
    TestCase(([-1, 0, 3, 5, 9, 12], 0), 1, "Target in middle-left"),
    TestCase(([-1, 0, 3, 5, 9, 12], 5), 3, "Target in middle-right"),
    TestCase(([], 1), -1, "Empty array"),
    TestCase(([1, 2, 3, 4, 5], 6), -1, "Target larger than all elements"),
]


def demo() -> str:
    """Run Binary Search demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(solution.search, test_cases, "LeetCode 704: Binary Search")

    return create_demo_output(
        "Binary Search",
        test_results,
        time_complexity="O(log n)",
        space_complexity="O(1)",
        approach_notes="""
Key insights:
1. Classic divide-and-conquer: eliminate half of search space each iteration
2. Use left + (right - left) // 2 to avoid integer overflow
3. Maintain loop invariant: target must be in [left, right] if it exists
4. Update pointers correctly: left = mid + 1, right = mid - 1 (not mid)
5. Loop condition left <= right ensures we check all possible positions
        """.strip(),
    )


# Register the problem
register_problem(
    id=704,
    slug="binary_search",
    title="Binary Search",
    category=Category.BINARY_SEARCH,
    difficulty=Difficulty.EASY,
    tags=["Array", "Binary Search"],
    url="https://leetcode.com/problems/binary-search/",
    notes="Classic binary search implementation on sorted array",
)
