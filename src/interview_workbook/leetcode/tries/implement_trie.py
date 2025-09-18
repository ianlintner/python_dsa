"""
Implement Trie

TODO: Add problem description
"""


class Trie:
    """
    Standard Trie implementation with insert, search, and startsWith.
    """

    def __init__(self):
        self.trie = {}

    def insert(self, word: str) -> None:
        node = self.trie
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node["$"] = True

    def search(self, word: str) -> bool:
        node = self.trie
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return "$" in node

    def startsWith(self, prefix: str) -> bool:
        node = self.trie
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True


class Solution:
    def solve(self, *args) -> None:
        """LeetCode driver-compatible entry (placeholder)."""
        return None


def demo():
    """Demonstrate Trie functionality."""
    import random

    random.seed(0)

    trie = Trie()
    trie.insert("apple")
    outputs = []
    outputs.append(trie.search("apple"))  # True
    outputs.append(trie.search("app"))  # False
    outputs.append(trie.startsWith("app"))  # True
    trie.insert("app")
    outputs.append(trie.search("app"))  # True
    print("Running demo for Implement Trie...")
    print(f"Search results: {outputs}")
    return str(outputs)
