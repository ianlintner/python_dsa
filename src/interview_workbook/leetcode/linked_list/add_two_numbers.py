"""
Add Two Numbers

Problem: Add Two Numbers
LeetCode link: https://leetcode.com/problems/add-two-numbers/
Description: Add two numbers represented as linked lists and return head of result list.
"""

from src.interview_workbook.leetcode._nodes import ListNode
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """
        Add two numbers represented by linked lists.
        Args: l1, l2 (ListNode)
        Returns: ListNode (head of result list)
        """
        l1, l2 = args
        dummy = ListNode(0)
        curr = dummy
        carry = 0
        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0
            s = val1 + val2 + carry
            carry = s // 10
            curr.next = ListNode(s % 10)
            curr = curr.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return dummy.next


def demo():
    """TODO: Implement demo function."""
    pass


register_problem(
    id=2,
    slug="add_two_numbers",
    title="Add Two Numbers",
    category=Category.LINKED_LIST,
    difficulty=Difficulty.MEDIUM,
    tags=["linked_list", "math"],
    url="https://leetcode.com/problems/add-two-numbers/",
    notes="",
)
