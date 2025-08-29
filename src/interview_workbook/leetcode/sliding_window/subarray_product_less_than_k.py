"""
Subarray Product Less Than K

TODO: Add problem description
"""


class Solution:
    def solve(self, *args):
        """Return count of subarrays where product < k."""
        nums, k = args
        if k <= 1:
            return 0
        prod = 1
        res = 0
        l = 0
        for r, n in enumerate(nums):
            prod *= n
            while prod >= k:
                prod //= nums[l]
                l += 1
            res += r - l + 1
        return res


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="subarray_product_less_than_k",
#     title="Subarray Product Less Than K",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
