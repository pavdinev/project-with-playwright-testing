from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.locator('.cart_item')
        self.checkout_btn = page.locator('[data-test="checkout"]')

    def get_item_names(self):
        return [el.inner_text() for el in self.page.locator('.inventory_item_name').all()]

    def remove_by_name(self, name: str):
        self.page.locator('.cart_item', has_text=name).locator('button:has-text("Remove")').click()

    def checkout(self):
        # Scroll button into view before clicking
        self.checkout_btn.scroll_into_view_if_needed(timeout=3000)
        self.checkout_btn.click(timeout=5000)
