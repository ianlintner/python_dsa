"""
Sliding Window Maximum

TODO: Add problem description
"""


from collections import deque

class Solution:
    def solve(self, *args):
        """Return list of max values in each sliding window."""
        nums, k = args
        if not nums or k == 0:
            return []
        q = deque()
        res = []
        for i, n in enumerate(nums):
            while q and q[0] <= i - k:
                q.popleft()
            while q and nums[q[-1]] < n:
                q.pop()
            q.append(i)
            if i >= k - 1:
                res.append(nums[q[0]])
        return res


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="sliding_window_maximum",
#     title="Sliding Window Maximum",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
