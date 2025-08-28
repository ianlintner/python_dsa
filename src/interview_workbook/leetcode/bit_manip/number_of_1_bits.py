"""
LeetCode 191: Number of 1 Bits

Write a function that takes the binary representation of an unsigned integer
and returns the number of '1' bits it has (also known as the Hamming weight).

Time Complexity: O(1) - at most 32 iterations for 32-bit integer
Space Complexity: O(1)
"""

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


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
TEST_CASES = [
    TestCase(
        input_args=(0b00000000000000000000000000001011,),  # 11
        expected=3,
        description="Binary: 1011 has three 1 bits",
    ),
    TestCase(
        input_args=(0b00000000000000000000000010000000,),  # 128
        expected=1,
        description="Binary: 10000000 has one 1 bit",
    ),
    TestCase(
        input_args=(0b11111111111111111111111111111101,),  # 4294967293
        expected=31,
        description="Binary with 31 ones (one zero)",
    ),
    TestCase(
        input_args=(1,),
        expected=1,
        description="Single 1 bit",
    ),
    TestCase(
        input_args=(0,),
        expected=0,
        description="No 1 bits",
    ),
    TestCase(
        input_args=(255,),  # 0b11111111
        expected=8,
        description="All 8 bits set",
    ),
    TestCase(
        input_args=(16,),  # 0b10000
        expected=1,
        description="Power of 2 has exactly one bit",
    ),
    TestCase(
        input_args=(1023,),  # 0b1111111111 (10 bits set)
        expected=10,
        description="Large number with multiple bits",
    ),
]


def create_demo_output() -> str:
    """Create comprehensive demo showing different approaches and analysis."""
    solution = Solution()

    output = []
    output.append("=== LeetCode 191: Number of 1 Bits ===\n")

    # Example with detailed explanation
    n = 12  # Binary: 1100
    output.append(f"Input: {n} (binary: {bin(n)})")
    output.append(f"Output: {solution.hammingWeight(n)}")
    output.append("")

    # Show Brian Kernighan's algorithm step by step
    output.append("Brian Kernighan's algorithm step-by-step:")
    temp_n = n
    count = 0
    step = 1

    while temp_n:
        output.append(f"  Step {step}: {temp_n} (binary: {bin(temp_n)})")
        temp_n &= temp_n - 1
        count += 1
        if temp_n:
            output.append(f"           -> {temp_n} (binary: {bin(temp_n)})")
        step += 1

    output.append(f"Final count: {count}")
    output.append("")

    # Show different approaches
    output.append("Comparison of approaches:")
    test_numbers = [11, 128, 255, 0]

    for num in test_numbers:
        output.append(f"\nNumber: {num} (binary: {bin(num)})")
        output.append(f"  Brian Kernighan: {solution.hammingWeight(num)}")
        output.append(f"  Built-in count:  {solution.hammingWeight_builtin(num)}")
        output.append(f"  Right shift:     {solution.hammingWeight_shift(num)}")
        output.append(f"  Lookup table:    {solution.hammingWeight_lookup(num)}")

    # Demonstrate efficiency of Brian Kernighan's algorithm
    output.append("\n=== Efficiency Demonstration ===")
    sparse_num = 0b10000000000000000000000000000001  # Only 2 bits set

    output.append(f"Sparse number ({sparse_num}): {bin(sparse_num)}")
    output.append("  - Brian Kernighan only needs 2 iterations")
    output.append("  - Right shift needs 32 iterations")
    output.append(f"  Result: {solution.hammingWeight(sparse_num)}")

    return "\n".join(output)


def test_solution():
    """Test the number of 1 bits solution."""
    solution = Solution()
    
    def run_tests(func_name: str, func):
        print(f"\nTesting {func_name}:")
        for i, test_case in enumerate(TEST_CASES):
            result = func(test_case.input_args[0])
            status = "✓" if result == test_case.expected else "✗"
            print(f"  Test {i + 1}: {status} - {test_case.description}")
            if result != test_case.expected:
                print(f"    Expected: {test_case.expected}, Got: {result}")

    run_tests("Brian Kernighan Approach", solution.hammingWeight)
    run_tests("Built-in Count", solution.hammingWeight_builtin)
    run_tests("Right Shift Approach", solution.hammingWeight_shift)
    run_tests("Lookup Table Approach", solution.hammingWeight_lookup)

    # Run standard test framework
    run_test_cases(
        solution.hammingWeight,
        TEST_CASES,
        "Number of 1 Bits",
    )


# Register the problem
register_problem(
    slug="number_of_1_bits",
    leetcode_num=191,
    title="Number of 1 Bits",
    difficulty=Difficulty.EASY,
    category=Category.BIT_MANIP,
    solution_func=lambda n: Solution().hammingWeight(n),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["bit-manipulation", "brian-kernighan"],
    notes="Brian Kernighan's algorithm: n & (n-1) removes rightmost set bit",
)
