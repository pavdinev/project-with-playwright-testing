import os
import re
from typing import List

PRICE_RE = re.compile(r"[-+]?[0-9]*\.?[0-9]+")


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def parse_price(text: str) -> float:
    """Extract first decimal number from strings like "$29.99" → 29.99"""
    m = PRICE_RE.search(text)
    return float(m.group(0)) if m else 0.0


def is_sorted(values: List, reverse: bool = False) -> bool:
    return values == sorted(values, reverse=reverse)