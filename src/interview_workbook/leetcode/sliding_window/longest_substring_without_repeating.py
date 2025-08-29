"""
Longest Substring Without Repeating

Problem: Longest Substring Without Repeating Characters
LeetCode link: https://leetcode.com/problems/longest-substring-without-repeating-characters/
Description: Given a string, find the length of the longest substring without repeating characters.
"""


class Solution:
    def solve(self, *args):
        """Return length of longest substring without repeating characters."""
        s, = args
        seen = {}
        l = 0
        res = 0
        for r, ch in enumerate(s):
            if ch in seen and seen[ch] >= l:
                l = seen[ch] + 1
            seen[ch] = r
            res = max(res, r - l + 1)
        return res


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="longest_substring_without_repeating",
#     title="Longest Substring Without Repeating",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
