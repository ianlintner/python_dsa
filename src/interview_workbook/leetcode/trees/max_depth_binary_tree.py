"""
Max Depth Binary Tree

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, root) -> int:
        """
        Find the maximum depth of a binary tree.
        """
        if not root:
            return 0
        return 1 + max(self.solve(root.left), self.solve(root.right))


def demo():
    """Run a simple demonstration of max depth of binary tree."""

    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    # Build tree:
    #       1
    #      / \
    #     2   3
    #    /
    #   4
    root = TreeNode(1)
    root.left = TreeNode(2, TreeNode(4))
    root.right = TreeNode(3)

    sol = Solution()
    depth = sol.solve(root)
    print("Running demo for Max Depth of Binary Tree...")
    print(f"Max depth of binary tree: {depth}")
    return f"Max depth of binary tree: {depth}"


register_problem(
    id=104,
    slug="max_depth_binary_tree",
    title="Maximum Depth of Binary Tree",
    category=Category.TREES,
    difficulty=Difficulty.EASY,
    tags=["tree", "binary_tree", "dfs"],
    url="https://leetcode.com/problems/maximum-depth-of-binary-tree/",
    notes="",
)
