from typing import Tuple

def manacher_longest_palindromic_substring(s: str) -> Tuple[int, str, int, int]:
    """
    Manacher's Algorithm: Longest Palindromic Substring in O(n) time.

    Returns:
      (length, substring, start_index, end_index_inclusive)

    Core idea:
    - Transform s into T with separators (#) to handle even-length palindromes uniformly.
      Example: s = "abba" -> T = "^#a#b#b#a#$" (sentinels to avoid bounds checks)
    - Maintain center C and right boundary R of the rightmost palindrome found so far.
    - For each i, mirror position i' = 2*C - i. Initialize P[i] = min(R - i, P[i']) if i < R.
      Then expand around i and update C, R as needed.

    Complexity:
    - Time: O(n)
    - Space: O(n)
    """
    if not s:
        return 0, "", 0, -1

    # Transform: add sentinels '^' and '$' to avoid bounds checking
    T = ["^"]
    for ch in s:
        T.append("#")
        T.append(ch)
    T.append("#")
    T.append("$")
    T_str = "".join(T)

    n = len(T_str)
    P = [0] * n  # P[i] = radius of palindrome centered at i (in T)
    C = 0        # center of the current rightmost palindrome
    R = 0        # right boundary of the current rightmost palindrome

    for i in range(1, n - 1):
        mirror = 2 * C - i
        if i < R:
            P[i] = min(R - i, P[mirror])

        # Expand around center i
        while T_str[i + 1 + P[i]] == T_str[i - 1 - P[i]]:
            P[i] += 1

        # Update center if palindrome at i expands past R
        if i + P[i] > R:
            C = i
            R = i + P[i]

    # Find longest palindromic substring
    max_len = 0
    center_index = 0
    for i in range(1, n - 1):
        if P[i] > max_len:
            max_len = P[i]
            center_index = i

    # Map back to original string indices
    # Start index in s:
    start = (center_index - max_len) // 2
    end = start + max_len - 1
    substring = s[start:end + 1]
    return max_len, substring, start, end


def is_palindrome(s: str) -> bool:
    """Utility to check if s is a palindrome."""
    return s == s[::-1]


def count_palindromic_substrings(s: str) -> int:
    """
    Count palindromic substrings in O(n) using Manacher's P array.

    For transformed string T and P:
      - Number of palindromes centered at i equals (P[i] + 1) // 2 in original string terms.
    """
    if not s:
        return 0

    # Build transformed string
    T = ["^"]
    for ch in s:
        T.append("#")
        T.append(ch)
    T.append("#")
    T.append("$")
    T_str = "".join(T)

    n = len(T_str)
    P = [0] * n
    C = 0
    R = 0

    for i in range(1, n - 1):
        mirror = 2 * C - i
        if i < R:
            P[i] = min(R - i, P[mirror])
        while T_str[i + 1 + P[i]] == T_str[i - 1 - P[i]]:
            P[i] += 1
        if i + P[i] > R:
            C = i
            R = i + P[i]

    # Sum palindromic counts mapped back to original string
    total = 0
    for i in range(1, n - 1):
        total += (P[i] + 1) // 2
    return total


def demo():
    print("Manacher's Algorithm Demo")
    print("=" * 40)

    examples = [
        "babad",
        "cbbd",
        "a",
        "ac",
        "abba",
        "abacdfgdcaba",
        "forgeeksskeegfor",
        "",
    ]

    for s in examples:
        result = manacher_longest_palindromic_substring(s)
        length, sub, start, end = result[0], result[1], result[2], result[3]
        print(f"String: '{s}'")
        print(f"  Longest palindrome: '{sub}' (len={length}, start={start}, end={end})")
        print(f"  Palindromic substrings count: {count_palindromic_substrings(s)}")
        print()

    print("Notes & Interview Tips:")
    print("  - O(n) time using transformed string with separators and radius array.")
    print("  - Compare with expand-around-center O(n^2) approach for clarity vs performance.")
    print("  - Useful in problems requiring palindrome counts or longest palindromic substring.")

if __name__ == "__main__":
    demo()
