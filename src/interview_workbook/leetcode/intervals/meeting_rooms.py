"""
Meeting Rooms

TODO: Add problem description
"""


class Solution:
    def solve(self, *args):
        """
        Meeting Rooms: Check if a person can attend all meetings.
        Args:
            intervals (List[List[int]])
        Returns:
            bool
        """
        intervals, = args
        intervals.sort(key=lambda x: x[0])
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i-1][1]:
                return False
        return True


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="meeting_rooms",
#     title="Meeting Rooms",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
