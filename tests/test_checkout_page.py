# tests/test_checkout_page.py
from tests.base_test import BaseTest
from pages.checkout_page import CheckoutPage

SPECIALS = ["!", "@", "/", "*", "\\", '"']

class CheckoutPageTests(BaseTest):

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

        # Fill valid data using the test's variables
        filled = checkout.enter_info(first_name, last_name, postal_code)
        assert filled is True

    def test_checkout_continue_and_cancel(self,
            first_name: str = first_name,
            last_name: str = last_name,
            postal_code: str = postal_code):
        """Test continue to overview and cancel/back to shopping"""
        checkout = CheckoutPage(self.page)
        checkout.enter_info(first_name, last_name, postal_code)
        assert checkout.click_continue() is True
        assert checkout.at_overview() is True

        # Cancel and ensure still on step one
        assert checkout.click_cancel() is True
        assert checkout.at_step_one() is True

    def test_checkout_finish_order(self,
            first_name: str = first_name,
            last_name: str = last_name,
            postal_code: str = postal_code):
        """Test completing the checkout process"""
        checkout = CheckoutPage(self.page)
        checkout.enter_info(first_name, last_name, postal_code)
        checkout.click_continue()
        assert checkout.at_overview() is True
        assert checkout.click_finish() is True
        # Optionally, check for confirmation message
        confirmation = self.page.locator('.complete-header')
        assert confirmation.is_visible() is True

    def test_checkout_fields_special_characters(self):
        """Test that fields handle special characters and produce error if invalid"""
        checkout = CheckoutPage(self.page)
        for s in SPECIALS:
            checkout.enter_info(s, s, s)
            checkout.click_continue()
            # Error should be visible if invalid
            assert checkout.error_visible() is True
            assert len(checkout.error_text()) > 0
