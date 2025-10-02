from collections import defaultdict, deque


def topological_sort_kahn(graph: dict[int, list[int]], num_nodes: int) -> list[int]:
    """
    Topological sort using Kahn's algorithm (BFS-based).

    Time: O(V + E) where V = vertices, E = edges
    Space: O(V) for in-degree array and queue

    Algorithm:
    1. Calculate in-degree for each node
    2. Add all nodes with in-degree 0 to queue
    3. Process queue: remove node, decrease in-degree of neighbors
    4. Add neighbors with in-degree 0 to queue
    5. If processed all nodes, return result; else cycle exists

    Args:
        graph: Adjacency list representation {node: [neighbors]}
        num_nodes: Total number of nodes (0 to num_nodes-1)

    Returns:
        Topologically sorted list, or empty list if cycle exists

    Interview follow-ups:
    - How to detect cycles? (If result length < num_nodes)
    - Multiple valid orderings? (Yes, any valid topological order works)
    - What if graph is disconnected? (Still works, processes all components)
    - Applications? (Course scheduling, build systems, dependency resolution)
    """
    # Calculate in-degrees
    in_degree = [0] * num_nodes
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # Initialize queue with nodes having in-degree 0
    queue = deque()
    for i in range(num_nodes):
        if in_degree[i] == 0:
            queue.append(i)

    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        # Reduce in-degree of neighbors
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check for cycle
    if len(result) != num_nodes:
        return []  # Cycle detected

    return result


def topological_sort_dfs(graph: dict[int, list[int]], num_nodes: int) -> list[int]:
    """
    Topological sort using DFS.

    Time: O(V + E)
    Space: O(V) for recursion stack and visited sets

    Algorithm:
    1. Use DFS to visit all nodes
    2. Add node to result after visiting all its neighbors
    3. Reverse the result to get topological order
    4. Use three colors: white (unvisited), gray (visiting), black (visited)

    Returns:
        Topologically sorted list, or empty list if cycle exists
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * num_nodes
    result = []
    has_cycle = False

    def dfs(node: int) -> None:
        nonlocal has_cycle
        if has_cycle:
            return

        if color[node] == GRAY:
            # Back edge found - cycle detected
            has_cycle = True
            return

        if color[node] == BLACK:
            # Already processed
            return

        color[node] = GRAY

        for neighbor in graph.get(node, []):
            dfs(neighbor)

        color[node] = BLACK
        result.append(node)

    # Visit all nodes
    for i in range(num_nodes):
        if color[i] == WHITE:
            dfs(i)

    if has_cycle:
        return []

    return result[::-1]  # Reverse to get correct order


def can_finish_courses(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Course Schedule problem - can all courses be finished?

    LeetCode 207: Course Schedule

    This is essentially cycle detection in a directed graph.
    If there's a cycle, some courses can't be completed.

    Args:
        num_courses: Number of courses (0 to num_courses-1)
        prerequisites: List of [course, prerequisite] pairs

    Returns:
        True if all courses can be finished, False otherwise
    """
    # Build adjacency list
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    # Use topological sort to detect cycles
    topo_order = topological_sort_kahn(graph, num_courses)
    return len(topo_order) == num_courses


def find_course_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """
    Course Schedule II - find a valid ordering of courses.

    LeetCode 210: Course Schedule II

    Returns:
        Valid course ordering, or empty list if impossible
    """
    # Build adjacency list
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    return topological_sort_kahn(graph, num_courses)


