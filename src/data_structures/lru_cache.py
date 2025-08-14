class Node:
    """Doubly linked list node for LRU cache."""

    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: Node | None = None
        self.next: Node | None = None


class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation.

    Time: O(1) for get and put operations
    Space: O(capacity)

    LeetCode 146: LRU Cache

    Key insights:
    - HashMap for O(1) access to nodes
    - Doubly linked list for O(1) insertion/deletion
    - Dummy head/tail nodes to simplify edge cases

    Interview follow-ups:
    - How would you implement LFU cache? (Need frequency tracking)
    - What if we need thread safety? (Add locks)
    - How to handle cache misses in distributed system? (Cache-aside pattern)
    - Memory vs speed trade-offs? (Smaller cache = more misses but less memory)
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, Node] = {}

        # Create dummy head and tail nodes
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node: Node) -> None:
        """Add node right after head."""
        node.prev = self.head
        node.next = self.head.next

        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """Remove an existing node from the linked list."""
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: Node) -> None:
        """Move node to head (mark as recently used)."""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> Node:
        """Remove the last node (least recently used)."""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node

    def get(self, key: int) -> int:
        """Get value by key and mark as recently used."""
        node = self.cache.get(key)

        if not node:
            return -1

        # Move to head to mark as recently used
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """Put key-value pair, evicting LRU item if necessary."""
        node = self.cache.get(key)

        if not node:
            new_node = Node(key, value)

            if len(self.cache) >= self.capacity:
                # Remove least recently used
                tail = self._pop_tail()
                del self.cache[tail.key]

            self.cache[key] = new_node
            self._add_node(new_node)
        else:
            # Update existing node
            node.value = value
            self._move_to_head(node)


class LFUCache:
    """
    Least Frequently Used (LFU) Cache implementation.

    Time: O(1) for get and put operations
    Space: O(capacity)

    LeetCode 460: LFU Cache

    More complex than LRU - tracks both frequency and recency.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0

        # key -> value
        self.key_to_val: dict[int, int] = {}
        # key -> frequency
        self.key_to_freq: dict[int, int] = {}
        # frequency -> list of keys with that frequency
        self.freq_to_keys: dict[int, list] = {}

    def _update_freq(self, key: int) -> None:
        """Update frequency of a key."""
        freq = self.key_to_freq[key]

        # Remove from current frequency list
        self.freq_to_keys[freq].remove(key)

        # If this was the only key with min_freq, increment min_freq
        if freq == self.min_freq and not self.freq_to_keys[freq]:
            self.min_freq += 1

        # Add to new frequency list
        new_freq = freq + 1
        self.key_to_freq[key] = new_freq

        if new_freq not in self.freq_to_keys:
            self.freq_to_keys[new_freq] = []
        self.freq_to_keys[new_freq].append(key)

    def get(self, key: int) -> int:
        """Get value and update frequency."""
        if key not in self.key_to_val:
            return -1

        self._update_freq(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        """Put key-value pair, evicting LFU item if necessary."""
        if self.capacity <= 0:
            return

        if key in self.key_to_val:
            # Update existing key
            self.key_to_val[key] = value
            self._update_freq(key)
            return

        # Need to add new key
        if len(self.key_to_val) >= self.capacity:
            # Evict LFU key (first in list for min_freq)
            evict_key = self.freq_to_keys[self.min_freq].pop(0)
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]

        # Add new key
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.min_freq = 1

        if 1 not in self.freq_to_keys:
            self.freq_to_keys[1] = []
        self.freq_to_keys[1].append(key)


class SimpleLRUCache:
    """
    Simple LRU cache using OrderedDict (Python-specific solution).

    This is more concise but less educational for interviews.
    Use the full implementation above to show understanding of data structures.
    """

    def __init__(self, capacity: int):
        from collections import OrderedDict

        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used (first item)
            self.cache.popitem(last=False)

        self.cache[key] = value


def demo():
    """Demo function for cache implementations."""
    print("LRU and LFU Cache Demo")
    print("=" * 40)

    # LRU Cache demo
    print("LRU Cache Demo:")
    lru = LRUCache(2)

    operations = [
        ("put", 1, 1),
        ("put", 2, 2),
        ("get", 1, None),  # returns 1
        ("put", 3, 3),  # evicts key 2
        ("get", 2, None),  # returns -1 (not found)
        ("put", 4, 4),  # evicts key 1
        ("get", 1, None),  # returns -1 (not found)
        ("get", 3, None),  # returns 3
        ("get", 4, None),  # returns 4
    ]

    for op in operations:
        if op[0] == "put":
            lru.put(op[1], op[2])
            print(f"  put({op[1]}, {op[2]})")
        else:
            result = lru.get(op[1])
            print(f"  get({op[1]}) -> {result}")

    print()

    # LFU Cache demo
    print("LFU Cache Demo:")
    lfu = LFUCache(2)

    lfu_operations = [
        ("put", 1, 1),
        ("put", 2, 2),
        ("get", 1, None),  # key 1 freq = 2, key 2 freq = 1
        ("put", 3, 3),  # evicts key 2 (lowest freq)
        ("get", 2, None),  # returns -1
        ("get", 3, None),  # returns 3
        ("put", 4, 4),  # evicts key 1 (both have freq 2, but 1 is older)
        ("get", 1, None),  # returns -1
        ("get", 3, None),  # returns 3
        ("get", 4, None),  # returns 4
    ]

    for op in lfu_operations:
        if op[0] == "put":
            lfu.put(op[1], op[2])
            print(f"  put({op[1]}, {op[2]})")
        else:
            result = lfu.get(op[1])
            print(f"  get({op[1]}) -> {result}")

    print()

    # Simple LRU using OrderedDict
    print("Simple LRU Cache (OrderedDict):")
    simple_lru = SimpleLRUCache(3)

    simple_ops = [
        ("put", "a", 1),
        ("put", "b", 2),
        ("put", "c", 3),
        ("get", "a", None),
        ("put", "d", 4),  # evicts "b"
        ("get", "b", None),  # returns -1
        ("get", "c", None),  # returns 3
        ("get", "d", None),  # returns 4
        ("get", "a", None),  # returns 1
    ]

    for op in simple_ops:
        if op[0] == "put":
            simple_lru.put(op[1], op[2])
            print(f"  put('{op[1]}', {op[2]})")
        else:
            result = simple_lru.get(op[1])
            print(f"  get('{op[1]}') -> {result}")

    print()

    # Performance comparison
    print("Cache Performance Analysis:")
    print("LRU Cache:")
    print("  - Get: O(1) - HashMap lookup + doubly linked list move")
    print("  - Put: O(1) - HashMap insert + doubly linked list operations")
    print("  - Space: O(capacity) - HashMap + linked list nodes")
    print()
    print("LFU Cache:")
    print("  - Get: O(1) - Multiple HashMap operations")
    print("  - Put: O(1) - Multiple HashMap operations")
    print("  - Space: O(capacity) - Multiple HashMaps")
    print("  - More complex but handles frequency-based eviction")
    print()
    print("Use cases:")
    print("  - LRU: General purpose, simpler, most common")
    print("  - LFU: When access patterns matter more than recency")
    print("  - Consider hybrid approaches for real systems")


if __name__ == "__main__":
    demo()
