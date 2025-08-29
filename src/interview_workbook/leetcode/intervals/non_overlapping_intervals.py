"""
Non Overlapping Intervals

TODO: Add problem description
"""


class Solution:
    def solve(self, *args):
        """
        Non-overlapping Intervals: Minimum to remove to avoid overlap.
        Args:
            intervals (List[List[int]])
        Returns:
            int
        """
        intervals, = args
        if not intervals:
            return 0
        intervals.sort(key=lambda x: x[1])
        count = 0
        prev_end = intervals[0][1]
        for i in range(1, len(intervals)):
            if intervals[i][0] < prev_end:
                count += 1
            else:
                prev_end = intervals[i][1]
        return count


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="non_overlapping_intervals",
#     title="Non Overlapping Intervals",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
