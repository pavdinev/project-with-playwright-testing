import os
import unittest
from playwright.sync_api import sync_playwright
from config import HEADLESS, SCREENSHOT_DIR
from utils.helpers import ensure_dir


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_dir(SCREENSHOT_DIR)
        cls._pw = sync_playwright().start()
        cls._browser = cls._pw.chromium.launch(headless=HEADLESS)
    
    
    @classmethod
    def tearDownClass(cls):
        cls._browser.close()
        cls._pw.stop()
    
    
    def setUp(self):
        self.context = self._browser.new_context()
        self.page = self.context.new_page()
    
    
    def tearDown(self):
        # Capture a screenshot artifact for every test (pass/fail)
        name = f"{self.__class__.__name__}.{self._testMethodName}.png"
        path = os.path.join(SCREENSHOT_DIR, name)
        try:
            self.page.screenshot(path=path, full_page=True)
        except Exception:
            pass
        finally:
            self.page.close()
            self.context.close()