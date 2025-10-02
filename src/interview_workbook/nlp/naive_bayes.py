from __future__ import annotations

import math
from typing import Dict, List, Sequence


class MultinomialNB:
    """
    Multinomial Naive Bayes for tokenized text classification (pure Python).
    - fit accepts documents as list of tokens and labels.
    - predict returns the most likely class per document.
    """

    def __init__(self, alpha: float = 1.0) -> None:
        self.alpha = alpha
        self.classes_: List[str] = []
        self.class_log_prior_: Dict[str, float] = {}
        self.feature_log_prob_: Dict[str, Dict[str, float]] = {}  # class -> token -> log P(t|c)
        self.vocabulary_: set[str] = set()

    def fit(self, docs_tokens: Sequence[Sequence[str]], y: Sequence[str]) -> "MultinomialNB":
        if len(docs_tokens) != len(y):
            raise ValueError("Mismatched X/y lengths")
        n = len(y)
        self.classes_ = sorted(set(y))
        self.vocabulary_ = set(t for doc in docs_tokens for t in doc)

        # Priors
        counts = {c: 0 for c in self.classes_}
        for label in y:
            counts[label] += 1
        self.class_log_prior_ = {c: math.log(counts[c] / n) for c in self.classes_}

        # Likelihoods
        token_counts: Dict[str, Dict[str, int]] = {c: {} for c in self.classes_}
        class_token_totals: Dict[str, int] = {c: 0 for c in self.classes_}
        for doc, label in zip(docs_tokens, y):
            for t in doc:
                token_counts[label][t] = token_counts[label].get(t, 0) + 1
                class_token_totals[label] += 1

        V = len(self.vocabulary_) or 1
        self.feature_log_prob_ = {c: {} for c in self.classes_}
        for c in self.classes_:
            total = class_token_totals[c]
            denom = total + self.alpha * V
            for t in self.vocabulary_:
                num = token_counts[c].get(t, 0) + self.alpha
                self.feature_log_prob_[c][t] = math.log(num / denom)
        return self

    def predict_log_proba(self, docs_tokens: Sequence[Sequence[str]]) -> List[Dict[str, float]]:
        if not self.classes_:
            raise RuntimeError("Model not fitted")
        out: List[Dict[str, float]] = []
        for doc in docs_tokens:
            logp = {c: self.class_log_prior_[c] for c in self.classes_}
            for t in doc:
                if t in self.vocabulary_:
                    for c in self.classes_:
                        logp[c] += self.feature_log_prob_[c][t]
            out.append(logp)
        return out

    def predict(self, docs_tokens: Sequence[Sequence[str]]) -> List[str]:
        scores = self.predict_log_proba(docs_tokens)
        return [max(s.items(), key=lambda kv: kv[1])[0] for s in scores]
