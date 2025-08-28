"""
LeetCode 692: Top K Frequent Words

Given an array of strings words and an integer k, return the k most frequent strings.

Return the answer sorted by the frequency from highest to lowest. 
Sort the words with the same frequency by their lexicographical order.

Examples:
    Input: words = ["i","love","leetcode","i","love","coding"], k = 2
    Output: ["i","love"]

    Input: words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4
    Output: ["the","is","sunny","day"]

Constraints:
    1 <= words.length <= 500
    1 <= words[i].length <= 10
    words[i] consists of lowercase English letters.
    k is in the range [1, the number of unique words]
"""

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty
from typing import List
from collections import Counter
import heapq


class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        """
        Find k most frequent words using min-heap approach.
        
        Algorithm:
        1. Count frequency of each word using Counter
        2. Use min-heap to maintain k most frequent words
        3. For equal frequencies, maintain lexicographical order
        4. Use custom comparison in heap (frequency, reverse lexicographical)
        
        Time Complexity: O(n log k) where n is number of words
        Space Complexity: O(n) for counter + O(k) for heap
        """
        # Count frequencies
        word_count = Counter(words)
        
        # Min-heap to maintain k most frequent words
        # Use tuple: (frequency, word) where word is compared lexicographically
        # For min-heap behavior with max frequencies, we need to negate frequency
        # For lexicographical order with same frequency, we want smaller words first
        heap = []
        
        for word, freq in word_count.items():
            if len(heap) < k:
                # Push (freq, word) - heap will compare freq first, then word lexicographically
                heapq.heappush(heap, (freq, word))
            elif freq > heap[0][0] or (freq == heap[0][0] and word < heap[0][1]):
                # If current word has higher frequency OR same frequency but lexicographically smaller
                heapq.heapreplace(heap, (freq, word))
        
        # Extract words from heap and sort by frequency (desc) then lexicographically (asc)
        result = []
        while heap:
            freq, word = heapq.heappop(heap)
            result.append(word)
        
        # Reverse to get highest frequency first, then sort by criteria
        result.reverse()
        
        # Sort the result by frequency (descending) and lexicographically (ascending)
        word_freq_map = {word: word_count[word] for word in result}
        result.sort(key=lambda word: (-word_freq_map[word], word))
        
        return result
    
    def topKFrequentSorting(self, words: List[str], k: int) -> List[str]:
        """
        Alternative approach using sorting.
        
        Algorithm:
        1. Count word frequencies
        2. Sort by frequency (descending) and lexicographically (ascending)
        3. Return first k elements
        
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        word_count = Counter(words)
        
        # Sort by frequency (descending) then lexicographically (ascending)
        sorted_words = sorted(word_count.keys(), key=lambda word: (-word_count[word], word))
        
        return sorted_words[:k]
    
    def topKFrequentHeapOptimized(self, words: List[str], k: int) -> List[str]:
        """
        Optimized heap approach with proper comparison.
        
        Algorithm:
        1. Count frequencies
        2. Use min-heap with custom comparison for tie-breaking
        3. Maintain exactly k elements in heap
        
        Time Complexity: O(n log k)
        Space Complexity: O(n)
        """
        word_count = Counter(words)
        
        # Create a custom class for heap comparison
        class WordFreq:
            def __init__(self, freq, word):
                self.freq = freq
                self.word = word
            
            def __lt__(self, other):
                # Min-heap: smaller elements first
                # For min-heap of k largest, we want:
                # - Lower frequency first (so higher freq stays in heap)
                # - For same frequency, lexicographically larger first 
                #   (so lexicographically smaller stays in heap)
                if self.freq != other.freq:
                    return self.freq < other.freq
                return self.word > other.word
        
        heap = []
        for word, freq in word_count.items():
            if len(heap) < k:
                heapq.heappush(heap, WordFreq(freq, word))
            else:
                # Compare with the minimum element
                if freq > heap[0].freq or (freq == heap[0].freq and word < heap[0].word):
                    heapq.heapreplace(heap, WordFreq(freq, word))
        
        # Extract and sort result
        result = [(item.freq, item.word) for item in heap]
        result.sort(key=lambda x: (-x[0], x[1]))  # Sort by freq desc, word asc
        
        return [word for freq, word in result]


def create_demo_output() -> str:
    """Create comprehensive demo showing different approaches and analysis."""
    solution = Solution()
    
    # Test cases for demonstration
    test_cases = [
        (["i","love","leetcode","i","love","coding"], 2, "Basic example"),
        (["the","day","is","sunny","the","the","the","sunny","is","is"], 4, "Multiple frequencies"),
        (["a", "aa", "aaa"], 3, "Lexicographical ordering"),
        (["apple","banana","apple","orange","banana","apple"], 2, "Simple frequency test"),
        (["word"], 1, "Single word")
    ]
    
    output = []
    output.append("=== LeetCode 692: Top K Frequent Words ===\n")
    
    for words, k, desc in test_cases:
        output.append(f"Test: {desc}")
        output.append(f"Input: words = {words}, k = {k}")
        
        # Show frequency analysis
        word_count = Counter(words)
        output.append(f"Frequencies: {dict(word_count)}")
        
        # Test all approaches
        result1 = solution.topKFrequent(words, k)
        result2 = solution.topKFrequentSorting(words, k)
        result3 = solution.topKFrequentHeapOptimized(words, k)
        
        output.append(f"Min-Heap approach: {result1}")
        output.append(f"Sorting approach: {result2}")
        output.append(f"Optimized Heap: {result3}")
        output.append("")
    
    # Performance analysis
    output.append("=== Performance Analysis ===")
    output.append("Min-Heap Approach:")
    output.append("  • Time: O(n log k) - Process n words, maintain k-size heap")
    output.append("  • Space: O(n + k) - Counter storage + heap")
    output.append("  • Best for: k << n (small k values)")
    output.append("")
    
    output.append("Sorting Approach:")
    output.append("  • Time: O(n log n) - Count + sort all unique words")
    output.append("  • Space: O(n) - Counter storage")
    output.append("  • Best for: Simple implementation, all frequencies needed")
    output.append("")
    
    output.append("Optimized Heap Approach:")
    output.append("  • Time: O(n log k) - Clean heap operations")
    output.append("  • Space: O(n + k) - Counter + heap with custom objects")
    output.append("  • Best for: Clean code with proper comparisons")
    output.append("")
    
    # Algorithm insights
    output.append("=== Key Insights ===")
    output.append("1. **Frequency Counting**: Use Counter for O(1) frequency lookups")
    output.append("2. **Heap Comparison**: Custom comparison for frequency + lexicographical order")
    output.append("3. **Tie-breaking**: Same frequency words sorted lexicographically")
    output.append("4. **Space Optimization**: Min-heap approach saves space when k << n")
    output.append("")
    
    # Edge cases
    output.append("=== Edge Cases & Considerations ===")
    output.append("• **Single characters**: Handle lexicographical ordering correctly")
    output.append("• **All same frequency**: Pure lexicographical sorting")
    output.append("• **k equals unique count**: Return all words in correct order")
    output.append("• **Memory constraints**: Choose heap vs sorting based on k vs n")
    output.append("")
    
    # Real-world applications
    output.append("=== Real-World Applications ===")
    output.append("• **Search Engines**: Top search terms analysis")
    output.append("• **Social Media**: Trending hashtags and keywords")
    output.append("• **Document Analysis**: Most frequent terms in corpus")
    output.append("• **Log Analysis**: Most common error messages or events")
    output.append("• **E-commerce**: Popular product categories or search terms")
    
    return "\n".join(output)


# Test cases
TEST_CASES = [
    TestCase(
        input_data={"words": ["i","love","leetcode","i","love","coding"], "k": 2},
        expected=["i","love"],
        description="Basic example with clear frequency differences"
    ),
    TestCase(
        input_data={"words": ["the","day","is","sunny","the","the","the","sunny","is","is"], "k": 4},
        expected=["the","is","sunny","day"],
        description="Multiple frequency levels with lexicographical ties"
    ),
    TestCase(
        input_data={"words": ["a", "aa", "aaa"], "k": 3},
        expected=["a","aa","aaa"],
        description="All same frequency - pure lexicographical order"
    ),
    TestCase(
        input_data={"words": ["apple","banana","apple","orange","banana","apple"], "k": 2},
        expected=["apple","banana"],
        description="Simple frequency ranking"
    ),
    TestCase(
        input_data={"words": ["word"], "k": 1},
        expected=["word"],
        description="Single word input"
    ),
    TestCase(
        input_data={"words": ["a","b","a","c","b","a"], "k": 3},
        expected=["a","b","c"],
        description="Mixed frequencies with lexicographical ordering"
    ),
    TestCase(
        input_data={"words": ["love","coding","love"], "k": 2},
        expected=["love","coding"],
        description="Two different frequencies"
    ),
    TestCase(
        input_data={"words": ["aaa","aa","a"], "k": 1},
        expected=["a"],
        description="Lexicographical ordering - shortest first"
    )
]


def test_solution():
    """Test all solution approaches."""
    solution = Solution()
    
    def run_tests(func_name: str, func):
        print(f"\nTesting {func_name}:")
        for i, test_case in enumerate(TEST_CASES):
            result = func(test_case.input_data["words"], test_case.input_data["k"])
            status = "✓" if result == test_case.expected else "✗"
            print(f"  Test {i+1}: {status} - {test_case.description}")
            if result != test_case.expected:
                print(f"    Expected: {test_case.expected}, Got: {result}")
    
    run_tests("Min-Heap Approach", solution.topKFrequent)
    run_tests("Sorting Approach", solution.topKFrequentSorting)
    run_tests("Optimized Heap", solution.topKFrequentHeapOptimized)
    
    # Run standard test framework
    run_test_cases(TEST_CASES, lambda tc: solution.topKFrequent(
        tc.input_data["words"], tc.input_data["k"]
    ))


# Register the problem
register_problem(
    slug="top_k_frequent_words",
    leetcode_num=692,
    title="Top K Frequent Words",
    difficulty=Difficulty.MEDIUM,
    category=Category.HEAP,
    solution_func=lambda words, k: Solution().topKFrequent(words, k),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["heap", "hash-table", "string", "trie", "sorting", "bucket-sort"],
    notes="Heap problem with custom comparison for frequency and lexicographical ordering"
)
