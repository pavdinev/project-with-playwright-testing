from config import DEFAULT_USER
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from tests.base_test import BaseTest


class TestLogin(BaseTest):
    def test_login_success(self):
        login = LoginPage(self.page)
        login.navigate()
        login.login(DEFAULT_USER["username"], DEFAULT_USER["password"])


        inv = InventoryPage(self.page)
        self.assertTrue(inv.is_loaded(), "Inventory should be visible after login")


    def test_login_failure(self):
        login = LoginPage(self.page)
        login.navigate()
        login.login("standard_user", "wrong_password")


        err = login.get_error()
        self.assertIn("Username and password do not match", err)