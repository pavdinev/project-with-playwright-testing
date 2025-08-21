# pages/login_page.py

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("h3[data-test='error']")

    def load(self):
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error(self):
        return self.error_message.inner_text()

    def has_error(self):
        return self.error_message.is_visible()
