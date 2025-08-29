"""
Merge Intervals

Problem: Merge Intervals
LeetCode link: https://leetcode.com/problems/merge-intervals/
Description: Given an array of intervals where intervals[i] = [start, end], merge all overlapping intervals and return an array of non-overlapping intervals covering all the input intervals.
"""


class Solution:
    def solve(self, *args):
        """
        Merge Intervals: Merge overlapping intervals.
        Args:
            intervals (List[List[int]])
        Returns:
            List[List[int]]
        """
        intervals, = args
        if not intervals:
            return []
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]
        for start, end in intervals[1:]:
            if start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return merged


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="merge_intervals",
#     title="Merge Intervals",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
