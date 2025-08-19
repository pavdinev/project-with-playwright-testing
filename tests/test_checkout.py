from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage


def test_checkout_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)  # headless=True if you want invisible run
        page = browser.new_page()

        # --- Step 1: Login ---
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")

        # --- Step 2: Inventory ---
        inventory_page = InventoryPage(page)
        inventory_page.set_sort("az")  # sort A-Z
        inventory_page.add_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.open_cart()

        # --- Step 3: Checkout ---
        checkout_page = CheckoutPage(page)
        checkout_page.start_checkout()
        checkout_page.enter_info("John", "Doe", "12345")
        checkout_page.finish()

        # --- Step 4: Verify success ---
        assert page.locator("h2.complete-header").inner_text() == "THANK YOU FOR YOUR ORDER"

        browser.close()
