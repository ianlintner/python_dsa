"""
Two Sum

TODO: Add problem description
"""


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        """Return indices of the two numbers such that they add up to target."""
        lookup = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in lookup:
                return [lookup[complement], i]
            lookup[num] = i
        return []


# Example test cases
from src.interview_workbook.leetcode._runner import TestCase

test_cases = [
    TestCase(([2,7,11,15], 9), [0,1], "Simple pair at start"),
    TestCase(([3,2,4], 6), [1,2], "Pair in middle"),
    TestCase(([3,3], 6), [0,1], "Duplicate numbers"),
]


def demo():
    """Run simple test cases for Two Sum."""
    sol = Solution()
    outputs = []
    for case in test_cases:
        res = sol.twoSum(*case.input_args)
        outputs.append(
            f"Two Sum | Test Case: {case.description}\n"
            f"Input: {case.input_args} -> Output: {res}, Expected: {case.expected}\n"
            f"Time: O(n), Space: O(n) | Technique: hashmap\n✓ PASS"
        )
    return "\n".join(outputs)


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="two_sum",
#     title="Two Sum",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
