from collections import deque
from typing import Dict, List, Set, Hashable, Optional, Tuple

# Type alias for adjacency list representation
Graph = Dict[Hashable, List[Hashable]]

def bfs(graph: Graph, start: Hashable) -> List[Hashable]:
    """
    Breadth-First Search traversal.
    
    Time: O(V + E) where V = vertices, E = edges
    Space: O(V) for queue and visited set
    
    Applications:
    - Shortest path in unweighted graphs
    - Level-order traversal
    - Connected components
    - Bipartite graph checking
    
    Interview follow-ups:
    - How to find shortest path? (Track parent pointers)
    - How to handle disconnected graphs? (Run BFS from each unvisited node)
    - Memory optimization? (Use bit vector for visited if nodes are integers)
    """
    if start not in graph:
        return []
    
    visited: Set[Hashable] = {start}
    queue = deque([start])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result

def bfs_shortest_path(graph: Graph, start: Hashable, target: Hashable) -> Optional[List[Hashable]]:
    """
    Find shortest path between start and target using BFS.
    Returns None if no path exists.
    """
    if start == target:
        return [start]
    
    if start not in graph:
        return None
    
    visited: Set[Hashable] = {start}
    queue = deque([(start, [start])])
    
    while queue:
        node, path = queue.popleft()
        
        for neighbor in graph.get(node, []):
            if neighbor == target:
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None

def bfs_level_order(graph: Graph, start: Hashable) -> List[List[Hashable]]:
    """
    BFS that returns nodes grouped by level/distance from start.
    """
    if start not in graph:
        return []
    
    visited: Set[Hashable] = {start}
    current_level = [start]
    levels = []
    
    while current_level:
        levels.append(current_level[:])
        next_level = []
        
        for node in current_level:
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_level.append(neighbor)
        
        current_level = next_level
    
    return levels

def dfs_recursive(graph: Graph, start: Hashable, visited: Optional[Set[Hashable]] = None) -> List[Hashable]:
    """
    Depth-First Search using recursion.
    
    Time: O(V + E)
    Space: O(V) for recursion stack and visited set
    
    Applications:
    - Topological sorting
    - Cycle detection
    - Path finding
    - Connected components
    - Maze solving
    """
    if visited is None:
        visited = set()
    
    if start in visited or start not in graph:
        return []
    
    visited.add(start)
    result = [start]
    
    for neighbor in graph.get(start, []):
        result.extend(dfs_recursive(graph, neighbor, visited))
    
    return result

def dfs_iterative(graph: Graph, start: Hashable) -> List[Hashable]:
    """
    Depth-First Search using explicit stack (iterative).
    """
    if start not in graph:
        return []
    
    visited: Set[Hashable] = set()
    stack = [start]
    result = []
    
    while stack:
        node = stack.pop()
        
        if node not in visited:
            visited.add(node)
            result.append(node)
            
            # Add neighbors in reverse order to maintain left-to-right traversal
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return result

def dfs_path_exists(graph: Graph, start: Hashable, target: Hashable) -> bool:
    """Check if path exists from start to target using DFS."""
    if start == target:
        return True
    
    visited: Set[Hashable] = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        
        if node == target:
            return True
        
        if node not in visited:
            visited.add(node)
            stack.extend(neighbor for neighbor in graph.get(node, []) 
                        if neighbor not in visited)
    
    return False

def find_all_paths(graph: Graph, start: Hashable, target: Hashable) -> List[List[Hashable]]:
    """
    Find all simple paths from start to target.
    Warning: Can be exponential in number of paths!
    """
    def dfs_all_paths(current: Hashable, target: Hashable, path: List[Hashable], 
                     visited: Set[Hashable], all_paths: List[List[Hashable]]):
        if current == target:
            all_paths.append(path[:])
            return
        
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                path.append(neighbor)
                visited.add(neighbor)
                dfs_all_paths(neighbor, target, path, visited, all_paths)
                path.pop()
                visited.remove(neighbor)
    
    all_paths = []
    if start in graph:
        dfs_all_paths(start, target, [start], {start}, all_paths)
    return all_paths

