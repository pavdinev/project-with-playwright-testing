class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.inventory_container = page.locator("[data-test='inventory-container']")
        self.sort_dropdown = page.locator("select[data-test='product_sort_container']")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.item_name_locators = page.locator(".inventory_item_name")

    def is_loaded(self):
        return self.inventory_container.is_visible()

    def set_sort(self, option_value: str):
        """Wait for dropdown to be visible, then select option"""
        self.sort_dropdown.wait_for(state="visible", timeout=10000)  # 10s
        self.sort_dropdown.select_option(option_value)

    def add_first_item_to_cart(self):
        self.page.locator("button:has-text('Add to cart')").first.click()

    def open_cart(self):
        self.cart_icon.click()

    def item_names(self):
        return [el.inner_text() for el in self.item_name_locators.all()]
