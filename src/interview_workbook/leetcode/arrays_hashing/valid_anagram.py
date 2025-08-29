"""
Valid Anagram

TODO: Add problem description
"""


class Solution:
    def solve(self, s: str, t: str) -> bool:
        """Check if two strings are anagrams using character counting."""
        if len(s) != len(t):
            return False

        from collections import Counter

        return Counter(s) == Counter(t)


def demo():
    """Demonstrate valid anagram solution."""
    sol = Solution()
    assert sol.solve("anagram", "nagaram") is True
    assert sol.solve("rat", "car") is False
    return "Valid Anagram demo passed."


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="valid_anagram",
#     title="Valid Anagram",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
