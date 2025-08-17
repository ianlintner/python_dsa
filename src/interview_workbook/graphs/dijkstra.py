from __future__ import annotations

import heapq
from collections import defaultdict

# Type aliases
Vertex = str
Weight = float
WeightedGraph = dict[Vertex, list[tuple[Vertex, Weight]]]


def dijkstra(graph: WeightedGraph, source: Vertex) -> dict[Vertex, Weight]:
    """
    Dijkstra's shortest path algorithm for non-negative edge weights.

    Time: O((V + E) log V) with binary heap
    Space: O(V) for distance map and priority queue

    Args:
        graph: Adjacency list with (neighbor, weight) tuples
        source: Starting vertex

    Returns:
        Dictionary mapping vertex -> shortest distance from source

    Pitfalls:
    - Only works with non-negative weights (use Bellman-Ford for negative)
    - Dense graphs might be better with adjacency matrix + array (O(V²))
    - Need to handle unreachable vertices (infinite distance)

    Interview follow-ups:
    - How to reconstruct path? (Track parent pointers)
    - What if edges can be negative? (Bellman-Ford algorithm)
    - How to optimize for dense graphs? (Use array instead of heap)
    - Early termination? (Stop when target is processed)
    """
    # Initialize distances
    distances = {vertex: float("inf") for vertex in graph}
    distances[source] = 0.0

    # Priority queue: (distance, vertex)
    pq = [(0.0, source)]
    visited: set[Vertex] = set()

    while pq:
        current_dist, current = heapq.heappop(pq)

        # Skip if already processed (handles duplicate entries)
        if current in visited:
            continue

        visited.add(current)

        # Relax all neighbors
        for neighbor, weight in graph.get(current, []):
            if neighbor in visited:
                continue

            new_dist = current_dist + weight

            if new_dist < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return distances


def dijkstra_with_path(
    graph: WeightedGraph, source: Vertex, target: Vertex | None = None
) -> tuple[dict[Vertex, Weight], dict[Vertex, Vertex | None]]:
    """
    Dijkstra with path reconstruction.

    Returns:
        (distances, parents) where parents[v] is the previous vertex in shortest path to v
    """
    distances = {vertex: float("inf") for vertex in graph}
    parents = {vertex: None for vertex in graph}
    distances[source] = 0.0

    pq = [(0.0, source)]
    visited: set[Vertex] = set()

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        # Early termination if we only care about one target
        if target and current == target:
            break

        for neighbor, weight in graph.get(current, []):
            if neighbor in visited:
                continue

            new_dist = current_dist + weight

            if new_dist < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_dist
                parents[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

    return distances, parents


def reconstruct_path(
    parents: dict[Vertex, Vertex | None], source: Vertex, target: Vertex
) -> list[Vertex] | None:
    """
    Reconstruct shortest path from parent pointers.
    Returns None if no path exists.
    """
    if target not in parents or parents[target] is None and target != source:
        return None

    path = []
    current = target

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()
    return path if path[0] == source else None


def dijkstra_single_target(
    graph: WeightedGraph, source: Vertex, target: Vertex
) -> tuple[Weight, list[Vertex] | None]:
    """
    Find shortest path to single target with early termination.

    Returns:
        (distance, path) or (inf, None) if unreachable
    """
    distances, parents = dijkstra_with_path(graph, source, target)
    distance = distances.get(target, float("inf"))
    path = reconstruct_path(parents, source, target) if distance != float("inf") else None
    return distance, path


def dijkstra_k_shortest_paths(
    graph: WeightedGraph, source: Vertex, target: Vertex, k: int
) -> list[tuple[Weight, list[Vertex]]]:
    """
    Find k shortest paths using modified Dijkstra (Yen's algorithm simplified).
    This is a basic version - full Yen's algorithm is more complex.
    """
    # For simplicity, this finds k shortest simple paths
    # Full implementation would use Yen's algorithm

    def find_paths_dfs(
        current: Vertex,
        target: Vertex,
        path: list[Vertex],
        cost: Weight,
        visited: set[Vertex],
        all_paths: list[tuple[Weight, list[Vertex]]],
    ):
        if len(all_paths) >= k:
            return

        if current == target:
            all_paths.append((cost, path[:]))
            return

        for neighbor, weight in sorted(graph.get(current, []), key=lambda x: x[1]):
            if neighbor not in visited and len(all_paths) < k:
                path.append(neighbor)
                visited.add(neighbor)
                find_paths_dfs(neighbor, target, path, cost + weight, visited, all_paths)
                path.pop()
                visited.remove(neighbor)

    all_paths = []
    find_paths_dfs(source, target, [source], 0.0, {source}, all_paths)
    return sorted(all_paths)[:k]


def dijkstra_all_pairs(graph: WeightedGraph) -> dict[Vertex, dict[Vertex, Weight]]:
    """
    All-pairs shortest paths using Dijkstra from each vertex.

    Time: O(V * (V + E) log V) = O(V³ log V) for dense graphs
    For dense graphs, Floyd-Warshall O(V³) might be better.
    """
    all_distances = {}

    for source in graph:
        all_distances[source] = dijkstra(graph, source)

    return all_distances


def create_graph_from_edges(edges: list[tuple[Vertex, Vertex, Weight]]) -> WeightedGraph:
    """Helper function to create adjacency list from edge list."""
    graph = defaultdict(list)

    for u, v, w in edges:
        graph[u].append((v, w))
        # Add reverse edge for undirected graph
        # graph[v].append((u, w))

    return dict(graph)


def find_shortest_path_with_constraints(
    graph: WeightedGraph, source: Vertex, target: Vertex, max_stops: int
) -> tuple[Weight, list[Vertex] | None]:
    """
    Find shortest path with maximum number of stops constraint.
    Uses modified Dijkstra with state (vertex, stops_used).
    """
    # State: (distance, vertex, stops_used, path)
    pq = [(0.0, source, 0, [source])]
    visited = set()

    while pq:
        dist, vertex, stops, path = heapq.heappop(pq)

        if vertex == target:
            return dist, path

        state = (vertex, stops)
        if state in visited or stops >= max_stops:
            continue

        visited.add(state)

        for neighbor, weight in graph.get(vertex, []):
            if stops + 1 <= max_stops:
                new_dist = dist + weight
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_dist, neighbor, stops + 1, new_path))

    return float("inf"), None


