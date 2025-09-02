import os
import unittest
import json
import time
from playwright.sync_api import sync_playwright
from config import HEADLESS, SCREENSHOT_DIR


class BaseTest(unittest.TestCase):
    """Base class for all Playwright + unittest tests.
    Uses a class-level browser to avoid Windows asyncio issues.
    Provides utilities like visibility checks, smart scrolling, caching, and screenshot-on-failure.
    """

    # ------------------- Class-level setup/teardown -------------------
    @classmethod
    def setUpClass(cls):
        os.path.isdir(SCREENSHOT_DIR)
        cls._pw = sync_playwright().start()
        cls._browser = cls._pw.chromium.launch(headless=HEADLESS)

    @classmethod
    def tearDownClass(cls):
        cls._browser.close()
        cls._pw.stop()

    # ------------------- Per-test setup/teardown -------------------
    def setUp(self):
        self.context = self._browser.new_context()
        self.page = self.context.new_page()

        # Directory for screenshots
        self.screenshot_dir = SCREENSHOT_DIR
        os.makedirs(self.screenshot_dir, exist_ok=True)

        # Initialize standard user cache
        self._standard_cache = {}

    def tearDown(self):
        # Screenshot on failure (or always)
        name = f"{self.__class__.__name__}.{self._testMethodName}.png"
        path = os.path.join(self.screenshot_dir, name)
        try:
            self.page.screenshot(path=path, full_page=True)
        except Exception:
            pass
        finally:
            self.page.close()
            self.context.close()

    # ------------------- Reusable baseline checks -------------------
    def is_visible(self, locator) -> bool:
        try:
            return locator.is_visible()
        except Exception:
            return False

    def is_enabled(self, locator) -> bool:
        try:
            return locator.is_enabled()
        except Exception:
            return False

    def element_has_text(self, locator, text: str) -> bool:
        try:
            return text in locator.inner_text()
        except Exception:
            return False

    def element_has_attribute(self, locator, attribute: str, value: str) -> bool:
        try:
            return locator.get_attribute(attribute) == value
        except Exception:
            return False

    # ------------------- Smart scroll -------------------
    @staticmethod
    def smart_scroll(page, pause: float = 0.3, back_to_top: bool = False, container_selector: str = None):
        """
        Scrolls the entire page (or a scrollable container) step by step until the bottom is reached.
        Optionally scrolls back to the top afterwards.

        Args:
            page: Playwright Page instance.
            pause: Pause in seconds between scroll steps.
            back_to_top: Whether to scroll back to the top after reaching the bottom.
            container_selector: CSS selector of a scrollable container (if not the whole page).
        """
        scrollable = (
            f'document.querySelector("{container_selector}")'
            if container_selector
            else "document.scrollingElement"
        )

        # Optional scroll to top first
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
                if same_count >= 2:  # stop when no further scrolling is possible
                    break
            else:
                same_count = 0
                page.evaluate(f"{scrollable}.scrollTop = {new_scroll}")
                time.sleep(pause)

            last_scroll = new_scroll

        # Optional scroll back to top
        if back_to_top:
            page.evaluate(f"{scrollable}.scrollTop = 0")
            time.sleep(pause)