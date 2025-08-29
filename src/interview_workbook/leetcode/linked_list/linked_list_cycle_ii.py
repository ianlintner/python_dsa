"""
Linked List Cycle Ii

TODO: Add problem description
"""


class Solution:
    def solve(self, *args):
        """
        Detect node where cycle begins.
        Args: head (ListNode)
        Returns: ListNode or None
        """
        head = args[0]
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        else:
            return None
        # reset one pointer to head
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        return slow


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="linked_list_cycle_ii",
#     title="Linked List Cycle Ii",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
