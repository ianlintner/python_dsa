"""
LeetCode 378: Kth Smallest Element in a Sorted Matrix

Given an n x n matrix where each of the rows and columns are sorted in
ascending order, return the kth smallest element in the matrix.

Note that it is the kth smallest element in the sorted order, not the kth distinct element.

You must find a solution with a memory complexity better than O(n^2).

Example 1:
Input: matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8
Output: 13
Explanation: The elements in the matrix are [1,5,9,10,11,12,13,13,15],
and the 8th smallest element is 13

Example 2:
Input: matrix = [[-5]], k = 1
Output: -5

Constraints:
- n == matrix.length == matrix[i].length
- 1 <= n <= 300
- -10^9 <= matrix[i][j] <= 10^9
- All the rows and columns of matrix are guaranteed to be sorted in non-decreasing order
- 1 <= k <= n^2
"""

import heapq
from typing import List

from interview_workbook.leetcode._registry import register_problem


class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        """
        Find kth smallest element in sorted matrix using binary search on values.

        Time: O(n * log(max - min) * log n) where n is matrix dimension
        Space: O(1)

        Algorithm:
        1. Binary search on the value range [min_val, max_val]
        2. For each mid value, count elements <= mid using row-wise search
        3. If count >= k, search left half; otherwise search right half
        """
        n = len(matrix)
        left, right = matrix[0][0], matrix[n - 1][n - 1]

        def count_less_equal(target: int) -> int:
            """Count elements <= target using row-wise traversal"""
            count = 0
            row, col = n - 1, 0  # Start from bottom-left

            while row >= 0 and col < n:
                if matrix[row][col] <= target:
                    count += row + 1  # All elements above in this column
                    col += 1
                else:
                    row -= 1

            return count

        # Binary search on values
        while left < right:
            mid = left + (right - left) // 2
            count = count_less_equal(mid)

            if count >= k:
                right = mid
            else:
                left = mid + 1

        return left

    def kthSmallestHeap(self, matrix: List[List[int]], k: int) -> int:
        """
        Alternative solution using min-heap (less optimal for large matrices).

        Time: O(k * log k)
        Space: O(k)
        """
        if not matrix or not matrix[0]:
            return 0

        n = len(matrix)
        heap = [(matrix[0][0], 0, 0)]
        visited = {(0, 0)}

        for _ in range(k):
            val, row, col = heapq.heappop(heap)

            # Add right neighbor
            if col + 1 < n and (row, col + 1) not in visited:
                heapq.heappush(heap, (matrix[row][col + 1], row, col + 1))
                visited.add((row, col + 1))

            # Add bottom neighbor
            if row + 1 < n and (row + 1, col) not in visited:
                heapq.heappush(heap, (matrix[row + 1][col], row + 1, col))
                visited.add((row + 1, col))

        return val


def demo():
    """Demo of Kth Smallest Element in a Sorted Matrix."""
    solution = Solution()

    test_cases = [
        {"matrix": [[1, 5, 9], [10, 11, 13], [12, 13, 15]], "k": 8, "expected": 13},
        {"matrix": [[-5]], "k": 1, "expected": -5},
        {"matrix": [[1, 2], [1, 3]], "k": 3, "expected": 2},
        {"matrix": [[1, 3, 5], [6, 7, 12], [11, 14, 14]], "k": 6, "expected": 11},
    ]

    print("=== LeetCode 378: Kth Smallest Element in a Sorted Matrix ===\n")

    for i, test in enumerate(test_cases, 1):
        matrix = test["matrix"]
        k = test["k"]
        expected = test["expected"]

        print(f"Test Case {i}:")
        print(f"Matrix: {matrix}")
        print(f"K: {k}")
        print(f"Expected: {expected}")

        # Test binary search solution
        result = solution.kthSmallest(matrix, k)
        print(f"Result (Binary Search): {result}")
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"Status: {status}")

        # Test heap solution for comparison
        result_heap = solution.kthSmallestHeap(matrix, k)
        print(f"Result (Heap): {result_heap}")
        print()


if __name__ == "__main__":
    demo()


# Register the problem
register_problem(
    id="378",
    title="Kth Smallest Element in a Sorted Matrix",
    difficulty="Medium",
    category="Binary Search",
    url="https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/",
    tags=["Array", "Binary Search", "Sorting", "Heap (Priority Queue)", "Matrix"],
    module_path="interview_workbook.leetcode.binary_search.find_kth_smallest_in_sorted_matrix",
)
