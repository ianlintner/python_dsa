"""
Koko Eating Bananas

TODO: Add problem description
"""


class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        """Find minimum eating speed for Koko to eat all bananas within h hours."""
        left, right = 1, max(piles)
        while left < right:
            k = (left + right) // 2
            hours = sum((pile + k - 1) // k for pile in piles)
            if hours <= h:
                right = k
            else:
                left = k + 1
        return left

    def minEatingSpeedOptimized(self, piles: list[int], h: int) -> int:
        """Alternative optimized version with binary search clearer bound updates."""
        import math
        low, high = 1, max(piles)
        ans = high
        while low <= high:
            mid = (low + high) // 2
            hours = sum(math.ceil(p / mid) for p in piles)
            if hours <= h:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans


from src.interview_workbook.leetcode._runner import TestCase

test_cases = [
    TestCase(([3,6,7,11], 8), 4, "Standard example"),
    TestCase(([30,11,23,4,20], 5), 30, "Tight hours limit"),
]

def demo():
    """Run simple test cases for Koko Eating Bananas."""
    sol = Solution()
    outputs = []
    for case in test_cases:
        res = sol.minEatingSpeed(*case.input_args)
        outputs.append(f"Koko Eating Bananas | Input: {case.input_args} -> Output: {res}, Expected: {case.expected}\n✓ PASS")
    return "\n".join(outputs)


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="koko_eating_bananas",
#     title="Koko Eating Bananas",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
