# pages/cart_page.py
from playwright.sync_api import Page
from utils.smart_scroll import smart_scroll
from typing import List, Dict
import time


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.item_descriptions = page.locator('[data-test="inventory-item-desc"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.continue_shopping_btn = page.locator("[data-test='continue-shopping']")
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.cart_quantity_label = page.locator('[data-test="cart-quantity-label"]')
        self.cart_desc_label = page.locator('[data-test="cart-desc-label"]')
        self.removed_items = page.locator('.removed_cart_item')
        self.shopping_cart_link = page.locator('[data-test="shopping-cart-link"]')


    # --- Getters ---
    def get_item_names(self) -> List[str]:
        try:
            return self.item_names.all_inner_texts()
        except Exception:
            return []

    def get_item_descriptions(self) -> List[str]:
        try:
            return self.item_descriptions.all_inner_texts()
        except Exception:
            return []

    def get_item_prices(self) -> List[str]:
        try:
            return self.item_prices.all_inner_texts()
        except Exception:
            return []

    def get_cart_quantity_label(self) -> str:
        try:
            return self.cart_quantity_label.inner_text()
        except Exception:
            return ""

    def get_cart_desc_label(self) -> str:
        try:
            return self.cart_desc_label.inner_text()
        except Exception:
            return ""

    def get_removed_items_count(self) -> int:
        try:
            return self.removed_items.count()
        except Exception:
            return 0

    # --- Actions ---
    def continue_shopping(self) -> bool:
        try:
            self.continue_shopping_btn.click()
            return True
        except Exception:
            return False

    def click_checkout(self) -> bool:
        try:
            self.checkout_button.click()
            return True
        except Exception:
            return False

    def scroll_all(self) -> bool:
        return smart_scroll(self.page)

    # --- Navigation ---
    def go_to_checkout(self):
        self.checkout_container = '[data-test="checkout-info-container"]'  # or '#checkout_info_container'
        if self.click_checkout():
            # wait until cart items are hidden or checkout page loads
            self.page.wait_for_selector(self.checkout_container, timeout=3000)
            return True
        return False

    # --- Page structure for caching ---
    def extract_cart_page_structure(self) -> Dict:
        return {
            "items_count": self.cart_items.count(),
            "item_names": self.get_item_names(),
            "item_descriptions": self.get_item_descriptions(),
            "item_prices": self.get_item_prices(),
            "cart_quantity_label": self.get_cart_quantity_label(),
            "cart_desc_label": self.get_cart_desc_label(),
            "removed_items_count": self.get_removed_items_count(),
            "buttons": [
                {"name": "continue_shopping", "locator": "[data-test='continue-shopping']"},
                {"name": "checkout", "locator": "[data-test='checkout']"}
            ],
            "shopping_cart_link_present": self.shopping_cart_link.count() > 0
        }
