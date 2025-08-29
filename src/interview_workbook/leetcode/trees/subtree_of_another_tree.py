"""
Subtree Of Another Tree

TODO: Add problem description
"""


class Solution:
    def solve(self, *args) -> bool:
        """Check if subRoot is a subtree of root using DFS."""
        if len(args) < 2:
            return False
        root, subRoot = args[0], args[1]

        def is_same(t1, t2):
            if not t1 and not t2:
                return True
            if not t1 or not t2:
                return False
            return (
                t1.val == t2.val
                and is_same(t1.left, t2.left)
                and is_same(t1.right, t2.right)
            )

        def dfs(node):
            if not node:
                return False
            if is_same(node, subRoot):
                return True
            return dfs(node.left) or dfs(node.right)

        return dfs(root)


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="subtree_of_another_tree",
#     title="Subtree Of Another Tree",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
