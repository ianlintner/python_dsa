"""
3Sum - LeetCode Problem

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that
i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.
"""

from typing import List
from .._registry import register_problem
from .._runner import TestCase, run_test_cases, create_demo_output
from .._types import Category, Difficulty


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        Find all unique triplets that sum to zero using sorting and two pointers.

        Time Complexity: O(n²) - outer loop O(n) * inner two pointers O(n)
        Space Complexity: O(1) - excluding output array, constant extra space

        Args:
            nums: List of integers

        Returns:
            List[List[int]]: List of unique triplets that sum to zero
        """
        nums.sort()  # Sort to enable two pointers technique
        result = []
        n = len(nums)

        for i in range(n - 2):  # Need at least 3 elements
            # Skip duplicate values for first element
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # Use two pointers for remaining elements
            left, right = i + 1, n - 1
            target = -nums[i]  # We want nums[left] + nums[right] = target

            while left < right:
                current_sum = nums[left] + nums[right]

                if current_sum == target:
                    # Found a triplet
                    result.append([nums[i], nums[left], nums[right]])

                    # Skip duplicates for second element
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    # Skip duplicates for third element
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1

                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1

        return result

    def threeSumBruteForce(self, nums: List[int]) -> List[List[int]]:
        """
        Brute force approach with three nested loops (not optimal).

        Time Complexity: O(n³) - three nested loops
        Space Complexity: O(1) - excluding output array
        """
        result = []
        n = len(nums)

        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        triplet = sorted([nums[i], nums[j], nums[k]])
                        if triplet not in result:  # Avoid duplicates
                            result.append(triplet)

        return result

    def threeSumHashSet(self, nums: List[int]) -> List[List[int]]:
        """
        Alternative using hash set for each pair (educational).

        Time Complexity: O(n²) - nested loops with O(1) hash set operations
        Space Complexity: O(n) - hash set storage
        """
        nums.sort()
        result = []
        n = len(nums)

        for i in range(n - 2):
            # Skip duplicates for first element
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            seen = set()
            target = -nums[i]

            for j in range(i + 1, n):
                complement = target - nums[j]

                if complement in seen:
                    result.append([nums[i], complement, nums[j]])
                    # Skip duplicates for second element
                    while j + 1 < n and nums[j] == nums[j + 1]:
                        j += 1

                seen.add(nums[j])

        return result


def demo():
    """Demonstrate 3Sum solution with test cases."""
    solution = Solution()

    def sort_result(result):
        """Sort triplets for consistent comparison."""
        return sorted([sorted(triplet) for triplet in result])

    test_cases = [
        TestCase(
            input_args=([-1, 0, 1, 2, -1, -4],),
            expected=[[-1, -1, 2], [-1, 0, 1]],
            description="Basic case with two triplets",
        ),
        TestCase(input_args=([0, 1, 1],), expected=[], description="No valid triplets"),
        TestCase(input_args=([0, 0, 0],), expected=[[0, 0, 0]], description="All zeros"),
        TestCase(
            input_args=([-2, 0, 0, 2, 2],),
            expected=[[-2, 0, 2]],
            description="Duplicates with one solution",
        ),
        TestCase(input_args=([-1, 0, 1, 0],), expected=[[-1, 0, 1]], description="Simple case"),
        TestCase(input_args=([1, -1, -1, 0],), expected=[[-1, 0, 1]], description="Needs sorting"),
        TestCase(
            input_args=([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6],),
            expected=[[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2], [-2, -2, 4], [-2, 0, 2]],
            description="Many duplicates",
        ),
        TestCase(input_args=([],), expected=[], description="Empty array"),
        TestCase(input_args=([1, 2],), expected=[], description="Less than 3 elements"),
    ]

    # Custom comparison function that handles any order
    def compare_results(actual, expected):
        return sort_result(actual) == sort_result(expected)

    results = []
    for i, test_case in enumerate(test_cases):
        try:
            import time

            start_time = time.perf_counter()
            actual = solution.threeSum(*test_case.input_args)
            end_time = time.perf_counter()

            passed = compare_results(actual, test_case.expected)
            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": test_case.input_args,
                    "expected": test_case.expected,
                    "actual": actual,
                    "passed": passed,
                    "time_ms": (end_time - start_time) * 1000,
                }
            )
        except Exception as e:
            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": test_case.input_args,
                    "expected": test_case.expected,
                    "actual": f"Error: {str(e)}",
                    "passed": False,
                    "time_ms": 0,
                }
            )

    return create_demo_output(
        title="3Sum",
        description="Find all unique triplets that sum to zero",
        results=results,
        complexity_analysis={
            "time": "O(n²) - outer loop O(n) × inner two pointers O(n)",
            "space": "O(1) - excluding output array, constant extra space",
        },
        key_insights=[
            "Sort array first to enable two pointers technique",
            "Fix first element, use two pointers for remaining pair",
            "Skip duplicates at all three levels to avoid duplicate triplets",
            "Two pointers approach reduces inner complexity from O(n²) to O(n)",
        ],
        common_pitfalls=[
            "Must skip duplicates to avoid duplicate triplets",
            "Remember to sort array first for two pointers",
            "Handle edge cases: empty array, less than 3 elements",
            "Be careful with indices when skipping duplicates",
        ],
        follow_up_questions=[
            "How would you solve 4Sum or kSum in general?",
            "What if you needed to find triplets with different target sum?",
            "How would you optimize for arrays with many duplicates?",
            "Can you solve without sorting the array?",
        ],
    )


# Register this problem
register_problem(
    id=15,
    slug="3sum",
    title="3Sum",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.MEDIUM,
    tags={"array", "two-pointers", "sorting"},
    module="src.interview_workbook.leetcode.two_pointers.three_sum",
    url="https://leetcode.com/problems/3sum/",
    notes="Sort + two pointers technique to find unique triplets summing to zero",
)
