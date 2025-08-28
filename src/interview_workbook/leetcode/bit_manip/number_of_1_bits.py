"""
LeetCode 191: Number of 1 Bits

Write a function that takes the binary representation of an unsigned integer
and returns the number of '1' bits it has (also known as the Hamming weight).

Time Complexity: O(1) - at most 32 iterations for 32-bit integer
Space Complexity: O(1)
"""

from ..._types import Category, Difficulty
from ..._runner import TestCase, run_test_cases, create_demo_output
from ..._registry import register_problem


class Solution:
    def hammingWeight(self, n: int) -> int:
        """
        Bit manipulation approach using Brian Kernighan's algorithm.

        Key insight: n & (n-1) removes the rightmost set bit.
        This allows us to count only the set bits, not all bits.

        Example: n = 12 (1100 in binary)
        - 12 & 11 = 1100 & 1011 = 1000 (8)
        - 8 & 7 = 1000 & 0111 = 0000 (0)
        - Count = 2
        """
        count = 0
        while n:
            n &= n - 1  # Remove the rightmost set bit
            count += 1
        return count

    def hammingWeight_builtin(self, n: int) -> int:
        """
        Using built-in bin() function for comparison.

        Time Complexity: O(log n)
        Space Complexity: O(log n) - for string conversion
        """
        return bin(n).count("1")

    def hammingWeight_shift(self, n: int) -> int:
        """
        Right shift approach - check each bit.

        Time Complexity: O(log n) - check all bits
        Space Complexity: O(1)
        """
        count = 0
        while n:
            count += n & 1  # Add 1 if rightmost bit is set
            n >>= 1  # Right shift to check next bit
        return count

    def hammingWeight_lookup(self, n: int) -> int:
        """
        Lookup table approach for 4-bit chunks.
        More efficient for repeated calls.

        Time Complexity: O(1) - constant number of operations
        Space Complexity: O(1) - small lookup table
        """
        # Precomputed lookup table for 4-bit values (0-15)
        lookup = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]

        count = 0
        while n:
            count += lookup[n & 0xF]  # Process 4 bits at a time
            n >>= 4
        return count


# Test cases
test_cases = [
    TestCase(
        name="Example 1",
        input={"n": 0b00000000000000000000000000001011},  # 11
        expected=3,
        description="Binary: 1011 has three 1 bits",
    ),
    TestCase(
        name="Example 2",
        input={"n": 0b00000000000000000000000010000000},  # 128
        expected=1,
        description="Binary: 10000000 has one 1 bit",
    ),
    TestCase(
        name="Example 3",
        input={"n": 0b11111111111111111111111111111101},  # 4294967293
        expected=31,
        description="Binary with 31 ones (one zero)",
    ),
    TestCase(name="Single bit", input={"n": 1}, expected=1, description="Single 1 bit"),
    TestCase(name="No bits set", input={"n": 0}, expected=0, description="No 1 bits"),
    TestCase(
        name="All bits set (8-bit)",
        input={"n": 255},  # 0b11111111
        expected=8,
        description="All 8 bits set",
    ),
    TestCase(
        name="Power of 2",
        input={"n": 16},  # 0b10000
        expected=1,
        description="Power of 2 has exactly one bit",
    ),
    TestCase(
        name="Large number",
        input={"n": 1023},  # 0b1111111111 (10 bits set)
        expected=10,
        description="Large number with multiple bits",
    ),
]


def demo():
    """Demonstrate different approaches to count 1 bits."""
    solution = Solution()

    print("=== LeetCode 191: Number of 1 Bits ===\n")

    # Example with detailed explanation
    n = 12  # Binary: 1100
    print(f"Input: {n} (binary: {bin(n)})")
    print(f"Output: {solution.hammingWeight(n)}")
    print()

    # Show Brian Kernighan's algorithm step by step
    print("Brian Kernighan's algorithm step-by-step:")
    temp_n = n
    count = 0
    step = 1

    while temp_n:
        print(f"  Step {step}: {temp_n} (binary: {bin(temp_n)})")
        temp_n &= temp_n - 1
        count += 1
        if temp_n:
            print(f"           -> {temp_n} (binary: {bin(temp_n)})")
        step += 1

    print(f"Final count: {count}")
    print()

    # Show different approaches
    print("Comparison of approaches:")
    test_numbers = [11, 128, 255, 0]

    for num in test_numbers:
        print(f"\nNumber: {num} (binary: {bin(num)})")
        print(f"  Brian Kernighan: {solution.hammingWeight(num)}")
        print(f"  Built-in count:  {solution.hammingWeight_builtin(num)}")
        print(f"  Right shift:     {solution.hammingWeight_shift(num)}")
        print(f"  Lookup table:    {solution.hammingWeight_lookup(num)}")

    # Demonstrate efficiency of Brian Kernighan's algorithm
    print("\n=== Efficiency Demonstration ===")
    sparse_num = 0b10000000000000000000000000000001  # Only 2 bits set
    dense_num = 0b11111111111111111111111111111111  # All 32 bits set

    print(f"Sparse number ({sparse_num}): {bin(sparse_num)}")
    print(f"  - Brian Kernighan only needs 2 iterations")
    print(f"  - Right shift needs 32 iterations")
    print(f"  Result: {solution.hammingWeight(sparse_num)}")

    return create_demo_output(
        title="Number of 1 Bits (Hamming Weight)",
        description="Count the number of 1 bits in binary representation",
        input_data={"n": n},
        expected_output=solution.hammingWeight(n),
    )


if __name__ == "__main__":
    run_test_cases(Solution().hammingWeight, test_cases)


# Register the problem
register_problem(
    slug="number-of-1-bits",
    leetcode_num=191,
    title="Number of 1 Bits",
    difficulty=Difficulty.EASY,
    category=Category.BIT_MANIP,
    solution_file=__file__,
)
