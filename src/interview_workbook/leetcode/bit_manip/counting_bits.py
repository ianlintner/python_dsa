"""
LeetCode 338: Counting Bits

Given an integer n, return an array ans of length n + 1 such that for each i (0 <= i <= n), 
ans[i] is the number of 1's in the binary representation of i.

Time Complexity: O(n)
Space Complexity: O(1) - excluding the output array
"""

from typing import List
from ..._types import Category, Difficulty
from ..._runner import TestCase, run_test_cases, create_demo_output
from ..._registry import register_problem


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
test_cases = [
    TestCase(
        name="Example 1",
        input={"n": 2},
        expected=[0, 1, 1],
        description="n=2: [0,1,2] -> [0,1,1]"
    ),
    TestCase(
        name="Example 2",
        input={"n": 5},
        expected=[0, 1, 1, 2, 1, 2],
        description="n=5: [0,1,2,3,4,5] -> [0,1,1,2,1,2]"
    ),
    TestCase(
        name="Single number",
        input={"n": 0},
        expected=[0],
        description="n=0: only number 0"
    ),
    TestCase(
        name="Small range",
        input={"n": 1},
        expected=[0, 1],
        description="n=1: numbers 0 and 1"
    ),
    TestCase(
        name="Power of 2",
        input={"n": 8},
        expected=[0, 1, 1, 2, 1, 2, 2, 3, 1],
        description="n=8: includes powers of 2"
    ),
    TestCase(
        name="Larger range",
        input={"n": 15},
        expected=[0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4],
        description="n=15: full 4-bit range"
    )
]


def demo():
    """Demonstrate different approaches to count bits."""
    solution = Solution()
    
    print("=== LeetCode 338: Counting Bits ===\n")
    
    # Example with detailed explanation
    n = 8
    print(f"Input: n = {n}")
    print(f"Output: {solution.countBits(n)}")
    print()
    
    # Show binary representations
    print("Binary representations and bit counts:")
    result = solution.countBits(n)
    for i in range(n + 1):
        binary = bin(i)[2:]  # Remove '0b' prefix
        print(f"  {i:2d}: {binary:>4s} -> {result[i]} bits")
    print()
    
    # Show DP recurrence step by step
    print("DP recurrence (dp[i] = dp[i >> 1] + (i & 1)):")
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        parent = i >> 1
        bit = i & 1
        dp[i] = dp[parent] + bit
        print(f"  dp[{i}] = dp[{parent}] + ({i} & 1) = {dp[parent]} + {bit} = {dp[i]}")
    print()
    
    # Compare approaches
    print("Comparison of approaches:")
    test_n = 5
    print(f"n = {test_n}")
    print(f"  Right shift DP:  {solution.countBits(test_n)}")
    print(f"  Kernighan DP:    {solution.countBits_kernighan(test_n)}")
    print(f"  Offset DP:       {solution.countBits_offset(test_n)}")
    print(f"  Naive approach:  {solution.countBits_naive(test_n)}")
    print()
    
    # Show pattern recognition
    print("Pattern in powers of 2:")
    powers = [1, 2, 4, 8, 16]
    for p in powers:
        if p <= 16:
            result_p = solution.countBits(p)
            print(f"  Range [0, {p}]: {result_p}")
    
    return create_demo_output(
        title="Counting Bits",
        description="Count 1 bits for all numbers from 0 to n",
        input_data={"n": n},
        expected_output=solution.countBits(n)
    )


if __name__ == "__main__":
    run_test_cases(Solution().countBits, test_cases)


# Register the problem
register_problem(
    slug="counting-bits",
    leetcode_num=338,
    title="Counting Bits",
    difficulty=Difficulty.EASY,
    category=Category.BIT_MANIP,
    solution_file=__file__
)
