"""
LeetCode 283: Move Zeroes

Given an integer array nums, move all 0's to the end of it while maintaining
the relative order of the non-zero elements.

Note that you must do this in-place without making a copy of the array.

URL: https://leetcode.com/problems/move-zeroes/
Difficulty: Easy
Category: Two Pointers

Patterns:
- Two pointers for in-place array modification
- Write pointer tracks position for next non-zero element
- Read pointer scans through entire array

Complexity:
- Time: O(n) - single pass through array
- Space: O(1) - in-place modification

Key Insights:
- Use write pointer to track where to place next non-zero element
- Read pointer finds non-zero elements to move
- After moving all non-zeros, fill remaining positions with zeros
- Alternative: swap elements to avoid explicit zero-filling

Edge Cases:
- Array with no zeros (no modification needed)
- Array with all zeros (no movement needed)
- Single element array
- Empty array
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty
from typing import List


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Move all zeros to end while maintaining relative order of non-zeros.
        Modifies array in-place.
        
        Args:
            nums: Array of integers (modified in-place)
        """
        # Two-pointer approach: write pointer tracks where to place next non-zero
        write_pos = 0
        
        # First pass: move all non-zero elements to the front
        for read_pos in range(len(nums)):
            if nums[read_pos] != 0:
                nums[write_pos] = nums[read_pos]
                write_pos += 1
        
        # Second pass: fill remaining positions with zeros
        while write_pos < len(nums):
            nums[write_pos] = 0
            write_pos += 1
    
    def moveZeroesSwap(self, nums: List[int]) -> None:
        """
        Alternative implementation using swapping.
        
        Args:
            nums: Array of integers (modified in-place)
        """
        left = 0  # Points to next position for non-zero element
        
        for right in range(len(nums)):
            if nums[right] != 0:
                # Swap non-zero element to left position
                nums[left], nums[right] = nums[right], nums[left]
                left += 1


# Helper function for testing since function modifies input
def test_move_zeroes(nums: List[int]) -> List[int]:
    """Wrapper function for testing - returns modified array."""
    nums_copy = nums.copy()
    solution = Solution()
    solution.moveZeroes(nums_copy)
    return nums_copy


# Test cases
test_cases = [
    TestCase(([0, 1, 0, 3, 12],), [1, 3, 12, 0, 0], "Basic case with mixed zeros"),
    TestCase(([0],), [0], "Single zero"),
    TestCase(([1],), [1], "Single non-zero"),
    TestCase(([0, 0, 1],), [1, 0, 0], "Multiple leading zeros"),
    TestCase(([1, 2, 3],), [1, 2, 3], "No zeros"),
    TestCase(([0, 0, 0],), [0, 0, 0], "All zeros"),
    TestCase(([1, 0, 2, 0, 3, 0],), [1, 2, 3, 0, 0, 0], "Alternating pattern"),
    TestCase(([-1, 0, -2, 0],), [-1, -2, 0, 0], "Negative numbers"),
]


def demo() -> str:
    """Run Move Zeroes demo with test cases."""
    test_results = run_test_cases(test_move_zeroes, test_cases, "LeetCode 283: Move Zeroes")
    
    return create_demo_output(
        "Move Zeroes",
        test_results,
        time_complexity="O(n)",
        space_complexity="O(1)",
        approach_notes="""
Two main approaches:

1. Two-pass approach:
   - First pass: copy all non-zero elements to front of array
   - Second pass: fill remaining positions with zeros
   - Clear separation of concerns, easy to understand

2. Swap approach:
   - Single pass with two pointers
   - Swap non-zero elements to correct positions
   - More operations but conceptually elegant

Both maintain relative order of non-zero elements and achieve O(n) time, O(1) space.
The two-pass approach may have better cache performance due to sequential writes.
        """.strip(),
    )


# Register the problem
register_problem(
    id=283,
    slug="move_zeroes",
    title="Move Zeroes",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.EASY,
    tags=["array", "two_pointers"],
    url="https://leetcode.com/problems/move-zeroes/",
    notes="Classic two-pointer problem for in-place array rearrangement",
)
