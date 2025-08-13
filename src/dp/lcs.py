from typing import List, Tuple

def lcs_length(a: str, b: str) -> int:
    """
    Longest Common Subsequence length between strings a and b.
    
    DP definition:
      dp[i][j] = LCS length of a[:i] and b[:j]
      Transition:
        if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1] + 1
        else:                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    Time: O(n*m)
    Space: O(min(n, m)) if optimized, O(n*m) here for clarity
    
    Pitfalls:
      - Do not confuse with longest common substring (which requires contiguous)
      - Reconstruct path requires tracking choices or re-walking dp table
    
    Returns:
      Length of an LCS.
    """
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return 0
    # Space-optimized 1D DP
    if m > n:
        # Ensure b is the shorter to reduce memory
        a, b = b, a
        n, m = m, n
    prev = [0] * (m + 1)
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        ai = a[i - 1]
        for j in range(1, m + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[m]


def lcs_reconstruct(a: str, b: str) -> str:
    """
    Reconstruct one valid LCS string using full 2D DP table.
    
    Time: O(n*m) build + O(n+m) reconstruct
    Space: O(n*m) for clarity
    """
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        ai = a[i - 1]
        for j in range(1, m + 1):
            if ai == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # Walk back to reconstruct
    i, j = n, m
    out: List[str] = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        else:
            # Prefer direction with larger dp value
            if dp[i - 1][j] >= dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
    return "".join(reversed(out))


def demo():
    print("Longest Common Subsequence (LCS) Demo")
    print("=" * 45)
    cases: List[Tuple[str, str]] = [
        ("abcde", "ace"),
        ("AGGTAB", "GXTXAYB"),
        ("", ""),
        ("abc", ""),
        ("abc", "abc"),
        ("abcdef", "zabcyf"),
    ]
    for i, (x, y) in enumerate(cases, 1):
        L = lcs_length(x, y)
        s = lcs_reconstruct(x, y)
        print(f"Case {i}: a='{x}', b='{y}'")
        print(f"  length = {L}")
        print(f"  lcs    = '{s}'")
        print()

    print("Notes:")
    print("  - LCS is a classic DP with O(n*m) complexity.")
    print("  - Use length-only 1D DP for memory efficiency.")
    print("  - Do not confuse with Longest Common Substring (contiguous).")


if __name__ == "__main__":
    demo()
