"""
 Nodes

TODO: Add problem description
"""

from typing import Optional


class TreeNode:
    """Binary tree node class used in tree-related problems."""

    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right


class ListNode:
    """Linked list node class used in linked list problems."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next
