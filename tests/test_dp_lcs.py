import pytest

from interview_workbook.dp.lcs import lcs_length, lcs_reconstruct


def test_lcs_length_basic():
    assert lcs_length("abcde", "ace") == 3
    assert lcs_length("AGGTAB", "GXTXAYB") == 4
    assert lcs_length("", "") == 0
    assert lcs_length("abc", "") == 0
    assert lcs_length("abc", "abc") == 3
    assert lcs_length("abcdef", "zabcyf") == 4  # 'abcf'


def test_lcs_reconstruct_examples():
    # Both functions should be consistent (length matches)
    pairs = [
        ("abcde", "ace"),
        ("AGGTAB", "GXTXAYB"),
        ("aaaa", "aa"),
        ("abcdef", "zabcyf"),
    ]
    for a, b in pairs:
        s = lcs_reconstruct(a, b)
        assert isinstance(s, str)
        assert len(s) == lcs_length(a, b)

        # s must be a subsequence of both a and b
        def is_subseq(x: str, t: str) -> bool:
            it = iter(t)
            return all(ch in it for ch in x)

        assert is_subseq(s, a)
        assert is_subseq(s, b)


def test_lcs_edge_cases():
    assert lcs_reconstruct("", "") == ""
    assert lcs_reconstruct("abc", "") == ""
    assert lcs_reconstruct("", "xyz") == ""
    # identical strings -> LCS equals the string
    assert lcs_reconstruct("banana", "banana") == "banana"


if __name__ == "__main__":
    pytest.main([__file__])
