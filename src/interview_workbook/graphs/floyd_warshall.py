from __future__ import annotations

INF = float("inf")
NEG_INF: float = float("-inf")


def build_adj_matrix(
    n: int, edges: list[tuple[int, int, float]], directed: bool = True
) -> list[list[float]]:
    """
    Build adjacency matrix from edge list.
    edges: list of (u, v, w). If not directed, adds both directions.
    """
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0.0
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = float(w)
        if not directed:
            if w < dist[v][u]:
                dist[v][u] = float(w)
    return dist


def floyd_warshall(dist: list[list[float]]) -> tuple[list[list[float]], list[list[int | None]]]:
    """
    Floyd–Warshall algorithm for All-Pairs Shortest Paths (APSP).

    Args:
        dist: adjacency matrix with dist[i][j] = weight(i->j), INF if no edge, 0 on diagonal

    Returns:
        (dist_out, next_hop) where:
          - dist_out[i][j] is the shortest distance from i to j
          - next_hop[i][j] is the next vertex after i on the shortest path to j (or None if unreachable)

    Time: O(V^3)
    Space: O(V^2)

    Notes:
    - Handles negative edges.
    - If a negative cycle is reachable between i and j, dist_out[i][j] will become -INF
      after negative-cycle propagation step below (optional but useful).
    """
    n = len(dist)
    # Initialize next-hop for path reconstruction
    next_hop: list[list[int | None]] = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if dist[i][j] != INF and i != j:
                next_hop[i][j] = j

    # Core triple loop
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            di = dist[i]
            dik = di[k]
            if dik == INF:
                continue
            dkk = dk
            for j in range(n):
                alt = dik + dkk[j]
                if alt < di[j]:
                    di[j] = alt
                    next_hop[i][j] = next_hop[i][k]

    # Detect negative cycles: if dist[i][i] < 0, vertex i is on or reaches a negative cycle.
    # Propagate -INF to pairs (i, j) that can go through any negative cycle.
    for k in range(n):
        if dist[k][k] < 0:
            for i in range(n):
                if dist[i][k] == INF:
                    continue
                for j in range(n):
                    if dist[k][j] == INF:
                        continue
                    dist[i][j] = NEG_INF
                    next_hop[i][j] = None  # path not well-defined due to negative cycle influence

    return dist, next_hop


def reconstruct_path(next_hop: list[list[int | None]], u: int, v: int) -> list[int]:
    """
    Reconstruct path from u to v using next_hop produced by floyd_warshall.
    Returns empty list if unreachable or path undefined due to negative cycle.
    """
    if u < 0 or v < 0 or u >= len(next_hop) or v >= len(next_hop):
        return []
    if next_hop[u][v] is None:
        return []
    path = [u]
    while u != v:
        u = next_hop[u][v]  # type: ignore[index]
        if u is None:
            # Undefined due to negative cycle propagation
            return []
        path.append(u)
        # Safety breaker to avoid infinite loops (shouldn't happen)
        if len(path) > len(next_hop) + 5:
            return []
    return path


def has_negative_cycle(dist: list[list[float]]) -> bool:
    """Return True if any dist[i][i] < 0 indicating a negative cycle."""
    return any(dist[i][i] < 0 for i in range(len(dist)))


def demo():
    print("Floyd–Warshall (All-Pairs Shortest Paths) Demo")
    print("=" * 55)

    # Example 1: Graph with negative edges, no negative cycles
    print("APSP with negative edges (no negative cycles):")
    n = 4
    edges = [
        (0, 1, 3),
        (0, 2, 10),
        (1, 2, -2),
        (2, 3, 2),
        (1, 3, 7),
    ]
    dist = build_adj_matrix(n, edges, directed=True)
    dist_out, next_hop = floyd_warshall(dist)
    for i in range(n):
        print(f"dist[{i}]: {dist_out[i]}")
    print("Path 0 -> 3:", reconstruct_path(next_hop, 0, 3))
    print(f"Has negative cycle? {has_negative_cycle(dist_out)}")
    print()

    # Example 2: Negative cycle case
    print("APSP with a negative cycle:")
    n2 = 3
    edges2 = [
        (0, 1, 1),
        (1, 2, -1),
        (2, 0, -1),  # cycle weight = -1
    ]
    dist2 = build_adj_matrix(n2, edges2, directed=True)
    dist2_out, next2 = floyd_warshall(dist2)
    for i in range(n2):
        print(f"dist[{i}]: {dist2_out[i]}")
    print(f"Has negative cycle? {has_negative_cycle(dist2_out)}")
    print("Path 0 -> 2:", reconstruct_path(next2, 0, 2), "(empty if undefined due to neg cycle)")
    print()

    # Example 3: Undirected graph APSP
    print("APSP on undirected weighted graph:")
    n3 = 5
    edges3 = [
        (0, 1, 2),
        (1, 2, 3),
        (0, 3, 1),
        (3, 4, 4),
        (2, 4, 2),
    ]
    dist3 = build_adj_matrix(n3, edges3, directed=False)
    dist3_out, next3 = floyd_warshall(dist3)
    for i in range(n3):
        print(f"dist[{i}]: {dist3_out[i]}")
    print("Path 0 -> 4:", reconstruct_path(next3, 0, 4))
    print()

    print("Complexity and Notes:")
    print("  - Time: O(V^3), Space: O(V^2)")
    print("  - Handles negative edges; detect cycles via dist[i][i] < 0")
    print("  - For sparse graphs and single-source queries, prefer Dijkstra/Bellman-Ford")
    print("  - For many sources on sparse graphs, Johnson's algorithm may be better")


if __name__ == "__main__":
    demo()
