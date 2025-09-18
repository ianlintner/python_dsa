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
    """Run a simple demonstration for Linked List Cycle problem."""
    from src.interview_workbook.leetcode._nodes import ListNode

    # Create a cycle list: 3 -> 2 -> 0 -> -4 -> back to 2
    n1, n2, n3, n4 = ListNode(3), ListNode(2), ListNode(0), ListNode(-4)
    n1.next, n2.next, n3.next, n4.next = n2, n3, n4, n2
    print("Created linked list with cycle at node with value 2")
    s = Solution()
    result = s.solve(n1)
    print(f"Cycle detected: {result}")
    return f"Cycle detected: {result}"


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
