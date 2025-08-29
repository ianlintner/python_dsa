"""
Search 2D Matrix

TODO: Add problem description
"""

from interview_workbook.leetcode._runner import TestCase


class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        """Search target in a matrix with sorted rows and columns."""
        if not matrix or not matrix[0]:
            return False
        rows, cols = len(matrix), len(matrix[0])
        left, right = 0, rows * cols - 1
        while left <= right:
            mid = (left + right) // 2
            val = matrix[mid // cols][mid % cols]
            if val == target:
                return True
            elif val < target:
                left = mid + 1
            else:
                right = mid - 1
        return False


test_cases = [
    TestCase(
        ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 50]], 3), True, "Element present in row 1"
    ),
    TestCase(
        ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 50]], 13), False, "Element not present"
    ),
]


def demo():
    """Run simple test cases for Search 2D Matrix."""
    sol = Solution()
    outputs = []
    for case in test_cases:
        res = sol.searchMatrix(*case.input_args)
        outputs.append(
            f"Search 2D Matrix | Input: {case.input_args} -> Output: {res}, Expected: {case.expected}"
        )
    return "\n".join(outputs)


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="search_2d_matrix",
#     title="Search 2D Matrix",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
