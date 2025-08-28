"""
LeetCode 211: Design Add and Search Words Data Structure
https://leetcode.com/problems/design-add-and-search-words-data-structure/

Design a data structure that supports adding new words and finding if a string
matches any previously added string.

Implement the WordDictionary class:

- WordDictionary() Initializes the object.
- void addWord(word) Adds word to the data structure, it can be matched later.
- bool search(word) Returns true if there is any string in the data structure
  that matches word or false otherwise. word may contain dots '.' where dots
  can be matched with any letter.

Examples:
    Input:
    ["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
    [[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]

    Output:
    [null,null,null,null,false,true,true,true]

    Explanation:
    WordDictionary wordDictionary = new WordDictionary();
    wordDictionary.addWord("bad");
    wordDictionary.addWord("dad");
    wordDictionary.addWord("mad");
    wordDictionary.search("pad"); // return False
    wordDictionary.search("bad"); // return True
    wordDictionary.search(".ad"); // return True
    wordDictionary.search("b.."); // return True

Constraints:
    * 1 <= word.length <= 25
    * word in addWord consists of lowercase English letters.
    * word in search consist of '.' or lowercase English letters.
    * There will be at most 2 dots in word for search queries.
    * At most 10^4 calls will be made to addWord and search.
"""

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class TrieNode:
    """Node class for the WordDictionary trie structure."""

    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.is_end_of_word = False  # Flag to mark end of a complete word


class WordDictionary:
    """
    Word dictionary with wildcard search support using Trie + Backtracking.

    The key insight is using backtracking when encountering '.' wildcards.
    For each '.', we try all possible characters and recursively search.

    Time Complexities:
    - addWord: O(m) where m is word length
    - search: O(n * 26^k) where n is number of nodes, k is number of dots

    Space Complexity: O(ALPHABET_SIZE * N * M) for trie storage
    """

    def __init__(self):
        """Initialize the word dictionary with empty trie."""
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        """
        Add a word to the dictionary.

        Algorithm:
        1. Traverse trie creating nodes as needed
        2. Mark final node as end of word

        Time: O(m) where m is word length
        Space: O(m) for new nodes in worst case
        """
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Search for a word with wildcard support.

        Algorithm:
        1. Use DFS with backtracking
        2. For regular characters, follow exact path
        3. For '.', try all possible children recursively
        4. Return true if any path leads to complete word

        Time: O(n * 26^k) where n is nodes, k is dots
        Space: O(m) for recursion stack
        """
        return self._search_helper(word, 0, self.root)

    def _search_helper(self, word: str, index: int, node: TrieNode) -> bool:
        """
        Recursive helper for wildcard search.

        Args:
            word: The search word (may contain '.')
            index: Current position in word
            node: Current trie node

        Returns:
            True if word can be matched from this position
        """
        # Base case: reached end of word
        if index == len(word):
            return node.is_end_of_word

        char = word[index]

        if char == ".":
            # Wildcard: try all possible children
            for child_node in node.children.values():
                if self._search_helper(word, index + 1, child_node):
                    return True
            return False
        else:
            # Regular character: follow exact path
            if char not in node.children:
                return False
            return self._search_helper(word, index + 1, node.children[char])


class WordDictionaryOptimized:
    """
    Alternative implementation with length-based optimization.

    Groups words by length to reduce search space for wildcard queries.
    Particularly effective when there are many words of different lengths.
    """

    def __init__(self):
        self.tries_by_length = {}  # Dictionary of tries indexed by word length

    def addWord(self, word: str) -> None:
        """Add word to length-specific trie."""
        length = len(word)

        if length not in self.tries_by_length:
            self.tries_by_length[length] = TrieNode()

        node = self.tries_by_length[length]
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Search in length-specific trie only."""
        length = len(word)

        if length not in self.tries_by_length:
            return False

        return self._search_helper(word, 0, self.tries_by_length[length])

    def _search_helper(self, word: str, index: int, node: TrieNode) -> bool:
        """Same recursive helper as main implementation."""
        if index == len(word):
            return node.is_end_of_word

        char = word[index]

        if char == ".":
            for child_node in node.children.values():
                if self._search_helper(word, index + 1, child_node):
                    return True
            return False
        else:
            if char not in node.children:
                return False
            return self._search_helper(word, index + 1, node.children[char])


