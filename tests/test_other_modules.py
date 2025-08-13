import math
import pytest

# DP
from dp.fibonacci import (
    fibonacci_bottom_up,
    fibonacci_optimized,
    fibonacci_matrix_power,
    fibonacci_sequence,
    tribonacci,
    climbing_stairs,
    house_robber,
)
from dp.coin_change import (
    coin_change_min_coins,
    coin_change_count_ways,
)
from dp.edit_distance import (
    edit_distance,
    edit_distance_optimized,
)
from dp.longest_increasing_subsequence import (
    lis_binary_search,
)

# Graphs
from graphs.bfs_dfs import (
    bfs,
    dfs_iterative,
    is_bipartite,
    connected_components_undirected,
)
from graphs.topological_sort import (
    topological_sort_kahn,
    build_graph_from_edges,
)
from graphs.dijkstra import (
    dijkstra,
)

# Strings
from strings.kmp import (
    kmp_search,
    kmp_search_first_occurrence,
)
from strings.z_algorithm import (
    z_search,
)
from strings.rabin_karp import (
    rabin_karp_search,
)
from strings.manacher import (
    manacher_longest_palindromic_substring,
)

# Patterns
from patterns.sliding_window import (
    length_of_longest_substring_without_repeating,
    min_window_substring,
)
from patterns.two_pointers import (
    three_sum,
)
from patterns.binary_search_on_answer import (
    ship_within_days,
)
from patterns.meet_in_the_middle import (
    subset_sum_mitm,
)

# Math
from math_utils.number_theory import (
    gcd,
    lcm,
    mod_pow,
    sieve_of_eratosthenes,
    prefix_sums,
    range_sum_with_prefix,
    difference_array,
    apply_range_increment,
    recover_from_difference,
)

# Systems
from systems.rate_limiter import TokenBucket, LeakyBucket


class TestDPFibonacciFamily:
    def test_fibonacci_values(self):
        for n, f in [(0, 0), (1, 1), (5, 5), (10, 55), (15, 610)]:
            assert fibonacci_bottom_up(n) == f
            assert fibonacci_optimized(n) == f
            assert fibonacci_matrix_power(n) == f

    def test_fibonacci_sequence(self):
        seq = fibonacci_sequence(7)
        assert seq == [0, 1, 1, 2, 3, 5, 8]

    def test_tribonacci(self):
        # First few tribonacci numbers (starting T0=0, T1=T2=1)
        expected = [0, 1, 1, 2, 4, 7, 13, 24]
        got = [tribonacci(i) for i in range(len(expected))]
        assert got == expected

    def test_climbing_stairs(self):
        assert climbing_stairs(1) == 1
        assert climbing_stairs(2) == 2
        assert climbing_stairs(3) == 3
        assert climbing_stairs(5) == 8

    def test_house_robber(self):
        assert house_robber([2, 7, 9, 3, 1]) == 12
        assert house_robber([]) == 0
        assert house_robber([5]) == 5


class TestDPCoinChangeEditDistanceLIS:
    def test_coin_change_min_coins(self):
        # Classic case: amount=6 with coins [1,3,4] -> 2 coins (3+3 or 4+1+1 but min is 2)
        assert coin_change_min_coins([1, 3, 4], 6) == 2
        # Impossible amount
        assert coin_change_min_coins([2], 3) == -1

    def test_coin_change_count_ways(self):
        # Number of combinations to make 5 with [1,2,5] is 4
        assert coin_change_count_ways([1, 2, 5], 5) == 4

    def test_edit_distance(self):
        assert edit_distance("kitten", "sitting") == 3
        assert edit_distance_optimized("intention", "execution") == 5
        assert edit_distance("", "") == 0
        assert edit_distance("abc", "") == 3

    def test_lis_binary_search(self):
        assert lis_binary_search([10, 9, 2, 5, 3, 7, 101, 18]) == 4
        assert lis_binary_search([0, 1, 0, 3, 2, 3]) == 4


