from playwright.sync_api import Page
from tests.base_test import BaseTest
from utils.logging_helper import safe_action

class LoginPage:
    """Page Object for the Login page with robust logging."""

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("h3[data-test='error']")

    # ------------------ Interactions ------------------
    def fill_username(self, username: str) -> bool:
        return safe_action(f"fill username with '{username}'", lambda: self.username_input.fill(username), default=False)

    def fill_password(self, password: str) -> bool:
        return safe_action(f"fill password", lambda: self.password_input.fill(password), default=False)

    def click_login(self) -> bool:
        return safe_action("click login button", lambda: self.login_button.click(), default=False)

    def scroll_all(self) -> bool:
        return safe_action("scroll full page", lambda: BaseTest.smart_scroll(self.page), default=False)

    # ------------------ Visibility checks ------------------
    def is_username_visible(self) -> bool:
        return safe_action("check username visibility", lambda: self.username_input.is_visible(), default=False)

    def is_password_visible(self) -> bool:
        return safe_action("check password visibility", lambda: self.password_input.is_visible(), default=False)

    def is_login_button_visible(self) -> bool:
        return safe_action("check login button visibility", lambda: self.login_button.is_visible(), default=False)

    def error_visible(self) -> bool:
        return safe_action("check error message visibility", lambda: self.error_message.is_visible(), default=False)

    # ------------------ Attribute getters ------------------
    def get_username_type(self):
        return safe_action("get username type", lambda: self.username_input.get_attribute("type"))

    def get_username_placeholder(self):
        return safe_action("get username placeholder", lambda: self.username_input.get_attribute("placeholder"))

    def get_username_classes(self):
        return safe_action("get username classes", lambda: self.username_input.get_attribute("class"))

    def get_username_visible(self):
        return self.is_username_visible()

    def get_password_type(self):
        return safe_action("get password type", lambda: self.password_input.get_attribute("type"))

    def get_password_placeholder(self):
        return safe_action("get password placeholder", lambda: self.password_input.get_attribute("placeholder"))

    def get_password_classes(self):
        return safe_action("get password classes", lambda: self.password_input.get_attribute("class"))

    def get_password_visible(self):
        return self.is_password_visible()

    def get_login_button_value(self):
        return safe_action("get login button value", lambda: self.login_button.get_attribute("value"))

    def get_login_button_text(self):
        return safe_action("get login button text", lambda: self.login_button.inner_text())

    def get_login_button_visible(self):
        return self.is_login_button_visible()

    def get_error_text(self) -> str:
        return safe_action("get error text", lambda: self.error_message.inner_text(), default="") if self.error_visible() else ""

    # ------------------ Extract full page structure for caching ------------------
    def extract_login_page_structure(self):
        return {
            "fields": [
                {
                    "name": "username",
                    "locator": "#user-name",
                    "type": self.get_username_type(),
                    "placeholder": self.get_username_placeholder(),
                    "classes": self.get_username_classes(),
                    "visible": self.get_username_visible()
                },
                {
                    "name": "password",
                    "locator": "#password",
                    "type": self.get_password_type(),
                    "placeholder": self.get_password_placeholder(),
                    "classes": self.get_password_classes(),
                    "visible": self.get_password_visible()
                },
            ],
            "buttons": [
                {
                    "name": "login",
                    "locator": "#login-button",
                    "value": self.get_login_button_value(),
                    "text": self.get_login_button_text(),
                    "visible": self.get_login_button_visible()
                }
            ],
            "error_message": {
                "locator": "h3[data-test='error']",
                "text": self.get_error_text(),
                "visible": self.error_visible()
            }
        }
