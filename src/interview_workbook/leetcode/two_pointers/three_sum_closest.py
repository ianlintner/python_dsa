"""
Three Sum Closest

TODO: Add problem description
"""


class Solution:
    def solve(self, *args):
        """Finds the sum of three integers closest to target."""
        nums, target = args
        nums.sort()
        closest = float("inf")
        res = None
        for i in range(len(nums) - 2):
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if abs(s - target) < closest:
                    closest = abs(s - target)
                    res = s
                if s < target:
                    l += 1
                elif s > target:
                    r -= 1
                else:
                    return s
        return res


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="three_sum_closest",
#     title="Three Sum Closest",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
