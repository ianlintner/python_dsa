"""
Same Tree (LeetCode 100)

Given two binary trees, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical
and the nodes have the same value.
"""


class Solution:
    def solve(self, *args) -> bool:
        """Check if two binary trees are the same using DFS recursion."""
        if len(args) < 2:
            return False
        p, q = args[0], args[1]

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

        return is_same(p, q)


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="same_tree",
#     title="Same Tree",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
