"""
Add And Search Word

Problem: Add and Search Word (Data structure design)
LeetCode link: https://leetcode.com/problems/add-and-search-word-data-structure-design/
Description: Design a data structure that adds new words and finds if a string with optional '.' wildcards matches any previously added word.
"""


class WordDictionary:
    """
    Implements Add and Search Word using a Trie.
    Supports '.' as a wildcard matching any character.
    """

    def __init__(self):
        self.trie = {}

    def addWord(self, word: str) -> None:
        node = self.trie
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node["$"] = True  # End of word marker

    def search(self, word: str) -> bool:
        def dfs(j, node):
            for i in range(j, len(word)):
                ch = word[i]
                if ch == ".":
                    for nxt in node:
                        if nxt != "$" and dfs(i + 1, node[nxt]):
                            return True
                    return False
                else:
                    if ch not in node:
                        return False
                    node = node[ch]
            return "$" in node

        return dfs(0, self.trie)


class Solution:
    def solve(self, *args) -> None:
        """LeetCode driver-compatible entry (placeholder)."""
        return None


def demo():
    """Demonstrate WordDictionary functionality."""
    import random

    random.seed(0)

    wd = WordDictionary()
    wd.addWord("bad")
    wd.addWord("dad")
    wd.addWord("mad")

    outputs = []
    outputs.append(wd.search("pad"))  # False
    outputs.append(wd.search("bad"))  # True
    outputs.append(wd.search(".ad"))  # True
    outputs.append(wd.search("b.."))  # True

    return str(outputs)


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="add_and_search_word",
#     title="Add And Search Word",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
