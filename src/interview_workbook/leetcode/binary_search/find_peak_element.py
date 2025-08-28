"""
LeetCode 162: Find Peak Element

A peak element is an element that is strictly greater than its neighbors.

Given a 0-indexed integer array nums, find a peak element, and return its index.
If the array contains multiple peaks, return the index to any of the peaks.

You may imagine that nums[-1] = nums[n] = -∞. In other words, an element is
always considered to be strictly greater than a neighbor that is outside the array.

You must write an algorithm that runs in O(log n) time.

Example 1:
Input: nums = [1,2,3,1]
Output: 2
Explanation: 3 is a peak element and your function should return the index number 2.

Example 2:
Input: nums = [1,2,1,3,5,6,4]
Output: 5
Explanation: Your function can return either index number 1 where the peak element is 2,
or index number 5 where the peak element is 6.

Constraints:
- 1 <= nums.length <= 1000
- -2^31 <= nums[i] <= 2^31 - 1
- nums[i] != nums[i + 1] for all valid i
"""

from typing import List

from interview_workbook.leetcode._registry import register_problem


class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        """
        Find peak element using binary search.

        Time: O(log n)
        Space: O(1)

        Algorithm:
        1. Binary search with the insight that we always move towards the higher neighbor
        2. If nums[mid] < nums[mid+1], there must be a peak on the right side
        3. If nums[mid] > nums[mid+1], there must be a peak on the left side (including mid)
        4. This works because nums[-1] = nums[n] = -∞
        """
        left, right = 0, len(nums) - 1

        while left < right:
            mid = left + (right - left) // 2

            if nums[mid] < nums[mid + 1]:
                # Peak must be on the right side
                left = mid + 1
            else:
                # Peak must be on the left side (including mid)
                right = mid

        return left

    def findPeakElementLinear(self, nums: List[int]) -> int:
        """
        Linear solution for comparison (not optimal but intuitive).

        Time: O(n)
        Space: O(1)
        """
        n = len(nums)

        # Check first element
        if n == 1 or nums[0] > nums[1]:
            return 0

        # Check last element
        if nums[n - 1] > nums[n - 2]:
            return n - 1

        # Check middle elements
        for i in range(1, n - 1):
            if nums[i] > nums[i - 1] and nums[i] > nums[i + 1]:
                return i

        return -1  # Should never reach here given constraints

    def findPeakElementRecursive(self, nums: List[int]) -> int:
        """
        Recursive binary search implementation.

        Time: O(log n)
        Space: O(log n) due to recursion stack
        """

        def binary_search(left: int, right: int) -> int:
            if left == right:
                return left

            mid = left + (right - left) // 2

            if nums[mid] < nums[mid + 1]:
                return binary_search(mid + 1, right)
            else:
                return binary_search(left, mid)

        return binary_search(0, len(nums) - 1)


def demo():
    """Demo of Find Peak Element."""
    solution = Solution()

    test_cases = [
        {"nums": [1, 2, 3, 1], "expected_indices": [2], "explanation": "3 is peak at index 2"},
        {
            "nums": [1, 2, 1, 3, 5, 6, 4],
            "expected_indices": [1, 5],
            "explanation": "Peaks at indices 1 (value 2) or 5 (value 6)",
        },
        {"nums": [1], "expected_indices": [0], "explanation": "Single element is always a peak"},
        {"nums": [1, 2], "expected_indices": [1], "explanation": "Last element is peak"},
        {"nums": [2, 1], "expected_indices": [0], "explanation": "First element is peak"},
        {"nums": [1, 3, 2, 1], "expected_indices": [1], "explanation": "3 is peak at index 1"},
    ]

    print("=== LeetCode 162: Find Peak Element ===\n")

    for i, test in enumerate(test_cases, 1):
        nums = test["nums"]
        expected_indices = test["expected_indices"]
        explanation = test["explanation"]

        print(f"Test Case {i}:")
        print(f"Nums: {nums}")
        print(f"Expected indices: {expected_indices}")
        print(f"Explanation: {explanation}")

        # Test binary search solution
        result = solution.findPeakElement(nums)
        print(f"Result (Binary Search): {result}")

        # Verify the result is valid
        def is_peak(arr: List[int], idx: int) -> bool:
            n = len(arr)
            left_ok = idx == 0 or arr[idx] > arr[idx - 1]
            right_ok = idx == n - 1 or arr[idx] > arr[idx + 1]
            return left_ok and right_ok

        is_valid_peak = is_peak(nums, result)
        is_expected = result in expected_indices

        print(f"Is valid peak: {'✓' if is_valid_peak else '✗'}")
        print(f"Is expected index: {'✓' if is_expected else '✗'}")

        status = "✓ PASS" if is_valid_peak else "✗ FAIL"
        print(f"Status: {status}")

        # Test other implementations
        result_linear = solution.findPeakElementLinear(nums)
        result_recursive = solution.findPeakElementRecursive(nums)
        print(f"Result (Linear): {result_linear}")
        print(f"Result (Recursive): {result_recursive}")

        if len(nums) <= 10:  # Only show values for small arrays
            print(f"Peak value: {nums[result]}")
        print()


if __name__ == "__main__":
    demo()


# Register the problem
register_problem(
    id="162",
    title="Find Peak Element",
    difficulty="Medium",
    category="Binary Search",
    url="https://leetcode.com/problems/find-peak-element/",
    tags=["Array", "Binary Search"],
    module_path="interview_workbook.leetcode.binary_search.find_peak_element",
)
