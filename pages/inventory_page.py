# pages/inventory_page.py
from playwright.sync_api import Page
import config
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
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")


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

    def add_to_cart_by_name(self, item_name: str) -> bool:
        """Add an item to the cart by its name. Returns True if added, False if button was missing or already added."""
        item = self.page.locator(f".inventory_item:has(.inventory_item_name:has-text('{item_name}'))")
        add_button = item.locator("button")
    
        if add_button.count() == 0:
            return False  # button not found
    
        text = add_button.inner_text()
        if text.lower() == "add to cart":
            add_button.click()
            return True
        else:
            return False  # already in cart or button not clickable

        
    def open_cart(self):
        self.get_open_cart.scroll_into_view_if_needed(timeout=2000)
        self.get_open_cart.click(timeout=5000)


    def logout(self):
        """Log out and return to the login page"""
        self.menu_button.click()
        self.logout_link.click()
        self.page.wait_for_url(config.BASE_URL)  # verify we’re back at login
    
    def logout(self):
        self.menu_button.click()
        self.logout_link.click()

    def add_all_to_cart(self):
        """Attempt to add all inventory items to the cart. Returns dict of success/fail per item."""
        all_items = self.item_names()
        added_items = []
        failed_items = []

        for item in all_items:
            success = self.add_to_cart_by_name(item)
            if success:
                added_items.append(item)
            else:
                failed_items.append(item)

        return {"added": added_items, "failed": failed_items}