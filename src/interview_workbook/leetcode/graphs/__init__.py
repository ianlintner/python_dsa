"""
Graph Algorithms - LeetCode Problems

This category contains graph algorithm implementations covering=- Graph traversal (BFS, DFS)
- Topological sorting and cycle detection
- Connected components and islands
- Graph cloning and construction
- Multi-source BFS and grid-based problems
- Course prerequisites and dependency resolution

Key Concepts=- Breadth-First Search (BFS): Level-order traversal, shortest path in unweighted graphs
- Depth-First Search (DFS): Path exploration, cycle detection, topological sort
- Union-Find: Disjoint sets for connectivity queries
- Grid-based graphs: 2D arrays as implicit graphs with 4/8-directional movement
- Adjacency representations=Lists, matrices, and edge lists
- Graph states: White/Gray/Black coloring for cycle detection
- Multi-source algorithms: Starting BFS/DFS from multiple points simultaneously

Common Patterns:
    - Island counting: DFS/BFS to find connected components in 2D grids
- Course scheduling: Topological sort with cycle detection using Kahn's algorithm
- Graph cloning: DFS with hash map to track visited nodes and their copies
- Boundary problems: Multi-source BFS from edges (Pacific-Atlantic water flow)
- State propagation: BFS for time-based spreading (rotting oranges)
- Region modification: DFS to mark and modify connected regions

Problem Categories:
    1. **Graph Traversal & Construction**
   - Number of Islands: Connected components in 2D grid
   - Clone Graph: Deep copy of graph structure

2. **Topological Sort & Scheduling**
   - Course Schedule: Cycle detection in directed graph
   - Course Schedule II: Topological ordering of courses

3. **Multi-source & Boundary Problems**
   - Pacific Atlantic Water Flow: Multi-source BFS from boundaries
   - Surrounded Regions: Boundary-connected region identification
   - Rotting Oranges: Time-based multi-source propagation

Time Complexities=- DFS/BFS: O(V + E) where V = vertices, E: edges
- Grid traversal: O(m * n) for m×n grid
- Topological sort: O(V + E) using Kahn's algorithm or DFS
- Union-Find: O(α(n)) per operation with path compression

Space Complexities:
    - Adjacency list: O(V + E)
- Grid problems=O(1) if modifying in-place, O(m * n) for visited array
- Recursion stack: O(V) for DFS in worst case
- BFS queue: O(V) maximum queue size

Real-world Applications=- Social networks=Friend recommendations, community detection
- Navigation systems=Route planning, reachability analysis
- Dependency resolution=Build systems, package managers
- Network analysis=Connectivity, shortest paths
- Game development=Pathfinding, level generation
- Distributed systems=Service dependencies, failure propagation
"""

from .._types import Category

# Graph algorithms category metadata
CATEGORY_INFO = {
    "name": "Graphs",
    "category": Category.GRAPHS,
    "description": "Graph algorithms including traversal, topological sorting, and connectivity",
    "key_concepts": [
        "Breadth-First Search (BFS) and Depth-First Search (DFS)",
        "Topological sorting and cycle detection",
        "Connected components and union-find",
        "Grid-based graph problems",
        "Multi-source algorithms and boundary conditions",
        "Graph construction and cloning",
    ],
    "common_patterns": [
        "Island counting with DFS/BFS traversal",
        "Course scheduling with topological sort",
        "Graph cloning with visited tracking",
        "Boundary propagation with multi-source BFS",
        "State spreading over time",
        "Region modification and marking",
    ],
}
