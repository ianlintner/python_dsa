"""
LeetCode 136: Single Number

Given a non-empty array of integers nums, every element appears twice except for one.
Find that single one.

You must implement a solution with a linear runtime complexity and use only constant extra space.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


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
TEST_CASES = [
    TestCase(
        input_args=([2, 2, 1],),
        expected=1,
        description="Single number at the end",
    ),
    TestCase(
        input_args=([4, 1, 2, 1, 2],),
        expected=4,
        description="Single number at the beginning",
    ),
    TestCase(
        input_args=([1],),
        expected=1,
        description="Single element array",
    ),
    TestCase(
        input_args=([-1, -1, -2, -2, -3],),
        expected=-3,
        description="Array with negative numbers",
    ),
    TestCase(
        input_args=([30000, 500, 100, 30000, 100],),
        expected=500,
        description="Array with large positive numbers",
    ),
    TestCase(
        input_args=([-4, -4, 8, -5, -5],),
        expected=8,
        description="Mixed positive and negative numbers",
    ),
    TestCase(
        input_args=([0, 1, 0],),
        expected=1,
        description="Array including zero",
    ),
]


def create_demo_output() -> str:
    """Create comprehensive demo showing different approaches and analysis."""
    solution = Solution()

    output = []
    output.append("=== LeetCode 136: Single Number ===\n")

    # Example with detailed explanation
    nums = [4, 1, 2, 1, 2]
    output.append(f"Input: {nums}")
    output.append(f"Output: {solution.singleNumber(nums)}")
    output.append("")

    # Show XOR step by step
    output.append("XOR Step-by-step:")
    result = 0
    for i, num in enumerate(nums):
        old_result = result
        result ^= num
        output.append(f"  Step {i + 1}: {old_result} ^ {num} = {result}")
    output.append(f"Final result: {result}")
    output.append("")

    # Show binary representation for better understanding
    output.append("Binary representation example:")
    test_nums = [2, 2, 1]
    output.append(f"Input: {test_nums}")

    result = 0
    for num in test_nums:
        output.append(f"  {result:04b} ^ {num:04b} = {result ^ num:04b}")
        result ^= num
    output.append(f"Result: {result} (binary: {result:04b})")
    output.append("")

    # Compare approaches
    output.append("Comparison of approaches:")
    test_array = [4, 1, 2, 1, 2]
    output.append(f"Input: {test_array}")
    output.append(f"XOR approach: {solution.singleNumber(test_array)}")
    output.append(f"HashSet approach: {solution.singleNumber_hashset(test_array)}")
    output.append(f"Sum approach: {solution.singleNumber_sum(test_array)}")

    return "\n".join(output)


def test_solution():
    """Test the single number solution."""
    solution = Solution()

    def run_tests(func_name: str, func):
        print(f"\nTesting {func_name}:")
        for i, test_case in enumerate(TEST_CASES):
            result = func(test_case.input_args[0])
            status = "✓" if result == test_case.expected else "✗"
            print(f"  Test {i + 1}: {status} - {test_case.description}")
            if result != test_case.expected:
                print(f"    Expected: {test_case.expected}, Got: {result}")

    run_tests("XOR Approach", solution.singleNumber)
    run_tests("HashSet Approach", solution.singleNumber_hashset)
    run_tests("Sum Approach", solution.singleNumber_sum)

    # Run standard test framework
    run_test_cases(
        solution.singleNumber,
        TEST_CASES,
        "Single Number",
    )


# Register the problem
register_problem(
    slug="single_number",
    leetcode_num=136,
    title="Single Number",
    difficulty=Difficulty.EASY,
    category=Category.BIT_MANIP,
    solution_func=lambda nums: Solution().singleNumber(nums),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["bit-manipulation", "xor"],
    notes="XOR all numbers - duplicates cancel out, single number remains",
)
