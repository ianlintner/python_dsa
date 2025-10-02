"""LeetCode 572: Subtree of Another Tree

Check if one binary tree is a subtree of another.
"""

from typing import Optional

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class TreeNode:
    """Basic binary tree node."""

    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right


def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    """Helper to check if two trees are structurally identical."""
    if not p and not q:
        return True
    if not p or not q:
        return False
    return (
        p.val == q.val
        and is_same_tree(p.left, q.left)
        and is_same_tree(p.right, q.right)
    )


def isSubtree(root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
    """Check if subRoot is a subtree of root."""
    if not subRoot:
        return True
    if not root:
        return False
    if is_same_tree(root, subRoot):
        return True
    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)


def demo() -> str:
    """Deterministic demo for subtree check."""
    # Build main tree: [3,4,5,1,2]
    root = TreeNode(3)
    root.left = TreeNode(4)
    root.right = TreeNode(5)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(2)

    # Build subtree: [4,1,2]
    sub = TreeNode(4)
    sub.left = TreeNode(1)
    sub.right = TreeNode(2)

    result = isSubtree(root, sub)
    print("Running demo for Subtree of Another Tree...")
    print(f"Is subtree: {result}")
    return str(result)


# Register problem metadata
register_problem(
    id=572,
    slug="subtree_of_another_tree",
    title="Subtree of Another Tree",
    difficulty=Difficulty.EASY,
    category=Category.TREES,
    url="https://leetcode.com/problems/subtree-of-another-tree/",
    tags=["Tree", "Binary Tree"],
)
