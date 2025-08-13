

def tarjan_scc(graph: dict[int, list[int]]) -> list[list[int]]:
    """
    Tarjan's algorithm to compute Strongly Connected Components (SCCs)
    in a directed graph.

    Input:
      - graph: adjacency list mapping node -> list of neighbors

    Output:
      - List of SCCs, each SCC is a list of nodes. Components are returned
        in reverse topological order of the condensation DAG (typical Tarjan behavior).

    Complexity:
      - Time: O(V + E)
      - Space: O(V)

    Pitfalls:
      - Recursion depth can be large on deep graphs; consider an iterative variant
        or increasing recursion limit for very large inputs.

    Example:
      g = {0:[1],1:[2],2:[0,3],3:[4],4:[5],5:[3]}
      tarjan_scc(g) -> e.g., [[0,2,1], [3,5,4]]
    """
    index = 0
    idx: dict[int, int] = {}  # discovery index of node
    low: dict[int, int] = {}  # low-link value
    on_stack: dict[int, bool] = {}
    stack: list[int] = []
    sccs: list[list[int]] = []

    def strongconnect(v: int) -> None:
        nonlocal index
        idx[v] = index
        low[v] = index
        index += 1
        stack.append(v)
        on_stack[v] = True

        for w in graph.get(v, []):
            if w not in idx:
                strongconnect(w)
                low[v] = min(low[v], low[w])
            elif on_stack.get(w, False):
                low[v] = min(low[v], idx[w])

        # If v is a root node, pop the stack and generate an SCC
        if low[v] == idx[v]:
            comp: list[int] = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                comp.append(w)
                if w == v:
                    break
            sccs.append(comp)

    # Ensure all nodes present in graph keys or as neighbors are visited
    nodes = set(graph.keys())
    for nbrs in graph.values():
        nodes.update(nbrs)

    for v in nodes:
        if v not in idx:
            strongconnect(v)

    return sccs


def kosaraju_scc(graph: dict[int, list[int]]) -> list[list[int]]:
    """
    Kosaraju's algorithm to compute SCCs.

    Steps:
      1) DFS on original graph to compute finishing times stack.
      2) Transpose graph.
      3) DFS in order of decreasing finish time on transposed graph to get SCCs.

    Complexity:
      - Time: O(V + E)
      - Space: O(V + E)
    """
    # Step 1: order by finish time
    visited: dict[int, bool] = {}
    order: list[int] = []

    def dfs1(u: int):
        visited[u] = True
        for v in graph.get(u, []):
            if not visited.get(v, False):
                dfs1(v)
        order.append(u)

    nodes = set(graph.keys())
    for nbrs in graph.values():
        nodes.update(nbrs)

    for u in nodes:
        if not visited.get(u, False):
            dfs1(u)

    # Step 2: transpose graph
    gt: dict[int, list[int]] = {u: [] for u in nodes}
    for u in nodes:
        for v in graph.get(u, []):
            gt[v].append(u)

    # Step 3: DFS on transposed graph in reverse finish order
    visited.clear()
    comps: list[list[int]] = []

    def dfs2(u: int, acc: list[int]):
        visited[u] = True
        acc.append(u)
        for v in gt.get(u, []):
            if not visited.get(v, False):
                dfs2(v, acc)

    for u in reversed(order):
        if not visited.get(u, False):
            acc: list[int] = []
            dfs2(u, acc)
            comps.append(acc)

    return comps


def demo():
    print("SCC Demo (Tarjan and Kosaraju)")
    print("=" * 40)
    g = {
        0: [1],
        1: [2],
        2: [0, 3],
        3: [4],
        4: [5],
        5: [3],
        6: [4, 7],
        7: [6],
    }
    print("Graph:", g)
    t = tarjan_scc(g)
    k = kosaraju_scc(g)
    print("Tarjan SCCs:   ", t)
    print("Kosaraju SCCs: ", k)
    print()
    print("Notes:")
    print("  - Both algorithms run in O(V+E).")
    print("  - Tarjan is single-pass with a stack; Kosaraju uses transpose.")
    print("  - Components order may differ; sets are equivalent.")


if __name__ == "__main__":
    demo()
