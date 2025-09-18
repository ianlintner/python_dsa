"""
Merge Two Sorted Lists

Problem: Merge Two Sorted Lists
LeetCode link: https://leetcode.com/problems/merge-two-sorted-lists/
Description: Merge two sorted linked lists and return the merged list.
"""

from src.interview_workbook.leetcode._nodes import ListNode
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


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
    """Run a simple demonstration for Merge Two Sorted Lists problem."""
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
    l1 = build_list([1, 2, 4])
    l2 = build_list([1, 3, 4])
    result = s.solve(l1, l2)
    return f"[1,2,4] + [1,3,4] -> {list_to_str(result)}"


register_problem(
    id=21,
    slug="merge_two_sorted_lists",
    title="Merge Two Sorted Lists",
    category=Category.LINKED_LIST,
    difficulty=Difficulty.EASY,
    tags=["linked_list"],
    url="https://leetcode.com/problems/merge-two-sorted-lists/",
    notes="",
)
