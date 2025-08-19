from playwright.sync_api import Page

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.zip_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")

    def start_checkout(self):
        self.page.locator("[data-test='checkout']").click()

    def enter_info(self, first_name: str, last_name: str, zip_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.zip_input.fill(zip_code)
        self.continue_button.click()

    def finish(self):
        self.finish_button.click()
