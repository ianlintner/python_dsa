"""LeetCode Problem 15: 3Sum
Find all unique triplets in the array which gives the sum of zero.
"""

from typing import List

from src.interview_workbook.leetcode._registry import register_problem


def threeSum(nums: List[int]) -> List[List[int]]:
    """Return all unique triplets [a, b, c] such that a+b+c = 0."""
    nums.sort()
    res: List[List[int]] = []
    n = len(nums)

    for i in range(n):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        target = -nums[i]
        l, r = i + 1, n - 1
        while l < r:
            s = nums[l] + nums[r]
            if s == target:
                res.append([nums[i], nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
                while l < r and nums[r] == nums[r + 1]:
                    r -= 1
            elif s < target:
                l += 1
            else:
                r -= 1
    return res


def demo() -> str:
    """Deterministic demo for 3Sum problem."""
    example = [-1, 0, 1, 2, -1, -4]
    result = threeSum(example)
    # Ensure deterministic ordering for testing
    result_sorted = sorted([sorted(triplet) for triplet in result])
    return str(result_sorted)


register_problem(
    problem_id=15,
    slug="3sum",
    category="TWO_POINTERS",
    difficulty="MEDIUM",
    tags=["Array", "Two Pointers", "Sorting"],
    url="https://leetcode.com/problems/3sum/",
)
