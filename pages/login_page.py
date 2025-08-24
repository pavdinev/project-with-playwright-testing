import config
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("h3[data-test='error']")

    def navigate(self):
        """Navigate to login page"""
        self.page.goto(config.BASE_URL)

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error(self):
        """Alias for get_error_message() so tests using login.get_error() don’t break"""
        return self.get_error_message()

    def get_error_message(self):
        return self.error_message.inner_text()