def demo():
    """Demo function for Dijkstra's algorithm."""
    print("Dijkstra's Algorithm Demo")
    print("=" * 40)

    # Create sample weighted graph
    edges = [
        ("A", "B", 4),
        ("A", "C", 1),
        ("B", "C", 2),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3),
    ]

    graph = create_graph_from_edges(edges)
    print("Graph edges:", edges)
    print("Adjacency list:", dict(graph))
    print()

    # Basic Dijkstra
    source = "A"
    distances = dijkstra(graph, source)
    print(f"Shortest distances from {source}:")
    for vertex, dist in sorted(distances.items()):
        print(f"  {source} -> {vertex}: {dist}")
    print()

    # Dijkstra with path reconstruction
    target = "F"
    distances, parents = dijkstra_with_path(graph, source)
    path = reconstruct_path(parents, source, target)

    print(f"Shortest path {source} -> {target}:")
    print(f"  Distance: {distances[target]}")
    print(f"  Path: {' -> '.join(path) if path else 'No path'}")
    print()

    # Single target with early termination
    dist, path = dijkstra_single_target(graph, source, target)
    print(f"Single target {source} -> {target}:")
    print(f"  Distance: {dist}")
    print(f"  Path: {' -> '.join(path) if path else 'No path'}")
    print()

    # Test with unreachable vertex
    isolated_graph = dict(graph)
    isolated_graph["Z"] = []  # Isolated vertex
    distances = dijkstra(isolated_graph, source)
    print(f"Distance to isolated vertex Z: {distances.get('Z', 'Not in graph')}")
    print()

    # All pairs shortest paths (small example)
    small_graph = {"A": [("B", 1), ("C", 4)], "B": [("C", 2), ("D", 5)], "C": [("D", 1)], "D": []}

    all_pairs = dijkstra_all_pairs(small_graph)
    print("All-pairs shortest paths:")
    for src in sorted(all_pairs.keys()):
        for dst in sorted(all_pairs[src].keys()):
            print(f"  {src} -> {dst}: {all_pairs[src][dst]}")
    print()

    # Path with constraints
    dist, path = find_shortest_path_with_constraints(graph, "A", "F", max_stops=3)
    print("Shortest path A -> F with max 3 stops:")
    print(f"  Distance: {dist}")
    print(f"  Path: {' -> '.join(path) if path else 'No path'}")


if __name__ == "__main__":
    demo()
