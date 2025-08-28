"""
LeetCode 208: Implement Trie (Prefix Tree)
https://leetcode.com/problems/implement-trie-prefix-tree/

A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently
store and retrieve keys in a dataset of strings. There are various applications of this
data structure, such as autocomplete and spellchecker.

Implement the Trie class:

- Trie() Initializes the trie object.
- void insert(String word) Inserts the string word into the trie.
- boolean search(String word) Returns true if the string word is in the trie
  (i.e., was inserted before), and false otherwise.
- boolean startsWith(String prefix) Returns true if there is a previously inserted
  string word that has the prefix prefix, and false otherwise.

Examples:
    Input:
    ["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
    [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]

    Output:
    [null, null, true, false, true, null, true]

    Explanation:
    Trie trie = new Trie();
    trie.insert("apple");
    trie.search("apple");   // return True
    trie.search("app");     // return False
    trie.startsWith("app"); // return True
    trie.insert("app");
    trie.search("app");     // return True

Constraints:
    * 1 <= word.length, prefix.length <= 2000
    * word and prefix consist only of lowercase English letters.
    * At most 3 * 10^4 calls in total will be made to insert, search, and startsWith.
"""

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class TrieNode:
    """Node class for the Trie data structure."""

    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.is_end_of_word = False  # Flag to mark end of a complete word


class Trie:
    """
    Trie (Prefix Tree) implementation for efficient string storage and retrieval.

    Time Complexities:
    - Insert: O(m) where m is length of word
    - Search: O(m) where m is length of word
    - StartsWith: O(p) where p is length of prefix

    Space Complexity: O(ALPHABET_SIZE * N * M) where N is number of keys and M is avg length
    """

    def __init__(self):
        """Initialize the trie with an empty root node."""
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.

        Algorithm:
        1. Start from root node
        2. For each character in word:
           - If character path doesn't exist, create new node
           - Move to that child node
        3. Mark final node as end of word

        Time: O(m) where m is word length
        Space: O(m) in worst case (new path)
        """
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Search for a complete word in the trie.

        Algorithm:
        1. Traverse trie following word's characters
        2. If any character path missing, return False
        3. If reach end, check if it's marked as end of word

        Time: O(m) where m is word length
        Space: O(1)
        """
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """
        Check if any word in trie starts with given prefix.

        Algorithm:
        1. Traverse trie following prefix's characters
        2. If can traverse entire prefix, return True
        3. If any character path missing, return False

        Time: O(p) where p is prefix length
        Space: O(1)
        """
        node = self._find_node(prefix)
        return node is not None

    def _find_node(self, word: str) -> TrieNode:
        """
        Helper method to find node corresponding to word/prefix.

        Returns:
            TrieNode if path exists, None otherwise
        """
        node = self.root

        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]

        return node


class TrieOptimized:
    """
    Alternative Trie implementation with array-based children for lowercase letters.

    Uses fixed-size array instead of dictionary for better cache locality.
    Only works for lowercase English letters (a-z).
    """

    def __init__(self):
        self.root = self._create_node()

    def _create_node(self):
        """Create a new trie node with array-based children."""
        return {
            "children": [None] * 26,  # a-z = 26 letters
            "is_end": False,
        }

    def insert(self, word: str) -> None:
        """Insert word using array-based approach."""
        node = self.root

        for char in word:
            index = ord(char) - ord("a")
            if node["children"][index] is None:
                node["children"][index] = self._create_node()
            node = node["children"][index]

        node["is_end"] = True

    def search(self, word: str) -> bool:
        """Search for complete word."""
        node = self._find_node(word)
        return node is not None and node["is_end"]

    def startsWith(self, prefix: str) -> bool:
        """Check if prefix exists."""
        return self._find_node(prefix) is not None

    def _find_node(self, word: str):
        """Find node for given word/prefix."""
        node = self.root

        for char in word:
            index = ord(char) - ord("a")
            if node["children"][index] is None:
                return None
            node = node["children"][index]

        return node


