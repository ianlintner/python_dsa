from __future__ import annotations

import random
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Sequence, Tuple


class NGramLM:
    """
    Simple n-gram language model with add-k smoothing and sampling.
    Expects tokenized corpus (list of tokens). Uses tuples for (n-1)-gram contexts.
    """

    def __init__(self, n: int = 2, k: float = 1.0, seed: Optional[int] = None) -> None:
        if n < 1:
            raise ValueError("n must be >= 1")
        self.n = n
        self.k = k
        self.rng = random.Random(seed)
        self.context_counts: Dict[Tuple[str, ...], Counter] = defaultdict(Counter)
        self.vocab: set[str] = set()

    def fit(self, tokens: Sequence[str]) -> "NGramLM":
        self.vocab = set(tokens)
        if self.n == 1:
            for t in tokens:
                self.context_counts[()].update([t])
            return self

        pad = ["<s>"] * (self.n - 1)
        seq = pad + list(tokens) + ["</s>"]
        for i in range(len(seq) - self.n + 1):
            ngram = tuple(seq[i : i + self.n])
            ctx, nxt = ngram[:-1], ngram[-1]
            self.context_counts[ctx].update([nxt])
        return self

    def prob(self, context: Sequence[str], token: str) -> float:
        if self.n == 1:
            ctx = ()
        else:
            ctx = tuple((["<s>"] * (self.n - 1 - len(context))) + list(context))[
                -(self.n - 1) :
            ]
        counts = self.context_counts.get(ctx, Counter())
        V = max(len(self.vocab), 1)
        num = counts.get(token, 0) + self.k
        denom = sum(counts.values()) + self.k * V
        return num / max(denom, 1e-12)

    def next_token(self, context: Sequence[str]) -> str:
        if not self.vocab:
            raise RuntimeError("Model not fitted")
        tokens = list(self.vocab) + ["</s>"]
        probs = [self.prob(context, t) for t in tokens]
        # Normalize
        s = sum(probs) or 1.0
        r = self.rng.random()
        acc = 0.0
        for t, p in zip(tokens, probs):
            acc += p / s
            if r <= acc:
                return t
        return tokens[-1]

    def generate(self, max_len: int = 20) -> List[str]:
        out: List[str] = []
        ctx: List[str] = []
        for _ in range(max_len):
            t = self.next_token(ctx)
            if t == "</s>":
                break
            out.append(t)
            ctx = (ctx + [t])[-(self.n - 1) :] if self.n > 1 else []
        return out
