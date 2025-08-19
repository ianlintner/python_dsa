"""
Top K Frequent Elements - LeetCode Problem

Given an integer array nums and an integer k, return the k most frequent elements.
You may return the answer in any order.
"""

import heapq
from collections import Counter
from typing import List

from .._registry import register_problem
from .._runner import TestCase, create_demo_output
from .._types import Category, Difficulty


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Find k most frequent elements using heap (priority queue).

        Time Complexity: O(n log k) - heap operations
        Space Complexity: O(n + k) - counter and heap storage

        Args:
            nums: List of integers
            k: Number of most frequent elements to return

        Returns:
            List[int]: K most frequent elements
        """
        # Count frequencies
        count = Counter(nums)

        # Use min heap to keep track of k most frequent
        # Store (frequency, element) pairs
        heap = []

        for num, freq in count.items():
            heapq.heappush(heap, (freq, num))
            if len(heap) > k:
                heapq.heappop(heap)

        # Extract elements from heap
        return [item[1] for item in heap]

    def topKFrequentBucketSort(self, nums: List[int], k: int) -> List[int]:
        """
        Alternative using bucket sort for O(n) solution.

        Time Complexity: O(n) - linear time
        Space Complexity: O(n) - buckets array
        """
        count = Counter(nums)

        # Create buckets where index represents frequency
        # Maximum frequency can be n (all elements same)
        buckets = [[] for _ in range(len(nums) + 1)]

        # Place elements in buckets by frequency
        for num, freq in count.items():
            buckets[freq].append(num)

        # Collect k most frequent from high frequency buckets
        result = []
        for freq in range(len(buckets) - 1, 0, -1):
            if buckets[freq]:
                result.extend(buckets[freq])
                if len(result) >= k:
                    break

        return result[:k]

    def topKFrequentQuickSelect(self, nums: List[int], k: int) -> List[int]:
        """
        Alternative using quick select for average O(n) solution.

        Time Complexity: O(n) average, O(n²) worst case
        Space Complexity: O(n) - for unique elements list
        """
        count = Counter(nums)
        unique = list(count.keys())

        def partition(left, right, pivot_index):
            pivot_frequency = count[unique[pivot_index]]
            # Move pivot to end
            unique[pivot_index], unique[right] = unique[right], unique[pivot_index]

            store_index = left
            for i in range(left, right):
                if count[unique[i]] < pivot_frequency:
                    unique[store_index], unique[i] = unique[i], unique[store_index]
                    store_index += 1

            # Move pivot to final place
            unique[right], unique[store_index] = unique[store_index], unique[right]
            return store_index

        def quickselect(left, right, k_smallest):
            if left == right:
                return

            # Select random pivot
            import random

            pivot_index = random.randint(left, right)

            # Partition around pivot
            pivot_index = partition(left, right, pivot_index)

            if k_smallest == pivot_index:
                return
            elif k_smallest < pivot_index:
                quickselect(left, pivot_index - 1, k_smallest)
            else:
                quickselect(pivot_index + 1, right, k_smallest)

        n = len(unique)
        # kth top frequent element is (n - k)th less frequent
        quickselect(0, n - 1, n - k)

        # Return top k frequent
        return unique[n - k :]


def demo():
    """Demonstrate Top K Frequent Elements solution with test cases."""
    solution = Solution()

    def sort_result(result):
        """Helper to sort result for consistent comparison."""
        return sorted(result)

    test_cases = [
        TestCase(
            input_args=([1, 1, 1, 2, 2, 3], 2), expected=[1, 2], description="Basic case with k=2"
        ),
        TestCase(input_args=([1], 1), expected=[1], description="Single element"),
        TestCase(
            input_args=([1, 2, 3, 4, 5], 3),
            expected=[1, 2, 3],
            description="All elements same frequency",
        ),
        TestCase(
            input_args=([4, 1, -1, 2, -1, 2, 3], 2),
            expected=[-1, 2],
            description="Negative numbers included",
        ),
        TestCase(
            input_args=([1, 1, 1, 2, 2, 2, 3, 3, 3], 3),
            expected=[1, 2, 3],
            description="All elements same frequency",
        ),
        TestCase(
            input_args=([5, 5, 5, 5, 1, 1, 2, 2, 3], 2),
            expected=[5, 1],
            description="Clear frequency differences",
        ),
    ]

    # Custom comparison function that handles any order
    def compare_results(actual, expected):
        return sort_result(actual) == sort_result(expected)

    results = []
    for i, test_case in enumerate(test_cases):
        try:
            import time

            start_time = time.perf_counter()
            actual = solution.topKFrequent(*test_case.input_args)
            end_time = time.perf_counter()

            passed = compare_results(actual, test_case.expected)
            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": test_case.input_args,
                    "expected": test_case.expected,
                    "actual": actual,
                    "passed": passed,
                    "time_ms": (end_time - start_time) * 1000,
                }
            )
        except Exception as e:
            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": test_case.input_args,
                    "expected": test_case.expected,
                    "actual": f"Error: {str(e)}",
                    "passed": False,
                    "time_ms": 0,
                }
            )

    # Format results as test results string
    test_results_lines = ["=== Top K Frequent Elements ===", ""]
    passed_count = 0
    total_time = sum(r["time_ms"] for r in results)

    for result in results:
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        test_results_lines.append(f"Test Case {result['test_case']}: {status}")
        test_results_lines.append(f"  Description: {result['description']}")
        test_results_lines.append(f"  Input: {result['input']}")
        test_results_lines.append(f"  Expected: {result['expected']}")
        test_results_lines.append(f"  Got: {result['actual']}")
        test_results_lines.append(f"  Time: {result['time_ms']:.3f}ms")
        test_results_lines.append("")
        if result["passed"]:
            passed_count += 1

    test_results_lines.append(f"Results: {passed_count}/{len(results)} passed")
    test_results_lines.append(f"Total time: {total_time:.3f}ms")

    if passed_count == len(results):
        test_results_lines.append("🎉 All tests passed!")
    else:
        test_results_lines.append(f"❌ {len(results) - passed_count} test(s) failed")

    test_results_str = "\n".join(test_results_lines)

    approach_notes = """
Key Insights:
• Min heap keeps track of k largest frequencies efficiently
• Counter from collections simplifies frequency counting
• Bucket sort approach achieves O(n) time complexity
• Quick select can also solve in average O(n) time

Common Pitfalls:
• Remember result can be returned in any order
• Consider edge case where k equals number of unique elements
• Min heap vs max heap choice affects implementation
• Bucket sort works well when frequency range is limited

Follow-up Questions:
• How would you optimize for very large k values?
• What if k is larger than number of unique elements?
• Can you solve in O(n) time guaranteed?
• How would you handle streaming data?
"""

    return create_demo_output(
        problem_title="Top K Frequent Elements",
        test_results=test_results_str,
        time_complexity="O(n log k) - heap operations, O(n) with bucket sort",
        space_complexity="O(n + k) - counter and heap storage",
        approach_notes=approach_notes,
    )


# Register this problem
register_problem(
    id=347,
    slug="top-k-frequent-elements",
    title="Top K Frequent Elements",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags=[
        "array",
        "hash-table",
        "divide-and-conquer",
        "sorting",
        "heap",
        "bucket-sort",
        "counting",
        "quickselect",
    ],
    url="https://leetcode.com/problems/top-k-frequent-elements/",
    notes="Heap-based solution for finding k most frequent elements",
)
