# tests/test_login_page.py
from tests.base_test import BaseTest
from pages.login_page import LoginPage
import config

SPECIALS = ["!", "@", "/", "*", "\\", '"']


class LoginPageTests(BaseTest):

    def setUp(self):
        super().setUp()
        self.page.goto(config.BASE_URL)
        self.login = LoginPage(self.page, record_fn=self.record_fn)

    # ------------------- Tests -------------------
    def test_fields_visible_and_scroll(self):
        self.login.scroll_all()
        self.assertTrue(self.login.is_username_visible(), "Username field should be visible")
        self.assertTrue(self.login.is_password_visible(), "Password field should be visible")
        self.assertTrue(self.login.is_login_button_visible(), "Login button should be visible")

    def test_wrong_credentials_show_error(self):
        self.login.fill_username("bad_user")
        self.login.fill_password("bad_pass")
        self.login.click_login()
        self.assertTrue(self.login.error_visible(), "Error message should be visible")
        self.assertGreater(len(self.login.get_error_text()), 0, "Error text should not be empty")

    def test_special_characters_in_fields(self):
        for s in SPECIALS:
            self.login.fill_username(s)
            self.login.fill_password(s)
        self.login.click_login()
        self.assertTrue(self.login.error_visible(), "Error message should appear for special chars")

    def test_empty_fields_login(self):
        self.login.fill_username("")
        self.login.fill_password("")
        self.login.click_login()
        self.assertTrue(self.login.error_visible(), "Error message should appear for empty fields")

    def test_login_standard_user(self):
        username = config.USERS["standard_user"]["username"]
        password = config.USERS["standard_user"]["password"]

        self.login.fill_username(username)
        self.login.fill_password(password)
        self.login.click_login()

        # Assert successful login
        self.assertTrue(
            self.page.url.endswith("inventory.html"),
            "Standard user should reach inventory page"
        )
