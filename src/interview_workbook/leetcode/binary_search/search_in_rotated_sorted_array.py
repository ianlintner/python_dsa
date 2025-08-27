"""
LeetCode 33: Search in Rotated Sorted Array

There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly rotated at an unknown pivot index k (1 <= k < nums.length) 
such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). 
For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and become [4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, 
or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Example 2:
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Example 3:
Input: nums = [1], target = 0
Output: -1

URL: https://leetcode.com/problems/search-in-rotated-sorted-array/
Difficulty: Medium
Category: Binary Search

Patterns:
- Modified binary search with rotation handling
- Divide and conquer with sorted half detection
- Two-phase search strategy

Complexity:
- Time: O(log n) - binary search with constant extra work per iteration
- Space: O(1) - only use constant extra space

Pitfalls:
- Need to handle the rotation point correctly
- Must determine which half is sorted at each step
- Edge cases with single element or no rotation
- Boundary conditions when target equals pivot elements

Follow-ups:
- What if array contains duplicates? (LeetCode 81)
- How to find the rotation point/minimum element?
- How to handle multiple rotations?
"""

from typing import List
from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """
        Search for target in rotated sorted array.
        
        Args:
            nums: Rotated sorted array with distinct values
            target: Target value to search for
            
        Returns:
            Index of target if found, -1 otherwise
        """
        if not nums:
            return -1
            
        left, right = 0, len(nums) - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            
            # Found the target
            if nums[mid] == target:
                return mid
            
            # Determine which half is sorted
            if nums[left] <= nums[mid]:  # Left half is sorted
                # Check if target is in the sorted left half
                if nums[left] <= target < nums[mid]:
                    right = mid - 1  # Search left half
                else:
                    left = mid + 1   # Search right half
            else:  # Right half is sorted
                # Check if target is in the sorted right half
                if nums[mid] < target <= nums[right]:
                    left = mid + 1   # Search right half
                else:
                    right = mid - 1  # Search left half
        
        return -1  # Target not found


# Test cases
test_cases = [
    TestCase(([4, 5, 6, 7, 0, 1, 2], 0), 4, "Example 1: target in rotated part"),
    TestCase(([4, 5, 6, 7, 0, 1, 2], 3), -1, "Example 2: target not found"),
    TestCase(([1], 0), -1, "Example 3: single element, target not found"),
    TestCase(([1], 1), 0, "Single element, target found"),
    TestCase(([4, 5, 6, 7, 0, 1, 2], 4), 0, "Target at beginning"),
    TestCase(([4, 5, 6, 7, 0, 1, 2], 2), 6, "Target at end"),
    TestCase(([4, 5, 6, 7, 0, 1, 2], 5), 1, "Target in sorted left part"),
    TestCase(([4, 5, 6, 7, 0, 1, 2], 1), 5, "Target in sorted right part"),
    TestCase(([1, 2, 3, 4, 5], 3), 2, "No rotation, target found"),
    TestCase(([5, 1, 2, 3, 4], 1), 1, "Rotation at index 1"),
    TestCase(([2, 3, 4, 5, 1], 1), 4, "Rotation at last position"),
    TestCase(([3, 1], 1), 1, "Two elements with rotation"),
]


def demo() -> str:
    """Run Search in Rotated Sorted Array demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(solution.search, test_cases, "LeetCode 33: Search in Rotated Sorted Array")

    return create_demo_output(
        "Search in Rotated Sorted Array",
        test_results,
        time_complexity="O(log n)",
        space_complexity="O(1)",
        approach_notes="""
Key insights:
1. Modified binary search: at each step, exactly one half is sorted
2. Determine sorted half by comparing nums[left] with nums[mid]
3. If left half sorted: check if target in [nums[left], nums[mid])
4. If right half sorted: check if target in (nums[mid], nums[right]]
5. Always eliminate one half of the search space to maintain O(log n)
6. Handle edge cases: single element, no rotation, target at boundaries

Algorithm steps:
- Use standard binary search template with left <= right
- At each iteration, identify which half is sorted
- Check if target lies within the sorted half's range
- If yes, search that half; otherwise search the other half
- Continue until target found or search space exhausted
        """.strip(),
    )


# Register the problem
register_problem(
    id=33,
    slug="search_in_rotated_sorted_array",
    title="Search in Rotated Sorted Array",
    category=Category.BINARY_SEARCH,
    difficulty=Difficulty.MEDIUM,
    tags=['array', 'binary_search'],
    url="https://leetcode.com/problems/search-in-rotated-sorted-array/",
    notes="Classic binary search variation handling rotation by detecting which half is sorted at each step",
)
