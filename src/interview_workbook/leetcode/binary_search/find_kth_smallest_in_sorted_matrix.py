"""
Find Kth Smallest In Sorted Matrix

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def kthSmallest(self, matrix: list[list[int]], k: int) -> int:
        """Return the kth smallest element in a sorted matrix using binary search on value range."""
        n = len(matrix)
        left, right = matrix[0][0], matrix[-1][-1]

        def count_less_equal(x: int) -> int:
            count, col = 0, n - 1
            for row in range(n):
                while col >= 0 and matrix[row][col] > x:
                    col -= 1
                count += col + 1
            return count

        while left < right:
            mid = (left + right) // 2
            if count_less_equal(mid) < k:
                left = mid + 1
            else:
                right = mid
        return left

    def kthSmallestHeap(self, matrix: list[list[int]], k: int) -> int:
        """Return the kth smallest element using a min-heap approach."""
        import heapq

        n = len(matrix)
        min_heap = []
        for r in range(min(n, k)):
            heapq.heappush(min_heap, (matrix[r][0], r, 0))

        count, num = 0, 0
        while min_heap:
            num, r, c = heapq.heappop(min_heap)
            count += 1
            if count == k:
                return num
            if c + 1 < n:
                heapq.heappush(min_heap, (matrix[r][c + 1], r, c + 1))
        return num


def demo():
    """Run simple test cases for Find Kth Smallest In Sorted Matrix."""
    solution = Solution()
    output = []
    matrix1 = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
    k1 = 8
    res1 = solution.kthSmallest(matrix1, k1)
    res1_heap = solution.kthSmallestHeap(matrix1, k1)
    output.append("Find Kth Smallest In Sorted Matrix")
    output.append("Time: O(n log(max-min)) | Space: O(1)")
    output.append(f"Test Case 1: matrix={matrix1}, k={k1} -> {res1} (heap: {res1_heap})")

    matrix2 = [[1, 2], [1, 3]]
    k2 = 3
    res2 = solution.kthSmallest(matrix2, k2)
    res2_heap = solution.kthSmallestHeap(matrix2, k2)
    output.append(f"Test Case 2: matrix={matrix2}, k={k2} -> {res2} (heap: {res2_heap})")

    return "\n".join(output)


register_problem(
    id=378,
    slug="find_kth_smallest_in_sorted_matrix",
    title="Kth Smallest Element in a Sorted Matrix",
    category=Category.BINARY_SEARCH,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "binary_search", "heap"],
    url="https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/",
    notes="",
)
