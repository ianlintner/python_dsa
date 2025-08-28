"""
LeetCode 215: Kth Largest Element in an Array

Given an integer array nums and an integer k, return the kth largest element in the array.
Note that it is the kth largest element in the sorted order, not the kth distinct element.

You must solve it in O(n) time complexity.

Examples:
    Input: nums = [3,2,1,5,6,4], k = 2
    Output: 5

    Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
    Output: 4

Constraints:
    1 <= k <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4
"""

import heapq
import random
from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        Find kth largest element using min-heap approach.

        Algorithm:
        1. Use a min-heap of size k to track the k largest elements
        2. For each number, if heap size < k, push to heap
        3. If heap size == k and num > heap top, pop and push num
        4. The root of the heap will be the kth largest element

        Time Complexity: O(n log k)
        Space Complexity: O(k)
        """
        # Min-heap to maintain k largest elements
        heap = []

        for num in nums:
            if len(heap) < k:
                heapq.heappush(heap, num)
            elif num > heap[0]:
                heapq.heapreplace(heap, num)

        return heap[0]

    def findKthLargestMaxHeap(self, nums: List[int], k: int) -> int:
        """
        Alternative approach using max-heap (negated values).

        Algorithm:
        1. Convert all numbers to negative to simulate max-heap
        2. Build heap from all elements
        3. Pop k-1 times to get the kth largest

        Time Complexity: O(n + k log n)
        Space Complexity: O(n)
        """
        # Convert to max-heap by negating values
        max_heap = [-num for num in nums]
        heapq.heapify(max_heap)

        # Pop k-1 times to get kth largest
        for _ in range(k - 1):
            heapq.heappop(max_heap)

        return -max_heap[0]

    def findKthLargestQuickSelect(self, nums: List[int], k: int) -> int:
        """
        Quickselect approach for O(n) average time complexity.

        Algorithm:
        1. Use partition algorithm from quicksort
        2. Partition around a pivot element
        3. If partition index == n-k, we found the answer
        4. Otherwise, recursively search left or right partition

        Time Complexity: O(n) average, O(n²) worst case
        Space Complexity: O(1) iterative version
        """

        def partition(left: int, right: int, pivot_idx: int) -> int:
            pivot = nums[pivot_idx]
            # Move pivot to end
            nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

            # Partition around pivot
            store_idx = left
            for i in range(left, right):
                if nums[i] < pivot:
                    nums[store_idx], nums[i] = nums[i], nums[store_idx]
                    store_idx += 1

            # Move pivot to final position
            nums[right], nums[store_idx] = nums[store_idx], nums[right]
            return store_idx

        def quickselect(left: int, right: int, k_smallest: int) -> int:
            if left == right:
                return nums[left]

            # Choose random pivot to avoid worst case
            pivot_idx = random.randint(left, right)
            pivot_idx = partition(left, right, pivot_idx)

            if k_smallest == pivot_idx:
                return nums[k_smallest]
            elif k_smallest < pivot_idx:
                return quickselect(left, pivot_idx - 1, k_smallest)
            else:
                return quickselect(pivot_idx + 1, right, k_smallest)

        # Convert to 0-indexed position for kth largest
        return quickselect(0, len(nums) - 1, len(nums) - k)


def create_demo_output() -> str:
    """Create comprehensive demo showing different approaches and performance."""
    solution = Solution()

    # Test cases for demonstration
    test_cases = [
        ([3, 2, 1, 5, 6, 4], 2, "Basic example"),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, "With duplicates"),
        ([1], 1, "Single element"),
        ([7, 10, 4, 3, 20, 15], 3, "Medium array"),
        ([-1, 2, 0], 1, "With negative numbers"),
    ]

    output = []
    output.append("=== LeetCode 215: Kth Largest Element in an Array ===\n")

    for nums, k, desc in test_cases:
        output.append(f"Test: {desc}")
        output.append(f"Input: nums = {nums}, k = {k}")

        # Test all three approaches
        nums_copy1 = nums.copy()
        nums_copy2 = nums.copy()
        nums_copy3 = nums.copy()

        result1 = solution.findKthLargest(nums_copy1, k)
        result2 = solution.findKthLargestMaxHeap(nums_copy2, k)
        result3 = solution.findKthLargestQuickSelect(nums_copy3, k)

        output.append(f"Min-Heap approach: {result1}")
        output.append(f"Max-Heap approach: {result2}")
        output.append(f"QuickSelect approach: {result3}")
        output.append(f"Sorted verification: {sorted(nums, reverse=True)[k - 1]}")
        output.append("")

    # Performance analysis
    output.append("=== Performance Analysis ===")
    output.append("Min-Heap Approach:")
    output.append("  • Time: O(n log k) - Only maintain k elements")
    output.append("  • Space: O(k) - Minimal space usage")
    output.append("  • Best for: k << n (small k)")
    output.append("")

    output.append("Max-Heap Approach:")
    output.append("  • Time: O(n + k log n) - Build heap + k pops")
    output.append("  • Space: O(n) - Store all elements")
    output.append("  • Best for: Multiple queries")
    output.append("")

    output.append("QuickSelect Approach:")
    output.append("  • Time: O(n) average, O(n²) worst case")
    output.append("  • Space: O(1) - In-place partitioning")
    output.append("  • Best for: Single query, guaranteed O(n)")
    output.append("")

    # Algorithm insights
    output.append("=== Key Insights ===")
    output.append(
        "1. **Heap Selection**: Use min-heap when k is small, max-heap for multiple queries"
    )
    output.append("2. **QuickSelect**: Optimal for single query with O(n) average time")
    output.append("3. **Trade-offs**: Memory vs time vs implementation complexity")
    output.append("4. **Stability**: Min-heap approach preserves original array")
    output.append("")

    # Real-world applications
    output.append("=== Real-World Applications ===")
    output.append("• **Data Analytics**: Finding top-k performing metrics")
    output.append("• **Recommendation Systems**: Top-k relevant items")
    output.append("• **Resource Allocation**: Priority-based scheduling")
    output.append("• **Statistical Analysis**: Percentile calculations")

    return "\n".join(output)


# Test cases
TEST_CASES = [
    TestCase(
        input_args={"nums": [3, 2, 1, 5, 6, 4],
        expected="k": 2},
        expected=5,
        description="Basic example - 2nd largest element",
    ),
    TestCase(
        input_args={"nums": [3, 2, 3, 1, 2, 4, 5, 5, 6],
        expected="k": 4},
        expected=4,
        description="Array with duplicates - 4th largest",
    ),
    TestCase(
        input_args={"nums": [1],
        expected="k": 1},
        expected=1,
        description="Single element array",
    ),
    TestCase(
        input_args={"nums": [7, 10, 4, 3, 20, 15],
        expected="k": 3},
        expected=10,
        description="Medium array - 3rd largest",
    ),
    TestCase(
        input_args={"nums": [-1, 2, 0],
        expected="k": 1},
        expected=2,
        description="Array with negative numbers",
    ),
    TestCase(
        input_args={"nums": [1, 2, 3, 4, 5],
        expected="k": 5},
        expected=1,
        description="Kth largest is minimum element",
    ),
    TestCase(
        input_args={"nums": [5, 4, 3, 2, 1],
        expected="k": 1},
        expected=5,
        description="Already sorted descending - 1st largest",
    ),
    TestCase(
        input_args={"nums": [3, 3, 3, 3, 3],
        expected="k": 2},
        expected=3,
        description="All elements same",
    ),
]


def test_solution():
    """Test all solution approaches."""
    solution = Solution()

    def run_tests(func_name: str, func):
        print(f"\nTesting {func_name}:")
        for i, test_case in enumerate(TEST_CASES):
            nums_copy = test_case.input_data["nums"].copy()
            result = func(nums_copy, test_case.input_data["k"])
            status = "✓" if result == test_case.expected else "✗"
            print(f"  Test {i + 1}: {status} - {test_case.description}")
            if result != test_case.expected:
                print(f"    Expected: {test_case.expected}, Got: {result}")

    run_tests("Min-Heap Approach", solution.findKthLargest)
    run_tests("Max-Heap Approach", solution.findKthLargestMaxHeap)
    run_tests("QuickSelect Approach", solution.findKthLargestQuickSelect)

    # Run standard test framework
    run_test_cases(
        TEST_CASES,
        lambda tc: solution.findKthLargest(tc.input_data["nums"].copy(), tc.input_data["k"]),
    )


# Register the problem
register_problem(
    slug="kth_largest_element",
    leetcode_num=215,
    title="Kth Largest Element in an Array",
    difficulty=Difficulty.MEDIUM,
    category=Category.HEAP,
    solution_func=lambda nums, k: Solution().findKthLargest(nums, k),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["heap", "quickselect", "sorting", "divide-conquer"],
    notes="Classic heap problem with multiple optimal approaches",
)
