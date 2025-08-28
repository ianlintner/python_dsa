"""
LeetCode 295: Find Median from Data Stream

The median is the middle value in an ordered integer list. If the size of the list is even,
there is no middle value, and the median is the mean of the two middle values.

Implement the MedianFinder class:
- MedianFinder() initializes the MedianFinder object.
- void addNum(int num) adds the integer num from the data stream to the data structure.
- double findMedian() returns the median of all elements so far.

Examples:
    Input: ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
           [[], [1], [2], [], [3], []]
    Output: [null, null, null, 1.5, null, 2.0]

Constraints:
    -10^5 <= num <= 10^5
    There will be at least one element in the data structure before calling findMedian.
    At most 5 * 10^4 calls will be made to addNum and findMedian.
"""

import heapq

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class MedianFinder:
    """
    Two-heap approach for maintaining running median.

    Algorithm:
    1. Use max-heap (left half) and min-heap (right half)
    2. Max-heap contains smaller half, min-heap contains larger half
    3. Maintain size constraint: len(max_heap) >= len(min_heap)
    4. Median is either max_heap top (odd total) or average of both tops (even total)

    Time Complexity:
    - addNum: O(log n) - heap operations
    - findMedian: O(1) - constant time access to tops
    Space Complexity: O(n) - store all numbers
    """

    def __init__(self):
        """Initialize the data structure."""
        # Max-heap for smaller half (use negative values for max behavior)
        self.max_heap = []  # Contains smaller half of numbers
        # Min-heap for larger half
        self.min_heap = []  # Contains larger half of numbers

    def addNum(self, num: int) -> None:
        """
        Add a number to the data structure.

        Strategy:
        1. Always add to max_heap first
        2. Move the largest from max_heap to min_heap
        3. If min_heap becomes larger, move its smallest back to max_heap

        This ensures: len(max_heap) >= len(min_heap) and proper ordering
        """
        # Add to max-heap (negate for max behavior with min-heap)
        heapq.heappush(self.max_heap, -num)

        # Move the largest element from max_heap to min_heap
        if self.max_heap:
            largest_in_left = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, largest_in_left)

        # Rebalance if min_heap becomes larger than max_heap
        if len(self.min_heap) > len(self.max_heap):
            smallest_in_right = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -smallest_in_right)

    def findMedian(self) -> float:
        """
        Return the median of all elements.

        Cases:
        1. If total count is odd: return top of max_heap (larger heap)
        2. If total count is even: return average of both heap tops
        """
        if len(self.max_heap) > len(self.min_heap):
            # Odd total count - median is top of max_heap
            return float(-self.max_heap[0])
        else:
            # Even total count - median is average of both tops
            left_median = -self.max_heap[0]
            right_median = self.min_heap[0]
            return (left_median + right_median) / 2.0


class MedianFinderAlternative:
    """
    Alternative implementation with explicit size tracking.
    """

    def __init__(self):
        self.max_heap = []  # Left half (smaller numbers)
        self.min_heap = []  # Right half (larger numbers)
        self.count = 0

    def addNum(self, num: int) -> None:
        """Add number with explicit balancing logic."""
        self.count += 1

        # Add to appropriate heap based on current medians
        if not self.max_heap or num <= -self.max_heap[0]:
            heapq.heappush(self.max_heap, -num)
        else:
            heapq.heappush(self.min_heap, num)

        # Rebalance heaps
        self._rebalance()

    def _rebalance(self):
        """Ensure heap sizes differ by at most 1, with max_heap having equal or +1."""
        if len(self.max_heap) > len(self.min_heap) + 1:
            # Move from max_heap to min_heap
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        elif len(self.min_heap) > len(self.max_heap):
            # Move from min_heap to max_heap
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)

    def findMedian(self) -> float:
        """Find median with explicit count checking."""
        if self.count % 2 == 1:
            # Odd count - median is in max_heap (guaranteed to have +1 element)
            return float(-self.max_heap[0])
        else:
            # Even count - average of both heap tops
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0


