from playwright.sync_api import Page
from utils.smart_scroll import smart_scroll

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.inventory_container = page.locator('[data-test="inventory-container"]')
        self.inventory_items = page.locator('[data-test="inventory-item-name"]')
        self.inventory_desc = page.locator('[data-test="inventory-item-desc"]')
        self.get_open_cart = page.locator("[data-test='shopping-cart-link']")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')

    def scroll_inventory(self) -> bool:
        try:
            smart_scroll(self.page, pause=0.2, back_to_top=False, container_selector='[data-test="inventory-container"]')
            smart_scroll(self.page, pause=0.2, back_to_top=True, container_selector='[data-test="inventory-container"]')
            return True
        except:
            return False

    def is_sort_dropdown_visible(self) -> bool:
        return self.sort_dropdown.is_visible()

    def is_inventory_container_visible(self) -> bool:
        return self.inventory_container.is_visible()

    def list_inventory_items(self) -> list:
        try:
            return [i.inner_text() for i in self.inventory_items.all()]
        except:
            return []

    def list_inventory_descriptions(self) -> list:
        try:
            return [d.inner_text() for d in self.inventory_desc.all()]
        except:
            return []

    def open_cart(self) -> bool:
        try:
            self.get_open_cart.click()
            return True
        except:
            return False

    def click_menu(self) -> bool:
        try:
            self.menu_button.click()
            return True
        except:
            return False

    def click_logout(self) -> bool:
        try:
            self.logout_link.click()
            return True
        except:
            return False
