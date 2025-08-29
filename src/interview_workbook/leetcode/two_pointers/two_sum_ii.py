"""
Two Sum Ii

TODO: Add problem description
"""


class Solution:
    def solve(self, *args):
        """Finds indices of two numbers whose sum equals target using two pointers."""
        numbers, target = args
        l, r = 0, len(numbers) - 1
        while l < r:
            s = numbers[l] + numbers[r]
            if s == target:
                return [l + 1, r + 1]
            elif s < target:
                l += 1
            else:
                r -= 1
        return []


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="two_sum_ii",
#     title="Two Sum Ii",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
