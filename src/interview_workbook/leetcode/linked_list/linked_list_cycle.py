"""
Linked List Cycle

TODO: Add problem description
"""


class Solution:
    def solve(self, *args):
        """
        Detect if linked list has a cycle.
        Args: head (ListNode)
        Returns: bool
        """
        head = args[0]
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="linked_list_cycle",
#     title="Linked List Cycle",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
