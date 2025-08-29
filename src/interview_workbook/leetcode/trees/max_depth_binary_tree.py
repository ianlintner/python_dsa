"""
Max Depth Binary Tree

TODO: Add problem description
"""


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
    return f"Max depth of binary tree: {depth}"


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="max_depth_binary_tree",
#     title="Max Depth Binary Tree",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
