"""
Trees - NeetCode Top 100 LeetCode Problems

Binary tree traversal, validation, and manipulation algorithms.
Focus on recursive and iterative approaches to common tree problems.

Problems in this category:
1. LeetCode 226: Invert Binary Tree (Easy)
2. LeetCode 104: Maximum Depth of Binary Tree (Easy)  
3. LeetCode 543: Diameter of Binary Tree (Easy)
4. LeetCode 110: Balanced Binary Tree (Easy)
5. LeetCode 100: Same Tree (Easy)
6. LeetCode 572: Subtree of Another Tree (Easy)
7. LeetCode 98: Validate Binary Search Tree (Medium)
8. LeetCode 102: Binary Tree Level Order Traversal (Medium)

Key Patterns:
- Recursive tree traversal (preorder, inorder, postorder)
- Tree validation and property checking
- Level-order traversal with queues
- Tree modification and reconstruction
- Height and depth calculations

Common Techniques:
- DFS: recursive traversal with base cases
- BFS: level-order processing with queues
- Tree properties: BST validation, balance checking
- Helper functions for complex tree operations
"""

from .._types import Category

CATEGORY_INFO = {
    "name": "Trees",
    "category": Category.TREES,
    "description": "Binary tree traversal, validation, and manipulation algorithms",
    "problems": 8,
    "patterns": [
        "Recursive tree traversal",
        "Tree validation and properties", 
        "Level-order traversal with BFS",
        "Tree modification and reconstruction",
        "Height and depth calculations"
    ]
}
