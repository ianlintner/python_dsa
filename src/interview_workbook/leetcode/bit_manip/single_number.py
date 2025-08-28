"""
LeetCode 136: Single Number

Given a non-empty array of integers nums, every element appears twice except for one.
Find that single one.

You must implement a solution with a linear runtime complexity and use only constant extra space.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List
from ..._types import Category, Difficulty
from ..._runner import TestCase, run_test_cases, create_demo_output
from ..._registry import register_problem


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        XOR-based solution using bit manipulation.

        Key insight:
        - x ^ x = 0 (any number XOR with itself is 0)
        - x ^ 0 = x (any number XOR with 0 is the number itself)
        - XOR is commutative and associative

        Since every number appears twice except one, when we XOR all numbers:
        - All pairs will cancel out (become 0)
        - Only the single number remains

        Example: [2, 2, 1]
        2 ^ 2 ^ 1 = 0 ^ 1 = 1
        """
        result = 0
        for num in nums:
            result ^= num
        return result

    def singleNumber_hashset(self, nums: List[int]) -> int:
        """
        Hash set approach for comparison.

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        seen = set()
        for num in nums:
            if num in seen:
                seen.remove(num)
            else:
                seen.add(num)
        return seen.pop()

    def singleNumber_sum(self, nums: List[int]) -> int:
        """
        Mathematical approach using sum.

        Key insight: 2 * sum(unique) - sum(all) = single number

        Time Complexity: O(n)
        Space Complexity: O(n) - for the set of unique numbers
        """
        unique_nums = set(nums)
        return 2 * sum(unique_nums) - sum(nums)


# Test cases
test_cases = [
    TestCase(
        name="Example 1",
        input={"nums": [2, 2, 1]},
        expected=1,
        description="Single number at the end",
    ),
    TestCase(
        name="Example 2",
        input={"nums": [4, 1, 2, 1, 2]},
        expected=4,
        description="Single number at the beginning",
    ),
    TestCase(name="Example 3", input={"nums": [1]}, expected=1, description="Single element array"),
    TestCase(
        name="Negative numbers",
        input={"nums": [-1, -1, -2, -2, -3]},
        expected=-3,
        description="Array with negative numbers",
    ),
    TestCase(
        name="Large numbers",
        input={"nums": [30000, 500, 100, 30000, 100]},
        expected=500,
        description="Array with large positive numbers",
    ),
    TestCase(
        name="Mixed positive/negative",
        input={"nums": [-4, -4, 8, -5, -5]},
        expected=8,
        description="Mixed positive and negative numbers",
    ),
    TestCase(
        name="Zero included",
        input={"nums": [0, 1, 0]},
        expected=1,
        description="Array including zero",
    ),
]


def demo():
    """Demonstrate the XOR-based bit manipulation approach."""
    solution = Solution()

    print("=== LeetCode 136: Single Number ===\n")

    # Example with detailed explanation
    nums = [4, 1, 2, 1, 2]
    print(f"Input: {nums}")
    print(f"Output: {solution.singleNumber(nums)}")
    print()

    # Show XOR step by step
    print("XOR Step-by-step:")
    result = 0
    for i, num in enumerate(nums):
        old_result = result
        result ^= num
        print(f"  Step {i + 1}: {old_result} ^ {num} = {result}")
    print(f"Final result: {result}")
    print()

    # Show binary representation for better understanding
    print("Binary representation example:")
    test_nums = [2, 2, 1]
    print(f"Input: {test_nums}")

    result = 0
    for num in test_nums:
        print(f"  {result:04b} ^ {num:04b} = {result ^ num:04b}")
        result ^= num
    print(f"Result: {result} (binary: {result:04b})")
    print()

    # Compare approaches
    print("Comparison of approaches:")
    test_array = [4, 1, 2, 1, 2]
    print(f"Input: {test_array}")
    print(f"XOR approach: {solution.singleNumber(test_array)}")
    print(f"HashSet approach: {solution.singleNumber_hashset(test_array)}")
    print(f"Sum approach: {solution.singleNumber_sum(test_array)}")

    return create_demo_output(
        title="Single Number",
        description="Find the number that appears once while others appear twice",
        input_data={"nums": nums},
        expected_output=solution.singleNumber(nums),
    )


if __name__ == "__main__":
    run_test_cases(Solution().singleNumber, test_cases)


# Register the problem
register_problem(
    slug="single-number",
    leetcode_num=136,
    title="Single Number",
    difficulty=Difficulty.EASY,
    category=Category.BIT_MANIP,
    solution_file=__file__,
)
