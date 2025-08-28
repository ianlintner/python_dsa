"""
LeetCode 875: Koko Eating Bananas

Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas.
The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile
of bananas and eats k bananas from that pile. If the pile has less than k bananas,
she eats all of them for that hour and will not eat any more bananas during that hour.

Koko likes to eat slowly but wants to finish all the bananas before the guards return.

Return the minimum integer k such that she can eat all bananas within h hours.

Example 1:
Input: piles = [3,6,7,11], h = 8
Output: 4

Example 2:
Input: piles = [30,11,23,4,20], h = 5
Output: 30

Example 3:
Input: piles = [30,11,23,4,20], h = 6
Output: 23

Constraints:
- 1 <= piles.length <= 10^4
- piles.length <= h <= 10^9
- 1 <= piles[i] <= 10^9
"""

from typing import List
from interview_workbook.leetcode._registry import register_problem
import math


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        """
        Find minimum eating speed using binary search.

        Time: O(n * log(max(piles))) where n is number of piles
        Space: O(1)

        Algorithm:
        1. Binary search on eating speed k from 1 to max(piles)
        2. For each speed k, calculate total hours needed
        3. If hours <= h, try smaller speed; otherwise try larger speed
        """

        def hours_needed(speed: int) -> int:
            """Calculate total hours needed at given eating speed"""
            total_hours = 0
            for pile in piles:
                # Ceiling division: (pile + speed - 1) // speed
                total_hours += math.ceil(pile / speed)
            return total_hours

        # Binary search on eating speed
        left, right = 1, max(piles)

        while left < right:
            mid = left + (right - left) // 2
            hours = hours_needed(mid)

            if hours <= h:
                right = mid  # Try smaller speed
            else:
                left = mid + 1  # Need faster speed

        return left

    def minEatingSpeedOptimized(self, piles: List[int], h: int) -> int:
        """
        Optimized version with better bounds.

        Time: O(n * log(sum/h)) where n is number of piles
        Space: O(1)
        """

        def hours_needed(speed: int) -> int:
            return sum(math.ceil(pile / speed) for pile in piles)

        # Optimized bounds: minimum possible is total_bananas / h
        total_bananas = sum(piles)
        left = math.ceil(total_bananas / h)
        right = max(piles)

        while left < right:
            mid = left + (right - left) // 2
            if hours_needed(mid) <= h:
                right = mid
            else:
                left = mid + 1

        return left


def demo():
    """Demo of Koko Eating Bananas."""
    solution = Solution()

    test_cases = [
        {
            "piles": [3, 6, 7, 11],
            "h": 8,
            "expected": 4,
            "explanation": "Speed 4: ceil(3/4) + ceil(6/4) + ceil(7/4) + ceil(11/4) = 1+2+2+3 = 8",
        },
        {
            "piles": [30, 11, 23, 4, 20],
            "h": 5,
            "expected": 30,
            "explanation": "Need to eat fastest pile in 1 hour",
        },
        {
            "piles": [30, 11, 23, 4, 20],
            "h": 6,
            "expected": 23,
            "explanation": "Speed 23: 2+1+1+1+1 = 6 hours",
        },
        {
            "piles": [312884470],
            "h": 312884469,
            "expected": 2,
            "explanation": "Large single pile test case",
        },
        {"piles": [1, 1, 1, 1], "h": 4, "expected": 1, "explanation": "Minimum speed of 1"},
    ]

    print("=== LeetCode 875: Koko Eating Bananas ===\n")

    for i, test in enumerate(test_cases, 1):
        piles = test["piles"]
        h = test["h"]
        expected = test["expected"]
        explanation = test["explanation"]

        print(f"Test Case {i}:")
        print(f"Piles: {piles}")
        print(f"Hours: {h}")
        print(f"Expected: {expected}")
        print(f"Explanation: {explanation}")

        # Test standard solution
        result = solution.minEatingSpeed(piles, h)
        print(f"Result (Standard): {result}")
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"Status: {status}")

        # Test optimized solution
        result_opt = solution.minEatingSpeedOptimized(piles, h)
        print(f"Result (Optimized): {result_opt}")

        # Verify the solution works
        def verify_speed(speed: int) -> bool:
            total_hours = sum(math.ceil(pile / speed) for pile in piles)
            return total_hours <= h

        is_valid = verify_speed(result)
        print(f"Verification: {'✓ Valid' if is_valid else '✗ Invalid'}")
        print()


if __name__ == "__main__":
    demo()


# Register the problem
register_problem(
    id="875",
    title="Koko Eating Bananas",
    difficulty="Medium",
    category="Binary Search",
    url="https://leetcode.com/problems/koko-eating-bananas/",
    tags=["Array", "Binary Search"],
    module_path="interview_workbook.leetcode.binary_search.koko_eating_bananas",
)
