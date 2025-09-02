# pages/inventory_page.py
from playwright.sync_api import Page
from utils.smart_scroll import smart_scroll
from pages.cart_page import CartPage
import time

class ProductItem:
    def __init__(self, name_locator, desc_locator, price_locator=None, add_to_cart_locator=None):
        self.name_locator = name_locator
        self.desc_locator = desc_locator
        self.price_locator = price_locator
        self.add_to_cart_locator = add_to_cart_locator

    def get_name(self) -> str:
        return self.name_locator.inner_text().strip()

    def get_description(self) -> str:
        return self.desc_locator.inner_text().strip() if self.desc_locator else ""

    def get_price(self) -> str:
        return self.price_locator.inner_text().strip() if self.price_locator else ""

    def is_available(self) -> bool:
        return self.add_to_cart_locator.is_visible() if self.add_to_cart_locator else True

    def get_positions(self) -> dict:
        positions = {}
        for key, locator in (("name", self.name_locator),
                             ("description", self.desc_locator),
                             ("price", self.price_locator)):
            if locator:
                box = locator.bounding_box()
                positions[key] = {"x": box["x"], "y": box["y"]} if box else None
            else:
                positions[key] = None
        return positions

    def is_add_to_cart(self) -> bool:
        """
        Check if the current button is still 'Add to cart'.
        Uses the add_to_cart_locator directly — no root locator needed.
        """
        if not self.add_to_cart_locator:
            return False
        data_test = self.add_to_cart_locator.get_attribute("data-test")
        return bool(data_test and data_test.startswith("add-to-cart"))

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.inventory_container = page.locator('[data-test="inventory-container"]')
        self.inventory_items = page.locator('[data-test="inventory-item-name"]')
        self.inventory_desc = page.locator('[data-test="inventory-item-desc"]')
        self.inventory_prices = page.locator('[data-test="inventory-item-price"]')  # Optional
        self.add_to_cart_buttons = page.locator('[data-test^="add-to-cart"]')       # Optional
        self.get_open_cart = page.locator("[data-test='shopping-cart-link']")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')

    # --- Scrolling ---
    def scroll_inventory(self, pause: float = 0.2) -> bool:
        try:
            smart_scroll(self.page, pause=pause, back_to_top=False, container_selector='[data-test="inventory-container"]')
            smart_scroll(self.page, pause=pause, back_to_top=True, container_selector='[data-test="inventory-container"]')
            return True
        except:
            return False

    # --- Visibility ---
    def is_sort_dropdown_visible(self) -> bool:
        return self.sort_dropdown.is_visible()

    def is_inventory_container_visible(self) -> bool:
        return self.inventory_container.is_visible()

    # --- Products ---
    def get_all_products(self) -> list:
        products = []
        names = self.inventory_items.all()
        descs = self.inventory_desc.all()
        prices = self.inventory_prices.all() if self.inventory_prices.count() > 0 else [None]*len(names)
        add_buttons = self.add_to_cart_buttons.all() if self.add_to_cart_buttons.count() > 0 else [None]*len(names)

        for i, name_el in enumerate(names):
            desc_el = descs[i] if i < len(descs) else None
            #print(desc_el.inner_text())
            price_el = prices[i] if i < len(prices) else None
            #print(price_el.inner_text())
            add_btn_el = add_buttons[i] if i < len(add_buttons) else None
            #print(add_btn_el.inner_text())
            products.append(ProductItem(name_el, desc_el, price_el, add_btn_el))
        return products

    # --- Positions ---
    def get_item_positions(self) -> dict:
        positions = {}
        for product in self.get_all_products():
            positions[product.get_name()] = product.get_positions()
        return positions

    # --- Cart & menu ---
    def go_to_cart(self) -> CartPage:
        self.get_open_cart.click()
        # Wait until at least 1 cart item is visible
        self.page.wait_for_selector(".cart_item, .cart_list", timeout=3000)
        return CartPage(self.page)

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
        
        # --- Add to cart actions ---
    def add_item_by_name(self, product_name: str) -> bool:
        """Click 'Add to cart' for a product by name."""
        for product in self.get_all_products():
            if product.get_name() == product_name:
                if product.is_available():
                    product.add_to_cart_locator.click()
                    return True
        return False
    
    def add_all_items(self) -> int:
        """
        Collect all 'Add to cart' buttons from the inventory list,
        print their locators for debug, then click each visible button.
        """
    
        count = 0
    
        # Find the inventory list container
        inventory_list = self.page.locator('[data-test="inventory-list"]')
    
        # Find all items inside the inventory list
        items = inventory_list.locator('[data-test="inventory-item"]')
        total_items = items.count()
    
        for i in range(total_items):
            item = items.nth(i)
            # Find the 'Add to cart' button inside the item
            btn = item.locator('button[data-test^="add-to-cart"]')
    
            # If the button exists, print its locator and click
            if btn.count() == 0:
                print(f"Item {i} has no add-to-cart button, skipping.")
                continue
            
            data_test = btn.get_attribute("data-test")
            if data_test:
                print(f'{data_test}')
    
            try:
                if btn.is_visible(timeout=2000):
                    btn.scroll_into_view_if_needed(timeout=5000)
                    btn.click(timeout=5000)
                    count += 1
                else:
                    print(f"Skipping '{data_test}': button not visible")
            except Exception as e:
                print(f"Failed to click '{data_test}': {e}")
    
        return count



    # --- Full page structure for caching ---
    def extract_inventory_page_structure(self) -> dict:
        structure = {
            "sort_dropdown_visible": self.is_sort_dropdown_visible(),
            "inventory_container_visible": self.is_inventory_container_visible(),
            "products": []
        }
        for product in self.get_all_products():
            structure["products"].append({
                "name": product.get_name(),
                "description": product.get_description(),
                "price": product.get_price(),
                "available": product.is_available(),
                "positions": product.get_positions()
            })
        return structure
