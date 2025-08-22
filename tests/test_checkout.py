# tests/test_checkout.py
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage
from tests.base_test import BaseTest
from config import DEFAULT_USER

class TestCheckoutFlow(BaseTest):
    
    def test_checkout_flow(self):
        # --- Step 1: Login ---
        login_page = LoginPage(self.page)
        login_page.navigate()  
        login_page.login(DEFAULT_USER["username"], DEFAULT_USER["password"])

        # --- Step 2: Inventory ---
        inventory_page = InventoryPage(self.page)
        inventory_page.set_sort("az")  # sort A-Z
        inventory_page.add_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.open_cart()

        # --- Step 3: Checkout ---
        checkout_page = CheckoutPage(self.page)
        checkout_page.start_checkout()
        checkout_page.enter_info("John", "Doe", "12345")
        checkout_page.finish()

        # --- Step 4: Verify success ---
        thank_you = self.page.locator("h2.complete-header").inner_text()
        self.assertEqual(thank_you, "Thank you for your order!", "Order completion message should match")
