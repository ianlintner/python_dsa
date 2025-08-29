"""
Permutation In String

TODO: Add problem description
"""


from collections import Counter

class Solution:
    def solve(self, *args):
        """Return True if any permutation of s1 is a substring of s2."""
        s1, s2 = args
        if len(s1) > len(s2):
            return False
        s1_count = Counter(s1)
        window = Counter()
        l = 0
        for r, ch in enumerate(s2):
            window[ch] += 1
            if r - l + 1 > len(s1):
                window[s2[l]] -= 1
                if window[s2[l]] == 0:
                    del window[s2[l]]
                l += 1
            if window == s1_count:
                return True
        return False


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="permutation_in_string",
#     title="Permutation In String",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
