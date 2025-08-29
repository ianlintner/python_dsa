"""
Minimum Window Substring

Problem: Minimum Window Substring
LeetCode link: https://leetcode.com/problems/minimum-window-substring/
Description: Given two strings s and t, return the minimum window substring of s such that every character in t is included in the window. If no such substring exists, return an empty string.
"""


from collections import Counter

class Solution:
    def solve(self, *args):
        """Return minimum window substring of s containing all chars of t."""
        s, t = args
        if not t or not s:
            return ""
        t_count = Counter(t)
        window = {}
        have, need = 0, len(t_count)
        res, res_len = [-1, -1], float("inf")
        l = 0
        for r, ch in enumerate(s):
            window[ch] = window.get(ch, 0) + 1
            if ch in t_count and window[ch] == t_count[ch]:
                have += 1
            while have == need:
                if (r - l + 1) < res_len:
                    res = [l, r]
                    res_len = r - l + 1
                window[s[l]] -= 1
                if s[l] in t_count and window[s[l]] < t_count[s[l]]:
                    have -= 1
                l += 1
        l, r = res
        return s[l:r+1] if res_len != float("inf") else ""


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="minimum_window_substring",
#     title="Minimum Window Substring",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
