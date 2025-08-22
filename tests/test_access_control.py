from pages.login_page import LoginPage
from tests.base_test import BaseTest

class TestAccessControl(BaseTest):

    def test_login_failure_invalid_credentials(self):
        login_page = LoginPage(self.page)
        login_page.navigate()
        login_page.login("wrong", "wrong")
        self.assertTrue(login_page.get_error_message())

    def test_locked_out_user(self):
        login_page = LoginPage(self.page)
        login_page.navigate()
        login_page.login("locked_out_user", "secret_sauce")
        self.assertIn("locked out", login_page.get_error_message())

    def test_direct_inventory_access_redirects_to_login(self):
        self.page.goto("https://www.saucedemo.com/inventory.html")
        self.assertEqual(self.page.url, "https://www.saucedemo.com/")
        login_page = LoginPage(self.page)
        self.assertTrue(login_page.get_error_message()) 