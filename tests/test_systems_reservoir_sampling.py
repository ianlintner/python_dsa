import itertools

from interview_workbook.systems.reservoir_sampling import (
    infinite_stream,
    reservoir_sample_k,
    reservoir_sample_k_weighted,
    reservoir_sample_one,
)


def test_reservoir_sample_one_deterministic():
    data = list(range(1, 101))
    # With seed set, result should be deterministic
    s1 = reservoir_sample_one(data, seed=42)
    s2 = reservoir_sample_one(data, seed=42)
    assert s1 == s2
    assert s1 in data


def test_reservoir_sample_k_basic_and_small_stream():
    data = list(range(10))
    # Deterministic with seed
    samp1 = reservoir_sample_k(data, 5, seed=0)
    samp2 = reservoir_sample_k(data, 5, seed=0)
    assert samp1 == samp2
    assert len(samp1) == 5
    assert all(x in data for x in samp1)

    # k <= 0 returns empty
    assert reservoir_sample_k(data, 0, seed=1) == []

    # Small stream returns all elements if fewer than k
    small = [10, 20, 30]
    got = reservoir_sample_k(small, 5, seed=123)
    assert sorted(got) == small


def test_reservoir_sample_k_weighted_bias_and_determinism():
    data = list(range(1, 21))
    weighted_stream = [(x, float(x)) for x in data]
    w1 = reservoir_sample_k_weighted(weighted_stream, 5, seed=123)
    w2 = reservoir_sample_k_weighted(weighted_stream, 5, seed=123)
    assert w1 == w2
    # With weights proportional to value, larger numbers should appear frequently
    assert all(x in data for x in w1)
    assert max(w1) > min(w1)


def test_infinite_stream_slice_with_reservoir():
    # Take first 1000 numbers from infinite stream and sample 5
    stream = infinite_stream(0)
    first_1000 = itertools.islice(stream, 1000)
    samp = reservoir_sample_k(first_1000, 5, seed=99)
    assert len(samp) == 5
    assert all(0 <= x < 1000 for x in samp)
