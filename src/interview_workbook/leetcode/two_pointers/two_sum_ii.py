"""
Two Sum II - Input Array Is Sorted - LeetCode Problem

Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order,
find two numbers such that they add up to a specific target number.

Return the indices of the two numbers (1-indexed) as an integer array [index1, index2] of length 2.

The tests are generated such that there is exactly one solution. You may not use the same element twice.

Your solution must use only constant extra space.
"""

from typing import List
from .._registry import register_problem
from .._runner import TestCase, run_test_cases, create_demo_output
from .._types import Category, Difficulty


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """
        Find two numbers that add up to target using two pointers technique.

        Time Complexity: O(n) - single pass with two pointers
        Space Complexity: O(1) - only using two pointer variables

        Args:
            numbers: 1-indexed sorted array of integers
            target: Target sum to find

        Returns:
            List[int]: 1-indexed positions of the two numbers
        """
        left = 0
        right = len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]

            if current_sum == target:
                return [left + 1, right + 1]  # Convert to 1-indexed
            elif current_sum < target:
                left += 1  # Need larger sum, move left pointer right
            else:
                right -= 1  # Need smaller sum, move right pointer left

        # Problem guarantees exactly one solution exists
        return [-1, -1]

    def twoSumBinarySearch(self, numbers: List[int], target: int) -> List[int]:
        """
        Alternative using binary search for each element (not optimal but educational).

        Time Complexity: O(n log n) - binary search for each element
        Space Complexity: O(1) - constant extra space
        """
        for i in range(len(numbers)):
            complement = target - numbers[i]

            # Binary search for complement in remaining array
            left, right = i + 1, len(numbers) - 1
            while left <= right:
                mid = (left + right) // 2
                if numbers[mid] == complement:
                    return [i + 1, mid + 1]  # Convert to 1-indexed
                elif numbers[mid] < complement:
                    left = mid + 1
                else:
                    right = mid - 1

        return [-1, -1]

    def twoSumHashMap(self, numbers: List[int], target: int) -> List[int]:
        """
        Using hash map approach (uses extra space, not meeting constraint).

        Time Complexity: O(n) - single pass
        Space Complexity: O(n) - hash map storage
        """
        num_to_index = {}

        for i, num in enumerate(numbers):
            complement = target - num
            if complement in num_to_index:
                return [num_to_index[complement] + 1, i + 1]  # Convert to 1-indexed
            num_to_index[num] = i

        return [-1, -1]


def demo():
    """Demonstrate Two Sum II solution with test cases."""
    solution = Solution()

    test_cases = [
        TestCase(
            input_args=([2, 7, 11, 15], 9),
            expected=[1, 2],
            description="Basic case - first two elements",
        ),
        TestCase(input_args=([2, 3, 4], 6), expected=[1, 3], description="First and last elements"),
        TestCase(input_args=([-1, 0], -1), expected=[1, 2], description="Negative numbers"),
        TestCase(
            input_args=([1, 2, 3, 4, 4, 9, 56, 90], 8),
            expected=[4, 5],
            description="Duplicate numbers",
        ),
        TestCase(
            input_args=([1, 3, 4, 5, 7, 11], 9), expected=[3, 4], description="Middle elements"
        ),
        TestCase(input_args=([-3, 3, 4, 90], 0), expected=[1, 2], description="Sum to zero"),
        TestCase(
            input_args=([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 19),
            expected=[9, 10],
            description="Last two elements",
        ),
        TestCase(input_args=([5, 25, 75], 100), expected=[2, 3], description="Large numbers"),
    ]

    results = run_test_cases(solution.twoSum, test_cases)

    return create_demo_output(
        title="Two Sum II - Input Array Is Sorted",
        description="Find two numbers that sum to target using two pointers",
        results=results,
        complexity_analysis={
            "time": "O(n) - single pass with two pointers",
            "space": "O(1) - only using two pointer variables",
        },
        key_insights=[
            "Two pointers technique leverages sorted array property",
            "Move left pointer right when sum is too small",
            "Move right pointer left when sum is too large",
            "Problem guarantees exactly one solution exists",
        ],
        common_pitfalls=[
            "Remember to return 1-indexed positions, not 0-indexed",
            "Don't forget that array is sorted - this enables two pointers",
            "Avoid using extra space (hash map) when two pointers suffices",
            "Handle negative numbers correctly",
        ],
        follow_up_questions=[
            "What if there were multiple solutions?",
            "How would you modify for 0-indexed output?",
            "What if the array wasn't sorted?",
            "Can you solve for three numbers summing to target?",
        ],
    )


# Register this problem
register_problem(
    id=167,
    slug="two-sum-ii-input-array-is-sorted",
    title="Two Sum II - Input Array Is Sorted",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.MEDIUM,
    tags={"array", "two-pointers", "binary-search"},
    module="src.interview_workbook.leetcode.two_pointers.two_sum_ii",
    url="https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/",
    notes="Two pointers technique on sorted array for O(1) space solution",
)
