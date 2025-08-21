# pages/inventory_page.py
from playwright.sync_api import Page

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.sort_dropdown = page.locator("select[data-test='product_sort_container']")
        self.inventory_container = page.locator('[data-test="inventory-container"]')
        self.inventory_items = page.locator(".inventory_item")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def is_loaded(self) -> bool:
        """Check if the inventory page is loaded by waiting for inventory container."""
        try:
            self.inventory_container.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def item_names(self):
        """Return a list of all item names in inventory."""
        self.inventory_items.first.wait_for(state="visible", timeout=10000)
        return [el.inner_text() for el in self.page.locator(".inventory_item_name").all()]

    def set_sort(self, sort_value: str):
        """Change the sorting dropdown (values: 'az', 'za', 'lohi', 'hilo')."""
        self.sort_dropdown.wait_for(state="visible", timeout=10000)
        self.sort_dropdown.select_option(sort_value)

    def add_first_item_to_cart(self):
        """Click 'Add to cart' on the first item in inventory."""
        first_button = self.page.locator(".inventory_item button").first
        first_button.click()

    def cart_count(self) -> int:
        """Return number of items in the cart."""
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())
