"""
Reverse Bits

TODO: Add problem description
"""
import random

class Solution:
    def solve(self, n: int) -> int:
        """Return the integer obtained by reversing the 32-bit binary representation of n."""
        result = 0
        for _ in range(32):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result




def demo() -> str:
    """Run a deterministic demo for Reverse Bits."""
    random.seed(0)
    sol = Solution()
    test_values = [0, 1, 43261596, 4294967293]
    results = {val: sol.solve(val) for val in test_values}
    return str(results)


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="reverse_bits",
#     title="Reverse Bits",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
