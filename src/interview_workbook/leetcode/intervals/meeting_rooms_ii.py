"""
Meeting Rooms Ii

TODO: Add problem description
"""


class Solution:
    def solve(self, *args):
        """
        Meeting Rooms II: Minimum meeting rooms required.
        Args:
            intervals (List[List[int]])
        Returns:
            int
        """
        intervals, = args
        if not intervals:
            return 0
        starts = sorted([i[0] for i in intervals])
        ends = sorted([i[1] for i in intervals])
        s = e = 0
        rooms = available = 0
        while s < len(intervals):
            if starts[s] < ends[e]:
                if available == 0:
                    rooms += 1
                else:
                    available -= 1
                s += 1
            else:
                available += 1
                e += 1
        return rooms


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="meeting_rooms_ii",
#     title="Meeting Rooms Ii",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
