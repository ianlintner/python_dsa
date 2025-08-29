"""
Climbing Stairs

TODO: Add problem description
"""


class Solution:
    def solve(self, *args) -> int:
        """Return the number of distinct ways to climb n stairs (1 or 2 steps at a time)."""
        if not args:
            return 0
        n = args[0]
        if n <= 2:
            return n
        prev, curr = 1, 2
        for _ in range(3, n + 1):
            prev, curr = curr, prev + curr
        return curr


def demo():
    """Run a demo for the Climbing Stairs problem."""
    solver = Solution()
    n = 5
    result = solver.solve(n)
    return str(result)


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="climbing_stairs",
#     title="Climbing Stairs",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