def create_demo_output() -> str:
    """Demonstrate trie operations with various test cases."""
    results = []

    # Basic functionality demo
    results.append("BASIC TRIE OPERATIONS")
    results.append("=" * 50)

    trie = Trie()
    operations = [
        ("insert", "apple"),
        ("search", "apple"),
        ("search", "app"),
        ("startsWith", "app"),
        ("insert", "app"),
        ("search", "app"),
        ("insert", "application"),
        ("startsWith", "app"),
        ("search", "application"),
    ]

    for i, (op, word) in enumerate(operations):
        if op == "insert":
            trie.insert(word)
            results.append(f"{i + 1}. insert('{word}') -> None")
        elif op == "search":
            result = trie.search(word)
            results.append(f"{i + 1}. search('{word}') -> {result}")
        elif op == "startsWith":
            result = trie.startsWith(word)
            results.append(f"{i + 1}. startsWith('{word}') -> {result}")

    # Dictionary/Autocomplete demo
    results.append("\n" + "=" * 50)
    results.append("DICTIONARY AUTOCOMPLETE DEMO")
    results.append("=" * 50)

    dictionary = Trie()
    words = ["car", "card", "care", "careful", "cars", "cat", "cats", "catastrophe"]

    for word in words:
        dictionary.insert(word)

    results.append(f"Dictionary words: {words}")

    # Test various prefixes
    prefixes = ["ca", "car", "care", "cat", "dog", "catastrophic"]

    for prefix in prefixes:
        has_prefix = dictionary.startsWith(prefix)
        is_word = dictionary.search(prefix)
        results.append(f"Prefix '{prefix}': exists={has_prefix}, is_word={is_word}")

    # Performance comparison demo
    results.append("\n" + "=" * 50)
    results.append("PERFORMANCE COMPARISON")
    results.append("=" * 50)

    import time

    # Large dataset test
    test_words = [f"word{i:04d}" for i in range(1000)]
    test_searches = [f"word{i:04d}" for i in range(0, 1000, 100)]
    test_prefixes = [f"word{i:01d}" for i in range(10)]

    implementations = [
        ("Dictionary-based Trie", Trie),
        ("Array-based Trie", TrieOptimized),
    ]

    for name, TrieClass in implementations:
        trie = TrieClass()

        # Insert performance
        start = time.perf_counter()
        for word in test_words:
            trie.insert(word)
        insert_time = time.perf_counter() - start

        # Search performance
        start = time.perf_counter()
        for word in test_searches:
            trie.search(word)
        search_time = time.perf_counter() - start

        # Prefix performance
        start = time.perf_counter()
        for prefix in test_prefixes:
            trie.startsWith(prefix)
        prefix_time = time.perf_counter() - start

        results.append(f"\n{name}:")
        results.append(f"  Insert 1000 words: {insert_time * 1000:.2f}ms")
        results.append(f"  Search 10 words: {search_time * 1000:.2f}ms")
        results.append(f"  Check 10 prefixes: {prefix_time * 1000:.2f}ms")

    # Memory usage insights
    results.append("\n" + "=" * 50)
    results.append("MEMORY USAGE INSIGHTS")
    results.append("=" * 50)

    results.append("Dictionary-based Trie:")
    results.append("  ✓ Flexible - supports any character set")
    results.append("  ✓ Dynamic memory allocation")
    results.append("  ✗ Higher memory overhead per node")

    results.append("\nArray-based Trie:")
    results.append("  ✓ Better cache locality")
    results.append("  ✓ Lower memory overhead per character")
    results.append("  ✗ Fixed character set (a-z only)")
    results.append("  ✗ Wastes space for sparse tries")

    return "\n".join(results)


# Test cases for validation
TEST_CASES = [
    TestCase(
        name="Basic trie operations example",
        input_args=(
            ["Trie", "insert", "search", "search", "startsWith", "insert", "search"],
            [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]],
        ),
        expected=[None, None, True, False, True, None, True],
        description="Basic trie operations example",
    ),
    TestCase(
        name="Multiple inserts and prefix checks",
        input_args=(
            ["Trie", "insert", "insert", "search", "search", "startsWith", "startsWith"],
            [[], ["hello"], ["help"], ["hello"], ["help"], ["hel"], ["hem"]],
        ),
        expected=[None, None, None, True, True, True, False],
        description="Multiple inserts and prefix checks",
    ),
    TestCase(
        name="Single character and extension",
        input_args=(
            ["Trie", "insert", "search", "search", "insert", "search"],
            [[], ["a"], ["a"], ["aa"], ["aa"], ["aa"]],
        ),
        expected=[None, None, True, False, None, True],
        description="Single character and extension",
    ),
    TestCase(
        name="Prefix check before and after insert",
        input_args=(["Trie", "startsWith", "insert", "startsWith"], [[], ["a"], ["a"], ["a"]]),
        expected=[None, False, None, True],
        description="Prefix check before and after insert",
    ),
]


def test_solution():
    """Test the trie implementation."""

    def run_operations(operations, inputs):
        """Helper to run sequence of trie operations."""
        trie = None
        results = []

        for _i, (op, args) in enumerate(zip(operations, inputs)):
            if op == "Trie":
                trie = Trie()
                results.append(None)
            elif op == "insert":
                trie.insert(args[0])
                results.append(None)
            elif op == "search":
                result = trie.search(args[0])
                results.append(result)
            elif op == "startsWith":
                result = trie.startsWith(args[0])
                results.append(result)

        return results

    def run_operations_test(test_case):
        """Run operations for a test case with the new format."""
        operations, inputs = test_case.input_args
        return run_operations(operations, inputs)

    run_test_cases(TEST_CASES, run_operations_test)


# Register the problem
register_problem(
    slug="implement_trie",
    leetcode_num=208,
    title="Implement Trie (Prefix Tree)",
    difficulty=Difficulty.MEDIUM,
    category=Category.TRIES,
    solution_func=lambda: Trie(),  # Return trie instance
    test_func=test_solution,
    demo_func=create_demo_output,
)


if __name__ == "__main__":
    # Run tests
    print("Testing Implement Trie...")
    result = test_solution()
    print(f"Tests passed: {result}")

    # Show demo
    print("\n" + "=" * 50)
    print("DEMO OUTPUT")
    print("=" * 50)
    print(create_demo_output())
