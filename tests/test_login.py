# tests/test_login.py
from pages.login_page import LoginPage
from tests.base_test import BaseTest
from config import DEFAULT_USER
from pages.inventory_page import InventoryPage

class TestLogin(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = LoginPage(self.page)
        self.login_page.navigate()

    def test_login_success(self):
        self.login_page.login(DEFAULT_USER["username"], DEFAULT_USER["password"])
        # use InventoryPage to check if logged in
        inv = InventoryPage(self.page)
        self.assertTrue(inv.is_loaded())
