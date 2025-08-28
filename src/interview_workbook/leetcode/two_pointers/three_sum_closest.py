"""
LeetCode 16: 3Sum Closest

Given an integer array nums of length n and an integer target, find three integers
in nums such that the sum is closest to target.

Return the sum of the three integers.

You may assume that each input would have exactly one solution.

URL: https://leetcode.com/problems/3sum-closest/
Difficulty: Medium
Category: Two Pointers

Patterns:
- Two pointers after fixing one element
- Sorting to enable efficient pointer movement
- Distance tracking for closest sum

Complexity:
- Time: O(n²) - one loop × two pointers
- Space: O(1) - only variables, or O(n) if sorting counts

Key Insights:
- Sort array first for two pointers technique
- For each element, use two pointers on remaining elements
- Track closest sum and update when closer distance found
- Move pointers based on sum comparison with target

Edge Cases:
- Array length exactly 3 (return sum directly)
- Multiple sums with same distance (return any)
- All negative or all positive numbers
"""

from typing import List

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        """
        Find three numbers whose sum is closest to target.

        Args:
            nums: Array of integers
            target: Target sum

        Returns:
            Sum of three integers closest to target
        """
        nums.sort()
        n = len(nums)
        closest_sum = float("inf")

        for i in range(n - 2):
            left, right = i + 1, n - 1

            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]

                # Update closest sum if current is closer
                if abs(target - current_sum) < abs(target - closest_sum):
                    closest_sum = current_sum

                # If exact match, return immediately
                if current_sum == target:
                    return current_sum
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1

        return closest_sum


# Test cases
test_cases = [
    TestCase(([-1, 2, 1, -4], 1), 2, "Basic case: closest sum is 2"),
    TestCase(([0, 0, 0], 1), 0, "All zeros"),
    TestCase(([-1, 0, 1, 2, -1, -4], 0), 0, "Target is 0, exact match exists"),
    TestCase(([1, 1, 1, 0], -100), 2, "Target far from possible sums"),
    TestCase(([-3, -2, -5, 3, -4], -1), -2, "Mix of negative and positive"),
    TestCase(([1, 1, -1], 0), 1, "Two equal elements"),
    TestCase(([0, 1, 2], 3), 3, "Exact match possible"),
]


def demo() -> str:
    """Run 3Sum Closest demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(solution.threeSumClosest, test_cases, "LeetCode 16: 3Sum Closest")

    return create_demo_output(
        "3Sum Closest",
        test_results,
        time_complexity="O(n²)",
        space_complexity="O(1)",
        approach_notes="""
Key insights:
1. Sort array to enable two pointers technique
2. Fix first element, use two pointers for remaining two
3. Track closest sum by comparing absolute differences with target
4. Move pointers based on comparison: if sum < target, move left pointer right;
   if sum > target, move right pointer left
5. Early termination when exact match found

This approach systematically considers all possible triplets in O(n²) time
while maintaining O(1) extra space (excluding sort space).
        """.strip(),
    )


# Register the problem
register_problem(
    id=16,
    slug="three_sum_closest",
    title="3Sum Closest",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "two_pointers", "sorting"],
    url="https://leetcode.com/problems/3sum-closest/",
    notes="Extension of 3Sum using distance tracking instead of exact matches",
)
