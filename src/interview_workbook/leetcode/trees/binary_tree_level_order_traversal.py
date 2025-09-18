"""
Binary Tree Level Order Traversal

Given the root of a binary tree, return the level order traversal of its
nodes' values. (i.e., from left to right, level by level).
"""

from collections import deque

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class TreeNode:
    """Binary tree node."""

    def __init__(self, val: int = 0, left: "TreeNode" = None, right: "TreeNode" = None):
        self.val = val
        self.left = left
        self.right = right


def levelOrder(root: TreeNode) -> list[list[int]]:
    """Return the level order traversal of a binary tree using BFS."""
    if not root:
        return []

    result: list[list[int]] = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level: list[int] = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)

    return result


def demo() -> str:
    """Builds a sample tree and demonstrates level order traversal."""
    # Example tree: [3,9,20,None,None,15,7]
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20, TreeNode(15), TreeNode(7))
    print("Running demo for Binary Tree Level Order Traversal...")
    result = levelOrder(root)
    print(f"Level order traversal: {result}")
    return str(result)


register_problem(
    id=102,
    slug="binary_tree_level_order_traversal",
    title="Binary Tree Level Order Traversal",
    category=Category.TREES,
    difficulty=Difficulty.MEDIUM,
    tags=["tree", "binary_tree", "bfs"],
    url="https://leetcode.com/problems/binary-tree-level-order-traversal/",
    notes="",
)
