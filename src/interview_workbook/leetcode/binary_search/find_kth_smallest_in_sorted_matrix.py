"""
Find Kth Smallest In Sorted Matrix

TODO: Add problem description
"""


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


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="find_kth_smallest_in_sorted_matrix",
#     title="Find Kth Smallest In Sorted Matrix",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
