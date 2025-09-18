"""
Reverse Linked List

Problem: Reverse Linked List
LeetCode link: https://leetcode.com/problems/reverse-linked-list/
Description: Reverse a singly linked list and return the reversed list.
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """
        Reverse a linked list.
        Args: head (ListNode)
        Returns: ListNode head
        """
        head = args[0]
        prev, curr = None, head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev


def demo():
    """Run a simple demonstration for Reverse Linked List problem."""
    from src.interview_workbook.leetcode._nodes import ListNode

    def build_list(nums):
        dummy = ListNode(0)
        curr = dummy
        for n in nums:
            curr.next = ListNode(n)
            curr = curr.next
        return dummy.next

    def list_to_str(node):
        vals = []
        while node:
            vals.append(str(node.val))
            node = node.next
        return "->".join(vals)

    s = Solution()
    head = build_list([1,2,3,4,5])
    result = s.solve(head)
    return f"[1,2,3,4,5] -> {list_to_str(result)}"


register_problem(
    id=206,
    slug="reverse_linked_list",
    title="Reverse Linked List",
    category=Category.LINKED_LIST,
    difficulty=Difficulty.EASY,
    tags=["linked_list"],
    url="https://leetcode.com/problems/reverse-linked-list/",
    notes="",
)
