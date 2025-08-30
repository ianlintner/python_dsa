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
    """TODO: Implement demo function."""
    pass


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
