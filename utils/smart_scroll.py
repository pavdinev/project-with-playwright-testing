# utils/smart_scroll.py
import time
from playwright.sync_api import Page

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
