"""
LeetCode 713: Subarray Product Less Than K

Given an array of integers nums and an integer k, return the number of contiguous
subarrays where the product of all the elements in the subarray is strictly less than k.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase
from .._types import Category, Difficulty


class Solution:
    def numSubarraysWithProduct(self, nums: List[int], k: int) -> int:
        """
        Two-pointer/sliding window approach.

        Key insight: For a valid window [left, right], all subarrays ending at 'right'
        and starting from any position between 'left' and 'right' are valid.
        The count is (right - left + 1).

        Algorithm:
        1. Use two pointers: left and right
        2. Expand right pointer and multiply product
        3. If product >= k, shrink from left until product < k
        4. Add (right - left + 1) to count for each valid window
        """
        if k <= 1:
            return 0  # No positive product can be less than 1

        count = 0
        product = 1
        left = 0

        for right in range(len(nums)):
            product *= nums[right]

            # Shrink window from left while product >= k
            while product >= k:
                product //= nums[left]
                left += 1

            # All subarrays ending at 'right' and starting from 'left' to 'right'
            # have product < k
            count += right - left + 1

        return count

    def numSubarraysWithProduct_bruteforce(self, nums: List[int], k: int) -> int:
        """
        Brute force approach for comparison.

        Time Complexity: O(n^2)
        Space Complexity: O(1)
        """
        if k <= 1:
            return 0

        count = 0
        n = len(nums)

        for i in range(n):
            product = 1
            for j in range(i, n):
                product *= nums[j]
                if product < k:
                    count += 1
                else:
                    break  # No need to continue as product will only increase

        return count


# Test cases
TEST_CASES = [
    TestCase(
        name="Example 1",
        input_args=([10, 5, 2, 6], 100),
        expected=8,
        description="Multiple valid subarrays",
    ),
    TestCase(
        name="Example 2",
        input_args=([1, 2, 3], 0),
        expected=0,
        description="k is 0, no valid subarrays",
    ),
    TestCase(
        name="Single element",
        input_args=([1], 2),
        expected=1,
        description="Single element less than k",
    ),
    TestCase(
        name="No valid subarrays",
        input_args=([10, 20, 30], 5),
        expected=0,
        description="All elements >= k",
    ),
    TestCase(
        name="All elements valid",
        input_args=([1, 1, 1], 10),
        expected=6,
        description="All subarrays have product < k",
    ),
    TestCase(
        name="Large numbers",
        input_args=([1, 2, 3, 4, 5], 10),
        expected=11,
        description="Mixed valid and invalid subarrays",
    ),
    TestCase(
        name="k is 1",
        input_args=([1, 2, 3], 1),
        expected=0,
        description="Edge case: k = 1, no positive products < 1",
    ),
]


def create_demo_output():
    """Demonstrate the sliding window approach for subarray product."""
    solution = Solution()

    print("=== LeetCode 713: Subarray Product Less Than K ===\n")

    # Example with detailed explanation
    nums = [10, 5, 2, 6]
    k = 100

    print(f"Input: nums = {nums}, k = {k}")
    print(f"Output: {solution.numSubarraysWithProduct(nums, k)}")
    print()

    # Show all valid subarrays manually
    print("Valid subarrays:")
    valid_count = 0
    for i in range(len(nums)):
        product = 1
        for j in range(i, len(nums)):
            product *= nums[j]
            if product < k:
                subarray = nums[i : j + 1]
                print(f"  {subarray} -> product = {product}")
                valid_count += 1
            else:
                break
    print(f"Total count: {valid_count}")
    print()

    # Compare approaches
    print("Comparison of approaches:")
    print(f"Sliding window: {solution.numSubarraysWithProduct(nums, k)}")
    print(f"Brute force: {solution.numSubarraysWithProduct_bruteforce(nums, k)}")

    return "\n".join(
        [
            "=== LeetCode 713: Subarray Product Less Than K ===",
            "",
            f"Input: nums = {nums}, k = {k}",
            f"Output: {solution.numSubarraysWithProduct(nums, k)}",
            "",
            "Valid subarrays with sliding window technique:",
            f"Total count: {valid_count}",
            "",
            "Comparison of approaches:",
            f"Sliding window: {solution.numSubarraysWithProduct(nums, k)}",
            f"Brute force: {solution.numSubarraysWithProduct_bruteforce(nums, k)}",
        ]
    )


def test_solution():
    """Test function for the subarray product less than k problem."""
    solution = Solution()

    for test_case in TEST_CASES:
        nums, k = test_case.input_args
        result = solution.numSubarraysWithProduct(nums, k)

        if result == test_case.expected:
            print(f"✓ {test_case.name}: PASS")
        else:
            print(f"✗ {test_case.name}: FAIL")
            print(f"  Expected: {test_case.expected}")
            print(f"  Got: {result}")


if __name__ == "__main__":
    test_solution()


# Register the problem
register_problem(
    slug="subarray-product-less-than-k",
    leetcode_num=713,
    title="Subarray Product Less Than K",
    difficulty=Difficulty.MEDIUM,
    category=Category.SLIDING_WINDOW,
    solution_func=lambda args: Solution().numSubarraysWithProduct(args[0], args[1]),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["sliding-window", "two-pointers", "array"],
    notes="Count subarrays with product less than k using sliding window technique",
)
