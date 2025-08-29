"""
Remove Nth Node From End

TODO: Add problem description
"""


from src.interview_workbook.leetcode._nodes import ListNode
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty

class Solution:
    def solve(self, *args):
        """Removes the nth node from end using two pointers and returns head."""
        head, n = args
        dummy = ListNode(0, head)
        first = second = dummy
        # Advance first by n+1 steps
        for _ in range(n + 1):
            first = first.next
        # Move both until first reaches end
        while first:
            first = first.next
            second = second.next
        # Remove node
        second.next = second.next.next
        return dummy.next


def demo():
    """Builds a linked list [1,2,3,4,5], removes 2nd from end, returns list as str."""
    # Build linked list
    head = ListNode(1)
    current = head
    for i in range(2, 6):
        current.next = ListNode(i)
        current = current.next

    # Remove nth node
    solver = Solution()
    new_head = solver.solve(head, 2)

    # Convert to list string
    result = []
    while new_head:
        result.append(str(new_head.val))
        new_head = new_head.next

    return "[" + ",".join(result) + "]"


register_problem(
    id=19,
    slug="remove-nth-node-from-end-of-list",
    title="Remove Nth Node From End of List",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.MEDIUM,
    tags=["Linked List", "Two Pointers"],
    url="https://leetcode.com/problems/remove-nth-node-from-end-of-list/",
)
