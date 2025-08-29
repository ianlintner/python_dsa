"""
Reverse Linked List

Problem: Reverse Linked List
LeetCode link: https://leetcode.com/problems/reverse-linked-list/
Description: Reverse a singly linked list and return the reversed list.
"""


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


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="reverse_linked_list",
#     title="Reverse Linked List",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
