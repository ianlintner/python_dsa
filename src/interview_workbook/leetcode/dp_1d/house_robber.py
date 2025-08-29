"""
House Robber

TODO: Add problem description
"""


class Solution:
    def solve(self, *args) -> int:
        """Return the maximum amount you can rob without robbing adjacent houses."""
        if not args:
            return 0
        nums = args[0]
        rob1, rob2 = 0, 0
        for n in nums:
            new_rob = max(rob2, rob1 + n)
            rob1, rob2 = rob2, new_rob
        return rob2


def demo():
    """Run a demo for the House Robber problem."""
    solver = Solution()
    nums = [1, 2, 3, 1]
    result = solver.solve(nums)
    return str(result)


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="house_robber",
#     title="House Robber",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
