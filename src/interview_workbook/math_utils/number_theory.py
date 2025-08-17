def gcd(a: int, b: int) -> int:
    """
    Greatest Common Divisor via Euclidean algorithm.
    Time: O(log min(a, b))
    """
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """
    Least Common Multiple using gcd.
    Time: O(log min(a, b))
    """
    if a == 0 or b == 0:
        return 0
    return abs(a // gcd(a, b) * b)


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean algorithm.
    Returns (g, x, y) such that ax + by = g = gcd(a, b)
    """
    if b == 0:
        return (abs(a), 1 if a > 0 else -1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)


def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Modular exponentiation (fast power).
    Computes (base^exp) % mod in O(log exp).
    """
    if mod == 1:
        return 0
    base %= mod
    res = 1
    e = exp
    while e > 0:
        if e & 1:
            res = (res * base) % mod
        base = (base * base) % mod
        e >>= 1
    return res


def mod_inverse_fermat(a: int, mod: int) -> int:
    """
    Modular multiplicative inverse using Fermat's Little Theorem.
    Only valid if mod is prime and gcd(a, mod) == 1.
    Returns a^(mod-2) % mod.
    """
    return mod_pow(a, mod - 2, mod)


def mod_inverse_extgcd(a: int, mod: int) -> int:
    """
    Modular inverse using Extended Euclidean algorithm.
    Works for any modulus where gcd(a, mod) == 1.
    Returns x such that (a*x) % mod == 1, in [0, mod-1].
    Raises ValueError if inverse does not exist.
    """
    a %= mod
    g, x, _ = extended_gcd(a, mod)
    if g != 1:
        raise ValueError(f"No modular inverse for a={a} under mod={mod}")
    return x % mod


def sieve_of_eratosthenes(n: int) -> list[int]:
    """
    Generate all prime numbers up to and including n.
    Time: O(n log log n)
    Space: O(n)
    """
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    p = 2
    while p * p <= n:
        if sieve[p]:
            step = p
            start = p * p
            sieve[start : n + 1 : step] = [False] * (((n - start) // step) + 1)
        p += 1
    return [i for i, is_prime in enumerate(sieve) if is_prime]


def smallest_prime_factors(n: int) -> list[int]:
    """
    Precompute smallest prime factor (spf) for each number up to n.
    Useful for fast factorization queries.
    Time: O(n)
    """
    spf = list(range(n + 1))
    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:  # prime
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


def factorize_with_spf(x: int, spf: list[int]) -> list[int]:
    """
    Factorize x using a precomputed SPF array.
    Returns prime factors (with multiplicity).
    """
    if x <= 1:
        return []
    res = []
    while x > 1:
        p = spf[x]
        res.append(p)
        x //= p
    return res


def prefix_sums(arr: list[int]) -> list[int]:
    """
    Compute 1D prefix sums where pref[i] = sum(arr[0..i-1]).
    Length of pref = len(arr) + 1, pref[0] = 0.
    Range sum [l, r] inclusive: pref[r+1] - pref[l]
    """
    n = len(arr)
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + arr[i]
    return pref


def range_sum_with_prefix(pref: list[int], left: int, right: int) -> int:
    """
    Compute range sum using prefix sums. left and right inclusive.
    """
    if right < left:
        return 0
    left = max(left, 0)
    right = min(right, len(pref) - 2)
    return pref[right + 1] - pref[left]


def difference_array(arr: list[int]) -> list[int]:
    """
    Build difference array diff of arr where:
    diff[0] = arr[0], diff[i] = arr[i] - arr[i-1].
    Range increment [l, r] by delta:
        diff[l] += delta
        if r+1 < n: diff[r+1] -= delta
    Recover array by computing prefix sum of diff.
    """
    if not arr:
        return []
    n = len(arr)
    diff = [0] * n
    diff[0] = arr[0]
    for i in range(1, n):
        diff[i] = arr[i] - arr[i - 1]
    return diff


def apply_range_increment(diff: list[int], left: int, right: int, delta: int) -> None:
    """
    Apply range increment to difference array diff for [left, right] by delta.
    Does in-place updates.
    """
    n = len(diff)
    if left < 0 or right >= n or left > right:
        return
    diff[left] += delta
    if right + 1 < n:
        diff[right + 1] -= delta


def recover_from_difference(diff: list[int]) -> list[int]:
    """
    Recover original array from difference array by prefix sums.
    """
    if not diff:
        return []
    arr = [0] * len(diff)
    arr[0] = diff[0]
    for i in range(1, len(diff)):
        arr[i] = arr[i - 1] + diff[i]
    return arr


def prefix_sums_2d(matrix: list[list[int]]) -> list[list[int]]:
    """
    Compute 2D prefix sums (integral image).
    pref[i+1][j+1] = sum of submatrix (0,0) .. (i,j)
    Time: O(n*m), Space: O(n*m)
    """
    if not matrix or not matrix[0]:
        return [[0]]
    n, m = len(matrix), len(matrix[0])
    pref = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        row_sum = 0
        for j in range(m):
            row_sum += matrix[i][j]
            pref[i + 1][j + 1] = pref[i][j + 1] + row_sum
    return pref


def sum_region(pref: list[list[int]], r1: int, c1: int, r2: int, c2: int) -> int:
    """
    Sum of rectangle with corners (r1, c1) to (r2, c2) inclusive using 2D prefix sums.
    """
    if r1 > r2 or c1 > c2:
        return 0
    r1 = max(r1, 0)
    c1 = max(c1, 0)
    r2 = min(r2, len(pref) - 2)
    c2 = min(c2, len(pref[0]) - 2)
    return pref[r2 + 1][c2 + 1] - pref[r1][c2 + 1] - pref[r2 + 1][c1] + pref[r1][c1]


def demo():
    print("Number Theory and Prefix Structures Demo")
    print("=" * 50)

    # GCD / LCM
    print("GCD / LCM:")
    a, b = 24, 36
    print(f"gcd({a}, {b}) = {gcd(a, b)}")
    print(f"lcm({a}, {b}) = {lcm(a, b)}")
    print()

    # Modular arithmetic
    print("Modular Arithmetic:")
    base, exp, mod = 5, 117, 1_000_000_007
    print(f"mod_pow({base}, {exp}, {mod}) = {mod_pow(base, exp, mod)}")
    x, m = 3, 11
    inv_fermat = mod_inverse_fermat(x, m)  # m is prime (11)
    inv_ext = mod_inverse_extgcd(x, m)
    print(f"mod_inverse_fermat({x}, {m}) = {inv_fermat}")
    print(f"mod_inverse_extgcd({x}, {m}) = {inv_ext}")
    print(f"Check: ({x} * inv) % {m} = {(x * inv_ext) % m}")
    print()

    # Sieve and factorization
    print("Sieve of Eratosthenes up to 50:")
    primes = sieve_of_eratosthenes(50)
    print(f"Primes: {primes}")
    spf = smallest_prime_factors(50)
    val = 42
    print("Smallest prime factors array up to 50 computed.")
    print(f"Factorization of {val} via SPF: {factorize_with_spf(val, spf)}")
    print()

    # 1D prefix sums and difference arrays
    print("1D Prefix Sums and Difference Array:")
    arr = [2, 1, 3, 4, 5]
    pref = prefix_sums(arr)
    print(f"Array: {arr}")
    print(f"Prefix sums: {pref}")
    left, right = 1, 3
    print(f"range_sum({left}, {right}) = {range_sum_with_prefix(pref, left, right)}")
    diff = difference_array(arr)
    print(f"Difference array: {diff}")
    print("Apply range increment [1, 3] by +2")
    apply_range_increment(diff, 1, 3, 2)
    arr2 = recover_from_difference(diff)
    print(f"Recovered array: {arr2}")
    print()

    # 2D prefix sums
    print("2D Prefix Sums (Integral Image):")
    mat = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    pref2d = prefix_sums_2d(mat)
    print(f"Matrix: {mat}")
    print(
        f"Sum of sub-rectangle (1,1) to (2,2): {sum_region(pref2d, 1, 1, 2, 2)} (expected 5+6+8+9=28)"
    )
    print()

    print("Complexity and Notes:")
    print("  - gcd/lcm: O(log min(a,b))")
    print("  - mod_pow: O(log exp)")
    print("  - mod_inverse (Fermat): requires prime modulus")
    print("  - mod_inverse (extgcd): any modulus with gcd(a, mod) == 1")
    print("  - sieve: O(n log log n)")
    print("  - prefix sums: O(n) build, O(1) range queries")
    print("  - difference array: O(1) range update, O(n) recover")
    print("  - 2D prefix sums: O(nm) build, O(1) region queries")


if __name__ == "__main__":
    demo()
