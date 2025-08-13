from typing import List, Tuple
import heapq

# Reuse the Union-Find from data_structures
try:
    from interview_workbook.data_structures.union_find import UnionFind
except Exception:
    # Minimal fallback UnionFind to keep this module self-contained if import fails
    class UnionFind:
        def __init__(self, n: int):
            self.parent = list(range(n))
            self.rank = [0] * n
            self.count = n

        def find(self, x: int) -> int:
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

        def union(self, x: int, y: int) -> bool:
            rx, ry = self.find(x), self.find(y)
            if rx == ry:
                return False
            if self.rank[rx] < self.rank[ry]:
                self.parent[rx] = ry
            elif self.rank[rx] > self.rank[ry]:
                self.parent[ry] = rx
            else:
                self.parent[ry] = rx
                self.rank[rx] += 1
            self.count -= 1
            return True


def kruskal_mst(
    n: int, edges: List[Tuple[int, int, int]]
) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Kruskal's algorithm for Minimum Spanning Tree (MST).

    Args:
        n: number of vertices (0..n-1)
        edges: list of edges (u, v, w), undirected graph

    Returns:
        (total_weight, mst_edges)

    Time: O(E log E) due to sorting
    Space: O(V)
    """
    # Sort edges by weight
    edges_sorted = sorted(edges, key=lambda e: e[2])
    uf = UnionFind(n)
    mst_weight = 0
    mst_edges: List[Tuple[int, int, int]] = []

    for u, v, w in edges_sorted:
        if uf.union(u, v):
            mst_weight += w
            mst_edges.append((u, v, w))
            if len(mst_edges) == n - 1:
                break

    # If not enough edges to connect all vertices, graph was disconnected
    if len(mst_edges) != n - 1:
        # Return forest weight/edges; caller may treat as no MST
        return mst_weight, mst_edges

    return mst_weight, mst_edges


def prim_mst(n: int, adj: List[List[Tuple[int, int]]]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Prim's algorithm for Minimum Spanning Tree (MST) using a min-heap.

    Args:
        n: number of vertices (0..n-1)
        adj: adjacency list where adj[u] contains (v, w) for undirected graph

    Returns:
        (total_weight, mst_edges)

    Time: O(E log V) using binary heap
    Space: O(V)
    """
    if n == 0:
        return 0, []

    visited = [False] * n
    mst_weight = 0
    mst_edges: List[Tuple[int, int, int]] = []
    min_heap: List[Tuple[int, int, int]] = []  # (w, u, v) edge from u->v

    def add_edges_from(u: int):
        visited[u] = True
        for v, w in adj[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (w, u, v))

    # Start from node 0 (if disconnected, we will restart from another component)
    components = 0
    for start in range(n):
        if visited[start]:
            continue
        components += 1
        add_edges_from(start)
        while min_heap:
            w, u, v = heapq.heappop(min_heap)
            if visited[v]:
                continue
            mst_weight += w
            mst_edges.append((u, v, w))
            add_edges_from(v)

    # If components > 1, graph is disconnected; result is a forest
    return mst_weight, mst_edges


def build_adj_list(n: int, edges: List[Tuple[int, int, int]]) -> List[List[Tuple[int, int]]]:
    """Build undirected adjacency list from edge list (u, v, w)."""
    adj: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def demo():
    print("Minimum Spanning Tree (MST) Demo - Kruskal and Prim")
    print("=" * 60)

    # Connected graph example
    print("Connected Graph Example:")
    n = 6
    edges = [
        (0, 1, 4),
        (0, 2, 4),
        (1, 2, 2),
        (1, 0, 4),
        (2, 0, 4),
        (2, 1, 2),
        (2, 3, 3),
        (2, 5, 2),
        (2, 4, 4),
        (3, 2, 3),
        (3, 4, 3),
        (3, 5, 2),
        (4, 2, 4),
        (4, 3, 3),
        (5, 2, 2),
        (5, 3, 2),
    ]
    # Deduplicate undirected duplicates for Kruskal
    edges_simple = {(min(u, v), max(u, v), w) for (u, v, w) in edges}
    edges_undirected = list(edges_simple)

    w_kruskal, mst_k = kruskal_mst(n, edges_undirected)
    print(f"Kruskal MST total weight: {w_kruskal}")
    print(f"Kruskal MST edges: {sorted(mst_k, key=lambda x: (x[0], x[1]))}")

    adj = build_adj_list(n, edges_undirected)
    w_prim, mst_p = prim_mst(n, adj)
    print(f"Prim MST total weight: {w_prim}")
    print(f"Prim MST edges: {sorted(mst_p, key=lambda x: (min(x[0], x[1]), max(x[0], x[1])))}")
    print()

    # Disconnected graph (forest) example
    print("Disconnected Graph Example (Forest):")
    n2 = 5
    edges2 = [
        (0, 1, 1),
        (1, 2, 2),
        # component break
        (3, 4, 3),
    ]
    wk2, mst_k2 = kruskal_mst(n2, edges2)
    print(f"Kruskal forest total weight: {wk2}, edges: {mst_k2}")
    adj2 = build_adj_list(n2, edges2)
    wp2, mst_p2 = prim_mst(n2, adj2)
    print(f"Prim forest total weight: {wp2}, edges: {mst_p2}")
    print()

    print("Notes and Interview Tips:")
    print("  - Kruskal: sort edges and union-find; great on sparse graphs.")
    print("  - Prim: grow MST from a start node using a min-heap; efficient with adjacency lists.")
    print("  - Both assume undirected, connected graphs for a single MST;")
    print("    on disconnected graphs they produce a minimum spanning forest.")
    print("  - If all edges have distinct weights, MST is unique.")


if __name__ == "__main__":
    demo()
