"""
LeetCode 543: Diameter of Binary Tree
https://leetcode.com/problems/diameter-of-binary-tree/

Given the root of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.

The length of a path between two nodes is represented by the number of edges between them.

Constraints:
- The number of nodes in the tree is in the range [1, 10^4]
- -100 <= Node.val <= 100
"""

from typing import Optional
from collections import deque
from .._types import Category
from .._registry import register_problem
from .._nodes import TreeNode


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """
        Find diameter using DFS with height calculation.

        Key insight: diameter is the maximum of:
        1. Diameter of left subtree
        2. Diameter of right subtree
        3. Longest path through root (left_height + right_height)

        Time: O(n) - visit each node once
        Space: O(h) - recursion stack, h = height of tree
        """
        self.max_diameter = 0

        def height(node: Optional[TreeNode]) -> int:
            """Calculate height and update max diameter."""
            if not node:
                return 0

            left_height = height(node.left)
            right_height = height(node.right)

            # Update max diameter at this node
            # Diameter through this node = left_height + right_height
            diameter_through_node = left_height + right_height
            self.max_diameter = max(self.max_diameter, diameter_through_node)

            # Return height of this subtree
            return 1 + max(left_height, right_height)

        height(root)
        return self.max_diameter

    def diameterOfBinaryTreeClean(self, root: Optional[TreeNode]) -> int:
        """
        Cleaner version without instance variable.

        Time: O(n) - visit each node once
        Space: O(h) - recursion stack
        """

        def dfs(node: Optional[TreeNode]) -> tuple[int, int]:
            """Return (height, diameter) for subtree rooted at node."""
            if not node:
                return 0, 0

            left_height, left_diameter = dfs(node.left)
            right_height, right_diameter = dfs(node.right)

            # Height of current node
            height = 1 + max(left_height, right_height)

            # Diameter could be:
            # 1. Left subtree diameter
            # 2. Right subtree diameter
            # 3. Path through current node (left_height + right_height)
            diameter = max(left_diameter, right_diameter, left_height + right_height)

            return height, diameter

        _, diameter = dfs(root)
        return diameter

    def diameterOfBinaryTreeIterative(self, root: Optional[TreeNode]) -> int:
        """
        Iterative approach using post-order traversal.

        Time: O(n) - visit each node once
        Space: O(h) - stack space
        """
        if not root:
            return 0

        stack = [(root, False)]
        heights = {}  # node -> height
        max_diameter = 0

        while stack:
            node, visited = stack.pop()

            if visited:
                # Post-order processing: both children processed
                left_height = heights.get(node.left, 0)
                right_height = heights.get(node.right, 0)

                # Calculate height of current node
                heights[node] = 1 + max(left_height, right_height)

                # Update max diameter
                diameter_through_node = left_height + right_height
                max_diameter = max(max_diameter, diameter_through_node)

            else:
                # Pre-order: mark as visited and add children
                stack.append((node, True))

                if node.right:
                    stack.append((node.right, False))
                if node.left:
                    stack.append((node.left, False))

        return max_diameter


