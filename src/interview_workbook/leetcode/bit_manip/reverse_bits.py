"""
LeetCode 190: Reverse Bits

Reverse bits of a given 32 bits unsigned integer.

Note: In some languages such as Java, there is no unsigned integer type.
In this case, both input and output will be given as a signed integer type.
They should not affect your implementation.

Time Complexity: O(1) - fixed 32 iterations
Space Complexity: O(1)
"""

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def reverseBits(self, n: int) -> int:
        """
        Bit manipulation approach - process each bit.

        Algorithm:
        1. Initialize result to 0
        2. For 32 iterations:
           - Left shift result by 1
           - Add the rightmost bit of n to result
           - Right shift n by 1

        Example: n = 43261596 (00000010100101000001111010011100)
        Result should be 964176192 (00111001011110000010100101000000)
        """
        result = 0

        for i in range(32):
            result = (result << 1) | (n & 1)
            n >>= 1

        return result

    def reverseBits_builtin(self, n: int) -> int:
        """
        Using built-in string operations for comparison.

        Time Complexity: O(1) - fixed operations
        Space Complexity: O(1) - fixed string size
        """
        # Convert to 32-bit binary string, reverse it, convert back
        binary_str = format(n, "032b")  # 32-bit binary with leading zeros
        reversed_str = binary_str[::-1]  # Reverse the string
        return int(reversed_str, 2)  # Convert back to integer

    def reverseBits_divide_conquer(self, n: int) -> int:
        """
        Divide and conquer approach - swap chunks of bits.

        More efficient for multiple calls as it processes multiple bits at once.

        Time Complexity: O(1) - fixed number of operations
        Space Complexity: O(1)
        """
        # Swap every two adjacent bits
        n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)

        # Swap every two adjacent pairs
        n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)

        # Swap every two adjacent quads
        n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)

        # Swap every two adjacent bytes
        n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)

        # Swap the two 16-bit halves
        n = (n >> 16) | (n << 16)

        return n & 0xFFFFFFFF  # Ensure 32-bit result

    def reverseBits_lookup(self, n: int) -> int:
        """
        Lookup table approach for 8-bit chunks.
        Efficient when this function is called many times.

        Time Complexity: O(1) - 4 lookups
        Space Complexity: O(1) - small lookup table
        """
        # Precomputed lookup table for 8-bit reversals (0-255)
        lookup = {}
        for i in range(256):
            lookup[i] = int(format(i, "08b")[::-1], 2)

        result = 0
        for i in range(4):  # Process 4 bytes (32 bits total)
            byte_val = (n >> (i * 8)) & 0xFF
            result |= lookup[byte_val] << (24 - i * 8)

        return result


# Test cases
TEST_CASES = [
    TestCase(
        input_args=(0b00000010100101000001111010011100,),  # 43261596
        expected=0b00111001011110000010100101000000,  # 964176192
        description="Standard bit reversal example",
    ),
    TestCase(
        input_args=(0b11111111111111111111111111111101,),  # 4294967293
        expected=0b10111111111111111111111111111111,  # 3221225471
        description="Nearly all bits set",
    ),
    TestCase(
        input_args=(0b00000000000000000000000000000000,),  # 0
        expected=0b00000000000000000000000000000000,  # 0
        description="All bits are zero",
    ),
    TestCase(
        input_args=(0b11111111111111111111111111111111,),  # 4294967295
        expected=0b11111111111111111111111111111111,  # 4294967295
        description="All bits are one",
    ),
    TestCase(
        input_args=(0b10000000000000000000000000000000,),  # 2147483648
        expected=0b00000000000000000000000000000001,  # 1
        description="Single bit at leftmost position",
    ),
    TestCase(
        input_args=(0b00000000000000000000000000000001,),  # 1
        expected=0b10000000000000000000000000000000,  # 2147483648
        description="Single bit at rightmost position",
    ),
    TestCase(
        input_args=(0b10101010101010101010101010101010,),  # 2863311530
        expected=0b01010101010101010101010101010101,  # 1431655765
        description="Alternating bit pattern",
    ),
]