def connected_components_undirected(graph: Graph) -> List[List[Hashable]]:
    """
    Find all connected components in undirected graph using BFS.
    """
    visited: Set[Hashable] = set()
    components = []
    
    for node in graph:
        if node not in visited:
            # BFS to find component
            component = []
            queue = deque([node])
            visited.add(node)
            
            while queue:
                current = queue.popleft()
                component.append(current)
                
                for neighbor in graph.get(current, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            components.append(component)
    
    return components

def has_cycle_undirected(graph: Graph) -> bool:
    """
    Detect cycle in undirected graph using DFS.
    A cycle exists if we visit a node that's already visited and it's not the parent.
    """
    visited: Set[Hashable] = set()
    
    def dfs_cycle(node: Hashable, parent: Optional[Hashable]) -> bool:
        visited.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs_cycle(neighbor, node):
                    return True
            elif neighbor != parent:
                return True  # Back edge found (cycle)
        
        return False
    
    for node in graph:
        if node not in visited:
            if dfs_cycle(node, None):
                return True
    
    return False

def has_cycle_directed(graph: Graph) -> bool:
    """
    Detect cycle in directed graph using DFS with colors.
    White (0) = unvisited, Gray (1) = visiting, Black (2) = visited
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    
    def dfs_cycle(node: Hashable) -> bool:
        color[node] = GRAY
        
        for neighbor in graph.get(node, []):
            if color.get(neighbor, WHITE) == GRAY:
                return True  # Back edge to gray node = cycle
            if color.get(neighbor, WHITE) == WHITE and dfs_cycle(neighbor):
                return True
        
        color[node] = BLACK
        return False
    
    for node in graph:
        if color[node] == WHITE:
            if dfs_cycle(node):
                return True
    
    return False

def is_bipartite(graph: Graph) -> bool:
    """
    Check if graph is bipartite using BFS coloring.
    A graph is bipartite if it can be colored with 2 colors such that
    no adjacent vertices have the same color.
    """
    color = {}
    
    for start in graph:
        if start in color:
            continue
        
        # BFS coloring
        queue = deque([start])
        color[start] = 0
        
        while queue:
            node = queue.popleft()
            
            for neighbor in graph.get(node, []):
                if neighbor not in color:
                    color[neighbor] = 1 - color[node]  # Alternate color
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False  # Same color = not bipartite
    
    return True

def demo():
    """Demo function for BFS/DFS algorithms."""
    print("BFS/DFS Demo")
    print("=" * 40)
    
    # Create sample graphs
    # Undirected graph
    undirected = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    # Directed graph
    directed = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': ['E'],
        'E': []
    }
    
    # Graph with cycle
    cyclic = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A']  # Creates cycle
    }
    
    print("Undirected graph:", undirected)
    print("BFS from A:", bfs(undirected, 'A'))
    print("DFS recursive from A:", dfs_recursive(undirected, 'A'))
    print("DFS iterative from A:", dfs_iterative(undirected, 'A'))
    print()
    
    # Shortest path
    path = bfs_shortest_path(undirected, 'A', 'F')
    print(f"Shortest path A -> F: {path}")
    
    # Level order
    levels = bfs_level_order(undirected, 'A')
    print(f"Level order from A: {levels}")
    print()
    
    # Connected components
    disconnected = {
        'A': ['B'], 'B': ['A'],
        'C': ['D'], 'D': ['C'],
        'E': []
    }
    components = connected_components_undirected(disconnected)
    print(f"Connected components: {components}")
    print()
    
    # Cycle detection
    print(f"Undirected has cycle: {has_cycle_undirected(undirected)}")
    print(f"Directed has cycle: {has_cycle_directed(directed)}")
    print(f"Cyclic has cycle: {has_cycle_directed(cyclic)}")
    print()
    
    # Bipartite check
    bipartite_graph = {
        'A': ['C', 'D'],
        'B': ['C', 'D'],
        'C': ['A', 'B'],
        'D': ['A', 'B']
    }
    print(f"Bipartite graph: {bipartite_graph}")
    print(f"Is bipartite: {is_bipartite(bipartite_graph)}")
    print(f"Undirected is bipartite: {is_bipartite(undirected)}")

if __name__ == "__main__":
    demo()
