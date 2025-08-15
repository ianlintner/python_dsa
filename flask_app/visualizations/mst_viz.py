from __future__ import annotations

import heapq
import math
import random
from typing import Any, Dict, List, Optional, Set, Tuple

Coord = Tuple[float, float]
Edge = Tuple[int, int, float]


def _circle_layout(n: int, jitter: float = 0.0, rng: Optional[random.Random] = None) -> List[Coord]:
    pts: List[Coord] = []
    rng = rng or random.Random()
    for i in range(n):
        theta = 2.0 * math.pi * (i / n)
        r = 0.42
        cx, cy = 0.5, 0.5
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        if jitter > 0.0:
            x += rng.uniform(-jitter, jitter)
            y += rng.uniform(-jitter, jitter)
        pts.append((x, y))
    return pts


def _dist(a: Coord, b: Coord) -> float:
    dx, dy = (a[0] - b[0]), (a[1] - b[1])
    return (dx * dx + dy * dy) ** 0.5


def generate_graph(n: int = 12, k: int = 3, seed: Optional[int] = None) -> Dict[str, Any]:
    """
    Geometric graph for MST visualization.
    - Place n nodes on a circle (slight jitter for variety)
    - Connect each node to its k nearest neighbors (undirected)
    - Weight of an edge is Euclidean distance between endpoints
    """
    rng = random.Random(seed)
    k = max(1, min(k, max(1, n - 1)))
    nodes_xy = _circle_layout(n, jitter=0.02, rng=rng)

    # Build KNN edges
    edges_set: Set[Tuple[int, int]] = set()
    for u in range(n):
        dists: List[Tuple[float, int]] = []
        for v in range(n):
            if u == v:
                continue
            d = _dist(nodes_xy[u], nodes_xy[v])
            dists.append((d, v))
        dists.sort()
        for i in range(min(k, len(dists))):
            v = dists[i][1]
            a, b = (u, v) if u < v else (v, u)
            edges_set.add((a, b))

    # Compute weights
    edges: List[Edge] = []
    for u, v in edges_set:
        w = _dist(nodes_xy[u], nodes_xy[v])
        edges.append((u, v, w))

    edges.sort(key=lambda e: e[2])
    nodes = [{"id": i, "x": x, "y": y} for i, (x, y) in enumerate(nodes_xy)]
    return {"n": n, "nodes": nodes, "edges": edges, "k": k}


def _frame(
    op: str,
    mst_edges: List[Tuple[int, int]],
    edge: Optional[Tuple[int, int]] = None,
    visited: Optional[Set[int]] = None,
) -> Dict[str, Any]:
    return {
        "op": op,
        "mst_edges": [list(e) for e in mst_edges],
        "edge": list(edge) if edge is not None else None,
        "visited": sorted(list(visited)) if visited is not None else [],
    }


def kruskal_frames(g: Dict[str, Any], max_steps: int = 50000) -> List[Dict[str, Any]]:
    n: int = g["n"]
    edges: List[Edge] = g["edges"]

    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> bool:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] += 1
        return True

    frames: List[Dict[str, Any]] = []
    mst: List[Tuple[int, int]] = []
    frames.append(_frame("init", mst))

    for u, v, _w in edges:
        if len(frames) >= max_steps:
            break
        frames.append(_frame("consider", mst, (u, v)))
        if union(u, v):
            mst.append((u, v))
            frames.append(_frame("add", mst, (u, v)))
            if len(mst) == n - 1:
                frames.append(_frame("done", mst))
                break
        else:
            frames.append(_frame("cycle", mst, (u, v)))

    if len(mst) != n - 1:
        frames.append(_frame("incomplete", mst))
    return frames


def prim_frames(g: Dict[str, Any], start: int = 0, max_steps: int = 50000) -> List[Dict[str, Any]]:
    n: int = g["n"]
    edges: List[Edge] = g["edges"]
    # Build adjacency
    adj: List[List[Tuple[int, float]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    for i in range(n):
        adj[i].sort(key=lambda t: t[1])

    frames: List[Dict[str, Any]] = []
    mst: List[Tuple[int, int]] = []
    visited: Set[int] = set([start])
    frames.append(_frame("start", mst, visited=visited))

    heap: List[Tuple[float, int, int]] = []  # (w, u, v) edge from u->v
    tie = 0
    for v, w in adj[start]:
        heapq.heappush(heap, (w, start, v))
        tie += 1

    while len(visited) < n and heap and len(frames) < max_steps:
        w, u, v = heapq.heappop(heap)
        # Show consideration
        frames.append(_frame("consider", mst, (u, v), visited=visited))
        if v in visited:
            frames.append(_frame("skip", mst, (u, v), visited=visited))
            continue
        # Accept edge
        mst.append((u, v))
        visited.add(v)
        frames.append(_frame("add", mst, (u, v), visited=visited))
        # Push new frontier edges
        for x, wx in adj[v]:
            if x not in visited:
                heapq.heappush(heap, (wx, v, x))

    if len(visited) == n:
        frames.append(_frame("done", mst, visited=visited))
    else:
        frames.append(_frame("incomplete", mst, visited=visited))
    return frames


ALGORITHMS = {
    "kruskal": {"name": "Minimum Spanning Tree (Kruskal)", "frames": kruskal_frames},
    "prim": {"name": "Minimum Spanning Tree (Prim)", "frames": prim_frames},
}


def visualize(
    algo_key: str, n: int = 12, k: int = 3, seed: Optional[int] = None, start: int = 0
) -> Dict[str, Any]:
    algo = ALGORITHMS.get(algo_key)
    if not algo:
        raise ValueError(f"Unknown algorithm '{algo_key}'")
    g = generate_graph(n=n, k=k, seed=seed)
    frames = algo["frames"](g, start=start) if algo_key == "prim" else algo["frames"](g)
    # Convert edges to serializable
    ser_edges = [[u, v, w] for (u, v, w) in g["edges"]]
    graph = {"n": g["n"], "nodes": g["nodes"], "edges": ser_edges, "k": g["k"]}
    return {
        "algorithm": algo_key,
        "name": algo["name"],
        "graph": graph,
        "frames": frames,
        "start": start,
        "seed": seed,
        "n": n,
        "k": g["k"],
    }
