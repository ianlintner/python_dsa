"""
Encode And Decode Strings

Design an algorithm to encode a list of strings to a single string, then decode
the single string back to the original list of strings.

This is a common problem to handle arbitrary text where delimiters might appear
within the input strings.
"""

import random

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty

random.seed(0)


class Solution:
    def solve(self, strs: list[str]) -> list[str]:
        """Encode and decode a list of strings deterministically.

        Approach:
        - Encode: prefix each string with its length and a delimiter '#'.
        - Decode: parse lengths and extract substrings accordingly.

        This ensures reversibility even if strings contain special characters.
        """
        encoded = self.encode(strs)
        return self.decode(encoded)

    def encode(self, strs: list[str]) -> str:
        """Encodes a list of strings to a single string."""
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s: str) -> list[str]:
        """Decodes a single string back into a list of strings."""
        res = []
        i = 0
        while i < len(s):
            j = i
            while s[j] != "#":
                j += 1
            length = int(s[i:j])
            i = j + 1
            res.append(s[i : i + length])
            i += length
        return res


def demo():
    """Demonstration of Encode and Decode Strings problem."""
    strs = ["hello", "world", "foo#bar", ""]
    solver = Solution()
    encoded = solver.encode(strs)
    decoded = solver.decode(encoded)
    return f"Original: {strs}\nEncoded: {encoded}\nDecoded: {decoded}"


register_problem(
    id=271,
    slug="encode_and_decode_strings",
    title="Encode And Decode Strings",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags=["string", "encoding"],
    url="https://leetcode.com/problems/encode-and-decode-strings/",
    notes="Uses length-prefix encoding with '#' delimiter to ensure reversibility.",
)
