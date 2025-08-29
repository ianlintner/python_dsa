"""
Top K Frequent Words

TODO: Add problem description
"""


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


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="top_k_frequent_words",
#     title="Top K Frequent Words",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
