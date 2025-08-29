"""
Word Break

TODO: Add problem description
"""


class Solution:
    def solve(self, *args) -> bool:
        """Return True if s can be segmented into words from wordDict, else False."""
        if len(args) != 2:
            return ""
        s, wordDict = args
        word_set = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break
        return dp[n]


def demo():
    """Run a demo for the Word Break problem."""
    solver = Solution()
    s = "leetcode"
    wordDict = ["leet", "code"]
    result = solver.solve(s, wordDict)
    return str(result)


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="word_break",
#     title="Word Break",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
