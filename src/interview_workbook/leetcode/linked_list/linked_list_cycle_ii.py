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
    """TODO: Implement demo function."""
    pass


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
