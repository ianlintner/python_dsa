"""
Reorder List

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


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
    """Run a simple demonstration for Reorder List problem."""
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
    head = build_list([1, 2, 3, 4])
    s.solve(head)
    return f"[1,2,3,4] -> {list_to_str(head)}"


register_problem(
    id=143,
    slug="reorder_list",
    title="Reorder List",
    category=Category.LINKED_LIST,
    difficulty=Difficulty.MEDIUM,
    tags=["linked_list", "two_pointers"],
    url="https://leetcode.com/problems/reorder-list/",
    notes="",
)
