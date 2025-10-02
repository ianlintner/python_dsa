from __future__ import annotations

from collections import OrderedDict


class LFUCache:
    """
    LFU Cache with O(1) average get/put using:
      - key -> (value, freq)
      - freq -> OrderedDict of keys (to resolve ties by LRU within same freq)
      - min_freq to know the lowest frequency present

    Operations:
      - get(key): return value or -1; increases key's frequency
      - put(key, value): insert/update; evict LFU (and LRU among them) if capacity exceeded

    Time:
      - get/put: O(1) amortized
    Space:
      - O(capacity)
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self.key_to_val_freq: dict[int, tuple[int, int]] = {}  # key -> (value, freq)
        self.freq_to_keys: dict[
            int, OrderedDict[int, None]
        ] = {}  # freq -> OrderedDict of keys (None placeholders)
        self.min_freq = 0

    def _touch(self, key: int, new_value: int | None = None) -> None:
        """Increase frequency of key; optionally update its value."""
        val, freq = self.key_to_val_freq[key]
        if new_value is not None:
            val = new_value

        # Remove from current frequency bucket
        bucket = self.freq_to_keys[freq]
        if key in bucket:
            bucket.pop(key)
        if not bucket:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        # Add to next frequency bucket
        freq += 1
        self.freq_to_keys.setdefault(freq, OrderedDict())
        self.freq_to_keys[freq][key] = None
        self.key_to_val_freq[key] = (val, freq)

    def get(self, key: int) -> int:
        if key not in self.key_to_val_freq:
            return -1
        self._touch(key)
        return self.key_to_val_freq[key][0]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.key_to_val_freq:
            # Update value and bump freq
            self._touch(key, new_value=value)
            return
        # Evict if needed
        if self.size >= self.capacity:
            # Evict LFU: pick key from min_freq bucket, LRU (front) within that freq
            bucket = self.freq_to_keys.get(self.min_freq)
            if bucket:
                evict_key, _ = bucket.popitem(last=False)
                if not bucket:
                    del self.freq_to_keys[self.min_freq]
                if evict_key in self.key_to_val_freq:
                    del self.key_to_val_freq[evict_key]
                self.size -= 1
        # Insert as freq=1
        self.key_to_val_freq[key] = (value, 1)
        self.freq_to_keys.setdefault(1, OrderedDict())
        self.freq_to_keys[1][key] = None
        self.min_freq = 1
        self.size += 1

    def __len__(self) -> int:
        return self.size


def demo():
    print("LFU Cache Demo (LeetCode 460 behavior)")
    print("=" * 40)
    cache = LFUCache(2)
    cache.put(1, 1)  # {1:1(f1)}
    cache.put(2, 2)  # {1:1(f1), 2:2(f1)}
    print(cache.get(1))  # 1; {1:1(f2), 2:2(f1)}
    cache.put(3, 3)  # evict key=2 (freq1 LRU); {1:1(f2), 3:3(f1)}
    print(cache.get(2))  # -1
    print(cache.get(3))  # 3; {1:1(f2), 3:3(f2)}
    cache.put(
        4, 4
    )  # evict key=1 (freq2 LRU among freq2? both 1 and 3 have f2; 1 is older) -> {3:3(f2),4:4(f1)}
    print(cache.get(1))  # -1
    print(cache.get(3))  # 3; {3:3(f3),4:4(f1)}
    print(cache.get(4))  # 4; {3:3(f3),4:4(f2)}

    print("\nNotes & Interview Tips:")
    print("  - Track min_freq to locate LFU bucket quickly.")
    print("  - Within same frequency, evict the least recently used (OrderedDict FIFO).")
    print("  - All operations are O(1) amortized using hash maps + OrderedDict.")


if __name__ == "__main__":
    demo()
