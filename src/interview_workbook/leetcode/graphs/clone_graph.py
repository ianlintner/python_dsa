"""
LeetCode 133: Clone Graph

Given a reference of a node in a connected undirected graph.

Return a deep copy (clone) of the graph.

Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

class Node {
    public int val;
    public List<Node> neighbors;
}

Test case format:

For simplicity, each node's value is the same as the node's index (1-indexed). For example,
the first node with val == 1, the second node with val == 2, and so on. The graph is
represented in the test case using an adjacency list.

An adjacency list is a collection of unordered lists used to represent a finite graph.
Each list describes the set of neighbors of a node in the graph.

The given node will always be the first node with val = 1. You must return the copy of the
given node as a reference to the cloned graph.

Example 1:
Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
Output: [[2,4],[1,3],[2,4],[1,3]]
Explanation: There are 4 nodes in the graph.
1st node (val = 1)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
2nd node (val = 2)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
3rd node (val = 3)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
4th node (val = 4)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).

Example 2:
Input: adjList = [[]]
Output: [[]]
Explanation: Note that the input contains one empty list. The graph consists of only one node with val = 1 and it does not have any neighbors.

Example 3:
Input: adjList = []
Output: []
Explanation: This an empty graph, it does not have any nodes.

Constraints:
- The number of nodes in the given graph is in the range [0, 100].
- 1 <= Node.val <= 100
- Node.val is unique for each node.
- There are no repeated edges and no self-loops in the graph.
- The Graph is connected and all nodes can be visited starting from the given node.
"""

from typing import Dict, List, Optional
from .._runner import TestCase, run_test_cases
from .._registry import register_problem
from .._types import Category, Difficulty


