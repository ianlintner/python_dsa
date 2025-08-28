"""
LeetCode 74: Search a 2D Matrix (Medium)
https://leetcode.com/problems/search-a-2d-matrix/

You are given an m x n integer matrix matrix with the following two properties:
- Each row is sorted in non-decreasing order.
- The first integer of each row is greater than the last integer of the previous row.

Given an integer target, return true if target is in matrix or false otherwise.

You must write a solution in O(log(m * n)) time complexity.

Example 1:
Input: matrix = [[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]], target = 5
Output: true

Example 2:
Input: matrix = [[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]], target = 13
Output: true

Example 3:
Input: matrix = [[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]], target = 20
Output: false

Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 100
- -10^4 <= matrix[i][j], target <= 10^4

Algorithm Insights:
- Treat 2D matrix as flattened 1D array for binary search
- Convert 1D index to 2D coordinates: row = index // n, col = index % n
- Since matrix properties ensure sorted order when flattened
- Use standard binary search on conceptual 1D array

Time Complexity: O(log(m * n)) - binary search on m*n elements
Space Complexity: O(1) - constant extra space
"""

from typing import List

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """
        Search for target in 2D matrix using binary search.

        The key insight is to treat the 2D matrix as a flattened 1D array
        since the matrix properties guarantee it would be sorted when flattened.

        Args:
            matrix: 2D matrix with sorted rows and sorted column starts
            target: Target value to search for

        Returns:
            True if target exists in matrix, False otherwise
        """
        if not matrix or not matrix[0]:
            return False

        m, n = len(matrix), len(matrix[0])
        left, right = 0, m * n - 1

        while left <= right:
            mid = left + (right - left) // 2

            # Convert 1D index to 2D coordinates
            row = mid // n
            col = mid % n
            mid_val = matrix[row][col]

            if mid_val == target:
                return True
            elif mid_val < target:
                left = mid + 1
            else:
                right = mid - 1

        return False


# Test cases
test_cases = [
    TestCase(
        ([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 5),
        True,
        "Example 1: target exists",
    ),
    TestCase(
        ([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 13),
        True,
        "Example 2: target at end",
    ),
    TestCase(
        ([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 20),
        False,
        "Example 3: target not found",
    ),
    TestCase(([[1]], 1), True, "Single element matrix - found"),
    TestCase(([[1]], 2), False, "Single element matrix - not found"),
    TestCase(([[1, 3]], 3), True, "Single row - target at end"),
    TestCase(([[1], [3]], 1), True, "Single column - target at start"),
    TestCase(
        ([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 1),
        True,
        "Target at beginning",
    ),
    TestCase(
        ([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 17),
        True,
        "Target at very end",
    ),
    TestCase(
        ([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 0),
        False,
        "Target smaller than all",
    ),
    TestCase(
        ([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 15),
        False,
        "Target between existing values",
    ),
    TestCase(([[-5, -2], [0, 3]], -2), True, "Negative numbers"),
]


def demo() -> str:
    """Run Search a 2D Matrix demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(
        solution.searchMatrix, test_cases, "LeetCode 74: Search a 2D Matrix"
    )

    return create_demo_output(
        "Search a 2D Matrix",
        test_results,
        time_complexity="O(log(m * n))",
        space_complexity="O(1)",
        approach_notes="""
Key insights:
1. Treat 2D matrix as conceptual 1D sorted array due to matrix properties
2. Convert 1D binary search index to 2D coordinates: row = idx // n, col = idx % n  
3. Matrix properties ensure flattened array would be sorted
4. Use standard binary search template with coordinate conversion
5. Handle edge cases: empty matrix, single element, boundary values

Algorithm steps:
- Initialize left = 0, right = m * n - 1 for total elements
- While left <= right: calculate mid index
- Convert mid to 2D: row = mid // n, col = mid % n
- Compare matrix[row][col] with target
- Update search bounds based on comparison
- Return true if found, false if search space exhausted
        """.strip(),
    )


# Register the problem
register_problem(
    id=74,
    slug="search_2d_matrix",
    title="Search a 2D Matrix",
    category=Category.BINARY_SEARCH,
    difficulty=Difficulty.MEDIUM,
    tags=["Array", "Binary Search", "Matrix"],
    url="https://leetcode.com/problems/search-a-2d-matrix/",
    notes="Binary search on 2D matrix treated as flattened 1D array",
)


if __name__ == "__main__":
    print(demo())
