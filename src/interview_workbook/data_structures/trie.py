from __future__ import annotations


class TrieNode:
    """Node in a Trie data structure."""

    __slots__ = ("children", "is_end", "count")

    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_end: bool = False  # True if this node represents end of a word
        self.count: int = 0  # Number of words ending at this node


class Trie:
    """
    Prefix Tree (Trie) for efficient string operations.

    Time complexities (where m = length of word):
    - Insert: O(m)
    - Search: O(m)
    - StartsWith: O(m)
    - Delete: O(m)

    Space: O(ALPHABET_SIZE * N * M) where N = number of words, M = avg length

    Applications:
    - Autocomplete/suggestions
    - Spell checkers
    - IP routing tables
    - Word games (Boggle, Scrabble)
    - Dictionary lookups

    Interview follow-ups:
    - How to handle case sensitivity? (Normalize or separate tries)
    - Memory optimization? (Compressed tries, suffix trees)
    - How to get all words with prefix? (DFS from prefix node)
    - Delete operation complexity? (May need to clean up unused nodes)
    """

    def __init__(self):
        self.root = TrieNode()
        self.size = 0  # Total number of words

    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        if not node.is_end:
            self.size += 1
        node.is_end = True
        node.count += 1

    def search(self, word: str) -> bool:
        """Check if word exists in the trie."""
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Check if any word in trie starts with given prefix."""
        return self._find_node(prefix) is not None

    def count_words_with_prefix(self, prefix: str) -> int:
        """Count number of words that start with given prefix."""
        node = self._find_node(prefix)
        if node is None:
            return 0
        return self._count_words_from_node(node)

    def get_words_with_prefix(self, prefix: str, limit: int = 10) -> list[str]:
        """Get up to 'limit' words that start with given prefix."""
        node = self._find_node(prefix)
        if node is None:
            return []

        words = []
        self._collect_words(node, prefix, words, limit)
        return words

    def delete(self, word: str) -> bool:
        """
        Delete a word from the trie.
        Returns True if word was deleted, False if word wasn't in trie.
        """

        def _delete_helper(node: TrieNode, word: str, index: int) -> bool:
            if index == len(word):
                if not node.is_end:
                    return False  # Word doesn't exist

                node.is_end = False
                node.count = 0
                # Return True if node has no children (can be deleted)
                return len(node.children) == 0

            char = word[index]
            child = node.children.get(char)
            if child is None:
                return False  # Word doesn't exist

            should_delete_child = _delete_helper(child, word, index + 1)

            if should_delete_child:
                del node.children[char]
                # Return True if current node can be deleted
                return not node.is_end and len(node.children) == 0

            return False

        if self.search(word):
            _delete_helper(self.root, word, 0)
            self.size -= 1
            return True
        return False

    def get_all_words(self) -> list[str]:
        """Get all words in the trie."""
        words = []
        self._collect_words(self.root, "", words, float("inf"))
        return words

    def longest_common_prefix(self) -> str:
        """Find longest common prefix of all words in trie."""
        if self.size == 0:
            return ""

        node = self.root
        prefix = ""

        while len(node.children) == 1 and not node.is_end:
            char = next(iter(node.children))
            prefix += char
            node = node.children[char]

        return prefix

    def _find_node(self, prefix: str) -> TrieNode | None:
        """Find the node corresponding to given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _count_words_from_node(self, node: TrieNode) -> int:
        """Count total words in subtree rooted at node."""
        count = node.count
        for child in node.children.values():
            count += self._count_words_from_node(child)
        return count

    def _collect_words(self, node: TrieNode, prefix: str, words: list[str], limit: int) -> None:
        """Collect words from subtree rooted at node."""
        if len(words) >= limit:
            return

        if node.is_end:
            words.append(prefix)

        for char, child in sorted(node.children.items()):
            if len(words) >= limit:
                break
            self._collect_words(child, prefix + char, words, limit)

    def __len__(self) -> int:
        return self.size

    def __contains__(self, word: str) -> bool:
        return self.search(word)


class WordDictionary:
    """
    Word dictionary supporting wildcard searches.

    LeetCode 211: Design Add and Search Words Data Structure
    Supports '.' as wildcard matching any character.
    """

    def __init__(self):
        self.trie = Trie()

    def add_word(self, word: str) -> None:
        """Add word to dictionary."""
        self.trie.insert(word)

    def search(self, word: str) -> bool:
        """Search word with '.' as wildcard."""
        return self._search_helper(word, 0, self.trie.root)

    def _search_helper(self, word: str, index: int, node: TrieNode) -> bool:
        """Recursive helper for wildcard search."""
        if index == len(word):
            return node.is_end

        char = word[index]

        if char == ".":
            # Wildcard: try all possible children
            for child in node.children.values():
                if self._search_helper(word, index + 1, child):
                    return True
            return False
        else:
            # Regular character
            if char not in node.children:
                return False
            return self._search_helper(word, index + 1, node.children[char])


def find_words_in_board(board: list[list[str]], words: list[str]) -> list[str]:
    """
    Find all words from dictionary that can be formed on 2D board.

    LeetCode 212: Word Search II
    Uses Trie for efficient prefix checking during DFS.
    """
    # Build trie from words
    trie = Trie()
    for word in words:
        trie.insert(word)

    result = set()
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, node: TrieNode, path: str, visited: set):
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or (r, c) in visited
            or board[r][c] not in node.children
        ):
            return

        char = board[r][c]
        node = node.children[char]
        path += char
        visited.add((r, c))

        if node.is_end:
            result.add(path)

        # Explore all 4 directions
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, node, path, visited)

        visited.remove((r, c))

    # Start DFS from each cell
    for i in range(rows):
        for j in range(cols):
            dfs(i, j, trie.root, "", set())

    return list(result)


def demo():
    """Demo function for Trie."""
    print("Trie Demo")
    print("=" * 40)

    # Basic operations
    trie = Trie()
    words = ["apple", "app", "apricot", "banana", "band", "bandana"]

    print("Inserting words:", words)
    for word in words:
        trie.insert(word)

    print(f"Trie size: {len(trie)}")
    print()

    # Search operations
    test_words = ["app", "apple", "appl", "application", "ban"]
    for word in test_words:
        exists = trie.search(word)
        print(f"Search '{word}': {exists}")

    print()

    # Prefix operations
    prefixes = ["app", "ban", "xyz"]
    for prefix in prefixes:
        has_prefix = trie.starts_with(prefix)
        count = trie.count_words_with_prefix(prefix)
        words_with_prefix = trie.get_words_with_prefix(prefix, 5)

        print(f"Prefix '{prefix}':")
        print(f"  Has prefix: {has_prefix}")
        print(f"  Word count: {count}")
        print(f"  Words: {words_with_prefix}")

    print()

    # Other operations
    print(f"All words: {trie.get_all_words()}")
    print(f"Longest common prefix: '{trie.longest_common_prefix()}'")

    # Delete operation
    print(f"\nDeleting 'app': {trie.delete('app')}")
    print(f"Search 'app' after deletion: {trie.search('app')}")
    print(f"Search 'apple' after deletion: {trie.search('apple')}")

    print()

    # Wildcard dictionary
    print("Wildcard Dictionary Demo:")
    wd = WordDictionary()
    for word in ["bad", "dad", "mad"]:
        wd.add_word(word)

    test_patterns = ["pad", "bad", ".ad", "b.."]
    for pattern in test_patterns:
        found = wd.search(pattern)
        print(f"Search '{pattern}': {found}")


if __name__ == "__main__":
    demo()