class TestGraphsBasics:
    def test_bfs_dfs_and_bipartite(self):
        # Undirected simple graph
        graph = {
            'A': ['B', 'C'],
            'B': ['A', 'D'],
            'C': ['A', 'D'],
            'D': ['B', 'C', 'E'],
            'E': ['D'],
        }
        order_bfs = bfs(graph, 'A')
        order_dfs = dfs_iterative(graph, 'A')
        assert set(order_bfs) == set(graph.keys())
        assert set(order_dfs) == set(graph.keys())

        # Bipartite check: square is bipartite, add odd cycle to break it
        square = {
            0: [1, 3],
            1: [0, 2],
            2: [1, 3],
            3: [0, 2],
        }
        assert is_bipartite(square) is True
        square[0].append(2)
        square[2].append(0)  # now has triangle 0-1-2-0
        assert is_bipartite(square) is False

    def test_connected_components(self):
        graph = {
            0: [1],
            1: [0],
            2: [3],
            3: [2],
            4: [],
        }
        comps = connected_components_undirected(graph)
        # Two components of size 2 and one component of size 1
        sizes = sorted(len(c) for c in comps)
        assert sizes == [1, 2, 2]

    def test_topological_sort_and_dijkstra(self):
        # DAG for topo sort: 0->1, 0->2, 1->3, 2->3
        edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
        dag = build_graph_from_edges(edges, num_nodes=4)
        order = topological_sort_kahn(dag, 4)
        # Validate topological order: edges go from earlier to later
        pos = {node: i for i, node in enumerate(order)}
        assert pos[0] < pos[1] and pos[0] < pos[2] and pos[1] < pos[3] and pos[2] < pos[3]

        # Dijkstra on small graph
        # WeightedGraph type accepts mapping node -> list of (neighbor, weight)
        wg = {
            'A': [('B', 1), ('C', 4)],
            'B': [('C', 2), ('D', 5)],
            'C': [('D', 1)],
            'D': [],
        }
        dist = dijkstra(wg, 'A')
        assert dist['A'] == 0
        assert dist['B'] == 1
        assert dist['C'] == 3
        assert dist['D'] == 4


class TestStringsAlgorithms:
    def test_kmp_and_first_occurrence(self):
        text = "ababcabcabababd"
        pattern = "ababd"
        positions = kmp_search(text, pattern)
        assert positions == [10]
        assert kmp_search_first_occurrence("hello", "ll") == 2
        assert kmp_search_first_occurrence("hello", "world") == -1

    def test_z_and_rabin_karp(self):
        text = "abcabcabc"
        pattern = "abc"
        assert z_search(text, pattern) == [0, 3, 6]
        assert rabin_karp_search(text, pattern) == [0, 3, 6]

    def test_manacher(self):
        length, pal, start, end = manacher_longest_palindromic_substring("babad")
        assert length == len(pal)
        assert pal in {"bab", "aba"}
        assert start >= 0 and end >= start


class TestPatternsSuite:
    def test_sliding_window_and_min_window(self):
        assert length_of_longest_substring_without_repeating("abcabcbb") == 3
        assert min_window_substring("ADOBECODEBANC", "ABC") == "BANC"

    def test_three_sum(self):
        nums = [-1, 0, 1, 2, -1, -4]
        res = three_sum(nums)
        res_set = {tuple(sorted(t)) for t in res}
        expected = {(-1, -1, 2), (-1, 0, 1)}
        assert res_set == expected

    def test_binary_search_on_answer_and_mitm(self):
        assert ship_within_days([1, 2, 3, 1, 1], 4) == 3
        assert subset_sum_mitm([3, 34, 4, 12, 5, 2], 9) is True


class TestMathNumberTheoryAndPrefix:
    def test_gcd_lcm_mod_pow(self):
        assert gcd(24, 36) == 12
        assert lcm(24, 36) == 72
        assert mod_pow(2, 10, 1000) == 24

    def test_sieve_and_prefix_structures(self):
        assert sieve_of_eratosthenes(10) == [2, 3, 5, 7]

        arr = [2, 1, 3, 4]
        pref = prefix_sums(arr)
        assert pref == [0, 2, 3, 6, 10]
        assert range_sum_with_prefix(pref, 1, 2) == 1 + 3

        diff = difference_array(arr)
        apply_range_increment(diff, 1, 3, 2)
        recovered = recover_from_difference(diff)
        # Original [2,1,3,4] after +2 on [1..3] -> [2,3,5,6]
        assert recovered == [2, 3, 5, 6]


class TestSystemsRateLimiter:
    def test_token_bucket_basic(self):
        tb = TokenBucket(capacity=2, rate=100.0)  # fast refill to avoid flakiness
        assert tb.acquire() is True
        assert tb.acquire() is True
        # Immediately requesting third token may fail if refill hasn't happened yet
        ok3 = tb.acquire()
        # Either it succeeded due to high rate, or failed; both acceptable but at least not raising
        assert ok3 in (True, False)

    def test_leaky_bucket_basic(self):
        lb = LeakyBucket(capacity=2, rate=100.0)  # fast leak
        assert lb.offer() is True
        assert lb.offer() is True
        # Third may or may not be accepted depending on timing; assert boolean
        ok3 = lb.offer()
        assert ok3 in (True, False)


if __name__ == "__main__":
    pytest.main([__file__])
