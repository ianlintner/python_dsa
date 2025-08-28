"""
LeetCode 100: Same Tree

Given the roots of two binary trees p and q, write a function to check if they
are the same or not.

Two binary trees are considered the same if they are structurally identical,
and the nodes have the same value.

Examples:
    Input: p = [1,2,3], q = [1,2,3]
    Output: true

    Input: p = [1,2], q = [1,null,2]
    Output: false

    Input: p = [1,2,1], q = [1,1,2]
    Output: false

Constraints:
    - The number of nodes in both trees is in the range [0, 100].
    - -10^4 <= Node.val <= 10^4

Time Complexity: O(min(m,n)) where m,n are the number of nodes in each tree
Space Complexity: O(min(m,n)) for recursion stack in worst case
"""

from collections import deque
from typing import Optional

from .._nodes import TreeNode
from .._registry import register_problem
from .._types import Category


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Approach 1: Recursive DFS comparison.
        """
        # Base cases
        if not p and not q:
            return True
        if not p or not q:
            return False

        # Check current nodes and recurse on children
        return (
            p.val == q.val and self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        )

    def isSameTree_iterative(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Approach 2: Iterative BFS using queue.
        """
        queue = deque([(p, q)])

        while queue:
            node1, node2 = queue.popleft()

            # Both are None - continue
            if not node1 and not node2:
                continue

            # One is None, other is not - different structure
            if not node1 or not node2:
                return False

            # Values are different
            if node1.val != node2.val:
                return False

            # Add children to queue for comparison
            queue.append((node1.left, node2.left))
            queue.append((node1.right, node2.right))

        return True

    def isSameTree_preorder(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Approach 3: Compare preorder serializations.
        """

        def serialize(root):
            if not root:
                return [None]
            return [root.val] + serialize(root.left) + serialize(root.right)

        return serialize(p) == serialize(q)

    def isSameTree_stack(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Approach 4: Iterative DFS using stack.
        """
        stack = [(p, q)]

        while stack:
            node1, node2 = stack.pop()

            if not node1 and not node2:
                continue

            if not node1 or not node2:
                return False

            if node1.val != node2.val:
                return False

            # Add children to stack (order matters for DFS)
            stack.append((node1.right, node2.right))
            stack.append((node1.left, node2.left))

        return True


def demo():
    """
    Demonstrate same tree checking with multiple approaches.
    """
    print("=== LeetCode 100: Same Tree ===\n")

    solution = Solution()

    # Helper function to create trees from lists
    def list_to_tree(arr):
        if not arr:
            return None

        nodes = [TreeNode(val) if val is not None else None for val in arr]
        kids = nodes[::-1]
        root = kids.pop()

        for node in nodes:
            if node:
                if kids:
                    node.left = kids.pop()
                if kids:
                    node.right = kids.pop()

        return root

    # Test cases
    test_cases = [
        # Same trees
        ([1, 2, 3], [1, 2, 3], True),
        # Different structure
        ([1, 2], [1, None, 2], False),
        # Different values
        ([1, 2, 1], [1, 1, 2], False),
        # Both empty
        ([], [], True),
        # One empty, one not
        ([1], [], False),
        # Single nodes same
        ([1], [1], True),
        # Single nodes different
        ([1], [2], False),
        # Complex same tree
        ([1, 2, 3, 4, 5, None, 6], [1, 2, 3, 4, 5, None, 6], True),
        # Complex different tree
        ([1, 2, 3, 4, 5, None, 6], [1, 2, 3, 4, None, 5, 6], False),
    ]

    for i, (tree1_list, tree2_list, expected) in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"Tree 1: {tree1_list}")
        print(f"Tree 2: {tree2_list}")
        print(f"Expected: {expected}")

        p = list_to_tree(tree1_list)
        q = list_to_tree(tree2_list)

        # Test all approaches
        result1 = solution.isSameTree(p, q)
        result2 = solution.isSameTree_iterative(p, q)
        result3 = solution.isSameTree_preorder(p, q)
        result4 = solution.isSameTree_stack(p, q)

        print(f"Recursive result: {result1}")
        print(f"BFS iterative result: {result2}")
        print(f"Preorder result: {result3}")
        print(f"DFS stack result: {result4}")

        # Verify all approaches give same result
        assert result1 == result2 == result3 == result4 == expected, f"Mismatch in test case {i}"
        print("✅ All approaches passed")
        print()

    print("Algorithm Analysis:")
    print("• Recursive: O(min(m,n)) time, O(min(m,n)) space")
    print("• BFS iterative: O(min(m,n)) time, O(min(m,n)) space")
    print("• Preorder serialization: O(m+n) time, O(m+n) space")
    print("• DFS stack: O(min(m,n)) time, O(min(m,n)) space")
    print("\nKey Insight:")
    print("• Two trees are the same if:")
    print("  1. Both have same structure (null positions)")
    print("  2. Corresponding nodes have same values")
    print("• Recursive solution is most intuitive and efficient")


# Register the problem
register_problem(
    id=100,
    slug="same_tree",
    title="Same Tree",
    category=Category.TREES,
    difficulty="Easy",
    tags=["tree", "dfs", "bfs", "binary-tree"],
    url="https://leetcode.com/problems/same-tree/",
)


if __name__ == "__main__":
    demo()
