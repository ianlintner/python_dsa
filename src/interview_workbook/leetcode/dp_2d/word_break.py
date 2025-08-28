"""
LeetCode 139: Word Break

Given a string s and a dictionary of strings wordDict, return true if s can be
segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the segmentation.

Example:
    Input: s = "leetcode", wordDict = ["leet","code"]
    Output: true
    Explanation: Return true because "leetcode" can be segmented as "leet code".

    Input: s = "applepenapple", wordDict = ["apple","pen"]
    Output: true
    Explanation: Return true because "applepenapple" can be segmented as "apple pen apple".
    Note that you are allowed to reuse a dictionary word.

Constraints:
    - 1 <= s.length <= 300
    - 1 <= wordDict.length <= 1000
    - 1 <= wordDict[i].length <= 20
    - s and wordDict[i] consist of only lowercase English letters.
    - All the strings of wordDict are unique.
"""

import time
from typing import List, Tuple

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """
        Optimized 1D DP approach with set lookup.

        dp[i] represents whether s[0:i] can be segmented using wordDict.
        For each position i, we check all possible previous positions j where
        dp[j] is True and s[j:i] is in wordDict.

        Time: O(n^2 + m*k) where n=len(s), m=len(wordDict), k=avg word length
        Space: O(n + m*k) for DP array and word set
        """
        n = len(s)
        word_set = set(wordDict)  # O(1) lookup instead of O(m) list search

        # dp[i] represents if s[0:i] can be segmented
        dp = [False] * (n + 1)
        dp[0] = True  # Empty string can always be segmented

        for i in range(1, n + 1):
            for j in range(i):
                # If s[0:j] can be segmented and s[j:i] is a valid word
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break  # Found one valid segmentation, no need to check more

        return dp[n]

    def wordBreakOptimized(self, s: str, wordDict: List[str]) -> bool:
        """
        More optimized approach that only checks valid word lengths.

        Instead of checking all positions j < i, we only check positions
        that could form valid words based on the word lengths in wordDict.

        Time: O(n * L) where L is the number of unique word lengths
        Space: O(n + m*k)
        """
        n = len(s)
        word_set = set(wordDict)
        word_lengths = set(len(word) for word in wordDict)  # Unique word lengths

        dp = [False] * (n + 1)
        dp[0] = True

        for i in range(1, n + 1):
            for length in word_lengths:
                if length <= i:
                    start_pos = i - length
                    if dp[start_pos] and s[start_pos:i] in word_set:
                        dp[i] = True
                        break

        return dp[n]

    def wordBreakRecursive(self, s: str, wordDict: List[str]) -> bool:
        """
        Recursive approach with memoization.

        For each position, try all possible words that could start at that position.

        Time: O(n^2 + m*k), Space: O(n + m*k)
        """
        word_set = set(wordDict)
        memo = {}

        def canBreak(start_idx: int) -> bool:
            # Base case: reached end of string
            if start_idx == len(s):
                return True

            if start_idx in memo:
                return memo[start_idx]

            # Try all possible words starting at current position
            for end_idx in range(start_idx + 1, len(s) + 1):
                word = s[start_idx:end_idx]
                if word in word_set and canBreak(end_idx):
                    memo[start_idx] = True
                    return True

            memo[start_idx] = False
            return False

        return canBreak(0)

    def wordBreakBFS(self, s: str, wordDict: List[str]) -> bool:
        """
        BFS approach treating each valid segmentation point as a graph node.

        We explore all possible segmentation points using BFS, where each
        position in the string is a node and edges exist between positions
        that form valid words.

        Time: O(n^2 + m*k), Space: O(n + m*k)
        """
        from collections import deque

        word_set = set(wordDict)
        queue = deque([0])  # Start from position 0
        visited = set()

        while queue:
            start = queue.popleft()

            if start == len(s):
                return True

            if start in visited:
                continue
            visited.add(start)

            # Try all possible words starting at current position
            for end in range(start + 1, len(s) + 1):
                if s[start:end] in word_set:
                    queue.append(end)

        return False

    def wordBreakWithPath(self, s: str, wordDict: List[str]) -> Tuple[bool, List[str]]:
        """
        Extended version that returns both result and one valid segmentation path.

        Uses DP with backtracking to reconstruct the actual word sequence.

        Time: O(n^2 + m*k), Space: O(n + m*k)
        """
        n = len(s)
        word_set = set(wordDict)

        # dp[i] stores (can_segment, previous_position)
        dp = [None] * (n + 1)
        dp[0] = (True, -1)  # Base case: empty string

        for i in range(1, n + 1):
            dp[i] = (False, -1)
            for j in range(i):
                if dp[j][0] and s[j:i] in word_set:
                    dp[i] = (True, j)
                    break

        if not dp[n][0]:
            return False, []

        # Reconstruct the path
        path = []
        pos = n
        while pos > 0:
            prev_pos = dp[pos][1]
            path.append(s[prev_pos:pos])
            pos = prev_pos

        return True, list(reversed(path))


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different word break scenarios.
    """
    solution = Solution()

    demo_cases = [
        ("leetcode", ["leet", "code"], "Basic example"),
        ("applepenapple", ["apple", "pen"], "Word reuse example"),
        ("catsandog", ["cats", "dog", "sand", "and", "cat"], "Impossible segmentation"),
        ("cars", ["car", "ca", "rs"], "Multiple valid paths"),
        ("aaaaaaa", ["aaaa", "aaa"], "Overlapping patterns"),
        ("abcd", ["a", "abc", "b", "cd"], "Greedy vs optimal"),
        ("", ["word"], "Empty string"),
        ("a", ["a"], "Single character"),
        ("programming", ["program", "ming", "pro", "gramming"], "Long word segmentation"),
        ("raceacar", ["race", "a", "car"], "Palindrome-like structure"),
    ]

    output = ["=== Word Break (LeetCode 139) ===\n"]

    output.append("ALGORITHM EXPLANATION:")
    output.append("The Word Break problem determines if a string can be segmented into")
    output.append("dictionary words. This is a classic DP problem where we build up")
    output.append("solutions for substrings and use them to solve for longer strings.\n")

    output.append("DP STATE DEFINITION:")
    output.append("dp[i] = True if s[0:i] can be segmented using wordDict")
    output.append("Base case: dp[0] = True (empty string)")
    output.append("Recurrence:")
    output.append("  dp[i] = True if exists j < i such that:")
    output.append("    dp[j] = True AND s[j:i] in wordDict\n")

    for s, word_dict, description in demo_cases:
        output.append(f"--- {description} ---")
        output.append(f"String: '{s}' (length {len(s)})")
        output.append(f"Dictionary: {word_dict}")

        # Get results from different approaches
        result_dp = solution.wordBreak(s, word_dict)
        result_optimized = solution.wordBreakOptimized(s, word_dict)
        result_recursive = solution.wordBreakRecursive(s, word_dict)
        result_bfs = solution.wordBreakBFS(s, word_dict)
        can_break, path = solution.wordBreakWithPath(s, word_dict)

        output.append(f"Can be segmented: {result_dp}")

        if can_break and path:
            output.append(f"Example segmentation: {' '.join(path)}")
            # Verify the segmentation
            reconstructed = "".join(path)
            assert reconstructed == s, f"Invalid segmentation: {path}"

        # Verify all approaches give same result
        assert result_dp == result_optimized == result_recursive == result_bfs == can_break
        output.append("")

    # Performance comparison
    output.append("PERFORMANCE COMPARISON:")
    # Create a challenging test case
    test_s = "a" * 50  # 50 'a's
    test_dict = ["a", "aa", "aaa", "aaaa", "aaaaa"]  # Multiple word lengths

    methods = [
        ("Standard DP", solution.wordBreak),
        ("Length-optimized DP", solution.wordBreakOptimized),
        ("Recursive + Memo", solution.wordBreakRecursive),
        ("BFS approach", solution.wordBreakBFS),
    ]

    for name, method in methods:
        start_time = time.perf_counter()
        result = method(test_s, test_dict)
        end_time = time.perf_counter()

        output.append(
            f"{name:20} | Result: {str(result):5} | Time: {(end_time - start_time) * 1000:.3f}ms"
        )

    output.append("\nSPACE COMPLEXITY ANALYSIS:")
    output.append("• Standard DP: O(n) for DP array + O(m*k) for word set")
    output.append("• Length-optimized: O(n) + O(m*k) + O(L) for length set")
    output.append("• Recursive: O(n) for memoization + O(n) recursion stack")
    output.append("• BFS: O(n) for queue and visited set + O(m*k) for word set")

    output.append("\nREAL-WORLD APPLICATIONS:")
    output.append("• Natural language processing and tokenization")
    output.append("• URL parsing and validation")
    output.append("• Code parsing in compilers and interpreters")
    output.append("• DNA sequence analysis in bioinformatics")
    output.append("• Text processing and word boundary detection")
    output.append("• Search query processing and auto-completion")
    output.append("• License plate recognition systems")

    # Visual example of DP progression
    output.append("\nDP PROGRESSION EXAMPLE (s='leetcode', dict=['leet','code']):")
    s_example = "leetcode"
    dict_example = ["leet", "code"]
    word_set = set(dict_example)
    n = len(s_example)
    dp = [False] * (n + 1)
    dp[0] = True

    output.append("Position:  0  1  2  3  4  5  6  7  8")
    output.append(f"String:      {' '.join(s_example)}")
    output.append("DP table:")

    # Show step by step DP computation
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s_example[j:i] in word_set:
                dp[i] = True
                break

        # Show current state
        dp_str = " ".join("T" if dp[k] else "F" for k in range(i + 1))
        output.append(f"Step {i:2}: {dp_str}")
        if dp[i]:
            # Find which segmentation made this true
            for j in range(i):
                if dp[j] and s_example[j:i] in word_set:
                    output.append(f"        Found word '{s_example[j:i]}' at position {j}-{i}")
                    break

    output.append(f"\nFinal result: {dp[n]} - String can be segmented!")

    output.append("\nALGORITHM VARIANTS:")
    output.append("• Word Break II: Find all possible segmentations")
    output.append("• Word Break with minimum cuts: Find segmentation with fewest words")
    output.append("• Palindrome partitioning: Similar DP pattern for palindromes")
    output.append("• Sentence segmentation without spaces")

    return "\n".join(output)


# Test cases covering various scenarios
TEST_CASES = [
    TestCase(
        input_args=("leetcode", ["leet", "code"],
    ),
        expected=True,
        description="Basic word break example",
    ),
    TestCase(
        input_args=("applepenapple", ["apple", "pen"],
    ),
        expected=True,
        description="Word reuse allowed",
    ),
    TestCase(
        input_args=("catsandog", ["cats", "dog", "sand", "and", "cat"],
    ),
        expected=False,
        description="Impossible to segment",
    ),
    TestCase(
        input_args=("", ["word"],
    ), expected=True, description="Empty string - always true"),
    TestCase(
        input_args=("a", ["a"],
    ), expected=True, description="Single character match"),
    TestCase(
        input_args=("a", ["b"],
    ), expected=False, description="Single character no match"),
    TestCase(
        input_args=("cars", ["car", "ca", "rs"],
    ),
        expected=True,
        description="Multiple valid segmentations",
    ),
    TestCase(
        input_args=("aaaaaaa", ["aaaa", "aaa"],
    ),
        expected=True,
        description="Overlapping word patterns",
    ),
    TestCase(
        input_args=("abcd", ["a", "abc", "b", "cd"],
    ),
        expected=True,
        description="Greedy might fail, DP works",
    ),
    TestCase(
        input_args=("bb", ["a", "b", "bbb", "bbbb"],
    ),
        expected=True,
        description="Multiple b's can be segmented as b + b",
    ),
    TestCase(
        input_args=(
            "fohhemkkaecojceoaejkkoedkofhmohkcjmkggcmnami",
            [
                "kfomka",
                "hecagbngambii",
                "anobmnikj",
                "c",
                "nnkmfelneemfgcl",
                "ah",
                "bgomgohl",
                "lcbjbg",
                "ebjfoiddndih",
                "hjknoamjbfhckb",
                "eioldlijmmla",
                "nbekmcnakif",
                "fgahmihodolmhbi",
                "gnjfe",
                "hk",
                "b",
                "jbfgm",
                "ecojceoaejkkoed",
                "cemodhmbcmgl",
                "j",
                "gdcnjj",
                "kolaijoicbc",
                "liibjjcini",
                "lmbenj",
                "eklingemgdjncaa",
                "m",
                "hkh",
                "fblb",
                "fk",
                "nnfkfanaga",
                "eldjml",
                "iejn",
                "gbmjfdooeeko",
                "jafogijka",
                "ngnfggojmhclkjd",
                "bfagnfclg",
                "imkeobcdidiifbm",
                "ogeo",
                "gicjog",
                "cjnibenelm",
                "ogoloc",
                "edciifkaff",
                "kbeeg",
                "nebn",
                "jdd",
                "aeojhccngebk",
                "io",
                "naj",
                "ckb",
                "hamijoiggj",
                "cgd",
            ],,
    ),
        expected=False,
        description="Complex LeetCode test case",
    ),
    TestCase(
        input_args=("goalspecial", ["go", "goal", "goals", "special"],
    ),
        expected=True,
        description="Prefix overlap case",
    ),
    TestCase(
        input_args=("abcdef", ["abc", "def"],
    ), expected=True, description="Perfect two-word split"
    ),
    TestCase(
        input_args=("programming", ["program", "ming"],
    ),
        expected=True,
        description="Simple two-word case",
    ),
    TestCase(
        input_args=("dddddd", ["dd", "ddd"],
    ),
        expected=True,
        description="Repeated pattern segmentation",
    ),
]


def test_solution():
    """Test the solution with various test cases."""
    solution = Solution()

    def test_function(s: str, word_dict: List[str]) -> bool:
        # Test all approaches give same result
        result1 = solution.wordBreak(s, word_dict)
        result2 = solution.wordBreakOptimized(s, word_dict)
        result3 = solution.wordBreakRecursive(s, word_dict)
        result4 = solution.wordBreakBFS(s, word_dict)

        assert (
            result1 == result2 == result3 == result4
        ), f"Inconsistent results: {result1}, {result2}, {result3}, {result4}"
        return result1

    run_test_cases(test_function, TEST_CASES)


# Register the problem
register_problem(
    slug="word-break",
    leetcode_num=139,
    title="Word Break",
    difficulty=Difficulty.MEDIUM,
    category=Category.DP_2D,
    solution_func=Solution().wordBreak,
    test_func=test_solution,
    demo_func=create_demo_output,
)
