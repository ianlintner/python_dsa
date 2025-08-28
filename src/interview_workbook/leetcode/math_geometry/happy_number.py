"""
LeetCode 202: Happy Number
https://leetcode.com/problems/happy-number/

Write an algorithm to determine if a number n is happy.

A happy number is a number defined by the following process:
- Starting with any positive integer, replace the number by the sum of the squares of its digits.
- Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
- Those numbers for which this process ends in 1 are happy.

Return true if n is a happy number, and false if not.

Examples:
    Input: n = 19
    Output: true
    Explanation:
    1² + 9² = 82
    8² + 2² = 68
    6² + 8² = 100
    1² + 0² + 0² = 1

    Input: n = 2
    Output: false

Constraints:
    * 1 <= n <= 2^31 - 1
"""

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def isHappy(self, n: int) -> bool:
        """
        Determine if number is happy using cycle detection with set.

        Algorithm:
        1. Keep calculating sum of squares of digits
        2. If we reach 1, it's happy
        3. If we see a number we've seen before, it's a cycle (not happy)
        4. Use set to track seen numbers for cycle detection

        Time: O(log n) - digits decrease, cycles are short
        Space: O(log n) - store seen numbers in set
        """
        seen = set()

        while n != 1 and n not in seen:
            seen.add(n)
            n = self._get_sum_of_squares(n)

        return n == 1

    def isHappy_floyd_cycle(self, n: int) -> bool:
        """
        Alternative: Use Floyd's cycle detection (two pointers) - O(1) space.

        Algorithm:
        1. Use slow/fast pointers like detecting cycle in linked list
        2. Slow moves one step, fast moves two steps
        3. If they meet and it's not 1, there's a cycle
        4. If slow reaches 1, it's happy

        Time: O(log n)
        Space: O(1) - constant space
        """
        slow = n
        fast = n

        while True:
            slow = self._get_sum_of_squares(slow)  # One step
            fast = self._get_sum_of_squares(self._get_sum_of_squares(fast))  # Two steps

            if slow == fast:
                break

        return slow == 1

    def _get_sum_of_squares(self, n: int) -> int:
        """Calculate sum of squares of digits."""
        total = 0
        while n > 0:
            digit = n % 10
            total += digit * digit
            n //= 10
        return total

    def isHappy_brute_force(self, n: int) -> bool:
        """
        Brute force: Track sequence with limited iterations.

        Time: O(log n * k) where k is max iterations
        Space: O(1)
        """
        max_iterations = 1000  # Prevent infinite loop

        for _ in range(max_iterations):
            if n == 1:
                return True
            n = self._get_sum_of_squares(n)

        return False


