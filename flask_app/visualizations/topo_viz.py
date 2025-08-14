from __future__ import annotations

import random
from typing import Any, Dict, List, Optional, Set, Tuple


def _layer_layout(n: int, layers: int) -> List[Tuple[float, float, int]]:
    """
    Return normalized coordinates (x,y) in [0,1] and the assigned layer for each node.
    Nodes are distributed across 'layers' columns left-to-right.
    """
    layers = max(2, layers)
    # Distribute nodes as evenly as possible across layers
    base = n // layers
    rem = n % layers
    counts = [base + (1 if i < rem else 0) for i in range(layers)]

    coords: List[Tuple[float, float, int]] = []
    idx = 0
    for li, cnt in enumerate(counts):
        x = 0.08 + (0.84 * li / (layers - 1))  # margin on sides
        if cnt == 0:
            continue
        for j in range(cnt):
            # vertically spread nodes within the layer
            if cnt == 1:
                y = 0.5
            else:
                y = 0.1 + 0.8 * (j / (cnt - 1))
            coords.append((x, y, li))
            idx += 1
    # If due to rounding the number differs, trim/pad
    if len(coords) > n:
        coords = coords[:n]
    elif len(coords) < n:
        # pad at the last layer vertically
        last_x = 0.92
        while len(coords) < n:
            coords.append((last_x, 0.5, layers - 1))
    return coords


def generate_dag(n: int = 12, layers: int = 3, p: float = 0.35, seed: Optional[int] = None) -> Dict[str, Any]:
    """
    Generate a random Directed Acyclic Graph (DAG) by assigning nodes to layers
    and adding edges that only go from a layer to a strictly later layer, with probability p.
    """
    rng = random.Random(seed)
    coords = _layer_layout(n, layers)
    nodes = [{"id": i, "x": coords[i][0], "y": coords[i][1], "layer": coords[i][2]} for i in range(n)]

    # group node ids by layer
    by_layer: Dict[int, List[int]] = {}
    for i, (_, _, li) in enumerate(coords):
        by_layer.setdefault(li, []).append(i)

    edges: List[Tuple[int, int]] = []
    # For each pair of layers (i, j) with j > i, add edges with prob p
    layer_keys = sorted(by_layer.keys())
    for i_idx, li in enumerate(layer_keys):
        for lj in layer_keys[i_idx + 1 :]:
            for u in by_layer[li]:
                for v in by_layer[lj]:
                    if rng.random() < p:
                        edges.append((u, v))

    # Ensure at least one edge if possible
    if not edges and n >= 2:
        # connect consecutive layer reps if available
        for i_idx, li in enumerate(layer_keys[:-1]):
            if by_layer[li] and by_layer[layer_keys[i_idx + 1]]:
                u = by_layer[li][0]
                v = by_layer[layer_keys[i_idx + 1]][0]
                edges.append((u, v))

    # Deduplicate edges (just in case) and sort
    edges = sorted(set(edges))
    return {
        "n": n,
        "nodes": nodes,
        "edges": [[u, v] for (u, v) in edges],
        "layers": layers,
        "p": p,
    }


def _frame(
    op: str,
    current: Optional[int],
    queue: List[int],
    removed: Set[int],
    highlight_edges: Optional[List[Tuple[int, int]]] = None,
    order: Optional[List[int]] = None,
) -> Dict[str, Any]:
    return {
        "op": op,
        "current": current,
        "queue": list(queue),
        "removed": sorted(list(removed)),
        "highlight_edges": [[u, v] for (u, v) in (highlight_edges or [])],
        "order": list(order or []),
    }


def kahn_frames(g: Dict[str, Any], max_steps: int = 50000) -> List[Dict[str, Any]]:
    """
    Kahn's algorithm frames for topological sorting.
    Frame fields:
      - current: node being removed (or considered)
      - queue: current zero in-degree queue
      - removed: set of nodes already removed (output order so far)
      - highlight_edges: currently inspected edges (u->v) whose in-degree is decremented
      - order: topological order built so far
      - op: textual operation state
    """
    n: int = g["n"]
    edges: List[Tuple[int, int]] = [tuple(e) for e in g["edges"]]
    adj: List[List[int]] = [[] for _ in range(n)]
    indeg: List[int] = [0] * n
    for (u, v) in edges:
        adj[u].append(v)
        indeg[v] += 1
    for i in range(n):
        adj[i].sort()

    from collections import deque

    q: deque[int] = deque([i for i in range(n) if indeg[i] == 0])
    removed: Set[int] = set()
    order: List[int] = []
    frames: List[Dict[str, Any]] = []
    frames.append(_frame("init", None, list(q), removed, order=order))

    steps = 0
    while q and steps < max_steps:
        u = q.popleft()
        frames.append(_frame("dequeue", u, list(q), removed, order=order))
        if u in removed:
            frames.append(_frame("skip", u, list(q), removed, order=order))
            continue
        # Remove u
        removed.add(u)
        order.append(u)
        frames.append(_frame("remove", u, list(q), removed, order=order))
        # Decrement indegrees of neighbors
        for v in adj[u]:
            frames.append(_frame("inspect", u, list(q), removed, highlight_edges=[(u, v)], order=order))
            indeg[v] -= 1
            frames.append(_frame("decrement", u, list(q), removed, highlight_edges=[(u, v)], order=order))
            if indeg[v] == 0:
                q.append(v)
                frames.append(_frame("enqueue", u, list(q), removed, highlight_edges=[(u, v)], order=order))
        steps += 1

    if len(order) == n:
        frames.append(_frame("done", None, list(q), removed, order=order))
    else:
        frames.append(_frame("cycle-detected", None, list(q), removed, order=order))
    return frames


ALGORITHMS = {
    "kahn": {"name": "Topological Sort (Kahn's Algorithm)", "frames": kahn_frames},
}


def visualize(algo_key: str, n: int = 12, layers: int = 3, p: float = 0.35, seed: Optional[int] = None) -> Dict[str, Any]:
    algo = ALGORITHMS.get(algo_key)
    if not algo:
        raise ValueError(f"Unknown algorithm '{algo_key}'")
    g = generate_dag(n=n, layers=layers, p=p, seed=seed)
    frames = algo["frames"](g)
    return {"algorithm": algo_key, "name": algo["name"], "graph": g, "frames": frames, "n": n, "layers": layers, "p": p, "seed": seed}
