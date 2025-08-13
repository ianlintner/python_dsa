from typing import List, Tuple, Optional

INF = float("inf")

def bellman_ford(n: int, edges: List[Tuple[int, int, int]], source: int) -> Tuple[List[float], List[int]]:
    """
    Bellman-Ford algorithm for single-source shortest paths with possible negative weights.

    Args:
        n: number of nodes (0..n-1)
        edges: list of (u, v, w) directed edges
        source: source vertex

    Returns:
        distances: list of distances from source (INF if unreachable)
        parent: predecessor array to reconstruct shortest paths

    Time: O(V * E)
    Space: O(V)

    Notes:
    - Detects negative cycles reachable from the source using one extra relaxation pass.
    - If a vertex's distance can still be decreased on the V-th iteration, then there exists a
      negative cycle reachable from the source that can reach that vertex.
    """
    dist = [INF] * n
    parent = [-1] * n
    dist[source] = 0

    # Relax edges V-1 times
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:
            break

    # Optional: detect negative cycle reachable from source
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            # Mark as -INF (or a special flag) if desired; here we just warn via parent=-2
            parent[v] = -2  # indicates part of or affected by a negative cycle

    return dist, parent


def reconstruct_path(parent: List[int], target: int) -> List[int]:
    """
    Reconstruct path using predecessor array from bellman_ford.
    Returns [] if unreachable. If parent[target] == -2 (neg cycle reachable) returns [] as path undefined.
    """
    if target < 0 or target >= len(parent):
        return []

    if parent[target] == -2:
        # Path not well-defined due to negative cycle influence
        return []

    path = []
    cur = target
    seen = set()
    while cur != -1:
        if cur in seen:
            # cycle detected during reconstruction (shouldn't happen for valid BF parents)
            return []
        seen.add(cur)
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def detect_negative_cycle(n: int, edges: List[Tuple[int, int, int]]) -> Optional[List[int]]:
    """
    Detect any negative cycle in a directed graph using Bellman-Ford style approach.

    Returns:
        A list of vertices forming one negative cycle if found, else None.

    Time: O(V * E)
    """
    dist = [0] * n  # start with zero to allow detection in any component
    parent = [-1] * n
    x = -1

    for _ in range(n):
        x = -1
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                x = v

    if x == -1:
        return None  # no cycle

    # Find a vertex guaranteed to be in a negative cycle
    y = x
    for _ in range(n):
        y = parent[y]

    # Recover the cycle
    cycle = []
    cur = y
    while True:
        cycle.append(cur)
        cur = parent[cur]
        if cur == y or cur == -1:
            break
    cycle.reverse()
    return cycle


def demo():
    print("Bellman-Ford and Negative Cycle Detection Demo")
    print("=" * 55)

    # Example graph with negative edge but no negative cycle
    print("Single-source shortest paths with negative edges (no negative cycle):")
    n = 5
    edges = [
        (0, 1, 6),
        (0, 3, 7),
        (1, 2, 5),
        (1, 3, 8),
        (1, 4, -4),
        (2, 1, -2),
        (3, 2, -3),
        (3, 4, 9),
        (4, 0, 2),
        (4, 2, 7),
    ]
    source = 0

    dist, parent = bellman_ford(n, edges, source)
    print(f"Distances from {source}: {dist}")
    for t in range(n):
        path = reconstruct_path(parent, t)
        if dist[t] == float('inf'):
            print(f"  {source} -> {t}: unreachable")
        elif parent[t] == -2:
            print(f"  {source} -> {t}: affected by negative cycle (no well-defined shortest path)")
        else:
            print(f"  {source} -> {t}: distance={dist[t]}, path={path}")
    print()

    # Example with a negative cycle
    print("Negative cycle detection example:")
    n2 = 4
    edges2 = [
        (0, 1, 1),
        (1, 2, -1),
        (2, 3, -1),
        (3, 1, -1),  # cycle 1->2->3->1 sum = -3
    ]
    cycle = detect_negative_cycle(n2, edges2)
    if cycle is None:
        print("  No negative cycle found.")
    else:
        print(f"  Negative cycle found: {cycle}")
    print()

    print("Notes and Interview Tips:")
    print("  - Use Dijkstra when edges are non-negative; BF handles negatives.")
    print("  - BF can detect negative cycles reachable from source by a V-th relaxation.")
    print("  - Complexity: O(V*E). On dense graphs, consider Johnson's algorithm for all-pairs.")
    print("  - For all-pairs shortest paths with negatives (but no negative cycles), use Floyd-Warshall.")


if __name__ == "__main__":
    demo()
