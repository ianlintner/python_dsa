"""
Longest Repeating Character Replacement

TODO: Add problem description
"""


from collections import defaultdict

class Solution:
    def solve(self, *args):
        """Return length of longest substring with at most k replacements."""
        s, k = args
        count = defaultdict(int)
        res = 0
        l = 0
        maxf = 0
        for r, ch in enumerate(s):
            count[ch] += 1
            maxf = max(maxf, count[ch])
            while (r - l + 1) - maxf > k:
                count[s[l]] -= 1
                l += 1
            res = max(res, r - l + 1)
        return res


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="longest_repeating_character_replacement",
#     title="Longest Repeating Character Replacement",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
