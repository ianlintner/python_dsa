"""
Binary Tree Level Order Traversal

TODO: Add problem description
"""


class Solution:
    def solve(self, *args) -> list[list[int]]:
        """Return the level order traversal of a binary tree using BFS."""
        if not args or args[0] is None:
            return []
        root = args[0]
        from collections import deque
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


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="binary_tree_level_order_traversal",
#     title="Binary Tree Level Order Traversal",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
