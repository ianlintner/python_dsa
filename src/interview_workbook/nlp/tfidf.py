from __future__ import annotations

import math
from typing import Dict, List, Sequence


class TfidfVectorizer:
    """
    Minimal TF-IDF vectorizer for tokenized documents (list of tokens per doc).
    Returns sparse vectors as dict[token, weight].
    """

    def __init__(self, smooth_idf: bool = True) -> None:
        self.smooth_idf = smooth_idf
        self.vocabulary_: Dict[str, int] = {}
        self.idf_: Dict[str, float] = {}

    def fit(self, corpus_tokens: Sequence[Sequence[str]]) -> "TfidfVectorizer":
        N = len(corpus_tokens)
        if N == 0:
            raise ValueError("Empty corpus")
        # Document frequency
        df: Dict[str, int] = {}
        for doc in corpus_tokens:
            seen = set(doc)
            for t in seen:
                df[t] = df.get(t, 0) + 1

        # Build vocab and idf
        self.vocabulary_.clear()
        self.idf_.clear()
        for i, token in enumerate(sorted(df.keys())):
            self.vocabulary_[token] = i
            if self.smooth_idf:
                # 1 + log((1 + N) / (1 + df))
                self.idf_[token] = 1.0 + math.log((1.0 + N) / (1.0 + df[token]))
            else:
                self.idf_[token] = math.log(N / df[token])
        return self

    def transform(self, docs_tokens: Sequence[Sequence[str]]) -> List[Dict[str, float]]:
        if not self.vocabulary_:
            raise RuntimeError("Vectorizer not fitted")
        vectors: List[Dict[str, float]] = []
        for doc in docs_tokens:
            tf: Dict[str, float] = {}
            for t in doc:
                if t in self.vocabulary_:
                    tf[t] = tf.get(t, 0.0) + 1.0
            length = sum(tf.values()) or 1.0
            # tf-idf
            vec: Dict[str, float] = {}
            for t, cnt in tf.items():
                vec[t] = (cnt / length) * self.idf_[t]
            vectors.append(vec)
        return vectors

    def fit_transform(
        self, corpus_tokens: Sequence[Sequence[str]]
    ) -> List[Dict[str, float]]:
        return self.fit(corpus_tokens).transform(corpus_tokens)
