"""
Linked List Cycle

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


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


register_problem(
    id=141,
    slug="linked_list_cycle",
    title="Linked List Cycle",
    category=Category.LINKED_LIST,
    difficulty=Difficulty.EASY,
    tags=["linked_list", "two_pointers"],
    url="https://leetcode.com/problems/linked-list-cycle/",
    notes="",
)
