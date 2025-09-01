from playwright.sync_api import Page
from tests.base_test import BaseTest
import logging
import traceback

class LoginPage:
    """Page Object for the Login page."""

    def __init__(self, page: Page):
        self.page = page
        # Updated locators based on HTML
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("h3[data-test='error']")

    # ------------------ Interactions ------------------
    def fill_username(self, username: str) -> bool:
        try:
            self.username_input.fill(username)
            return True
        except Exception as e:
            logging.error(
                f"Failed to fill username. Exception: {e.__class__.__name__}: {e}"
            )
            logging.debug(traceback.format_exc())  # full traceback for debugging
            return False

    def fill_password(self, password: str) -> bool:
        try:
            self.password_input.fill(password)
            return True
        except Exception:
            return False

    def click_login(self) -> bool:
        try:
            self.login_button.click()
            return True
        except Exception:
            return False

    # ------------------ Checks ------------------
    def is_username_visible(self) -> bool:
        return self.username_input.is_visible()

    def is_password_visible(self) -> bool:
        return self.password_input.is_visible()

    def is_login_button_visible(self) -> bool:
        return self.login_button.is_visible()

    def error_visible(self) -> bool:
        return self.error_message.is_visible()

    def get_error_text(self) -> str:
        return self.error_message.inner_text() if self.error_visible() else ""

    def scroll_all(self) -> bool:
        try:
            BaseTest.smart_scroll(self.page)
            return True
        except Exception:
            return False

    # ------------------ Attribute getters for caching ------------------
    def get_username_type(self):
        return self.username_input.get_attribute("type")

    def get_username_placeholder(self):
        return self.username_input.get_attribute("placeholder")

    def get_username_classes(self):
        return self.username_input.get_attribute("class")

    def get_username_visible(self):
        return self.username_input.is_visible()

    def get_password_type(self):
        return self.password_input.get_attribute("type")

    def get_password_placeholder(self):
        return self.password_input.get_attribute("placeholder")

    def get_password_classes(self):
        return self.password_input.get_attribute("class")

    def get_password_visible(self):
        return self.password_input.is_visible()

    def get_login_button_value(self):
        return self.login_button.get_attribute("value")

    def get_login_button_text(self):
        return self.login_button.inner_text()

    def get_login_button_visible(self):
        return self.login_button.is_visible()

    # ------------------ Extract full page structure for caching ------------------
    def extract_login_page_structure(self):
        """Return a cache-friendly structure of login page"""
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
