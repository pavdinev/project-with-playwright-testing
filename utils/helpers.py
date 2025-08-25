import os
import re
from typing import List
import traceback
import time
from playwright.sync_api import Page

PRICE_RE = re.compile(r"[-+]?[0-9]*\.?[0-9]+")


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def parse_price(text: str) -> float:
    """Extract first decimal number from strings like "$29.99" → 29.99"""
    m = PRICE_RE.search(text)
    return float(m.group(0)) if m else 0.0


def is_sorted(values: List, reverse: bool = False) -> bool:
    return values == sorted(values, reverse=reverse)


def format_error(e: Exception) -> str:
    """
    Returns formatted error string with file, line, and function details.
    Example:
    ValueError: Invalid input (File test_full_pipeline.py, line 42, in run_pipeline)
    """
    tb = traceback.extract_tb(e.__traceback__)
    if tb:
        last_call = tb[-1]
        return f"{str(e)} (File {last_call.filename}, line {last_call.lineno}, in {last_call.name})"
    return str(e)

def smart_scroll(page: Page, pause: float = 0.3, back_to_top: bool = False, container_selector: str = None):
    """
    Scroll through a page or a container until the bottom (or top if back_to_top=True).
    """
    if container_selector:
        scrollable = f'document.querySelector("{container_selector}")'
    else:
        scrollable = "document.scrollingElement"

    if back_to_top:
        page.evaluate(f"{scrollable}.scrollTop = 0")
        time.sleep(pause)

    last_scroll = -1
    same_count = 0
    while True:
        scroll_height = page.evaluate(f"{scrollable}.scrollHeight")
        scroll_top = page.evaluate(f"{scrollable}.scrollTop")
        client_height = page.evaluate(f"{scrollable}.clientHeight")
        new_scroll = min(scroll_top + client_height, scroll_height)
        if new_scroll == last_scroll:
            same_count += 1
            if same_count >= 2:
                break
        else:
            same_count = 0
            page.evaluate(f"{scrollable}.scrollTop = {new_scroll}")
            time.sleep(pause)
        last_scroll = new_scroll

    if back_to_top:
        page.evaluate(f"{scrollable}.scrollTop = 0")
        time.sleep(pause)