def demo():
    """Demonstrate diameter calculation with comprehensive test cases."""
    solution = Solution()

    def list_to_tree(vals: list) -> Optional[TreeNode]:
        """Convert level-order list to tree for testing."""
        if not vals:
            return None

        root = TreeNode(vals[0])
        queue = deque([root])
        i = 1

        while queue and i < len(vals):
            node = queue.popleft()

            if i < len(vals) and vals[i] is not None:
                node.left = TreeNode(vals[i])
                queue.append(node.left)
            i += 1

            if i < len(vals) and vals[i] is not None:
                node.right = TreeNode(vals[i])
                queue.append(node.right)
            i += 1

        return root

    test_cases = [
        {
            "name": "Example 1: balanced tree",
            "input": [1, 2, 3, 4, 5],
            "expected": 3,
            "explanation": "Path: 4 -> 2 -> 1 -> 3 (3 edges)",
        },
        {
            "name": "Example 2: single node",
            "input": [1],
            "expected": 0,
            "explanation": "No edges in single node",
        },
        {
            "name": "Left skewed tree",
            "input": [1, 2, None, 3, None, 4],
            "expected": 3,
            "explanation": "Path: 4 -> 3 -> 2 -> 1 (3 edges)",
        },
        {
            "name": "Right skewed tree",
            "input": [1, None, 2, None, 3, None, 4],
            "expected": 3,
            "explanation": "Path: 1 -> 2 -> 3 -> 4 (3 edges)",
        },
        {
            "name": "Complete binary tree",
            "input": [1, 2, 3, 4, 5, 6, 7],
            "expected": 4,
            "explanation": "Path: 4 -> 2 -> 1 -> 3 -> 6 (4 edges)",
        },
        {
            "name": "Diameter through root",
            "input": [1, 2, 3, 4, 5, None, None, 6],
            "expected": 4,
            "explanation": "Path: 6 -> 4 -> 2 -> 1 -> 3 (4 edges)",
        },
        {
            "name": "Diameter not through root",
            "input": [1, 2, None, 3, 4, 5, None, 6],
            "expected": 3,
            "explanation": "Path: 6 -> 5 -> 3 -> 4 (3 edges)",
        },
        {
            "name": "Two node tree",
            "input": [1, 2],
            "expected": 1,
            "explanation": "Path: 1 -> 2 (1 edge)",
        },
        {
            "name": "Deep left subtree",
            "input": [1, 2, 3, 4, None, None, None, 5, None, 6],
            "expected": 4,
            "explanation": "Long path through left subtree",
        },
    ]

    print("=== LeetCode 543: Diameter of Binary Tree ===\n")

    for i, test in enumerate(test_cases, 1):
        root = list_to_tree(test["input"])
        result = solution.diameterOfBinaryTree(root)

        status = "✓ PASS" if result == test["expected"] else "✗ FAIL"
        print(f"Test Case {i}: {status}")
        print(f"  Description: {test['name']}")
        print(f"  Input: {test['input']}")
        print(f"  Expected: {test['expected']}")
        print(f"  Got: {result}")
        print(f"  Explanation: {test['explanation']}")

        if result != test["expected"]:
            print(f"  ❌ Mismatch!")
        print()

    # Test all approaches on a sample case
    print("Algorithm Comparison:")
    test_input = [1, 2, 3, 4, 5]
    expected = 3

    approaches = [
        ("DFS with instance var", solution.diameterOfBinaryTree),
        ("DFS clean (return tuple)", solution.diameterOfBinaryTreeClean),
        ("Iterative post-order", solution.diameterOfBinaryTreeIterative),
    ]

    for name, method in approaches:
        root = list_to_tree(test_input)
        result = method(root)
        status = "✓" if result == expected else "✗"
        print(f"  {name}: {status} (diameter = {result})")

    print(f"\nComplexity Analysis:")
    print(f"  Time: O(n) - visit every node exactly once")
    print(f"  Space: O(h) - recursion/stack depth")
    print(f"    Best case (balanced): O(log n)")
    print(f"    Worst case (skewed): O(n)")

    print(f"\nKey Insights:")
    print(f"  • Diameter = longest path between any two nodes")
    print(f"  • Path may or may not pass through root")
    print(f"  • At each node, consider diameter through that node")
    print(f"  • Diameter through node = left_height + right_height")
    print(f"  • Global diameter = max over all nodes")
    print(f"  • Can combine height calculation with diameter tracking")


# Register the problem
register_problem(
    id=543,
    slug="diameter_of_binary_tree",
    title="Diameter of Binary Tree",
    category=Category.TREES,
    difficulty="Easy",
    tags=["tree", "dfs", "binary-tree", "recursion"],
    url="https://leetcode.com/problems/diameter-of-binary-tree/",
)


if __name__ == "__main__":
    demo()
