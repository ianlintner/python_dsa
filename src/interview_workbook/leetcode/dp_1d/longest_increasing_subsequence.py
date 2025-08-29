"""
Longest Increasing Subsequence

TODO: Add problem description
"""


class Solution:
    def solve(self, *args) -> int:
        """Return the length of the longest increasing subsequence."""
        if not args:
            return 0
        nums = args[0]
        import bisect
        sub = []
        for x in nums:
            i = bisect.bisect_left(sub, x)
            if i == len(sub):
                sub.append(x)
            else:
                sub[i] = x
        return len(sub)


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="longest_increasing_subsequence",
#     title="Longest Increasing Subsequence",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
