from playwright.sync_api import Page
from utils.smart_scroll import smart_scroll
from functools import wraps


def record_step(description):
    """Decorator to wrap LoginPage methods for automatic step recording."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            step_desc = description or fn.__name__
            try:
                result = fn(self, *args, **kwargs)
                if self.record_fn:
                    self.record_fn({
                        "name": step_desc,
                        "ok": True,
                        "details": {"args": args, "kwargs": kwargs, "result": result}
                    })
                return result
            except Exception as e:
                if self.record_fn:
                    self.record_fn({
                        "name": step_desc,
                        "ok": False,
                        "details": {
                            "error": f"{e.__class__.__name__}: {e}",
                            "args": args,
                            "kwargs": kwargs
                        }
                    })
                raise
        return wrapper
    return decorator


class LoginPage:
    """Page Object for the Login page with automatic step recording via decorator."""

    def __init__(self, page: Page, record_fn=None):
        self.page = page
        self.record_fn = record_fn

        # Locators
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("h3[data-test='error']")

    # ------------------ Interactions (actions only, no return values) ------------------
    @record_step("fill username")
    def fill_username(self, username: str) -> None:
        self.username_input.fill(username)

    @record_step("fill password")
    def fill_password(self, password: str) -> None:
        self.password_input.fill(password)

    @record_step("click login button")
    def click_login(self) -> None:
        self.login_button.click()

    @record_step("scroll full page")
    def scroll_all(self) -> None:
        smart_scroll(self.page)

    # ------------------ Visibility checks ------------------
    @record_step("check username visibility")
    def is_username_visible(self) -> bool:
        return self.username_input.is_visible()

    @record_step("check password visibility")
    def is_password_visible(self) -> bool:
        return self.password_input.is_visible()

    @record_step("check login button visibility")
    def is_login_button_visible(self) -> bool:
        return self.login_button.is_visible()

    @record_step("check error message visibility")
    def error_visible(self) -> bool:
        return self.error_message.is_visible()

    # ------------------ Attribute getters ------------------
    @record_step("get username type")
    def get_username_type(self) -> str:
        return self.username_input.get_attribute("type")

    @record_step("get username placeholder")
    def get_username_placeholder(self) -> str:
        return self.username_input.get_attribute("placeholder")

    @record_step("get username classes")
    def get_username_classes(self) -> str:
        return self.username_input.get_attribute("class")

    @record_step("get password type")
    def get_password_type(self) -> str:
        return self.password_input.get_attribute("type")

    @record_step("get password placeholder")
    def get_password_placeholder(self) -> str:
        return self.password_input.get_attribute("placeholder")

    @record_step("get password classes")
    def get_password_classes(self) -> str:
        return self.password_input.get_attribute("class")

    @record_step("get login button value")
    def get_login_button_value(self) -> str:
        return self.login_button.get_attribute("value")

    @record_step("get login button text")
    def get_login_button_text(self) -> str:
        return self.login_button.inner_text()

    @record_step("get error text")
    def get_error_text(self) -> str:
        return self.error_message.inner_text() if self.error_visible() else ""

    # ------------------ Extract full page structure for caching ------------------
    @record_step("extract login page structure")
    def extract_login_page_structure(self):
        return {
            "fields": [
                {
                    "name": "username",
                    "locator": "#user-name",
                    "type": self.get_username_type(),
                    "placeholder": self.get_username_placeholder(),
                    "classes": self.get_username_classes(),
                    "visible": self.is_username_visible()
                },
                {
                    "name": "password",
                    "locator": "#password",
                    "type": self.get_password_type(),
                    "placeholder": self.get_password_placeholder(),
                    "classes": self.get_password_classes(),
                    "visible": self.is_password_visible()
                },
            ],
            "buttons": [
                {
                    "name": "login",
                    "locator": "#login-button",
                    "value": self.get_login_button_value(),
                    "text": self.get_login_button_text(),
                    "visible": self.is_login_button_visible()
                }
            ],
            "error_message": {
                "locator": "h3[data-test='error']",
                "text": self.get_error_text(),
                "visible": self.error_visible()
            }
        }