# Definition for a Node
class Node:
    def __init__(self, val: int = 0, neighbors: Optional[List["Node"]] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def __repr__(self) -> str:
        return f"Node({self.val}, neighbors=[{', '.join(str(n.val) for n in self.neighbors)}])"


class Solution:
    def cloneGraph(self, node: Optional[Node]) -> Optional[Node]:
        """
        Clone a graph using DFS with hash map to track visited nodes.

        Key insight: Use a hash map to store mapping from original node to cloned node.
        For each node, create a clone if not exists, then recursively clone all neighbors.

        Time: O(V + E) where V = vertices, E = edges. Visit each node and edge once.
        Space: O(V) for hash map and recursion stack.

        Args:
            node: Reference to a node in the connected undirected graph

        Returns:
            Reference to the cloned graph (same structure, different objects)
        """
        if not node:
            return None

        # Hash map to store original_node -> cloned_node mapping
        visited = {}

        def dfs(original_node: Node) -> Node:
            """DFS helper to clone nodes and their connections."""
            # If already cloned, return the clone
            if original_node in visited:
                return visited[original_node]

            # Create clone of current node (without neighbors initially)
            clone = Node(original_node.val)
            visited[original_node] = clone

            # Clone all neighbors recursively
            for neighbor in original_node.neighbors:
                clone.neighbors.append(dfs(neighbor))

            return clone

        return dfs(node)

    def cloneGraphBFS(self, node: Optional[Node]) -> Optional[Node]:
        """
        Clone graph using BFS with queue and hash map.

        BFS approach processes nodes level by level, which can be more intuitive
        for some developers and avoids potential stack overflow for deep graphs.

        Time: O(V + E)
        Space: O(V) for queue and hash map
        """
        from collections import deque

        if not node:
            return None

        # Hash map to store original_node -> cloned_node mapping
        visited = {}

        # Create clone of starting node
        clone_start = Node(node.val)
        visited[node] = clone_start

        # BFS queue
        queue = deque([node])

        while queue:
            current = queue.popleft()

            # Process each neighbor
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    # Create clone for unvisited neighbor
                    visited[neighbor] = Node(neighbor.val)
                    queue.append(neighbor)

                # Add cloned neighbor to current node's clone
                visited[current].neighbors.append(visited[neighbor])

        return clone_start

    def cloneGraphIterative(self, node: Optional[Node]) -> Optional[Node]:
        """
        Clone graph using iterative DFS with explicit stack.

        This avoids recursion while still using DFS traversal pattern.
        Uses explicit stack instead of function call stack.

        Time: O(V + E)
        Space: O(V) for stack and hash map
        """
        if not node:
            return None

        visited = {}
        stack = [node]

        # Create clone of starting node
        visited[node] = Node(node.val)

        while stack:
            current = stack.pop()

            # Process each neighbor
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    # Create clone for unvisited neighbor
                    visited[neighbor] = Node(neighbor.val)
                    stack.append(neighbor)

                # Add cloned neighbor to current node's clone
                visited[current].neighbors.append(visited[neighbor])

        return visited[node]


def create_demo_output() -> str:
    """
    Create comprehensive demo showing different approaches to graph cloning.

    Returns:
        Formatted string with examples, performance analysis, and insights.
    """
    solution = Solution()

    demo_parts = []
    demo_parts.append("=== LeetCode 133: Clone Graph - Comprehensive Demo ===\n")

    # Helper function to create graph from adjacency list
    def create_graph_from_adj_list(adj_list: List[List[int]]) -> Optional[Node]:
        """Create graph from adjacency list representation."""
        if not adj_list:
            return None

        # Create all nodes first
        nodes = {}
        for i in range(len(adj_list)):
            nodes[i + 1] = Node(i + 1)

        # Connect neighbors
        for i, neighbors in enumerate(adj_list):
            for neighbor_val in neighbors:
                nodes[i + 1].neighbors.append(nodes[neighbor_val])

        return nodes[1] if nodes else None

    # Helper function to convert graph to adjacency list for comparison
    def graph_to_adj_list(node: Optional[Node]) -> List[List[int]]:
        """Convert graph to adjacency list for easy comparison."""
        if not node:
            return []

        visited = set()
        adj_list = {}

        def dfs(curr_node):
            if curr_node.val in visited:
                return
            visited.add(curr_node.val)
            adj_list[curr_node.val] = [n.val for n in curr_node.neighbors]
            for neighbor in curr_node.neighbors:
                dfs(neighbor)

        dfs(node)

        # Convert to list format (1-indexed)
        if not adj_list:
            return []
        max_val = max(adj_list.keys())
        result = []
        for i in range(1, max_val + 1):
            result.append(sorted(adj_list.get(i, [])))
        return result

    # Test cases
    test_cases = [
        ([[2, 4], [1, 3], [2, 4], [1, 3]], "4-node cycle graph"),
        ([[]], "Single node with no neighbors"),
        ([], "Empty graph"),
        ([[2], [1]], "Two connected nodes"),
        ([[2, 3], [1, 3], [1, 2]], "Triangle graph"),
        ([[2, 3, 4], [1], [1], [1]], "Star graph - center connected to all"),
    ]

    for adj_list, description in test_cases:
        demo_parts.append(f"\nTest Case: {description}")
        demo_parts.append(f"Input adjacency list: {adj_list}")

        # Create original graph
        original = create_graph_from_adj_list(adj_list)

        if original:
            demo_parts.append(f"Original graph starting node: {original.val}")

            # Test different approaches
            clone1 = solution.cloneGraph(original)
            clone2 = solution.cloneGraphBFS(original)
            clone3 = solution.cloneGraphIterative(original)

            # Convert back to adjacency lists for comparison
            original_adj = graph_to_adj_list(original)
            clone1_adj = graph_to_adj_list(clone1)
            clone2_adj = graph_to_adj_list(clone2)
            clone3_adj = graph_to_adj_list(clone3)

            demo_parts.append(f"DFS clone adjacency list: {clone1_adj}")
            demo_parts.append(f"BFS clone adjacency list: {clone2_adj}")
            demo_parts.append(f"Iterative clone adjacency list: {clone3_adj}")

            # Verify structure is same but objects are different
            structure_match = original_adj == clone1_adj == clone2_adj == clone3_adj
            demo_parts.append(f"Structure matches: {structure_match}")

            # Verify objects are different (deep copy)
            if clone1:
                objects_different = original is not clone1
                demo_parts.append(f"Objects are different (deep copy): {objects_different}")
        else:
            demo_parts.append("Original graph: None (empty)")
            demo_parts.append("All clones: None")

    # Algorithm analysis
    demo_parts.append("\n=== Algorithm Analysis ===")

    demo_parts.append("\nRecursive DFS:")
    demo_parts.append("  • Time: O(V + E) - visit each vertex and edge once")
    demo_parts.append("  • Space: O(V) - hash map + recursion stack")
    demo_parts.append("  • Pros: Clean, intuitive implementation")
    demo_parts.append("  • Cons: Stack overflow risk for deep graphs")

    demo_parts.append("\nBFS with Queue:")
    demo_parts.append("  • Time: O(V + E) - same as DFS")
    demo_parts.append("  • Space: O(V) - hash map + queue")
    demo_parts.append("  • Pros: Level-by-level processing, no recursion")
    demo_parts.append("  • Cons: Slightly more complex implementation")

    demo_parts.append("\nIterative DFS:")
    demo_parts.append("  • Time: O(V + E) - same as recursive")
    demo_parts.append("  • Space: O(V) - hash map + explicit stack")
    demo_parts.append("  • Pros: Avoids recursion, explicit control")
    demo_parts.append("  • Cons: More complex than recursive DFS")

    # Key concepts and patterns
    demo_parts.append("\n=== Key Concepts ===")
    demo_parts.append("1. **Deep Copy**: Create entirely new objects with same structure")
    demo_parts.append("2. **Hash Map Tracking**: Map original nodes to cloned nodes")
    demo_parts.append("3. **Graph Traversal**: Visit all reachable nodes exactly once")
    demo_parts.append("4. **Circular Reference Handling**: Hash map prevents infinite loops")
    demo_parts.append("5. **Two-Phase Process**: Create node first, then establish connections")

    # Common pitfalls
    demo_parts.append("\n=== Common Pitfalls ===")
    demo_parts.append("1. **Infinite Loops**: Must track visited nodes due to cycles")
    demo_parts.append("2. **Shallow vs Deep Copy**: Need new objects, not just references")
    demo_parts.append("3. **Neighbor Connection**: Must clone neighbors recursively")
    demo_parts.append("4. **Null Handling**: Check for null/empty input graphs")
    demo_parts.append("5. **Memory References**: Cloned graph must be completely separate")

    # Real-world applications
    demo_parts.append("\n=== Real-World Applications ===")
    demo_parts.append("1. **Social Network Analysis**: Copy user connection graphs")
    demo_parts.append("2. **Game State Management**: Clone game world representations")
    demo_parts.append("3. **Version Control**: Create branches of dependency graphs")
    demo_parts.append("4. **Distributed Systems**: Replicate network topology")
    demo_parts.append("5. **Circuit Design**: Copy circuit component connections")
    demo_parts.append("6. **Data Structure Libraries**: Generic graph copying utilities")

    # Implementation variations
    demo_parts.append("\n=== Implementation Variations ===")
    demo_parts.append("1. **Node Identification**: Use node values vs. object identity")
    demo_parts.append("2. **Traversal Method**: DFS vs. BFS vs. iterative approaches")
    demo_parts.append("3. **Memory Management**: Consider memory usage for large graphs")
    demo_parts.append("4. **Thread Safety**: Concurrent access to shared hash map")
    demo_parts.append("5. **Error Handling**: Invalid graph structures, cycles validation")

    return "\n".join(demo_parts)


def create_test_graph(adj_list: List[List[int]]) -> Optional[Node]:
    """Helper function to create graph from adjacency list."""
    if not adj_list:
        return None

    nodes = {}
    for i in range(len(adj_list)):
        nodes[i + 1] = Node(i + 1)

    for i, neighbors in enumerate(adj_list):
        for neighbor_val in neighbors:
            nodes[i + 1].neighbors.append(nodes[neighbor_val])

    return nodes[1] if nodes else None


def graph_to_adj_list(node: Optional[Node]) -> List[List[int]]:
    """Helper function to convert graph back to adjacency list."""
    if not node:
        return []

    visited = set()
    adj_map = {}

    def dfs(curr_node):
        if curr_node.val in visited:
            return
        visited.add(curr_node.val)
        adj_map[curr_node.val] = [n.val for n in curr_node.neighbors]
        for neighbor in curr_node.neighbors:
            dfs(neighbor)

    dfs(node)

    if not adj_map:
        return []

    max_val = max(adj_map.keys())
    result = []
    for i in range(1, max_val + 1):
        result.append(sorted(adj_map.get(i, [])))
    return result


# Test cases
TEST_CASES = [
    TestCase(
        input_data={"adj_list": [[2, 4], [1, 3], [2, 4], [1, 3]]},
        expected_output=[[2, 4], [1, 3], [2, 4], [1, 3]],
        description="4-node cycle graph",
    ),
    TestCase(
        input_data={"adj_list": [[]]},
        expected_output=[[]],
        description="Single node with no neighbors",
    ),
    TestCase(input_data={"adj_list": []}, expected_output=[], description="Empty graph"),
    TestCase(
        input_data={"adj_list": [[2], [1]]},
        expected_output=[[2], [1]],
        description="Two connected nodes",
    ),
    TestCase(
        input_data={"adj_list": [[2, 3], [1, 3], [1, 2]]},
        expected_output=[[2, 3], [1, 3], [1, 2]],
        description="Triangle graph",
    ),
]


def test_solution():
    """Test the solution with all test cases."""

    def test_function(adj_list):
        original = create_test_graph(adj_list)
        solution = Solution()
        cloned = solution.cloneGraph(original)
        return graph_to_adj_list(cloned)

    run_test_cases(test_function, TEST_CASES)


# Register the problem
register_problem(
    slug="clone-graph",
    leetcode_num=133,
    title="Clone Graph",
    difficulty=Difficulty.MEDIUM,
    category=Category.GRAPHS,
    solution_func=lambda adj_list: graph_to_adj_list(
        Solution().cloneGraph(create_test_graph(adj_list))
    ),
    test_func=test_solution,
    demo_func=create_demo_output,
)
