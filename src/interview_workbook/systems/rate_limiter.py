from __future__ import annotations

import threading
import time


class TokenBucket:
    """
    Token Bucket rate limiter.

    - capacity: max tokens the bucket can hold
    - rate: tokens added per second (float supported)

    acquire(n=1) returns True if n tokens are available immediately, else False.
    acquire_blocking(n=1, timeout=None) waits up to timeout seconds for tokens.

    Thread-safe.

    Use cases:
      - API request limiting (QPS)
      - Smooth burst handling up to capacity
    """

    def __init__(self, capacity: int, rate: float):
        if capacity <= 0 or rate <= 0:
            raise ValueError("capacity and rate must be > 0")
        self.capacity = float(capacity)
        self.rate = float(rate)
        self._tokens = float(capacity)
        self._last = time.monotonic()
        self._lock = threading.Lock()
        self._cv = threading.Condition(self._lock)

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last
        if elapsed > 0:
            self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
            self._last = now

    def acquire(self, n: int = 1) -> bool:
        with self._lock:
            self._refill()
            if self._tokens >= n:
                self._tokens -= n
                return True
            return False

    def acquire_blocking(self, n: int = 1, timeout: float | None = None) -> bool:
        end = None if timeout is None else time.monotonic() + timeout
        with self._cv:
            while True:
                self._refill()
                if self._tokens >= n:
                    self._tokens -= n
                    return True
                if timeout is not None:
                    remaining = end - time.monotonic()
                    if remaining <= 0:
                        return False
                    # Wait a bit or remaining time, whichever smaller
                    self._cv.wait(timeout=min(remaining, 0.05))
                else:
                    self._cv.wait(timeout=0.05)


class LeakyBucket:
    """
    Leaky Bucket rate limiter.

    - capacity: max queue size
    - rate: leak rate (items per second)

    offer() returns True if request accepted into bucket, else False when bucket full.
    drip() is called implicitly on offer to leak according to rate.

    Behavior:
      - Smooths bursts by queuing up to capacity
      - Constant leak rate over time

    Thread-safe.
    """

    def __init__(self, capacity: int, rate: float):
        if capacity <= 0 or rate <= 0:
            raise ValueError("capacity and rate must be > 0")
        self.capacity = capacity
        self.rate = rate
        self._queue = 0  # queued items
        self._last = time.monotonic()
        self._lock = threading.Lock()

    def _drip(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last
        if elapsed <= 0:
            return
        leaked = elapsed * self.rate
        if leaked > 0:
            self._queue = max(0, self._queue - leaked)
            self._last = now

    def offer(self) -> bool:
        with self._lock:
            self._drip()
            if self._queue + 1 <= self.capacity:
                self._queue += 1
                return True
            return False


def demo():
    print("Rate Limiter Demo (TokenBucket, LeakyBucket)")
    print("=" * 50)

    # Token bucket: capacity 5 tokens, refill 2 tokens/sec
    tb = TokenBucket(capacity=5, rate=2.0)
    print("TokenBucket test (5 capacity, 2 tokens/sec):")
    accepted = 0
    for _ in range(10):
        ok = tb.acquire()
        print(f"  acquire() -> {ok}")
        if ok:
            accepted += 1
        time.sleep(0.2)  # simulate time passing
    print(f"Accepted immediately: {accepted}/10")
    print()

    # Token bucket blocking acquire
    print("TokenBucket acquire_blocking for 3 tokens with timeout:")
    ok = tb.acquire_blocking(n=3, timeout=3.0)
    print(f"  acquire_blocking(3, timeout=3) -> {ok}")
    print()

    # Leaky bucket: capacity 5 queued, leak 2 items/sec
    lb = LeakyBucket(capacity=5, rate=2.0)
    print("LeakyBucket test (5 capacity, leak 2/sec):")
    results = []
    for _ in range(10):
        ok = lb.offer()
        results.append(ok)
        time.sleep(0.1)
    print(f"  offer() results: {results}")
    print()

    print("Notes & Interview Tips:")
    print("  - Token bucket: limits average rate while allowing bursts up to capacity.")
    print("  - Leaky bucket: enforces a fixed outflow rate by queuing/dropping excess.")
    print(
        "  - Distributed systems: combine local buckets with centralized quota for global rate limiting."
    )
    print(
        "  - Consider time precision, thread/process safety, and fairness across clients."
    )


if __name__ == "__main__":
    demo()
