"""
Reorder List

TODO: Add problem description
"""


class Solution:
    def solve(self, *args):
        """
        Reorder list in-place L0→Ln→L1→Ln-1...
        Args: head (ListNode)
        Returns: None (modifies in-place)
        """
        head = args[0]
        if not head or not head.next:
            return head
        # find middle
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        # reverse second half
        prev, curr = None, slow.next
        slow.next = None
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        # merge two halves
        first, second = head, prev
        while second:
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first, second = tmp1, tmp2
        return head


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="reorder_list",
#     title="Reorder List",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
