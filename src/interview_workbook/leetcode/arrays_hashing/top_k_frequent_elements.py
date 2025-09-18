"""
LeetCode 347: Top K Frequent Elements

Given an integer array nums and an integer k, return the k most frequent elements.
You may return the answer in any order.

Example 1:
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]

Example 2:
Input: nums = [1], k = 1
Output: [1]

URL: https://leetcode.com/problems/top-k-frequent-elements/
Difficulty: Medium
Category: Array & Hashing

Patterns:
- Hash map for counting frequencies
- Heap for finding top k elements
- Bucket sort for O(n) solution

Complexity:
- Time: O(n log k) with heap, O(n) with bucket sort
- Space: O(n) for hash map and result

Key Insights:
- Count frequencies first with hash map
- Use min heap of size k for efficient top k selection
- Bucket sort approach: group by frequency for O(n) time
- Python Counter and heapq modules are helpful

Edge Cases:
- k equals array length (return all unique elements)
- All elements have same frequency
- Single element array
"""

import heapq
from collections import Counter
from typing import List

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Find k most frequent elements using heap approach.

        Args:
            nums: List of integers
            k: Number of most frequent elements to return

        Returns:
            List of k most frequent elements
        """
        # Count frequencies
        count = Counter(nums)

        # Use heap to find top k frequent
        # nlargest returns k largest elements
        return heapq.nlargest(k, count.keys(), key=count.get)

    def topKFrequentBucketSort(self, nums: List[int], k: int) -> List[int]:
        """
        Alternative O(n) solution using bucket sort by frequency.

        Args:
            nums: List of integers
            k: Number of most frequent elements to return

        Returns:
            List of k most frequent elements
        """
        count = Counter(nums)

        # Create buckets for each frequency (0 to len(nums))
        buckets = [[] for _ in range(len(nums) + 1)]

        # Place elements in buckets based on their frequency
        for num, freq in count.items():
            buckets[freq].append(num)

        # Collect top k elements from highest frequency buckets
        result = []
        for i in range(len(buckets) - 1, -1, -1):
            for num in buckets[i]:
                result.append(num)
                if len(result) == k:
                    return result

        return result


def demo():
    """Run Top K Frequent Elements demo with test cases."""
    test_cases = [
        TestCase(input_args=([1, 1, 1, 2, 2, 3], 2), expected=[1, 2]),
        TestCase(input_args=([1], 1), expected=[1]),
        TestCase(input_args=([1, 2], 2), expected=[1, 2]),
        TestCase(input_args=([4, 1, -1, 2, -1, 2, 3], 2), expected=[-1, 2]),
        TestCase(input_args=([3, 0, 1, 0], 1), expected=[0]),
    ]

    def test_top_k_frequent(args):
        nums, k = args
        return Solution().topKFrequent(nums, k)

    test_results = run_test_cases(
        test_top_k_frequent, test_cases, "LeetCode 347: Top K Frequent Elements"
    )
    print("\n".join(test_results))

    return create_demo_output(
        "Top K Frequent Elements",
        test_results,
        time_complexity="O(n log k)",
        space_complexity="O(n)",
        approach_notes="""
Two main approaches:

1. Heap approach (implemented):
   - Count frequencies with Counter
   - Use heapq.nlargest() to get top k elements
   - Time: O(n log k), Space: O(n)

2. Bucket sort approach:
   - Create buckets for each possible frequency
   - Group elements by their frequency
   - Collect from highest frequency buckets
   - Time: O(n), Space: O(n)

The heap approach is simpler and works well for most cases.
Bucket sort is optimal for time complexity but uses more space.
        """.strip(),
    )


# Register the problem
register_problem(
    id=347,
    slug="top_k_frequent_elements",
    title="Top K Frequent Elements",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags=[
        "array",
        "hash-table",
        "divide-and-conquer",
        "sorting",
        "heap-priority-queue",
        "bucket-sort",
        "counting",
        "quickselect",
    ],
    url="https://leetcode.com/problems/top-k-frequent-elements/",
    notes="Classic problem for heap usage and frequency analysis",
)
