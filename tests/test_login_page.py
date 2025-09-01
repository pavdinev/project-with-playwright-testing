# tests/test_login_page.py
from tests.base_test import BaseTest
from pages.login_page import LoginPage
import config

SPECIALS = ["!", "@", "/", "*", "\\", '"']

class LoginPageTests(BaseTest):

    def setUp(self):
        super().setUp()
        self.page.goto(config.BASE_URL)  # Login page URL
        self.login = LoginPage(self.page)

    def test_fields_visible_and_scroll(self):
        # Scroll the page using smart_scroll to detect fields/buttons
        assert self.login.scroll_all() is True
        assert self.login.is_username_visible() is True
        assert self.login.is_password_visible() is True
        assert self.login.is_login_button_visible() is True

    def test_wrong_credentials_show_error(self):
        assert self.login.fill_username("bad_user")
        assert self.login.fill_password("bad_pass")
        assert self.login.click_login()
        assert self.login.error_visible() is True
        assert len(self.login.get_error_text()) > 0

    def test_special_characters_in_fields(self):
        for s in SPECIALS:
            assert self.login.fill_username(s)
            assert self.login.fill_password(s)
        assert self.login.click_login()
        assert self.login.error_visible() is True

    def test_empty_fields_login(self):
        assert self.login.fill_username("")
        assert self.login.fill_password("")
        assert self.login.click_login()
        assert self.login.error_visible() is True

    def test_login_standard_user(self):
        """Perform correct login to cache standard user login page elements."""
        username = config.USERS["standard_user"]["username"]
        password = config.USERS["standard_user"]["password"]

        # Fill fields and click login
        assert self.login.fill_username(username)
        assert self.login.fill_password(password)
        assert self.login.click_login()

        # Stop immediately if login fails
        self.assertTrue(self.page.url.endswith("inventory.html"),
                        "Standard user should reach inventory page")

        # --- Cache login page elements only (not inventory) ---
        self.cache_standard_user_state("login_username_visible", self.login.is_username_visible())
        self.cache_standard_user_state("login_password_visible", self.login.is_password_visible())
        self.cache_standard_user_state("login_button_visible", self.login.is_login_button_visible())

        self.cache_standard_user_state("login_username_type", self.login.get_username_type())
        self.cache_standard_user_state("login_password_type", self.login.get_password_type())
        self.cache_standard_user_state("login_button_value", self.login.get_login_button_value())

        self.save_standard_cache_to_file()
