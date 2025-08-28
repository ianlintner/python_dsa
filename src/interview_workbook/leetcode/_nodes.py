"""
Shared node types for LeetCode problems.

These classes provide consistent data structures for linked list and tree problems,
with convenience methods for converting between Python data structures.
"""

from __future__ import annotations

from typing import List, Optional


class ListNode:
    """Definition for singly-linked list."""

    def __init__(self, val: int = 0, next: Optional[ListNode] = None):
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        """String representation of the linked list."""
        values = []
        current = self
        seen = set()  # Detect cycles

        while current and current not in seen:
            seen.add(current)
            values.append(str(current.val))
            current = current.next

        if current:  # Cycle detected
            values.append("...")

        return " -> ".join(values)

    def __eq__(self, other) -> bool:
        """Compare two linked lists for equality."""
        if not isinstance(other, ListNode):
            return False

        current1, current2 = self, other
        while current1 and current2:
            if current1.val != current2.val:
                return False
            current1, current2 = current1.next, current2.next

        return current1 is None and current2 is None

    def to_list(self) -> List[int]:
        """Convert linked list to Python list."""
        result = []
        current = self
        seen = set()  # Detect cycles

        while current and current not in seen:
            seen.add(current)
            result.append(current.val)
            current = current.next

        return result

    @classmethod
    def from_list(cls, values: List[int]) -> Optional[ListNode]:
        """Create linked list from Python list."""
        if not values:
            return None

        head = cls(values[0])
        current = head

        for val in values[1:]:
            current.next = cls(val)
            current = current.next

        return head


class TreeNode:
    """Definition for a binary tree node."""

    def __init__(
        self, val: int = 0, left: Optional[TreeNode] = None, right: Optional[TreeNode] = None
    ):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """String representation of the tree (level-order)."""
        if not self:
            return "[]"

        result = []
        queue = [self]

        while queue:
            node = queue.pop(0)
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("null")

        # Remove trailing nulls
        while result and result[-1] == "null":
            result.pop()

        return f"[{', '.join(result)}]"

    def __eq__(self, other) -> bool:
        """Compare two trees for structural and value equality."""
        if not isinstance(other, TreeNode):
            return False

        if self is None and other is None:
            return True
        if self is None or other is None:
            return False
        if self.val != other.val:
            return False

        return self.left == other.left and self.right == other.right

    def to_list(self) -> List[Optional[int]]:
        """Convert tree to level-order list representation."""
        if not self:
            return []

        result = []
        queue = [self]

        while queue:
            node = queue.pop(0)
            if node:
                result.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append(None)

        # Remove trailing None values
        while result and result[-1] is None:
            result.pop()

        return result

    @classmethod
    def from_list(cls, values: List[Optional[int]]) -> Optional[TreeNode]:
        """Create binary tree from level-order list representation."""
        if not values or values[0] is None:
            return None

        root = cls(values[0])
        queue = [root]
        i = 1

        while queue and i < len(values):
            node = queue.pop(0)

            # Left child
            if i < len(values) and values[i] is not None:
                node.left = cls(values[i])
                queue.append(node.left)
            i += 1

            # Right child
            if i < len(values) and values[i] is not None:
                node.right = cls(values[i])
                queue.append(node.right)
            i += 1

        return root

    def inorder(self) -> List[int]:
        """Return inorder traversal of the tree."""
        result = []
        self._inorder_helper(result)
        return result

    def _inorder_helper(self, result: List[int]) -> None:
        """Helper for inorder traversal."""
        if self:
            if self.left:
                self.left._inorder_helper(result)
            result.append(self.val)
            if self.right:
                self.right._inorder_helper(result)

    def preorder(self) -> List[int]:
        """Return preorder traversal of the tree."""
        result = []
        self._preorder_helper(result)
        return result

    def _preorder_helper(self, result: List[int]) -> None:
        """Helper for preorder traversal."""
        if self:
            result.append(self.val)
            if self.left:
                self.left._preorder_helper(result)
            if self.right:
                self.right._preorder_helper(result)

    def postorder(self) -> List[int]:
        """Return postorder traversal of the tree."""
        result = []
        self._postorder_helper(result)
        return result

    def _postorder_helper(self, result: List[int]) -> None:
        """Helper for postorder traversal."""
        if self:
            if self.left:
                self.left._postorder_helper(result)
            if self.right:
                self.right._postorder_helper(result)
            result.append(self.val)


# Convenience functions for common operations
def create_linked_list(values: List[int]) -> Optional[ListNode]:
    """Create a linked list from a list of values."""
    return ListNode.from_list(values)


def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    """Convert a linked list to a Python list."""
    return head.to_list() if head else []


def create_binary_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Create a binary tree from a level-order list."""
    return TreeNode.from_list(values)


def binary_tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """Convert a binary tree to a level-order list."""
    return root.to_list() if root else []


def create_cycle(head: Optional[ListNode], pos: int) -> Optional[ListNode]:
    """
    Create a cycle in the linked list by connecting the tail to the node at position pos.
    pos = -1 means no cycle.
    """
    if not head or pos == -1:
        return head

    # Find the node at position pos and the tail
    nodes = []
    current = head
    while current:
        nodes.append(current)
        current = current.next

    if pos >= len(nodes):
        return head  # Invalid position

    # Create cycle by connecting tail to node at pos
    if nodes:
        nodes[-1].next = nodes[pos]

    return head


def detect_cycle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Detect if there's a cycle in the linked list using Floyd's algorithm.
    Returns the node where the cycle begins, or None if no cycle.
    """
    if not head or not head.next:
        return None

    slow = fast = head

    # Phase 1: Detect if cycle exists
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle

    # Phase 2: Find start of cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow
