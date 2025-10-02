from __future__ import annotations

import re
from typing import List


def whitespace_tokenize(text: str, lowercase: bool = True) -> List[str]:
    """Simple whitespace tokenizer."""
    if lowercase:
        text = text.lower()
    return [t for t in text.split() if t]


def regex_tokenize(text: str, pattern: str = r"\w+|[^\w\s]", lowercase: bool = True) -> List[str]:
    """Regex tokenizer; default keeps words and punctuation as tokens."""
    if lowercase:
        text = text.lower()
    return re.findall(pattern, text)
