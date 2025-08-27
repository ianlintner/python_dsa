"""
LeetCode 153: Find Minimum in Rotated Sorted Array (Medium)
https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/

Suppose an array of length n sorted in ascending order is rotated between 1 and n times.
For example, the array nums = [0,1,2,4,5,6,7] might become:
- [4,5,6,7,0,1,2] if it was rotated 4 times.
- [0,1,2,4,5,6,7] if it was rotated 7 times.

Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].

Given the rotated sorted array nums of unique integers, return the minimum element of this array.
You must write an algorithm that runs in O(log n) time.

Example 1:
Input: nums = [3,4,5,1,2]
Output: 1
Explanation: The original array was [1,2,3,4,5] rotated 3 times.

Example 2:
Input: nums = [4,5,6,7,0,1,2]
Output: 0
Explanation: The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.

Example 3:
Input: nums = [11,13,15,17]
Output: 11
Explanation: The original array was [11,13,15,17] and it was rotated 4 times.

Constraints:
- n == nums.length
- 1 <= n <= 5000
- -5000 <= nums[i] <= 5000
- All the integers of nums are unique.
- nums is sorted and rotated between 1 and n times.

Algorithm Insights:
- Use binary search to find the rotation point where the minimum element lies
- In a rotated sorted array, the minimum element is where the rotation occurs
- If nums[mid] > nums[right], the minimum is in the right half
- If nums[mid] < nums[right], the minimum is in the left half (including mid)
- Continue until left == right

Time Complexity: O(log n) - binary search
Space Complexity: O(1) - constant extra space
"""

from typing import List
from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def findMin(self, nums: List[int]) -> int:
        """
        Find the minimum element in a rotated sorted array using binary search.
        
        The key insight is that in a rotated sorted array, one half will always
        be properly sorted. We can use this to determine which half contains
        the minimum element.
        
        Args:
            nums: Rotated sorted array of unique integers
            
        Returns:
            The minimum element in the array
        """
        left, right = 0, len(nums) - 1
        
        # If array is not rotated, first element is minimum
        if nums[left] <= nums[right]:
            return nums[left]
        
        while left < right:
            mid = left + (right - left) // 2
            
            # If mid element is greater than rightmost element,
            # the minimum must be in the right half
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                # If mid element is less than or equal to rightmost element,
                # the minimum could be mid or in the left half
                right = mid
                
        return nums[left]


def demo():
    """
    Demonstrate finding minimum in rotated sorted arrays with examples.
    """
    solution = Solution()
    
    test_cases = [
        # Example 1: Basic rotation
        ([3, 4, 5, 1, 2], 1),
        
        # Example 2: Heavy rotation
        ([4, 5, 6, 7, 0, 1, 2], 0),
        
        # Example 3: No effective rotation (rotated n times)
        ([11, 13, 15, 17], 11),
        
        # Edge case: Single element
        ([1], 1),
        
        # Edge case: Two elements, rotated
        ([2, 1], 1),
        
        # Edge case: Two elements, not rotated
        ([1, 2], 1),
        
        # Large rotation with negative numbers
        ([5, 1, 2, 3, 4], 1),
        
        # Mixed positive and negative
        ([-1, 0, 1, 2, -3, -2], -3),
        
        # All negative numbers
        ([-3, -2, -1, -5, -4], -5),
    ]
    
    print("Find Minimum in Rotated Sorted Array - LeetCode 153")
    print("=" * 55)
    
    for i, (nums, expected) in enumerate(test_cases, 1):
        result = solution.findMin(nums.copy())  # Copy to avoid modifying original
        status = "✓" if result == expected else "✗"
        
        print(f"\nTest {i}: {status}")
        print(f"Input:    {nums}")
        print(f"Expected: {expected}")
        print(f"Got:      {result}")
        
        if result != expected:
            print(f"❌ MISMATCH!")
    
    print(f"\n📊 Algorithm Analysis:")
    print(f"⏰ Time Complexity:  O(log n) - binary search")
    print(f"💾 Space Complexity: O(1) - constant extra space")
    
    print(f"\n🔍 Key Insights:")
    print(f"• In rotated sorted array, minimum is at the rotation point")
    print(f"• Compare mid with rightmost element to determine search direction")
    print(f"• If nums[mid] > nums[right], minimum is in right half")
    print(f"• If nums[mid] ≤ nums[right], minimum is in left half (including mid)")
    
    print(f"\n⚠️  Common Pitfalls:")
    print(f"• Comparing mid with left element instead of right")
    print(f"• Not handling the case where array is not rotated")
    print(f"• Off-by-one errors in binary search bounds")
    
    print(f"\n🔄 Follow-up Questions:")
    print(f"• What if duplicates are allowed? (LeetCode 154)")
    print(f"• How to find the rotation count?")
    print(f"• Can you solve without knowing the array is rotated?")


# Register the problem
register_problem(
    id=153,
    slug="find_min_in_rotated_sorted_array",
    title="Find Minimum in Rotated Sorted Array",
    category=Category.BINARY_SEARCH,
    difficulty=Difficulty.MEDIUM,
    tags=["Array", "Binary Search"],
    url="https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/",
    notes="Binary search to find minimum in rotated sorted array"
)


if __name__ == "__main__":
    demo()
