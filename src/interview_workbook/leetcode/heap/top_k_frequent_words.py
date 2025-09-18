"""
Top K Frequent Words

TODO: Add problem description
"""

import heapq
import random
from collections import Counter

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


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
    outputs = []

    # First example
    words = ["i", "love", "leetcode", "i", "love", "coding"]
    k = 2
    sol = Solution()
    result = sol.top_k_frequent(words, k)
    out1 = f"Words: {words}, K: {k}, Top K Frequent: {result}"
    print(out1)
    outputs.append(out1)

    # Second example
    words2 = ["apple", "banana", "apple", "orange", "banana", "apple"]
    k2 = 2
    result2 = sol.top_k_frequent(words2, k2)
    out2 = f"Words: {words2}, K: {k2}, Top K Frequent: {result2}"
    print(out2)
    outputs.append(out2)

    return "\n".join(outputs)


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

if __name__ == "__main__":
    demo()
