"""
Linked List Cycle Ii

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


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
    """Run a simple demonstration for Linked List Cycle II problem."""
    from src.interview_workbook.leetcode._nodes import ListNode

    # Create a cycle list: 3 -> 2 -> 0 -> -4 -> back to 2
    n1, n2, n3, n4 = ListNode(3), ListNode(2), ListNode(0), ListNode(-4)
    n1.next, n2.next, n3.next, n4.next = n2, n3, n4, n2

    s = Solution()
    entry = s.solve(n1)
    return f"Cycle entry node value: {entry.val if entry else None}"


register_problem(
    id=142,
    slug="linked_list_cycle_ii",
    title="Linked List Cycle II",
    category=Category.LINKED_LIST,
    difficulty=Difficulty.MEDIUM,
    tags=["linked_list", "two_pointers"],
    url="https://leetcode.com/problems/linked-list-cycle-ii/",
    notes="",
)
