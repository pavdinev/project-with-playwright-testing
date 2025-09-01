# tests/test_full_pipeline.py
import unittest
from tests.base_test import BaseTest
from tests.test_login_page import LoginPageTests
from tests.test_inventory_page import InventoryPage
from tests.test_checkout_page import CheckoutPageTests
from utils.results_collector import UserResult
from utils.report_generator import generate_full_pipeline_report
import config

class FullPipelineTest(BaseTest):

    def test_full_pipeline_all_users(self):
        """
        Runs the full pipeline for all users defined in config.USERS.
        Captures steps, pass/fail, and timings in UserResult for reporting.
        """
        all_results = {}

        for user_key, user_data in config.USERS.items():
            user_result = UserResult(username=user_key)
            self.page.goto(config.BASE_URL)  # start fresh per user

            # --- Login ---
            login_tests = LoginPageTests()
            login_tests.page = self.page  # inject current page
            try:
                user_result.log("login_fields_visible", login_tests.test_fields_visible_and_scroll())
                user_result.log("login_wrong_credentials", login_tests.test_wrong_credentials_show_error())
                user_result.log("login_special_chars", login_tests.test_special_characters_in_fields())
            except Exception as e:
                user_result.log("login_exception", False, error=str(e))

            # --- Inventory ---
            inventory_tests = InventoryPage(self.page)
            inventory_tests.page = self.page
            try:
                user_result.log("inventory_scroll", inventory_tests.test_inventory_scroll())
                user_result.log("inventory_item_list", inventory_tests.test_inventory_list_items())
                user_result.log("inventory_item_desc_list", inventory_tests.test_inventory_list_descriptions())
                user_result.log("cart_behavior", inventory_tests.test_cart_functionality())
            except Exception as e:
                user_result.log("inventory_exception", False, error=str(e))

            # --- Checkout ---
            checkout_tests = CheckoutPageTests()
            checkout_tests.page = self.page
            try:
                user_result.log("checkout_fields", checkout_tests.test_checkout_fields_visible_and_fill())
                user_result.log("checkout_continue_cancel", checkout_tests.test_checkout_continue_and_cancel())
                user_result.log("checkout_finish_order", checkout_tests.test_checkout_finish_order())
                user_result.log("checkout_special_chars", checkout_tests.test_checkout_fields_special_characters())
            except Exception as e:
                user_result.log("checkout_exception", False, error=str(e))

            all_results[user_key] = user_result.to_dict()

        # --- Generate Report ---
        generate_full_pipeline_report(all_results)

if __name__ == "__main__":
    unittest.main()
