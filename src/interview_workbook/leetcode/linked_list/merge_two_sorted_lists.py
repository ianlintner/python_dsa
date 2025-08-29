"""
Merge Two Sorted Lists

TODO: Add problem description
"""


class Solution:
    def solve(self, *args):
        """
        Merge two sorted linked lists.
        Args: l1, l2 (ListNode)
        Returns: ListNode head
        """
        l1, l2 = args
        dummy = ListNode(0)
        curr = dummy
        while l1 and l2:
            if l1.val <= l2.val:
                curr.next = l1
                l1 = l1.next
            else:
                curr.next = l2
                l2 = l2.next
            curr = curr.next
        curr.next = l1 if l1 else l2
        return dummy.next


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="merge_two_sorted_lists",
#     title="Merge Two Sorted Lists",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
