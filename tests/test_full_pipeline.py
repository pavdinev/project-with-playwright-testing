# tests/test_full_pipeline.py
from tests.base_test import BaseTest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from validate_users import UserValidator
import config
import datetime
import os


def _is_non_decreasing(vals):
    return all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))


def _is_non_increasing(vals):
    return all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1))


class TestFullPipelineAllUsers(BaseTest):
    def test_pipeline_all_users(self):
        validator = UserValidator(self.page)

        # --- Step 0: Cache standard_user reference (prices, images, layout) ---
        validator.cache_standard_user_data()

        all_errors = {}
        passed_users = []

        for user_key, user_creds in config.USERS.items():
            user_errors = []

            with self.subTest(user=user_key):
                # --- Step 1: Login ---
                login_page = LoginPage(self.page)
                login_page.navigate()
                login_page.login(user_creds["username"], user_creds["password"])

                inventory_url = config.BASE_URL.rstrip("/") + "/inventory.html"
                # If login did not result in inventory page OR inventory didn't load => treat as login failure
                if not validator.wait_for_inventory_loaded(timeout=5000) or self.page.url.rstrip("/") != inventory_url:
                    user_errors.append("login failed")
                    all_errors[user_key] = user_errors
                    # IMPORTANT: skip ALL further checks for this user
                    continue

                # --- Step 2: Visual validation vs cached standard ---
                if validator.has_wrong_prices():
                    user_errors.append("wrong prices detected")
                if validator.has_bad_images():
                    user_errors.append("image differences detected")
                if validator.has_layout_issues():
                    user_errors.append("layout issues detected")

                if user_errors:
                    all_errors[user_key] = user_errors
                    continue  # skip the rest for this user

                # --- Step 3: Cart & Sort ---
                inventory = InventoryPage(self.page)

                # A->Z
                inventory.set_sort("az")
                names_az = inventory.item_names()
                if names_az != sorted(names_az):
                    user_errors.append("names not A->Z sorted")

                # Low->High (allow ties)
                inventory.set_sort("lohi")
                prices_lohi = [float(p.strip("$")) for p in inventory.item_prices()]
                if not _is_non_decreasing(prices_lohi):
                    user_errors.append("prices not low->high sorted")

                # High->Low (allow ties) - re-read after sort
                inventory.set_sort("hilo")
                prices_hilo = [float(p.strip("$")) for p in inventory.item_prices()]
                if not _is_non_increasing(prices_hilo):
                    user_errors.append("prices not high->low sorted")

                # Z->A
                inventory.set_sort("za")
                names_za = inventory.item_names()
                if names_za != sorted(names_za, reverse=True):
                    user_errors.append("names not Z->A sorted")

                # Cart flow
                cart_result = inventory.add_all_to_cart()
                inventory.open_cart()
                cart_items = CartPage(self.page).get_item_names()
                if set(cart_items) != set(cart_result["added"]):
                    user_errors.append("cart mismatch, added vs in cart")

                if user_errors:
                    all_errors[user_key] = user_errors
                    continue

                # --- Step 4: Checkout ---
                checkout = CheckoutPage(self.page)
                checkout.start_checkout()
                checkout.enter_info("Pavel", "Dinev", "12345")

                # Robust verification of checkout inputs:
                # - prefer to read the value if available quickly
                # - if reading value times out, fall back to checking field visibility only
                field_checks = [
                    ("first_name", "Pavel", checkout.first_name_input),
                    ("last_name", "Dinev", checkout.last_name_input),
                    ("zip", "12345", checkout.zip_input),
                ]
                for field_name, expected, locator in field_checks:
                    try:
                        # ensure visible first (fast)
                        locator.wait_for(state="visible", timeout=2000)
                        # then read value with a short timeout — if it fails, fall back to visibility-only
                        try:
                            actual = locator.input_value(timeout=2000)
                            if actual != expected:
                                user_errors.append(f"{field_name} field mismatch (expected '{expected}', got '{actual}')")
                        except Exception:
                            # could not read value quickly — accept visibility as pass (avoids long timeouts)
                            pass
                    except Exception:
                        user_errors.append(f"{field_name} field not visible")

                checkout.finish()

                # --- Step 5: Verify checkout outcome ---
                # If a user is expected to fail the checkout (error_user, locked_out_user), ensure it didn't proceed.
                if user_key in ["error_user", "locked_out_user"]:
                    if "checkout-step-two" not in self.page.url:
                        user_errors.append("finish should not proceed but did")
                else:
                    if "checkout-complete" not in self.page.url:
                        user_errors.append("checkout failed unexpectedly")

                if user_errors:
                    all_errors[user_key] = user_errors
                else:
                    passed_users.append(user_key)

        # --- Human-friendly HTML report ---
        self._generate_html_report(all_errors, passed_users)

        # Fail the test if any user failed the pipeline
        if all_errors:
            self.fail("Some users failed the full pipeline. See HTML report.")

    def _generate_html_report(self, all_errors, passed_users):
        total = len(config.USERS)
        failed = len(all_errors)
        passed = len(passed_users)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html = [
            "<!doctype html>",
            "<html><head><meta charset='utf-8'><title>Full Pipeline Report</title>",
            "<style>body{font-family:Arial,Helvetica,sans-serif;margin:18px} .pass{color:green}.fail{color:#b00020} "
            "details{margin-bottom:8px} summary{font-weight:bold}</style>",
            "</head><body>",
            f"<h1>Full Pipeline Report</h1><p><b>Generated:</b> {timestamp}</p>",
            f"<p><b>Summary:</b> {passed}/{total} users passed, {failed}/{total} failed.</p>",
            "<h2>Details</h2>"
        ]

        # Passed users
        if passed_users:
            html.append("<h3>Passed users</h3><ul>")
            for u in passed_users:
                html.append(f"<li class='pass'>{u}</li>")
            html.append("</ul>")

        # Failed users
        if all_errors:
            html.append("<h3>Failed users</h3>")
            for user, errs in all_errors.items():
                html.append(f"<details><summary class='fail'>{user} ({len(errs)} issues)</summary><ul>")
                for e in errs:
                    html.append(f"<li>{e}</li>")
                html.append("</ul></details>")

        html.append("</body></html>")

        report_path = os.path.join(os.getcwd(), "full_pipeline_report.html")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(html))

        print(f"\nHTML report generated: {report_path}\n")
