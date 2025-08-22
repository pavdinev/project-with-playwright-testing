# pages/inventory_page.py
from playwright.sync_api import Page

class InventoryPage:
    """Page object for the inventory page."""
    default_timeout = 1000  # default timeout for waits
    def __init__(self, page: Page):
        self.page = page
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.inventory_container = page.locator('[data-test="inventory-container"]')
        self.inventory_items = page.locator(".inventory_item")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.get_open_cart = page.locator("[data-test='shopping-cart-link']")

    def is_loaded(self) -> bool:
        """Check if the inventory page is loaded by waiting for inventory container."""
        try:
            self.page.locator(".inventory_item").first.wait_for(state="visible")
            return True
        except Exception:
            return False

    def item_names(self):
        """Return a list of all item names in inventory."""
        self.inventory_items.first.wait_for(state="visible", timeout=self.default_timeout)
        return [el.inner_text() for el in self.page.locator(".inventory_item_name").all()]

    def set_sort(self, sort_value: str):
        """Change the sorting dropdown (values: 'az', 'za', 'lohi', 'hilo')."""
        self.sort_dropdown.wait_for(state="visible", timeout=self.default_timeout)
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
    
    def item_prices(self):
        """Return a list of all item prices in inventory."""
        self.inventory_items.first.wait_for(state="visible", timeout=self.default_timeout)
        return [el.inner_text() for el in self.page.locator(".inventory_item_price").all()]

    def add_to_cart_by_name(self, item_name: str):
        """Add an item to the cart by its name."""
        item = self.page.locator(f".inventory_item:has(.inventory_item_name:has-text('{item_name}'))")
        add_button = item.locator("button")
        add_button.click()
        
    def open_cart(self):
        """Click the cart icon to go to the cart page."""
        try:
            self.get_open_cart.wait_for(state="visible", timeout=self.default_timeout)
        except Exception as e:
            print(f"Cart icon not visible: {e}")
            raise
        self.get_open_cart.click()