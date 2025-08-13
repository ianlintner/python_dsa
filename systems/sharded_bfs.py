from collections import deque, defaultdict
from typing import Deque, Dict, Iterable, List, Set, Tuple

"""
Sharded (Level-Synchronous) BFS Simulation

Goal:
  Demonstrate how BFS can be horizontally sharded across multiple workers/machines.
  We simulate synchronous "supersteps" (like BSP model): each shard processes its
  local frontier, generates messages for remote shards, then we exchange messages
  between supersteps.

Model:
  - Graph is partitioned into S shards: shard_id = partition(node)
  - Each shard keeps adjacency for nodes it owns
  - Distances dictionary is globally combined (or maintained per-shard + reduce)
  - At each level:
      * Process local frontier, visit neighbors
      * If neighbor belongs to same shard, handle locally
      * If neighbor belongs to another shard, produce a message to that shard
  - At barrier between levels, deliver messages to build next frontier per shard

Notes:
  - In a real system, each shard is a process/machine communicating via RPC/queues.
  - This simulation is single-process, but preserves algorithmic structure.
  - Fault tolerance, network partitions, stragglers, etc., are not handled here.

Complexity:
  - Same as BFS: O(V + E), but distributed across shards.
  - Communication cost: proportional to inter-shard edges traversed.
"""

Graph = Dict[int, List[int]]
Partitions = Dict[int, int]  # node -> shard_id
ShardGraphs = Dict[int, Graph]  # shard_id -> subgraph (only owns adjacency for its nodes)

def partition_round_robin(nodes: Iterable[int], num_shards: int) -> Partitions:
    return {n: (idx % num_shards) for idx, n in enumerate(sorted(nodes))}

def build_shard_graph(graph: Graph, parts: Partitions, num_shards: int) -> ShardGraphs:
    shards: ShardGraphs = {s: defaultdict(list) for s in range(num_shards)}
    for u, nbrs in graph.items():
        s = parts[u]
        shards[s][u] = list(nbrs)
    return shards

def sharded_bfs(
    graph: Graph,
    start: int,
    num_shards: int = 3,
    partitioner=partition_round_robin
) -> Dict[int, int]:
    """
    Simulate a sharded level-synchronous BFS.

    Returns:
        distances dict: node -> shortest hop count from start
    """
    if start not in graph:
        return {}

    # Partition
    parts = partitioner(graph.keys(), num_shards)
    shards = build_shard_graph(graph, parts, num_shards)

    # Per-shard state
    distances: Dict[int, int] = {}  # global distances
    frontiers: Dict[int, Set[int]] = {s: set() for s in range(num_shards)}

    start_shard = parts[start]
    frontiers[start_shard].add(start)
    distances[start] = 0

    visited: Set[int] = {start}
    level = 0

    while any(frontiers[s] for s in range(num_shards)):
        # Messages to send to shard_id: set(nodes)
        messages: Dict[int, Set[int]] = {s: set() for s in range(num_shards)}

        # Each shard processes its local frontier
        for s in range(num_shards):
            local_frontier = frontiers[s]
            if not local_frontier:
                continue
            for u in local_frontier:
                for v in shards[s].get(u, []):
                    if v in visited:
                        continue
                    sv = parts[v]
                    # If target node belongs to same shard, we can mark now
                    if sv == s:
                        visited.add(v)
                        distances[v] = level + 1
                        messages[s].add(v)  # still use messages to gather next frontier
                    else:
                        # Send to remote shard to consider in next superstep
                        messages[sv].add(v)

        # Barrier: exchange messages -> build next frontiers
        frontiers = {s: set() for s in range(num_shards)}
        for s in range(num_shards):
            if not messages[s]:
                continue
            for v in messages[s]:
                if v not in visited:
                    visited.add(v)
                    distances[v] = level + 1
                frontiers[s].add(v)

        level += 1

    return distances


def demo():
    print("Sharded Level-Synchronous BFS (Simulation)")
    print("=" * 50)

    # Example graph (undirected edges as two directed edges here)
    graph: Graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1, 6],
        5: [2, 6],
        6: [4, 5, 7],
        7: [6],
    }
    # Mirror edges to ensure symmetry
    for u, nbrs in list(graph.items()):
        for v in nbrs:
            graph.setdefault(v, [])
            if u not in graph[v]:
                graph[v].append(u)

    print("Graph adjacency (small demo):")
    for u in sorted(graph):
        print(f"  {u}: {sorted(graph[u])}")
    print()

    start = 0
    for shards in [2, 3, 4]:
        dist = sharded_bfs(graph, start=start, num_shards=shards)
        print(f"Distances from {start} with {shards} shards: {dict(sorted(dist.items()))}")
    print()

    print("Notes & Interview Tips:")
    print("  - Partition strategy impacts cross-shard edges (communication).")
    print("  - Level-synchronous model: frontier expansion + barrier + exchange.")
    print("  - In practice, each shard is a process/machine; messages via queues/RPC.")
    print("  - Consider skew, hot-spot nodes, and dynamic repartitioning for balance.")


if __name__ == "__main__":
    demo()
