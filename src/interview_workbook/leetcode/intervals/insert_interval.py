"""
Insert Interval

TODO: Add problem description
"""


class Solution:
    def solve(self, *args):
        """
        Insert Interval: Given intervals and a new interval, insert and merge.
        Args:
            intervals (List[List[int]]), newInterval (List[int])
        Returns:
            List[List[int]]
        """
        intervals, newInterval = args
        res = []
        i = 0
        n = len(intervals)
        # add all intervals ending before newInterval starts
        while i < n and intervals[i][1] < newInterval[0]:
            res.append(intervals[i])
            i += 1
        # merge overlapping intervals
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        res.append(newInterval)
        # add the rest
        while i < n:
            res.append(intervals[i])
            i += 1
        return res


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="insert_interval",
#     title="Insert Interval",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
