"""
Top K Frequent Words

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


import heapq
from collections import Counter
import random


class Solution:
    def top_k_frequent(self, words: list[str], k: int) -> list[str]:
        """
        Return the k most frequent words sorted by frequency and lexicographic order.
        """
        counts = Counter(words)
        # min-heap with custom ordering
        heap = [(-freq, word) for word, freq in counts.items()]
        heapq.heapify(heap)

        result = []
        for _ in range(k):
            if heap:
                freq, word = heapq.heappop(heap)
                result.append(word)
        return result


def demo() -> str:
    """Demonstration of Top K Frequent Words with deterministic seeding."""
    random.seed(0)
    words = ["i", "love", "leetcode", "i", "love", "coding"]
    k = 2
    sol = Solution()
    result = sol.top_k_frequent(words, k)
    return f"Words: {words}, K: {k}, Top K Frequent: {result}"


register_problem(
    id=692,
    slug="top_k_frequent_words",
    title="Top K Frequent Words",
    category=Category.HEAP,
    difficulty=Difficulty.MEDIUM,
    tags=["string", "hashmap", "heap", "sorting"],
    url="https://leetcode.com/problems/top-k-frequent-words/",
    notes="",
)
