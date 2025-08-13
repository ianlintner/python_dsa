import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def timeit(fn: Callable) -> Callable:
    """Decorator to time function execution."""

    @wraps(fn)
    def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            dur = (time.perf_counter() - start) * 1000
            print(f"{fn.__name__} took {dur:.2f} ms")

    return wrapper


def time_algorithms(*algorithms):
    """Time multiple algorithms with the same input."""

    def decorator(test_fn):
        @wraps(test_fn)
        def wrapper(*args, **kwargs):
            print("\n=== Timing comparison ===")
            results = {}
            for algo in algorithms:
                start = time.perf_counter()
                result = test_fn(algo, *args, **kwargs)
                dur = (time.perf_counter() - start) * 1000
                results[algo.__name__] = (result, dur)
                print(f"{algo.__name__}: {dur:.2f} ms")
            return results

        return wrapper

    return decorator
