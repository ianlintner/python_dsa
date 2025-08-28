"""
LeetCode 226: Invert Binary Tree
https://leetcode.com/problems/invert-binary-tree/

Given the root of a binary tree, invert the tree, and return its root.

Constraints:
- The number of nodes in the tree is in the range [0, 100]
- -100 <= Node.val <= 100
"""

from typing import Optional
from collections import deque
from .._types import Category
from .._registry import register_problem
from .._nodes import TreeNode


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Invert binary tree recursively.
        
        Time: O(n) - visit each node once
        Space: O(h) - recursion stack, h = height of tree
        """
        if not root:
            return None
        
        # Swap left and right children
        root.left, root.right = root.right, root.left
        
        # Recursively invert subtrees
        self.invertTree(root.left)
        self.invertTree(root.right)
        
        return root
    
    def invertTreeIterative(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Invert binary tree iteratively using stack.
        
        Time: O(n) - visit each node once
        Space: O(w) - queue space, w = maximum width
        """
        if not root:
            return None
        
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            
            # Swap children
            node.left, node.right = node.right, node.left
            
            # Add children to queue for processing
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return root
    
    def invertTreePreorder(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Invert using explicit preorder traversal with stack.
        
        Time: O(n) - visit each node once
        Space: O(h) - stack space
        """
        if not root:
            return None
            
        stack = [root]
        
        while stack:
            node = stack.pop()
            
            # Process current node - swap children
            node.left, node.right = node.right, node.left
            
            # Add children to stack (right first for preorder)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        
        return root


def demo():
    """Demonstrate invert binary tree with comprehensive test cases."""
    solution = Solution()
    
    def tree_to_list(root: Optional[TreeNode]) -> list:
        """Convert tree to level-order list for testing."""
        if not root:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            if node:
                result.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append(None)
        
        # Remove trailing None values
        while result and result[-1] is None:
            result.pop()
        
        return result
    
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
            "name": "Example 1: symmetric tree",
            "input": [4, 2, 7, 1, 3, 6, 9],
            "expected": [4, 7, 2, 9, 6, 3, 1]
        },
        {
            "name": "Example 2: simple tree",
            "input": [2, 1, 3],
            "expected": [2, 3, 1]
        },
        {
            "name": "Single node",
            "input": [1],
            "expected": [1]
        },
        {
            "name": "Empty tree",
            "input": [],
            "expected": []
        },
        {
            "name": "Left skewed tree",
            "input": [1, 2, None, 3],
            "expected": [1, None, 2, None, 3]
        },
        {
            "name": "Right skewed tree", 
            "input": [1, None, 2, None, 3],
            "expected": [1, 2, None, 3]
        },
        {
            "name": "Complete binary tree",
            "input": [1, 2, 3, 4, 5, 6, 7],
            "expected": [1, 3, 2, 7, 6, 5, 4]
        },
        {
            "name": "Tree with negative values",
            "input": [-1, -2, -3, -4, -5],
            "expected": [-1, -3, -2, None, -5, -4]
        }
    ]
    
    print("=== LeetCode 226: Invert Binary Tree ===\n")
    
    for i, test in enumerate(test_cases, 1):
        # Test recursive approach
        root = list_to_tree(test["input"])
        result_root = solution.invertTree(root)
        result = tree_to_list(result_root)
        
        status = "✓ PASS" if result == test["expected"] else "✗ FAIL"
        print(f"Test Case {i}: {status}")
        print(f"  Description: {test['name']}")
        print(f"  Input: {test['input']}")
        print(f"  Expected: {test['expected']}")
        print(f"  Got: {result}")
        
        if result != test["expected"]:
            print(f"  ❌ Mismatch!")
        print()
    
    # Test all approaches on a sample case
    print("Algorithm Comparison:")
    test_input = [4, 2, 7, 1, 3, 6, 9]
    expected = [4, 7, 2, 9, 6, 3, 1]
    
    approaches = [
        ("Recursive", solution.invertTree),
        ("Iterative BFS", solution.invertTreeIterative), 
        ("Iterative DFS", solution.invertTreePreorder)
    ]
    
    for name, method in approaches:
        root = list_to_tree(test_input)
        result_root = method(root)
        result = tree_to_list(result_root)
        status = "✓" if result == expected else "✗"
        print(f"  {name}: {status}")
    
    print(f"\nComplexity Analysis:")
    print(f"  Time: O(n) - must visit every node")
    print(f"  Space: O(h) - recursion depth or explicit stack")
    print(f"    Best case (balanced): O(log n)")
    print(f"    Worst case (skewed): O(n)")
    
    print(f"\nKey Insights:")
    print(f"  • Simple recursive solution: swap children then recurse")
    print(f"  • Iterative approaches use BFS (queue) or DFS (stack)")
    print(f"  • All approaches have same time complexity")
    print(f"  • Space complexity depends on tree height")


# Register the problem
register_problem(
    id=226,
    slug="invert_binary_tree",
    title="Invert Binary Tree",
    category=Category.TREES,
    difficulty="Easy",
    tags=["tree", "dfs", "bfs", "binary-tree"],
    url="https://leetcode.com/problems/invert-binary-tree/"
)


if __name__ == "__main__":
    demo()