def create_demo_output() -> str:
    """Create comprehensive demo showing MedianFinder usage and analysis."""
    output = []
    output.append("=== LeetCode 295: Find Median from Data Stream ===\n")

    # Demo 1: Basic usage
    output.append("=== Demo 1: Basic Usage ===")
    median_finder = MedianFinder()
    operations = [1, 2, 3, 4, 5]

    output.append("Operations: addNum(1), addNum(2), findMedian(), addNum(3), findMedian()")
    for i, num in enumerate(operations):
        median_finder.addNum(num)
        median = median_finder.findMedian()
        output.append(f"After adding {num}: median = {median}")

        # Show heap states for understanding
        max_heap_vals = [-x for x in median_finder.max_heap]
        min_heap_vals = list(median_finder.min_heap)
        output.append(f"  Max-heap (left): {sorted(max_heap_vals, reverse=True)}")
        output.append(f"  Min-heap (right): {sorted(min_heap_vals)}")
        output.append("")

    # Demo 2: Edge cases
    output.append("=== Demo 2: Edge Cases ===")

    # Single element
    mf_single = MedianFinder()
    mf_single.addNum(5)
    output.append(f"Single element (5): median = {mf_single.findMedian()}")

    # Two elements
    mf_two = MedianFinder()
    mf_two.addNum(1)
    mf_two.addNum(3)
    output.append(f"Two elements (1,3): median = {mf_two.findMedian()}")

    # Negative numbers
    mf_neg = MedianFinder()
    for num in [-1, -2, 0, 1, 2]:
        mf_neg.addNum(num)
    output.append(f"Mixed signs (-1,-2,0,1,2): median = {mf_neg.findMedian()}")
    output.append("")

    # Demo 3: Performance comparison
    output.append("=== Demo 3: Algorithm Analysis ===")

    # Simulate large stream
    import time

    mf = MedianFinder()
    test_nums = list(range(1000, 0, -1))  # Reverse order for worst-case

    start_time = time.time()
    for num in test_nums[:100]:  # Sample for demo
        mf.addNum(num)
    end_time = time.time()

    output.append("Added 100 numbers in reverse order")
    output.append(f"Time taken: {(end_time - start_time) * 1000:.2f} ms")
    output.append(f"Final median: {mf.findMedian()}")
    output.append("")

    # Algorithm comparison
    output.append("=== Performance Analysis ===")
    output.append("Two-Heap Approach (MedianFinder):")
    output.append("  • addNum(): O(log n) - heap push/pop operations")
    output.append("  • findMedian(): O(1) - constant time access")
    output.append("  • Space: O(n) - store all numbers in heaps")
    output.append("")

    output.append("Alternative Approaches:")
    output.append("1. **Sorted Array**: Insert O(n), Find O(1), Space O(n)")
    output.append("2. **Binary Search Tree**: Insert O(log n), Find O(n), Space O(n)")
    output.append("3. **Order Statistics Tree**: Insert O(log n), Find O(log n), Space O(n)")
    output.append("")

    # Key insights
    output.append("=== Key Insights ===")
    output.append("1. **Heap Invariant**: max_heap contains smaller half, min_heap larger half")
    output.append("2. **Size Constraint**: |max_heap| >= |min_heap| and difference <= 1")
    output.append("3. **Median Logic**: Odd total -> max_heap top, Even -> average of tops")
    output.append("4. **Balancing**: Always add through one heap and rebalance")
    output.append("")

    # Real-world applications
    output.append("=== Real-World Applications ===")
    output.append("• **Real-time Analytics**: Running median of sensor data")
    output.append("• **Financial Systems**: Moving median of stock prices")
    output.append("• **Quality Control**: Median response times in systems")
    output.append("• **Data Processing**: Streaming quantile estimation")
    output.append("• **Network Monitoring**: Median latency tracking")

    return "\n".join(output)


# Test cases for MedianFinder
def test_median_finder():
    """Test MedianFinder with various scenarios."""

    test_cases = [
        {
            "operations": ["MedianFinder", "addNum", "findMedian", "addNum", "findMedian"],
            "inputs": [[], [1], [], [2], []],
            "expected": [None, None, 1.0, None, 1.5],
            "description": "Basic two elements",
        },
        {
            "operations": [
                "MedianFinder",
                "addNum",
                "addNum",
                "findMedian",
                "addNum",
                "findMedian",
            ],
            "inputs": [[], [1], [2], [], [3], []],
            "expected": [None, None, None, 1.5, None, 2.0],
            "description": "Three elements progression",
        },
        {
            "operations": ["MedianFinder", "addNum", "addNum", "addNum", "addNum", "findMedian"],
            "inputs": [[], [6], [10], [2], [6], []],
            "expected": [None, None, None, None, None, 6.0],
            "description": "Unordered input with duplicates",
        },
    ]

    for i, test_case in enumerate(test_cases):
        print(f"\nTest {i + 1}: {test_case['description']}")
        median_finder = MedianFinder()
        results = []

        for j, (op, inp) in enumerate(zip(test_case["operations"], test_case["inputs"])):
            if op == "MedianFinder":
                results.append(None)
            elif op == "addNum":
                median_finder.addNum(inp[0])
                results.append(None)
            elif op == "findMedian":
                results.append(median_finder.findMedian())

        success = results == test_case["expected"]
        status = "✓" if success else "✗"
        print(f"  {status} Expected: {test_case['expected']}")
        print(f"     Got: {results}")


TEST_CASES = [
    TestCase(
        input_data={
            "operations": ["MedianFinder", "addNum", "findMedian", "addNum", "findMedian"],
            "inputs": [[], [1], [], [2], []],
        },
        expected=[None, None, 1.0, None, 1.5],
        description="Basic two-element median finding",
    ),
    TestCase(
        input_data={
            "operations": [
                "MedianFinder",
                "addNum",
                "addNum",
                "findMedian",
                "addNum",
                "findMedian",
            ],
            "inputs": [[], [1], [2], [], [3], []],
        },
        expected=[None, None, None, 1.5, None, 2.0],
        description="Three-element progression",
    ),
]


def test_solution():
    """Test the MedianFinder implementation."""
    test_median_finder()

    # Test with standard framework
    def run_operations(test_case):
        median_finder = MedianFinder()
        results = []

        for op, inp in zip(test_case.input_data["operations"], test_case.input_data["inputs"]):
            if op == "MedianFinder":
                results.append(None)
            elif op == "addNum":
                median_finder.addNum(inp[0])
                results.append(None)
            elif op == "findMedian":
                results.append(median_finder.findMedian())

        return results

    run_test_cases(TEST_CASES, run_operations)


# Register the problem
register_problem(
    slug="find_median_from_data_stream",
    leetcode_num=295,
    title="Find Median from Data Stream",
    difficulty=Difficulty.HARD,
    category=Category.HEAP,
    solution_func=lambda: MedianFinder(),  # Factory function
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["heap", "two-pointers", "data-stream", "design"],
    notes="Classic two-heap problem for maintaining running median in data stream",
)
