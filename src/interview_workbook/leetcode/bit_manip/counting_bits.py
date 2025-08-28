"""
LeetCode 338: Counting Bits

Given an integer n, return an array ans of length n + 1 such that for each i (0 <= i <= n),
ans[i] is the number of 1's in the binary representation of i.

Time Complexity: O(n)
Space Complexity: O(1) - excluding the output array
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def countBits(self, n: int) -> List[int]:
        """
        Dynamic Programming approach using bit manipulation.

        Key insight: For any number i, dp[i] = dp[i >> 1] + (i & 1)
        - i >> 1 is i divided by 2 (remove rightmost bit)
        - i & 1 is 1 if i is odd, 0 if even (rightmost bit)

        Example: i = 6 (110 in binary)
        - dp[6] = dp[3] + (6 & 1) = dp[3] + 0 = 2 + 0 = 2
        - 3 in binary is 11 (2 ones), 6 in binary is 110 (2 ones)
        """
        dp = [0] * (n + 1)

        for i in range(1, n + 1):
            dp[i] = dp[i >> 1] + (i & 1)

        return dp

    def countBits_kernighan(self, n: int) -> List[int]:
        """
        DP approach using Brian Kernighan's algorithm pattern.

        Key insight: dp[i] = dp[i & (i - 1)] + 1
        - i & (i - 1) removes the rightmost set bit
        - So we add 1 to the count of that number
        """
        dp = [0] * (n + 1)

        for i in range(1, n + 1):
            dp[i] = dp[i & (i - 1)] + 1

        return dp

    def countBits_offset(self, n: int) -> List[int]:
        """
        DP approach using offset pattern.

        Key insight: Pattern repeats with powers of 2
        - For range [2^k, 2^(k+1) - 1], we add 1 to pattern [0, 2^k - 1]
        """
        dp = [0] * (n + 1)
        offset = 1

        for i in range(1, n + 1):
            if offset * 2 == i:
                offset = i
            dp[i] = 1 + dp[i - offset]

        return dp

    def countBits_naive(self, n: int) -> List[int]:
        """
        Naive approach - count bits for each number.

        Time Complexity: O(n log n)
        Space Complexity: O(1) - excluding output
        """
        result = []

        for i in range(n + 1):
            count = 0
            num = i
            while num:
                count += num & 1
                num >>= 1
            result.append(count)

        return result


# Test cases
TEST_CASES = [
    TestCase(
        input_args=(2,),
        expected=[0, 1, 1],
        description="n=2: [0,1,2] -> [0,1,1]",
    ),
    TestCase(
        input_args=(5,),
        expected=[0, 1, 1, 2, 1, 2],
        description="n=5: [0,1,2,3,4,5] -> [0,1,1,2,1,2]",
    ),
    TestCase(
        input_args=(0,),
        expected=[0],
        description="n=0: only number 0",
    ),
    TestCase(
        input_args=(1,),
        expected=[0, 1],
        description="n=1: numbers 0 and 1",
    ),
    TestCase(
        input_args=(8,),
        expected=[0, 1, 1, 2, 1, 2, 2, 3, 1],
        description="n=8: includes powers of 2",
    ),
    TestCase(
        input_args=(15,),
        expected=[0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4],
        description="n=15: full 4-bit range",
    ),
]


def create_demo_output() -> str:
    """Create comprehensive demo showing different approaches and analysis."""
    solution = Solution()

    output = []
    output.append("=== LeetCode 338: Counting Bits ===\n")

    # Example with detailed explanation
    n = 8
    output.append(f"Input: n = {n}")
    output.append(f"Output: {solution.countBits(n)}")
    output.append("")

    # Show binary representations
    output.append("Binary representations and bit counts:")
    result = solution.countBits(n)
    for i in range(n + 1):
        binary = bin(i)[2:]  # Remove '0b' prefix
        output.append(f"  {i:2d}: {binary:>4s} -> {result[i]} bits")
    output.append("")

    # Show DP recurrence step by step
    output.append("DP recurrence (dp[i] = dp[i >> 1] + (i & 1)):")
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        parent = i >> 1
        bit = i & 1
        dp[i] = dp[parent] + bit
        output.append(f"  dp[{i}] = dp[{parent}] + ({i} & 1) = {dp[parent]} + {bit} = {dp[i]}")
    output.append("")

    # Compare approaches
    output.append("Comparison of approaches:")
    test_n = 5
    output.append(f"n = {test_n}")
    output.append(f"  Right shift DP:  {solution.countBits(test_n)}")
    output.append(f"  Kernighan DP:    {solution.countBits_kernighan(test_n)}")
    output.append(f"  Offset DP:       {solution.countBits_offset(test_n)}")
    output.append(f"  Naive approach:  {solution.countBits_naive(test_n)}")
    output.append("")

    # Show pattern recognition
    output.append("Pattern in powers of 2:")
    powers = [1, 2, 4, 8, 16]
    for p in powers:
        if p <= 16:
            result_p = solution.countBits(p)
            output.append(f"  Range [0, {p}]: {result_p}")

    return "\n".join(output)


def test_solution():
    """Test the counting bits solution."""
    solution = Solution()
    
    def run_tests(func_name: str, func):
        print(f"\nTesting {func_name}:")
        for i, test_case in enumerate(TEST_CASES):
            result = func(test_case.input_args[0])
            status = "✓" if result == test_case.expected else "✗"
            print(f"  Test {i + 1}: {status} - {test_case.description}")
            if result != test_case.expected:
                print(f"    Expected: {test_case.expected}, Got: {result}")

    run_tests("Right Shift DP", solution.countBits)
    run_tests("Kernighan DP", solution.countBits_kernighan)
    run_tests("Offset DP", solution.countBits_offset)
    run_tests("Naive Approach", solution.countBits_naive)

    # Run standard test framework
    run_test_cases(
        solution.countBits,
        TEST_CASES,
        "Counting Bits",
    )


# Register the problem
register_problem(
    slug="counting_bits",
    leetcode_num=338,
    title="Counting Bits",
    difficulty=Difficulty.EASY,
    category=Category.BIT_MANIP,
    solution_func=lambda n: Solution().countBits(n),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["bit-manipulation", "dynamic-programming"],
    notes="DP: dp[i] = dp[i >> 1] + (i & 1) - right shift removes bit, add back if odd",
)