def create_demo_output() -> str:
    """Create comprehensive demo showing different approaches and analysis."""
    solution = Solution()

    output = []
    output.append("=== LeetCode 190: Reverse Bits ===\n")

    # Example with detailed explanation
    n = 43261596  # 00000010100101000001111010011100
    output.append(f"Input:  {n}")
    output.append(f"Binary: {format(n, '032b')}")

    result = solution.reverseBits(n)
    output.append(f"Output: {result}")
    output.append(f"Binary: {format(result, '032b')}")
    output.append("")

    # Show bit-by-bit reversal process
    output.append("Bit-by-bit reversal process:")
    temp_n = n
    temp_result = 0

    output.append(f"Input:  {format(temp_n, '032b')}")
    for i in range(5):  # Show first 5 steps
        bit = temp_n & 1
        temp_result = (temp_result << 1) | bit
        temp_n >>= 1
        output.append(f"Step {i + 1}: {format(temp_result, '032b')} (added bit {bit})")

    output.append("...")
    output.append(f"Final:  {format(result, '032b')}")
    output.append("")

    # Compare different approaches
    output.append("Comparison of approaches:")
    test_cases_demo = [
        (1, "00000000000000000000000000000001"),
        (43261596, "00000010100101000001111010011100"),
        (2863311530, "10101010101010101010101010101010"),
    ]

    for num, binary in test_cases_demo:
        output.append(f"\nInput: {num} ({binary})")
        output.append(f"  Bit-by-bit:      {solution.reverseBits(num)}")
        output.append(f"  Built-in string: {solution.reverseBits_builtin(num)}")
        output.append(f"  Divide-conquer:  {solution.reverseBits_divide_conquer(num)}")
        output.append(f"  Lookup table:    {solution.reverseBits_lookup(num)}")

    # Show divide and conquer steps
    output.append("\n=== Divide and Conquer Approach ===")
    output.append("Example with n = 43261596:")

    demo_n = 43261596
    output.append(f"Original: {format(demo_n, '032b')}")

    # Step by step divide and conquer
    steps = [
        ("Swap adjacent bits", "0xaaaaaaaa & 0x55555555"),
        ("Swap adjacent pairs", "0xcccccccc & 0x33333333"),
        ("Swap adjacent quads", "0xf0f0f0f0 & 0x0f0f0f0f"),
        ("Swap adjacent bytes", "0xff00ff00 & 0x00ff00ff"),
        ("Swap 16-bit halves", ">> 16 | << 16"),
    ]

    for i, (desc, mask) in enumerate(steps, 1):
        output.append(f"Step {i}: {desc}")
        output.append(f"         Mask: {mask}")

    final_result = solution.reverseBits_divide_conquer(demo_n)
    output.append(f"Final:   {format(final_result, '032b')} = {final_result}")

    return "\n".join(output)


def test_solution():
    """Test the reverse bits solution."""
    solution = Solution()
    
    def run_tests(func_name: str, func):
        print(f"\nTesting {func_name}:")
        for i, test_case in enumerate(TEST_CASES):
            result = func(test_case.input_args[0])
            status = "✓" if result == test_case.expected else "✗"
            print(f"  Test {i + 1}: {status} - {test_case.description}")
            if result != test_case.expected:
                print(f"    Expected: {test_case.expected}, Got: {result}")

    run_tests("Bit-by-bit Approach", solution.reverseBits)
    run_tests("Built-in String", solution.reverseBits_builtin)
    run_tests("Divide-Conquer", solution.reverseBits_divide_conquer)
    run_tests("Lookup Table", solution.reverseBits_lookup)

    # Run standard test framework
    run_test_cases(
        solution.reverseBits,
        TEST_CASES,
        "Reverse Bits",
    )


# Register the problem
register_problem(
    slug="reverse_bits",
    leetcode_num=190,
    title="Reverse Bits",
    difficulty=Difficulty.EASY,
    category=Category.BIT_MANIP,
    solution_func=lambda n: Solution().reverseBits(n),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["bit-manipulation", "divide-and-conquer"],
    notes="Reverse 32-bit integer: bit-by-bit or divide-and-conquer approaches",
)
