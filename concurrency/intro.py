import time
import threading
import asyncio
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import List, Tuple

"""
Concurrency & Parallelism in Python - Practical Overview

Covers:
- Threading (and GIL limitations)
- Producer-Consumer pattern with threads
- Multiprocessing (true parallel CPU-bound work)
- asyncio (async/await patterns for IO-bound concurrency)
- concurrent.futures (unified high-level API)

Guidance:
- CPU-bound: Prefer multiprocessing or native extensions (NumPy) due to the GIL.
- IO-bound (network/file/db): threading or asyncio are effective.
- Avoid oversubscription: too many threads/processes can degrade performance.
"""


# ------------------------
# Threading Basics (IO-Bound)
# ------------------------
def fetch_io_simulated(id: int, delay: float = 0.3) -> Tuple[int, float]:
    """Simulate IO-bound task (e.g., HTTP request) with time.sleep."""
    time.sleep(delay)
    return id, delay


def threading_demo(num_tasks: int = 10, delay: float = 0.3, max_workers: int = 4) -> List[Tuple[int, float]]:
    """
    Use ThreadPoolExecutor for IO-bound tasks. Demonstrates GIL-friendly concurrency.
    """
    start = time.perf_counter()
    results: List[Tuple[int, float]] = []
    with ThreadPoolExecutor(max_workers=max_workers) as tp:
        futures = [tp.submit(fetch_io_simulated, i, delay) for i in range(num_tasks)]
        for fut in as_completed(futures):
            results.append(fut.result())
    elapsed = time.perf_counter() - start
    print(f"[threading] Completed {num_tasks} I/O tasks in {elapsed:.2f}s with {max_workers} threads")
    return results


# ------------------------
# Producer-Consumer (Threads + Queue)
# ------------------------
def producer_consumer_demo(num_items: int = 20, num_workers: int = 3) -> None:
    """
    Classic producer-consumer using Queue for thread-safe communication.
    """
    q: Queue[int] = Queue(maxsize=50)

    def producer():
        for i in range(num_items):
            q.put(i)
            # Simulate production time
            time.sleep(0.01)
        # Signal shutdown to workers
        for _ in range(num_workers):
            q.put(None)  # type: ignore

    def worker(wid: int):
        while True:
            item = q.get()
            if item is None:
                q.task_done()
                print(f"[worker-{wid}] shutting down")
                break
            # Simulate processing
            time.sleep(0.02)
            print(f"[worker-{wid}] processed {item}")
            q.task_done()

    threads = [threading.Thread(target=worker, args=(w,)) for w in range(num_workers)]
    for t in threads:
        t.start()

    prod = threading.Thread(target=producer)
    prod.start()

    q.join()
    prod.join()
    for t in threads:
        t.join()


# ------------------------
# Multiprocessing (CPU-Bound)
# ------------------------
def cpu_bound(n: int) -> int:
    """
    CPU-bound task: sum of squares 0..n-1 (toy example).
    Real CPU tasks might be image processing, ML, crypto, etc.
    """
    total = 0
    for i in range(n):
        total += i * i
    return total


def multiprocessing_demo(work_items: List[int], max_workers: int = 4) -> List[int]:
    """
    Use ProcessPoolExecutor for true parallelism on CPU-bound tasks.
    """
    start = time.perf_counter()
    results: List[int] = []
    with ProcessPoolExecutor(max_workers=max_workers) as pp:
        futures = [pp.submit(cpu_bound, n) for n in work_items]
        for fut in as_completed(futures):
            results.append(fut.result())
    elapsed = time.perf_counter() - start
    print(f"[multiprocessing] Completed {len(work_items)} CPU tasks in {elapsed:.2f}s with {max_workers} processes")
    return results


# ------------------------
# asyncio (IO-Bound, High Concurrency)
# ------------------------
async def async_fetch_io_simulated(id: int, delay: float = 0.3) -> Tuple[int, float]:
    await asyncio.sleep(delay)
    return id, delay


async def asyncio_demo(num_tasks: int = 20, delay: float = 0.1, concurrency: int = 10) -> List[Tuple[int, float]]:
    """
    Run many IO-bound tasks concurrently with asyncio & semaphore (rate limiting).
    """
    sem = asyncio.Semaphore(concurrency)
    results: List[Tuple[int, float]] = []

    async def bounded_task(i: int):
        async with sem:
            res = await async_fetch_io_simulated(i, delay)
            results.append(res)

    start = time.perf_counter()
    await asyncio.gather(*(bounded_task(i) for i in range(num_tasks)))
    elapsed = time.perf_counter() - start
    print(f"[asyncio] Completed {num_tasks} async I/O tasks in {elapsed:.2f}s with concurrency={concurrency}")
    return results


def demo():
    print("Concurrency & Parallelism Demo")
    print("=" * 40)

    # Threading demo (I/O-bound)
    threading_demo(num_tasks=12, delay=0.2, max_workers=4)
    print()

    # Producer-Consumer
    print("Producer-Consumer (threads + Queue):")
    producer_consumer_demo(num_items=12, num_workers=3)
    print()

    # Multiprocessing demo (CPU-bound)
    work = [5_000_00, 600_000, 700_000, 800_000]  # adjust workload to your machine
    multiprocessing_demo(work_items=work, max_workers=4)
    print()

    # asyncio demo (I/O-bound, high concurrency)
    print("asyncio high-concurrency demo:")
    asyncio.run(asyncio_demo(num_tasks=25, delay=0.05, concurrency=8))
    print()

    print("Notes & Interview Tips:")
    print("  - GIL: only one Python bytecode thread runs at a time; use threads for I/O, processes for CPU.")
    print("  - asyncio: single-threaded concurrency via event loop; great for sockets/HTTP/db with async drivers.")
    print("  - concurrent.futures: unified interface; ThreadPoolExecutor vs ProcessPoolExecutor.")
    print("  - Producer-Consumer: Queue provides safe cross-thread communication and backpressure.")
    print("  - Be mindful of context switching overhead, and use appropriate pool sizes.")


if __name__ == "__main__":
    demo()
