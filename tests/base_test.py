import os
import unittest
from playwright.sync_api import sync_playwright
from config import HEADLESS, SCREENSHOT_DIR
from utils.report_generator import generate_full_pipeline_report


class BaseTest(unittest.TestCase):
    """Base class for all Playwright + unittest tests.
    Uses a class-level browser to avoid Windows asyncio issues.
    Provides utilities like visibility checks, smart scrolling,
    caching, screenshot-on-failure, and step collection for reports.
    """

    # ------------------- Class-level setup/teardown -------------------
    @classmethod
    def setUpClass(cls):
        os.path.isdir(SCREENSHOT_DIR)
        cls._pw = sync_playwright().start()
        cls._browser = cls._pw.chromium.launch(headless=HEADLESS)
        cls.all_steps = []  # accumulator for all steps across tests

    @classmethod
    def tearDownClass(cls):
        # generate full pipeline report at the end of all tests
        if cls.all_steps:
            user_data = {cls.__name__: {"steps": [s for t in cls.all_steps for s in t["steps"]]}}
            generate_full_pipeline_report(user_data, report_root="reports")
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

        # Per-test step collection
        self.steps = []
        self.record_fn = self.steps.append  # callback for page objects

    def tearDown(self):
        # Record this test's steps in class-level list
        self.__class__.all_steps.append({
            "test_name": self._testMethodName,
            "steps": self.steps
        })

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
