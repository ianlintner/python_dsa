"""
Single Number

TODO: Add problem description
"""
import random

class Solution:
    def solve(self, nums: list[int]) -> int:
        """Return the element that appears only once in the array where every other element appears twice."""
        result = 0
        for num in nums:
            result ^= num
        return result




def demo() -> str:
    """Run a deterministic demo for Single Number."""
    random.seed(0)
    sol = Solution()
    test_values = [
        [2, 2, 1],
        [4, 1, 2, 1, 2],
        [1],
    ]
    results = {str(lst): sol.solve(lst) for lst in test_values}
    return str(results)


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="single_number",
#     title="Single Number",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