def alien_dictionary(words: list[str]) -> str:
    """
    Alien Dictionary - determine order of characters in alien language.

    LeetCode 269: Alien Dictionary

    Build graph from character ordering constraints, then topological sort.

    Args:
        words: List of words in alien dictionary order

    Returns:
        String representing character order, or empty if invalid
    """
    # Build graph and find all unique characters
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    chars = set()

    # Get all characters
    for word in words:
        for char in word:
            chars.add(char)

    # Initialize in-degrees
    for char in chars:
        in_degree[char] = 0

    # Build graph from adjacent words
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        min_len = min(len(word1), len(word2))

        # Check for invalid case: word1 is prefix of word2 but comes after
        if len(word1) > len(word2) and word1[:min_len] == word2[:min_len]:
            return ""

        # Find first differing character
        for j in range(min_len):
            if word1[j] != word2[j]:
                if word2[j] not in graph[word1[j]]:
                    graph[word1[j]].add(word2[j])
                    in_degree[word2[j]] += 1
                break

    # Topological sort
    queue = deque()
    for char in chars:
        if in_degree[char] == 0:
            queue.append(char)

    result = []
    while queue:
        char = queue.popleft()
        result.append(char)

        for neighbor in graph[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check if all characters are included (no cycle)
    if len(result) != len(chars):
        return ""

    return "".join(result)


def minimum_height_trees(n: int, edges: list[list[int]]) -> list[int]:
    """
    Minimum Height Trees - find roots that minimize tree height.

    LeetCode 310: Minimum Height Trees

    Uses topological sort idea: repeatedly remove leaf nodes.
    The last remaining nodes are the answer.

    Args:
        n: Number of nodes
        edges: List of edges [u, v]

    Returns:
        List of root nodes that give minimum height trees
    """
    if n <= 2:
        return list(range(n))

    # Build adjacency list
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    # Initialize leaves (nodes with degree 1)
    leaves = deque()
    for i in range(n):
        if len(graph[i]) == 1:
            leaves.append(i)

    remaining = n

    # Remove leaves layer by layer
    while remaining > 2:
        leaf_count = len(leaves)
        remaining -= leaf_count

        for _ in range(leaf_count):
            leaf = leaves.popleft()

            # Remove leaf from its neighbor
            neighbor = graph[leaf].pop()
            graph[neighbor].remove(leaf)

            # If neighbor becomes a leaf, add to queue
            if len(graph[neighbor]) == 1:
                leaves.append(neighbor)

    return list(leaves)


def build_graph_from_edges(edges: list[list[int]], num_nodes: int) -> dict[int, list[int]]:
    """Helper function to build adjacency list from edge list."""
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    return graph


def demo():
    """Demo function for topological sorting algorithms."""
    print("Topological Sort Demo")
    print("=" * 40)

    # Basic topological sort example
    print("Basic Topological Sort:")
    edges = [[5, 2], [5, 0], [4, 0], [4, 1], [2, 3], [3, 1]]
    num_nodes = 6
    graph = build_graph_from_edges(edges, num_nodes)

    print(f"Graph edges: {edges}")
    print(f"Adjacency list: {dict(graph)}")

    kahn_result = topological_sort_kahn(graph, num_nodes)
    dfs_result = topological_sort_dfs(graph, num_nodes)

    print(f"Kahn's algorithm result: {kahn_result}")
    print(f"DFS algorithm result: {dfs_result}")
    print()

    # Course scheduling example
    print("Course Scheduling:")
    courses = 4
    prereqs = [[1, 0], [2, 0], [3, 1], [3, 2]]

    can_finish = can_finish_courses(courses, prereqs)
    course_order = find_course_order(courses, prereqs)

    print(f"Courses: {courses}, Prerequisites: {prereqs}")
    print(f"Can finish all courses: {can_finish}")
    print(f"Course order: {course_order}")
    print()

    # Cycle detection example
    print("Cycle Detection:")
    cyclic_prereqs = [[1, 0], [0, 1]]  # Circular dependency

    can_finish_cyclic = can_finish_courses(2, cyclic_prereqs)
    cyclic_order = find_course_order(2, cyclic_prereqs)

    print(f"Cyclic prerequisites: {cyclic_prereqs}")
    print(f"Can finish: {can_finish_cyclic}")
    print(f"Order: {cyclic_order}")
    print()

    # Alien dictionary example
    print("Alien Dictionary:")
    alien_words = ["wrt", "wrf", "er", "ett", "rftt"]
    alien_order = alien_dictionary(alien_words)

    print(f"Words: {alien_words}")
    print(f"Character order: '{alien_order}'")
    print()

    # Invalid alien dictionary
    invalid_words = ["z", "x", "z"]
    invalid_order = alien_dictionary(invalid_words)
    print(f"Invalid words: {invalid_words}")
    print(f"Character order: '{invalid_order}' (empty = invalid)")
    print()

    # Minimum height trees
    print("Minimum Height Trees:")
    mht_edges = [[1, 0], [1, 2], [1, 3]]
    mht_n = 4

    mht_roots = minimum_height_trees(mht_n, mht_edges)
    print(f"Edges: {mht_edges}")
    print(f"Minimum height tree roots: {mht_roots}")
    print()

    # Performance comparison
    print("Algorithm Comparison:")
    print("Kahn's Algorithm (BFS-based):")
    print("  - Pros: Easy to understand, natural cycle detection")
    print("  - Cons: Requires in-degree calculation")
    print("  - Best for: When you need to process nodes level by level")
    print()
    print("DFS-based:")
    print("  - Pros: More space-efficient, natural recursion")
    print("  - Cons: Requires careful cycle detection with colors")
    print("  - Best for: When you want to process dependencies deeply first")
    print()
    print("Applications:")
    print("  - Build systems (compile dependencies)")
    print("  - Course scheduling")
    print("  - Task scheduling with dependencies")
    print("  - Spreadsheet formula evaluation")
    print("  - Package manager dependency resolution")


if __name__ == "__main__":
    demo()
