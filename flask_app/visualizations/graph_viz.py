from __future__ import annotations

import math
import random
from collections import deque
from typing import Any


def _circle_layout(n: int) -> list[tuple[float, float]]:
    # Normalized coordinates in [0,1] arranged on a circle
    pts: list[tuple[float, float]] = []
    for i in range(n):
        theta = 2.0 * math.pi * (i / max(1, n))
        r = 0.42
        cx, cy = 0.5, 0.5
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        pts.append((x, y))
    return pts


def _ensure_connected(n: int, edges: set[tuple[int, int]], rng: random.Random) -> None:
    # Simple union-find to ensure the graph is connected by adding ring edges
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for u, v in edges:
        union(u, v)

    # Connect components by adding ring edges
    comp: dict[int, list[int]] = {}
    for i in range(n):
        comp.setdefault(find(i), []).append(i)
    reps = list(comp.keys())
    if len(reps) <= 1:
        return
    # Connect representatives in a chain
    ordered = [comp[r][0] for r in reps]
    for i in range(len(ordered) - 1):
        u, v = ordered[i], ordered[i + 1]
        e = (min(u, v), max(u, v))
        if e not in edges:
            edges.add(e)


def generate_graph(
    n: int = 12, p: float = 0.25, seed: int | None = None
) -> dict[str, Any]:
    """
    Generate an undirected simple graph with n nodes.
    - Start with no edges, add each possible edge with probability p
    - Ensure connectivity by linking components
    - Provide circular layout positions in [0,1] coords
    """
    rng = random.Random(seed)
    edges: set[tuple[int, int]] = set()
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                edges.add((u, v))
    _ensure_connected(n, edges, rng)
    nodes = [{"id": i, "x": x, "y": y} for i, (x, y) in enumerate(_circle_layout(n))]
    # Keep edges as tuples of ints (front-end can handle lists after jsonify)
    return {"n": n, "nodes": nodes, "edges": sorted(list(edges))}


def _frame(state: dict[str, Any]) -> dict[str, Any]:
    # Copy for JSON frame
    return {
        "current": state.get("current"),
        "visited": list(state.get("visited", [])),
        "frontier": list(state.get("frontier", [])),
        "tree_edges": list(state.get("tree_edges", [])),
        "op": state.get("op", ""),
    }


def bfs_frames(
    g: dict[str, Any], start: int = 0, max_steps: int = 20000
) -> list[dict[str, Any]]:
    n = g["n"]
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in g["edges"]:
        adj[u].append(v)
        adj[v].append(u)
    for i in range(n):
        adj[i].sort()

    visited: set[int] = set()
    q: deque[int] = deque([start])
    tree_edges: list[tuple[int, int]] = []
    frames: list[dict[str, Any]] = []
    state = {
        "current": None,
        "visited": set(),
        "frontier": list(q),
        "tree_edges": list(tree_edges),
        "op": "init",
    }
    frames.append(_frame(state))
    while q and len(frames) < max_steps:
        u = q.popleft()
        state = {
            "current": u,
            "visited": set(visited),
            "frontier": list(q),
            "tree_edges": list(tree_edges),
            "op": "dequeue",
        }
        frames.append(_frame(state))
        if u in visited:
            continue
        visited.add(u)
        state = {
            "current": u,
            "visited": set(visited),
            "frontier": list(q),
            "tree_edges": list(tree_edges),
            "op": "visit",
        }
        frames.append(_frame(state))
        for v in adj[u]:
            state = {
                "current": u,
                "visited": set(visited),
                "frontier": list(q),
                "tree_edges": list(tree_edges),
                "op": "inspect",
            }
            frames.append(_frame(state))
            if v not in visited:
                q.append(v)
                tree_edges.append((u, v))
                state = {
                    "current": u,
                    "visited": set(visited),
                    "frontier": list(q),
                    "tree_edges": list(tree_edges),
                    "op": "enqueue",
                }
                frames.append(_frame(state))
    return frames


def dfs_frames(
    g: dict[str, Any], start: int = 0, max_steps: int = 20000
) -> list[dict[str, Any]]:
    n = g["n"]
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in g["edges"]:
        adj[u].append(v)
        adj[v].append(u)
    for i in range(n):
        adj[i].sort()

    frames: list[dict[str, Any]] = []
    visited: set[int] = set()
    stack: list[tuple[int, int | None, int]] = [(start, None, 0)]  # (node, parent, idx)

    def snapshot(u: int | None, op: str) -> None:
        frontier = [s[0] for s in stack]
        frames.append(
            _frame(
                {
                    "current": u,
                    "visited": set(visited),
                    "frontier": frontier,
                    "tree_edges": list(tree_edges),
                    "op": op,
                }
            )
        )

    tree_edges: list[tuple[int, int]] = []
    snapshot(None, "init")

    while stack and len(frames) < max_steps:
        u, parent, idx = stack.pop()
        snapshot(u, "pop")
        if u in visited:
            continue
        visited.add(u)
        snapshot(u, "visit")
        if parent is not None:
            tree_edges.append((parent, u))
            snapshot(u, "tree-edge")
        # Push neighbors in reverse to process in ascending order
        neigh = sorted(adj[u], reverse=True)
        for v in neigh:
            snapshot(u, "inspect")
            if v not in visited:
                stack.append((v, u, 0))
                snapshot(u, "push")
    return frames


ALGORITHMS = {
    "bfs": {"name": "Breadth-First Search", "frames": bfs_frames},
    "dfs": {"name": "Depth-First Search", "frames": dfs_frames},
}


def visualize(
    algo_key: str, n: int = 12, p: float = 0.25, seed: int | None = None, start: int = 0
) -> dict[str, Any]:
    algo = ALGORITHMS.get(algo_key)
    if not algo:
        raise ValueError(f"Unknown algorithm '{algo_key}'")
    g = generate_graph(n=n, p=p, seed=seed)
    frames = algo["frames"](g, start=start)
    return {
        "algorithm": algo_key,
        "name": algo["name"],
        "graph": g,
        "frames": frames,
        "start": start,
        "seed": seed,
        "n": n,
        "p": p,
    }
