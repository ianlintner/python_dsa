"""
Product of Array Except Self - LeetCode Problem

Given an integer array nums, return an array answer such that answer[i] is equal to
the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, create_demo_output, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        Calculate product of all elements except self using left and right pass approach.

        Time Complexity: O(n) - two passes through array
        Space Complexity: O(1) - excluding output array

        Args:
            nums: List of integers

        Returns:
            List[int]: Products of all elements except self
        """
        n = len(nums)
        result = [1] * n

        # First pass: calculate left products
        # result[i] contains product of all elements to the left of i
        for i in range(1, n):
            result[i] = result[i - 1] * nums[i - 1]

        # Second pass: multiply by right products
        # Use a variable to track product of elements to the right
        right_product = 1
        for i in range(n - 1, -1, -1):
            result[i] = result[i] * right_product
            right_product *= nums[i]

        return result

    def productExceptSelfTwoArrays(self, nums: List[int]) -> List[int]:
        """
        Alternative approach using separate left and right arrays for clarity.

        Time Complexity: O(n)
        Space Complexity: O(n) - for left and right arrays
        """
        n = len(nums)

        # Calculate left products
        left = [1] * n
        for i in range(1, n):
            left[i] = left[i - 1] * nums[i - 1]

        # Calculate right products
        right = [1] * n
        for i in range(n - 2, -1, -1):
            right[i] = right[i + 1] * nums[i + 1]

        # Multiply left and right products
        result = []
        for i in range(n):
            result.append(left[i] * right[i])

        return result

    def productExceptSelfDivision(self, nums: List[int]) -> List[int]:
        """
        Alternative using division (not allowed in problem but educational).

        Time Complexity: O(n)
        Space Complexity: O(1) - excluding output array

        Note: This approach doesn't work if array contains zeros and
        division is not allowed in the problem statement.
        """

        # Count zeros and calculate product of non-zero elements
        zero_count = 0
        product = 1

        for num in nums:
            if num == 0:
                zero_count += 1
            else:
                product *= num

        result = []
        for num in nums:
            if zero_count > 1:
                # More than one zero means all results are 0
                result.append(0)
            elif zero_count == 1:
                # Exactly one zero means only that position gets the product
                result.append(product if num == 0 else 0)
            else:
                # No zeros, divide total product by current number
                result.append(product // num)

        return result


def demo():
    """Demonstrate Product of Array Except Self solution with test cases."""
    solution = Solution()

    test_cases = [
        TestCase(
            input_args=([1, 2, 3, 4],),
            expected=[24, 12, 8, 6],
            description="Basic case with positive integers",
        ),
        TestCase(
            input_args=([-1, 1, 0, -3, 3],), expected=[0, 0, 9, 0, 0], description="Array with zero"
        ),
        TestCase(input_args=([2, 3],), expected=[3, 2], description="Two elements"),
        TestCase(input_args=([1, 0],), expected=[0, 1], description="One and zero"),
        TestCase(
            input_args=([-1, -2, -3],), expected=[6, 3, 2], description="All negative numbers"
        ),
        TestCase(input_args=([2, 2, 2, 2],), expected=[8, 8, 8, 8], description="All same numbers"),
        TestCase(input_args=([0, 0],), expected=[0, 0], description="Multiple zeros"),
        TestCase(
            input_args=([5, 0, 3, 0, 7],),
            expected=[0, 0, 0, 0, 0],
            description="Multiple zeros in array",
        ),
    ]

    results = run_test_cases(solution.productExceptSelf, test_cases)

    # Format results as test results string
    test_results_lines = ["=== Product of Array Except Self ===", ""]
    passed_count = 0
    total_time = sum(r.get("time_ms", 0) for r in results)
    
    for result in results:
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        test_results_lines.append(f"Test Case {result['test_case']}: {status}")
        test_results_lines.append(f"  Description: {result['description']}")
        test_results_lines.append(f"  Input: {result['input']}")
        test_results_lines.append(f"  Expected: {result['expected']}")
        test_results_lines.append(f"  Got: {result['actual']}")
        if "time_ms" in result:
            test_results_lines.append(f"  Time: {result['time_ms']:.3f}ms")
        test_results_lines.append("")
        if result["passed"]:
            passed_count += 1
    
    test_results_lines.append(f"Results: {passed_count}/{len(results)} passed")
    test_results_lines.append(f"Total time: {total_time:.3f}ms")
    
    if passed_count == len(results):
        test_results_lines.append("🎉 All tests passed!")
    else:
        test_results_lines.append(f"❌ {len(results) - passed_count} test(s) failed")
    
    test_results_str = "\n".join(test_results_lines)
    
    approach_notes = """
Key Insights:
• Two-pass approach: left products then right products
• Result array serves as left products array to save space
• No division operation needed, works with zeros
• O(1) extra space complexity (excluding output)

Common Pitfalls:
• Handle edge cases with zeros correctly
• Remember space complexity doesn't count output array
• Division approach fails with zeros
• Be careful with array bounds in loops

Follow-up Questions:
• Can you solve it in one pass? (No, need both directions)
• What if we can use division operation?
• How would you handle overflow in languages without big integers?
• Can you optimize further for memory usage?
"""

    return create_demo_output(
        problem_title="Product of Array Except Self",
        test_results=test_results_str,
        time_complexity="O(n) - two passes through array",
        space_complexity="O(1) - excluding output array, constant extra space",
        approach_notes=approach_notes,
    )


# Register this problem
register_problem(
    id=238,
    slug="product-of-array-except-self",
    title="Product of Array Except Self",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "prefix-sum"],
    url="https://leetcode.com/problems/product-of-array-except-self/",
    notes="Left and right pass approach to calculate products without division",
)