def create_demo_output() -> str:
    """Demonstrate happy number detection with various test cases."""
    test_cases = [
        # Happy numbers
        (1, "Trivial happy number"),
        (19, "Classic example: 19"),
        (7, "Single digit happy: 7"),
        (10, "Happy number: 10"),
        (13, "Happy number: 13"),
        (23, "Happy number: 23"),
        (28, "Happy number: 28"),
        (97, "Happy number: 97"),
        # Unhappy numbers
        (2, "Classic unhappy: 2"),
        (3, "Unhappy: 3"),
        (4, "Unhappy: 4 (enters cycle quickly)"),
        (5, "Unhappy: 5"),
        (6, "Unhappy: 6"),
        (8, "Unhappy: 8"),
        (9, "Unhappy: 9"),
        (20, "Unhappy: 20"),
        # Edge cases
        (2147483647, "Max 32-bit integer"),
        (999999999, "Many 9s"),
    ]

    solution = Solution()
    results = []

    for num, description in test_cases:
        is_happy = solution.isHappy(num)

        # Show the sequence for small numbers
        sequence = []
        temp = num
        seen = set()

        while temp != 1 and temp not in seen and len(sequence) < 10:
            seen.add(temp)
            sequence.append(temp)
            temp = solution._get_sum_of_squares(temp)

        if temp == 1:
            sequence.append(1)
        elif temp in seen:
            sequence.append(f"cycle at {temp}")
        else:
            sequence.append("...")

        results.append(f"\n{description}: {num}")
        results.append(f"Happy: {is_happy}")
        results.append(f"Sequence: {' -> '.join(map(str, sequence))}")

    # Demonstrate different approaches
    results.append("\n" + "=" * 50)
    results.append("ALGORITHM COMPARISON")
    results.append("=" * 50)

    import time

    test_numbers = [19, 2, 999999999, 2147483647] * 250  # 1000 total tests

    approaches = [
        (solution.isHappy, "Hash Set Cycle Detection"),
        (solution.isHappy_floyd_cycle, "Floyd's Cycle Detection (O(1) space)"),
        (solution.isHappy_brute_force, "Brute Force with Max Iterations"),
    ]

    for method, name in approaches:
        start = time.perf_counter()
        for num in test_numbers:
            method(num)
        end = time.perf_counter()

        results.append(f"\n{name}:")
        results.append(f"Time: {(end - start) * 1000:.2f}ms for {len(test_numbers)} tests")
        results.append(f"Avg per test: {((end - start) * 1000000 / len(test_numbers)):.1f}μs")

    # Show mathematical insights
    results.append("\n" + "=" * 50)
    results.append("MATHEMATICAL INSIGHTS")
    results.append("=" * 50)

    results.append("\nKnown cycles for unhappy numbers:")
    results.append("4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 (length 8)")

    results.append("\nAll unhappy numbers eventually enter this cycle!")
    results.append("This is why Floyd's cycle detection works perfectly.")

    # Count happy vs unhappy in first 100
    happy_count = sum(1 for i in range(1, 101) if solution.isHappy(i))
    results.append(f"\nIn first 100 numbers: {happy_count} happy, {100 - happy_count} unhappy")

    return "\n".join(results)


# Test cases for validation
TEST_CASES = [
    TestCase(
        input_args=(19,,
    ), expected=True, description="Classic happy number example"),
    TestCase(
        input_args=(2,,
    ), expected=False, description="Classic unhappy number example"),
    TestCase(
        input_args=(1,,
    ), expected=True, description="Trivial case: 1 is happy"),
    TestCase(
        input_args=(7,,
    ), expected=True, description="Single digit happy number"),
    TestCase(
        input_args=(10,,
    ), expected=True, description="Happy number: 10"),
    TestCase(
        input_args=(13,,
    ), expected=True, description="Happy number: 13"),
    TestCase(
        input_args=(23,,
    ), expected=True, description="Happy number: 23"),
    TestCase(
        input_args=(3,,
    ), expected=False, description="Unhappy number: 3"),
    TestCase(
        input_args=(4,,
    ), expected=False, description="Unhappy number that enters cycle quickly"
    ),
    TestCase(
        input_args=(5,,
    ), expected=False, description="Unhappy number: 5"),
    TestCase(
        input_args=(82,,
    ), expected=True, description="Part of 19's sequence, should be happy"),
    TestCase(
        input_args=(999999999,,
    ), expected=False, description="Large number with many 9s"),
]


def test_solution():
    """Test the happy number solution."""
    solution = Solution()

    def run_test(n, expected, description):
        result = solution.isHappy(n)
        if result == expected:
            return True, ""
        else:
            return False, f"Input: {n}, Expected: {expected}, Got: {result}"

    return run_test_cases(TEST_CASES, run_test)


# Register the problem
register_problem(
    slug="happy_number",
    leetcode_num=202,
    title="Happy Number",
    difficulty=Difficulty.EASY,
    category=Category.MATH_GEOMETRY,
    solution_func=Solution().isHappy,
    test_func=test_solution,
    demo_func=create_demo_output,
)


if __name__ == "__main__":
    # Run tests
    print("Testing Happy Number...")
    result = test_solution()
    print(f"Tests passed: {result}")

    # Show demo
    print("\n" + "=" * 50)
    print("DEMO OUTPUT")
    print("=" * 50)
    print(create_demo_output())
