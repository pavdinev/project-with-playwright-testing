# pages/checkout_page.py
from playwright.sync_api import Page

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        # --- Step One Locators ---
        self.sel_first = "[data-test='firstName']"
        self.sel_last = "[data-test='lastName']"
        self.sel_zip = "[data-test='postalCode']"
        self.sel_continue = "[data-test='continue']"
        self.sel_cancel = "[data-test='cancel']"

        # --- Other locators (unchanged) ---
        self.sel_finish = "[data-test='finish']"
        self.sel_error = "[data-test='error']"
        self.sel_overview_item = ".cart_item"
        self.sel_item_total = ".summary_subtotal_label"

    # --- Step One ---
    def at_step_one(self) -> bool:
        return self.page.locator(self.sel_first).is_visible()

    def enter_info(self, first: str, last: str, zipc: str) -> bool:
        self.page.wait_for_selector(self.sel_first, timeout=5000)
        self.page.fill(self.sel_first, first)
        self.page.fill(self.sel_last, last)
        self.page.fill(self.sel_zip, zipc)
        ok = (
            self.page.input_value(self.sel_first) == first and
            self.page.input_value(self.sel_last) == last and
            self.page.input_value(self.sel_zip) == zipc
        )
        return ok

    def click_continue(self) -> bool:
        self.page.locator(self.sel_continue).click()
        return True

    def click_cancel(self) -> bool:
        self.page.locator(self.sel_cancel).click()
        return True

    # --- Step Two ---
    def at_overview(self) -> bool:
        return self.page.locator(self.sel_overview_item).count() > 0

    def click_finish(self) -> bool:
        self.page.locator(self.sel_finish).click()
        return True

    # --- Errors ---
    def error_visible(self) -> bool:
        return self.page.locator(self.sel_error).is_visible()

    def error_text(self) -> str:
        loc = self.page.locator(self.sel_error)
        return loc.inner_text() if loc.is_visible() else ""

    # --- Overview ---
    def overview_item_total(self) -> float:
        text = self.page.locator(self.sel_item_total).inner_text()
        if "$" in text:
            val = text.split("$")[-1]
            return float(val.strip())
        digits = "".join(c for c in text if c.isdigit() or c == '.')
        return float(digits) if digits else 0.0

    # --- Extraction for caching ---
    def extract_step_one_structure(self):
        return {
            "fields": [
                {"name": "firstName", "locator": "#first-name"},
                {"name": "lastName", "locator": "#last-name"},
                {"name": "postalCode", "locator": "#postal-code"},
            ],
            "buttons": [
                {"name": "continue", "locator": "#continue"},
                {"name": "cancel", "locator": "#cancel"}
            ]
        }

    def extract_step_two_structure(self):
        return {
            "items_count": self.page.locator(".cart_item").count(),
            "buttons": [
                {"name": "finish", "locator": "#finish"}
            ]
        }

    def extract_complete_structure(self):
        return {
            "header": self.page.locator(".complete-header").inner_text(),
            "buttons": [
                {"name": "back_home", "locator": "#back-to-products"}
            ]
        }
       # ---------- Checkout Step Two ----------
    def extract_step_two_structure(self):
        """Extract all visible elements on Checkout Step Two page."""
        elements = self.page.locator("body *:visible").all()
        structure = []
        for el in elements:
            try:
                structure.append({
                    "tag": el.evaluate("el => el.tagName"),
                    "text": el.inner_text().strip(),
                    "x": el.bounding_box()["x"] if el.bounding_box() else None,
                    "y": el.bounding_box()["y"] if el.bounding_box() else None,
                })
            except Exception:
                continue
        return structure

    def finish_checkout(self):
        """Click the finish button to complete checkout."""
        self.page.click("data-test=finish")
        
        # ---------- Checkout Complete ----------
    def extract_complete_structure(self):
        """Extract all visible elements on Checkout Complete page."""
        elements = self.page.locator("body *:visible").all()
        structure = []
        for el in elements:
            try:
                structure.append({
                    "tag": el.evaluate("el => el.tagName"),
                    "text": el.inner_text().strip(),
                    "x": el.bounding_box()["x"] if el.bounding_box() else None,
                    "y": el.bounding_box()["y"] if el.bounding_box() else None,
                })
            except Exception:
                continue
        return structure

    def back_to_home(self):
        """Click the Back Home button after checkout complete."""
        self.page.click("data-test=back-to-products")
        
    # ---------- Fill checkout info for tests only because it cannot be inherited correctly from the test
    # class ----------
    first_name = "John"
    last_name = "Doe" 
    postal_code = "12345"    
    def test_checkout_fields_visible_and_fill(self,
            first_name: str = first_name,
            last_name: str = last_name,
            postal_code: str = postal_code):
        """Check that first, last, postal code fields are visible and can be filled"""
        checkout = CheckoutPage(self.page)
        self.page.wait_for_url("**/checkout-step-one.html") 
        assert checkout.at_step_one() is True
        # Fill valid data using the test's va   riables
        filled = checkout.enter_info(first_name, last_name, postal_code)
        assert filled is True