from typing import List, Dict, Any


class UnionFind:
    """
    Disjoint Set Union (Union-Find) with path compression and union by rank.

    Time: Nearly O(1) amortized per operation (inverse Ackermann function)
    Space: O(n)

    Applications:
    - Kruskal's MST algorithm
    - Connected components in graphs
    - Cycle detection in undirected graphs
    - Dynamic connectivity queries
    - Percolation problems

    Interview follow-ups:
    - How does path compression work? (Flattens tree during find)
    - What's union by rank? (Attach smaller tree under larger)
    - Why nearly O(1)? (Inverse Ackermann grows extremely slowly)
    """

    def __init__(self, n: int):
        """Initialize n disjoint sets."""
        self.parent = list(range(n))  # Each node is its own parent initially
        self.rank = [0] * n  # Height of tree rooted at i
        self.size = [1] * n  # Size of component rooted at i
        self.components = n  # Number of connected components

    def find(self, x: int) -> int:
        """
        Find root of set containing x with path compression.
        Path compression flattens the tree for faster future queries.
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Union sets containing x and y using union by rank.
        Returns True if union performed, False if already connected.
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already in same set

        # Union by rank: attach smaller tree under larger tree
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]

        # Only increase rank if trees had same height
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1

        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """Check if x and y are in the same connected component."""
        return self.find(x) == self.find(y)

    def component_size(self, x: int) -> int:
        """Get size of component containing x."""
        return self.size[self.find(x)]

    def num_components(self) -> int:
        """Get number of connected components."""
        return self.components

    def get_components(self) -> Dict[int, List[int]]:
        """Get all components as dict mapping root -> list of nodes."""
        components = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in components:
                components[root] = []
            components[root].append(i)
        return components


class UnionFindWithValues:
    """
    Union-Find that can work with arbitrary hashable values, not just integers.
    """

    def __init__(self):
        self.parent: Dict[Any, Any] = {}
        self.rank: Dict[Any, int] = {}
        self.size: Dict[Any, int] = {}
        self.components = 0

    def make_set(self, x: Any) -> None:
        """Create a new set containing only x."""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.size[x] = 1
            self.components += 1

    def find(self, x: Any) -> Any:
        """Find with path compression."""
        if x not in self.parent:
            self.make_set(x)
            return x

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: Any, y: Any) -> bool:
        """Union by rank."""
        self.make_set(x)
        self.make_set(y)

        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]

        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1

        self.components -= 1
        return True

    def connected(self, x: Any, y: Any) -> bool:
        """Check connectivity."""
        return self.find(x) == self.find(y)


def count_connected_components(n: int, edges: List[List[int]]) -> int:
    """
    Count connected components in undirected graph.

    LeetCode 323: Number of Connected Components in an Undirected Graph
    """
    uf = UnionFind(n)

    for u, v in edges:
        uf.union(u, v)

    return uf.num_components()


def has_cycle_undirected(n: int, edges: List[List[int]]) -> bool:
    """
    Detect cycle in undirected graph using Union-Find.

    If we try to union two nodes that are already connected,
    we've found a cycle.
    """
    uf = UnionFind(n)

    for u, v in edges:
        if uf.connected(u, v):
            return True
        uf.union(u, v)

    return False


def accounts_merge(accounts: List[List[str]]) -> List[List[str]]:
    """
    Merge accounts that belong to the same person.

    LeetCode 721: Accounts Merge
    Uses Union-Find to group emails belonging to same person.
    """
    uf = UnionFindWithValues()
    email_to_name = {}

    # Build union-find structure
    for account in accounts:
        name = account[0]
        first_email = account[1]

        for email in account[1:]:
            email_to_name[email] = name
            uf.union(first_email, email)

    # Group emails by root
    groups = {}
    for email in email_to_name:
        root = uf.find(email)
        if root not in groups:
            groups[root] = []
        groups[root].append(email)

    # Format result
    result = []
    for emails in groups.values():
        emails.sort()
        name = email_to_name[emails[0]]
        result.append([name] + emails)

    return result


def demo():
    """Demo function for Union-Find."""
    print("Union-Find Demo")
    print("=" * 40)

    # Basic operations
    print("Basic Union-Find operations:")
    uf = UnionFind(6)
    print(f"Initial components: {uf.num_components()}")

    # Connect some nodes
    operations = [(0, 1), (1, 2), (3, 4)]
    for u, v in operations:
        uf.union(u, v)
        print(f"Union({u}, {v}) -> components: {uf.num_components()}")

    # Test connectivity
    test_pairs = [(0, 2), (0, 3), (3, 4), (4, 5)]
    for u, v in test_pairs:
        connected = uf.connected(u, v)
        print(f"Connected({u}, {v}): {connected}")

    print(f"Component sizes: {[uf.component_size(i) for i in range(6)]}")
    print(f"All components: {uf.get_components()}")

    print()

    # Graph problems
    print("Graph applications:")

    # Connected components
    edges1 = [[0, 1], [1, 2], [3, 4]]
    components = count_connected_components(5, edges1)
    print(f"Edges {edges1} -> {components} components")

    # Cycle detection
    edges2 = [[0, 1], [1, 2], [2, 0]]  # Has cycle
    edges3 = [[0, 1], [1, 2], [3, 4]]  # No cycle

    print(f"Edges {edges2} has cycle: {has_cycle_undirected(3, edges2)}")
    print(f"Edges {edges3} has cycle: {has_cycle_undirected(5, edges3)}")

    print()

    # Accounts merge example
    print("Accounts merge:")
    accounts = [
        ["John", "johnsmith@mail.com", "john00@mail.com"],
        ["John", "johnnybravo@mail.com"],
        ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
        ["Mary", "mary@mail.com"],
    ]
    merged = accounts_merge(accounts)
    print("Input accounts:")
    for acc in accounts:
        print(f"  {acc}")
    print("Merged accounts:")
    for acc in merged:
        print(f"  {acc}")


if __name__ == "__main__":
    demo()
