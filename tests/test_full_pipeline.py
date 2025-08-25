# tests/test_full_pipeline.py
from tests.base_test import BaseTest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from validate_users import UserValidator
import config
import os
import time
import datetime


class TestFullPipelineAllUsers(BaseTest):

    def test_pipeline_all_users(self):
        validator = UserValidator(self.page)
        validator.cache_standard_user_data()  # baseline

        # Prepare report folder
        report_root = os.path.join(os.getcwd(), "reports")
        timestamp_dir = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_dir = os.path.join(report_root, timestamp_dir)
        os.makedirs(report_dir, exist_ok=True)

        all_errors = {}
        passed_users = []

        for user_key, user_creds in config.USERS.items():
            user_entry = {
                "errors": [],
                "wrong_prices": [],
                "image_diffs": [],
                "description_diffs": [],
                "position_diffs": [],
                "timings": {},
                "login_time": None,
                "screenshot": None
            }

            with self.subTest(user=user_key):
                login_page = LoginPage(self.page)
                login_page.navigate()

                # Login timing
                t0 = time.perf_counter()
                login_page.login(user_creds["username"], user_creds["password"])
                t1 = time.perf_counter()
                user_entry["login_time"] = round(t1 - t0, 3)

                # Stop immediately if login fails
                if not validator.wait_for_inventory_loaded(timeout=5000):
                    user_entry["errors"].append("login failed")
                    shot = os.path.join(report_dir, f"{user_key}_login_fail.png")
                    try:
                        self.page.screenshot(path=shot)
                        user_entry["screenshot"] = shot
                    except Exception:
                        pass
                    all_errors[user_key] = user_entry
                    continue

                # Visual / inventory checks
                user_entry["wrong_prices"] = validator.list_wrong_prices()
                user_entry["image_diffs"] = validator.list_bad_images()
                user_entry["description_diffs"] = validator.list_description_mismatches()
                user_entry["position_diffs"] = validator.list_position_mismatches()
                user_entry["timings"] = validator._standard_cache.get("timings", {})

                if any(user_entry[k] for k in ["wrong_prices", "image_diffs", "description_diffs", "position_diffs"]):
                    user_entry["errors"].append("visual differences detected")
                    shot = os.path.join(report_dir, f"{user_key}_visual_fail.png")
                    try:
                        self.page.screenshot(path=shot)
                        user_entry["screenshot"] = shot
                    except Exception:
                        pass
                    all_errors[user_key] = user_entry
                    continue

                # Cart & sort checks
                inventory = InventoryPage(self.page)
                for sort_key, check in [("az", sorted), ("za", lambda x: sorted(x, reverse=True))]:
                    inventory.set_sort(sort_key)
                    items = inventory.item_names() if sort_key in ["az", "za"] else inventory.item_prices()
                    if items != check(items):
                        user_entry["errors"].append(f"sort {sort_key} not correct")

                cart_added = inventory.add_all_to_cart()
                inventory.open_cart()
                cart_items = CartPage(self.page).get_item_names()
                if set(cart_items) != set(cart_added["added"]):
                    user_entry["errors"].append("cart mismatch: added vs in cart")

                # Checkout
                errors, checkout_screenshot = validator.check_checkout_field_errors(report_dir=report_dir)
                user_entry["errors"].extend(errors)
                if checkout_screenshot:
                    user_entry["screenshot"] = checkout_screenshot

                checkout = CheckoutPage(self.page)
                if not user_entry["errors"]:
                    checkout.enter_info("Pavel", "Dinev", "12345")
                    checkout.finish()

                if user_entry["errors"]:
                    all_errors[user_key] = user_entry
                else:
                    passed_users.append(user_key)

        # Generate HTML report
        validator.generate_full_pipeline_report(
            all_errors, passed_users, report_root=report_root, timestamp_dir=timestamp_dir
        )

        if all_errors:
            self.fail("Some users failed the full pipeline. See HTML report.")
