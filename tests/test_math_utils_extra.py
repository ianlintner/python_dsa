import pytest

from interview_workbook.math_utils.number_theory import (
    extended_gcd,
    factorize_with_spf,
    mod_inverse_extgcd,
    mod_inverse_fermat,
    prefix_sums_2d,
    sieve_of_eratosthenes,
    smallest_prime_factors,
    sum_region,
)


def test_smallest_prime_factors_and_factorize():
    n = 50
    spf = smallest_prime_factors(n)
    # Spot-check primes have themselves as SPF
    for p in [2, 3, 5, 7, 11, 13, 17, 19]:
        assert spf[p] == p
    # Composite examples
    assert spf[4] == 2
    assert spf[6] in (2, 3)
    assert spf[49] == 7

    # Factorization with multiplicity
    assert factorize_with_spf(1, spf) == []
    assert factorize_with_spf(2, spf) == [2]
    assert factorize_with_spf(18, spf) == [2, 3, 3]
    assert factorize_with_spf(42, spf) in (
        [2, 3, 7],
        [3, 2, 7],
        [2, 7, 3],
        [7, 2, 3],
        [7, 3, 2],
        [3, 7, 2],
    )


def test_prefix_sums_2d_and_sum_region():
    mat = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    pref = prefix_sums_2d(mat)
    # Single cell
    assert sum_region(pref, 0, 0, 0, 0) == 1
    # Row range
    assert sum_region(pref, 1, 0, 1, 2) == 4 + 5 + 6
    # Rectangle bottom-right 2x2
    assert sum_region(pref, 1, 1, 2, 2) == 5 + 6 + 8 + 9
    # Out-of-bounds clamped + empty rectangle
    assert sum_region(pref, 2, 2, 1, 1) == 0
    assert sum_region(pref, -10, -10, 100, 100) == sum(sum(row) for row in mat)


def test_modular_inverses_and_extended_gcd_consistency():
    # For prime modulus, Fermat and ExtGCD should agree
    mod = 1_000_000_007
    for a in [1, 2, 3, 1234567, mod - 3]:
        inv1 = mod_inverse_fermat(a, mod)
        inv2 = mod_inverse_extgcd(a, mod)
        assert (a * inv1) % mod == 1
        assert (a * inv2) % mod == 1
        assert inv1 == inv2

    # For non-coprime, extgcd should raise
    with pytest.raises(ValueError):
        mod_inverse_extgcd(6, 9)

    # extended_gcd correctness: ax + by = g
    g, x, y = extended_gcd(240, 46)
    assert g == 2
    assert 240 * x + 46 * y == g


def test_sieve_consistency():
    assert sieve_of_eratosthenes(1) == []
    assert sieve_of_eratosthenes(2) == [2]
    assert sieve_of_eratosthenes(10) == [2, 3, 5, 7]
