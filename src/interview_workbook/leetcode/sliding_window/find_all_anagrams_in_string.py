"""
Find All Anagrams In String

TODO: Add problem description
"""


from collections import Counter

class Solution:
    def solve(self, *args):
        """Return list of start indices of anagrams of p in s."""
        s, p = args
        res = []
        if len(p) > len(s):
            return res
        p_count = Counter(p)
        s_count = Counter()
        l = 0
        for r, ch in enumerate(s):
            s_count[ch] += 1
            if r - l + 1 > len(p):
                s_count[s[l]] -= 1
                if s_count[s[l]] == 0:
                    del s_count[s[l]]
                l += 1
            if s_count == p_count:
                res.append(l)
        return res


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="find_all_anagrams_in_string",
#     title="Find All Anagrams In String",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
