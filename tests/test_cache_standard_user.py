# tests/test_cache_standard_user.py
import os
import json
import config
from tests.base_test import BaseTest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

CACHE_FILE = "cache/standard_user.json"

class CacheStandardUserTests(BaseTest):

    def setUp(self):
        super().setUp()
        self.page.goto(config.BASE_URL)

    def test_cache_standard_user_state(self):
        # Skip caching if file already exists and is not empty
        if os.path.exists(CACHE_FILE) and os.path.getsize(CACHE_FILE) > 0:
            print("Standard user cache already exists. Skipping...")
            return
        #Initialize login page object
        login = LoginPage(self.page)
        
        # Initialize cache structure
        cache_data = {}

        # --- Login page ---
        cache_data["login"] = login.extract_login_page_structure()

        # --- Login as standard user ---
        login.fill_username(config.USERS["standard_user"]["username"])
        #login.username_input.fill(config.USERS["standard_user"]["username"])
        login.fill_password(config.USERS["standard_user"]["password"])
        login.click_login()
        self.assertTrue(self.page.url.endswith("inventory.html"),
                        "Standard user should reach inventory page")

        # --- Inventory page ---
        inventory = InventoryPage(self.page)
        cache_data["inventory"] = inventory.extract_inventory_page_structure()
        inventory.add_all_items()

        # --- Cart page ---
        inventory.go_to_cart()
        cart = CartPage(self.page)
        cache_data["cart"] = cart.extract_cart_page_structure()

        # --- Checkout step one ---
        cart.go_to_checkout()
        checkout = CheckoutPage(self.page)
        cache_data["checkout_step_one"] = checkout.extract_step_one_structure()
        checkout.test_checkout_fields_visible_and_fill()
        checkout.click_continue()
        
        # --- Checkout step two ---
        cache_data["checkout_step_two"] = checkout.extract_step_two_structure()
        checkout.finish_checkout()
        # --- Checkout step three ---
        cache_data["checkout_complete"] = checkout.extract_complete_structure()
        checkout.back_to_home()

        # --- Save cache ---
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2)

        print(f"Standard user cache (step one) created at {CACHE_FILE}")
