"""
Invert Binary Tree

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, root):
        """
        Invert a binary tree (mirror it).
        """
        if not root:
            return None
        root.left, root.right = self.solve(root.right), self.solve(root.left)
        return root


def demo():
    """Run a simple demonstration of invert binary tree with BFS before/after."""
    import random

    random.seed(0)

    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    # Build tree:
    #        4
    #       / \
    #      2   7
    #     / \ / \
    #    1  3 6  9
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(7)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(9)

    def bfs(node):
        if not node:
            return []
        res = []
        queue = [node]
        while queue:
            curr = queue.pop(0)
            res.append(curr.val)
            if curr.left:
                queue.append(curr.left)
            if curr.right:
                queue.append(curr.right)
        return res

    before = bfs(root)
    Solution().solve(root)
    after = bfs(root)
    return f"Before: {before}, After: {after}"


register_problem(
    id=226,
    slug="invert_binary_tree",
    title="Invert Binary Tree",
    category=Category.TREES,
    difficulty=Difficulty.EASY,
    tags=["tree", "binary_tree", "dfs", "bfs"],
    url="https://leetcode.com/problems/invert-binary-tree/",
    notes="",
)