def create_demo_output() -> str:
    """Demonstrate word dictionary operations with various test cases."""
    results = []

    # Basic functionality demo
    results.append("BASIC WORD DICTIONARY OPERATIONS")
    results.append("=" * 50)

    wd = WordDictionary()
    operations = [
        ("addWord", "bad"),
        ("addWord", "dad"),
        ("addWord", "mad"),
        ("search", "pad"),
        ("search", "bad"),
        ("search", ".ad"),
        ("search", "b.."),
        ("search", "..."),
        ("search", "ba."),
        ("addWord", "bat"),
        ("search", "ba."),
    ]

    for i, (op, word) in enumerate(operations):
        if op == "addWord":
            wd.addWord(word)
            results.append(f"{i + 1}. addWord('{word}') -> None")
        elif op == "search":
            result = wd.search(word)
            results.append(f"{i + 1}. search('{word}') -> {result}")

    # Wildcard patterns demo
    results.append("\n" + "=" * 50)
    results.append("WILDCARD PATTERN MATCHING")
    results.append("=" * 50)

    dictionary = WordDictionary()
    words = ["cat", "car", "card", "care", "careful", "cats", "bat", "bad", "bag"]

    for word in words:
        dictionary.addWord(word)

    results.append(f"Dictionary words: {words}")

    # Test various wildcard patterns
    patterns = [
        "cat",  # exact match
        "ca.",  # single wildcard
        "c..",  # multiple wildcards at end
        ".ar",  # wildcard at start
        "c.r.",  # wildcards in middle
        "....",  # all wildcards (4 chars)
        ".....",  # all wildcards (5 chars)
        ".a.",  # pattern matching multiple words
        "ba.",  # pattern matching multiple words
        "xyz",  # no match
    ]

    for pattern in patterns:
        found = dictionary.search(pattern)
        results.append(f"Pattern '{pattern}': {found}")

    # Performance comparison demo
    results.append("\n" + "=" * 50)
    results.append("PERFORMANCE COMPARISON")
    results.append("=" * 50)

    import time

    # Create test datasets
    test_words = [f"word{i:04d}" for i in range(1000)]
    # Test patterns for performance testing
    patterns = [
        "word0001",  # exact match
        "word..01",  # pattern with wildcards
        ".ord0001",  # wildcard at start
        "word0..1",  # wildcards in middle
        "........",  # all wildcards (8 chars)
    ]

    implementations = [
        ("Standard Trie", WordDictionary),
        ("Length-Optimized Trie", WordDictionaryOptimized),
    ]

    for name, DictClass in implementations:
        dict_impl = DictClass()

        # Insert performance
        start = time.perf_counter()
        for word in test_words:
            dict_impl.addWord(word)
        insert_time = time.perf_counter() - start

        # Search performance (exact)
        start = time.perf_counter()
        dict_impl.search("word0500")
        exact_search_time = time.perf_counter() - start

        # Search performance (wildcard)
        start = time.perf_counter()
        dict_impl.search("word..00")
        wildcard_time = time.perf_counter() - start

        results.append(f"\n{name}:")
        results.append(f"  Insert 1000 words: {insert_time * 1000:.2f}ms")
        results.append(f"  Exact search: {exact_search_time * 1000:.2f}ms")
        results.append(f"  Wildcard search: {wildcard_time * 1000:.2f}ms")

    # Algorithm insights
    results.append("\n" + "=" * 50)
    results.append("ALGORITHM INSIGHTS")
    results.append("=" * 50)

    results.append("Wildcard Search Complexity:")
    results.append("  • Worst case: O(n * 26^k) where k = number of dots")
    results.append("  • Each '.' branches to all 26 possible characters")
    results.append("  • Backtracking explores all possible paths")

    results.append("\nOptimization Strategies:")
    results.append("  1. Length-based grouping reduces search space")
    results.append("  2. Early termination when path doesn't exist")
    results.append("  3. Iterative deepening for very long patterns")

    results.append("\nReal-world Applications:")
    results.append("  • Autocomplete with fuzzy matching")
    results.append("  • Spell checkers with partial word matching")
    results.append("  • Pattern matching in text editors")
    results.append("  • Regular expression engines (simplified)")

    return "\n".join(results)


# Test cases for validation
TEST_CASES = [
    TestCase(
        input_data=(
            [
                "WordDictionary",
                "addWord",
                "addWord",
                "addWord",
                "search",
                "search",
                "search",
                "search",
            ],
            [[], ["bad"], ["dad"], ["mad"], ["pad"], ["bad"], [".ad"], ["b.."]],
        ),
        expected=[None, None, None, None, False, True, True, True],
        description="Basic word dictionary operations",
    ),
    TestCase(
        input_data=(
            ["WordDictionary", "addWord", "search", "search", "search"],
            [[], ["a"], ["a"], ["."], ["aa"]],
        ),
        expected=[None, None, True, True, False],
        description="Single character and wildcard",
    ),
    TestCase(
        input_data=(
            ["WordDictionary", "addWord", "addWord", "search", "search", "search"],
            [[], ["at"], ["and"], ["an"], [".at"], [".nd"]],
        ),
        expected=[None, None, None, False, False, True],
        description="Multiple words with patterns",
    ),
    TestCase(
        input_data=(
            ["WordDictionary", "addWord", "addWord", "search", "search"],
            [[], ["word"], ["wor"], ["word"], ["wor."]],
        ),
        expected=[None, None, None, True, False],
        description="Prefix vs exact word",
    ),
]


def test_solution():
    """Test the word dictionary implementation."""

    def run_operations(operations, inputs):
        """Helper to run sequence of word dictionary operations."""
        wd = None
        results = []

        for op, args in zip(operations, inputs):
            if op == "WordDictionary":
                wd = WordDictionary()
                results.append(None)
            elif op == "addWord":
                wd.addWord(args[0])
                results.append(None)
            elif op == "search":
                result = wd.search(args[0])
                results.append(result)

        return results

    def run_test(test_input, expected, description):
        operations, inputs = test_input
        result = run_operations(operations, inputs)

        if result == expected:
            return True, ""
        else:
            return (
                False,
                f"Operations: {operations}, Inputs: {inputs}, Expected: {expected}, Got: {result}",
            )

    return run_test_cases(TEST_CASES, run_test)


# Register the problem
register_problem(
    slug="add_and_search_word",
    leetcode_num=211,
    title="Design Add and Search Words Data Structure",
    difficulty=Difficulty.MEDIUM,
    category=Category.TRIES,
    solution_func=lambda: WordDictionary(),  # Return word dictionary instance
    test_func=test_solution,
    demo_func=create_demo_output,
)


if __name__ == "__main__":
    # Run tests
    print("Testing Add and Search Word...")
    result = test_solution()
    print(f"Tests passed: {result}")

    # Show demo
    print("\n" + "=" * 50)
    print("DEMO OUTPUT")
    print("=" * 50)
    print(create_demo_output())
