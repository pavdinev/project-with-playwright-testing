from playwright.sync_api import Page

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")

    def start_checkout(self):
        checkout_btn = self.page.locator("[data-test='checkout']")
        checkout_btn.scroll_into_view_if_needed(timeout=2000)
        checkout_btn.wait_for(state="visible", timeout=10000)
        checkout_btn.click()

    def enter_info(self, first_name, last_name, postal_code):
        # Wait for inputs to appear
        self.page.wait_for_selector("[data-test='firstName']", state="visible", timeout=10000)
        self.page.wait_for_selector("[data-test='lastName']", state="visible", timeout=10000)
        self.page.wait_for_selector("[data-test='postalCode']", state="visible", timeout=10000)

        # Scroll + fill
        self.first_name_input.scroll_into_view_if_needed(timeout=2000)
        self.first_name_input.fill(first_name)

        self.last_name_input.scroll_into_view_if_needed(timeout=2000)
        self.last_name_input.fill(last_name)

        self.postal_code_input.scroll_into_view_if_needed(timeout=2000)
        self.postal_code_input.fill(postal_code)

        # Scroll + click continue
        self.continue_button.scroll_into_view_if_needed(timeout=2000)
        self.continue_button.wait_for(state="visible", timeout=10000)
        self.continue_button.click()

    def finish(self):
        self.finish_button.scroll_into_view_if_needed(timeout=2000)
        self.finish_button.wait_for(state="visible", timeout=10000)
        self.finish_button.click()

    def checkout_btn(self):
        return self.page.locator("button[data-test='checkout']")

    def continue_shopping_btn(self):
        return self.page.locator("button[data-test='continue-shopping']")
