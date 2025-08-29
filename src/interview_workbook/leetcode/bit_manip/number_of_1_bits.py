"""
Number Of 1 Bits

TODO: Add problem description
"""
import random

class Solution:
    def solve(self, n: int) -> int:
        """Return the number of 1 bits in the binary representation of n."""
        count = 0
        while n:
            count += n & 1
            n >>= 1
        return count


def demo() -> str:
    """Run a deterministic demo for Number Of 1 Bits."""
    random.seed(0)
    sol = Solution()
    test_values = [0, 1, 2, 3, 7, 8, 15, 16, 31]
    results = {val: sol.solve(val) for val in test_values}
    return str(results)


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="number_of_1_bits",
#     title="Number Of 1 Bits",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
