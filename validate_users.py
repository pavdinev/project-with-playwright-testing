# validate_users.py
import config
import time
import os
import datetime
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import smart_scroll

class UserValidator:
    _standard_cache = None  # Cache for standard_user

    def __init__(self, page):
        self.page = page

    # ------------------- Page load helper -------------------
    def measure_page_load_time(self, url):
        t0 = time.perf_counter()
        self.page.goto(url, wait_until="networkidle")
        t1 = time.perf_counter()
        return round(t1 - t0, 3)

    def wait_for_inventory_loaded(self, timeout=8000) -> bool:
        try:
            self.page.locator(".inventory_item").first.wait_for(timeout=timeout)
            return True
        except Exception:
            return False

    # ------------------- Standard user caching -------------------
    def cache_standard_user_data(self):
        if self._standard_cache is not None:
            return

        login_page = LoginPage(self.page)
        login_page.navigate()
        login_page.login(
            config.USERS["standard_user"]["username"],
            config.USERS["standard_user"]["password"]
        )

        self._standard_cache = {}
        self._standard_cache["timings"] = {}

        # Inventory
        inventory_url = config.BASE_URL.rstrip("/") + "/inventory.html"
        self._standard_cache["timings"]["inventory"] = self.measure_page_load_time(inventory_url)
        if not self.wait_for_inventory_loaded(timeout=8000):
            raise RuntimeError("standard_user inventory did not load")

        self._standard_cache["inventory"] = self.collect_inventory_data()

        # Sorting references
        self._standard_cache["sorting"] = {}
        inventory = InventoryPage(self.page)
        for sort_key in ["az", "za", "lohi", "hilo"]:
            inventory.set_sort(sort_key)
            if sort_key in ["az", "za"]:
                self._standard_cache["sorting"][sort_key] = inventory.item_names()
            else:
                self._standard_cache["sorting"][sort_key] = inventory.item_prices()

        # Cart
        inventory.add_all_to_cart()
        self._standard_cache["cart_items"] = self.collect_cart_data()
        self._standard_cache["timings"]["cart"] = self.measure_page_load_time(config.BASE_URL.rstrip("/") + "/cart.html")

        # Checkout
        checkout = CheckoutPage(self.page)
        checkout.start_checkout()
        self._standard_cache["timings"]["checkout_step_one"] = self.measure_page_load_time(
            config.BASE_URL.rstrip("/") + "/checkout-step-one.html"
        )
        checkout.enter_info("Pavel", "Dinev", "12345")
        self._standard_cache["timings"]["checkout_step_two"] = self.measure_page_load_time(
            config.BASE_URL.rstrip("/") + "/checkout-step-two.html"
        )
        checkout.finish()
        self._standard_cache["timings"]["finish"] = self.measure_page_load_time(
            config.BASE_URL.rstrip("/") + "/checkout-complete.html"
        )

    # ------------------- Inventory helpers -------------------
    def _get_inventory_cards_data(self, inventory):
        # Scroll inventory page to ensure all items are loaded
        smart_scroll(self.page, container_selector="body")

        inventory.inventory_items.first.wait_for(state="visible", timeout=5000)
        cards = []

        for el in inventory.inventory_items.all():
            name = el.locator(".inventory_item_name").inner_text() if el.locator(".inventory_item_name") else None
            desc = el.locator(".inventory_item_desc").inner_text() if el.locator(".inventory_item_desc") else None
            price = el.locator(".inventory_item_price").inner_text() if el.locator(".inventory_item_price") else None
            img_src = el.locator(".inventory_item_img img").get_attribute("src") if el.locator(".inventory_item_img img") else None
            try:
                btn_box = el.locator("button").bounding_box()
                btn_pos = {"x": btn_box["x"], "y": btn_box["y"]} if btn_box else None
            except Exception:
                btn_pos = None

            cards.append({
                "name": name,
                "desc": desc,
                "price": price,
                "img_src": img_src,
                "button_pos": btn_pos
            })
        return cards

    def collect_inventory_data(self):
        inventory = InventoryPage(self.page)
        return self._get_inventory_cards_data(inventory)

    def collect_cart_data(self):
        InventoryPage(self.page).open_cart()
        smart_scroll(self.page)
        return CartPage(self.page).get_item_names()

    def collect_checkout_data(self):
        checkout = CheckoutPage(self.page)
        checkout.start_checkout()
        smart_scroll(self.page)
        return checkout

    # ------------------- Comparisons -------------------
    def list_wrong_prices(self):
        return self._compare_field("price")

    def list_description_mismatches(self):
        return self._compare_field("desc")

    def list_bad_images(self):
        return self._compare_field("img_src")

    def list_position_mismatches(self, threshold=5):
        deltas = []
        for std_card, cur_card in zip(self._standard_cache["inventory"], self.collect_inventory_data()):
            std_btn = std_card.get("button_pos")
            cur_btn = cur_card.get("button_pos")
            if std_btn and cur_btn:
                dx = abs(std_btn["x"] - cur_btn["x"])
                dy = abs(std_btn["y"] - cur_btn["y"])
                if dx > threshold or dy > threshold:
                    deltas.append({"name": cur_card.get("name"), "dx": dx, "dy": dy})
        return deltas

    def _compare_field(self, field_name):
        diffs = []
        for std_card, cur_card in zip(self._standard_cache["inventory"], self.collect_inventory_data()):
            std_val = std_card.get(field_name)
            cur_val = cur_card.get(field_name)
            if std_val != cur_val:
                diffs.append({"name": cur_card.get("name"), "expected": std_val, "actual": cur_val})
        return diffs

    # ------------------- Checkout field validation -------------------
    def check_checkout_field_errors(self, report_dir=None):
        errors = []
        screenshot_path = None

        try:
            

            InventoryPage(self.page).open_cart()
            checkout = CheckoutPage(self.page)
            checkout.checkout_btn().wait_for(state="visible", timeout=5000)
            checkout.checkout_btn().click()

        except Exception as e:
            errors.append(f"Checkout start/click failed: {str(e)}")
            if report_dir is None:
                date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                report_dir = os.path.join(os.getcwd(), "reports", date_str)
            os.makedirs(report_dir, exist_ok=True)
            screenshot_path = os.path.join(report_dir, "checkout_click_fail.png")
            self.page.screenshot(path=screenshot_path)

        return errors, screenshot_path

    # ------------------- Full pipeline HTML report -------------------
    def generate_full_pipeline_report(self, all_user_data, report_root="reports", timestamp_dir=None):
        """
        Generates HTML report for all users.
        all_user_data: dict of user_key -> user_entry (includes errors, timings, diffs, screenshot)
        """
        # Use provided timestamp folder, or create new one
        if timestamp_dir is None:
            timestamp_dir = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_dir = os.path.join(report_root, timestamp_dir)
        os.makedirs(report_dir, exist_ok=True)
    
        total = len(all_user_data)
        failed_users = {k: v for k, v in all_user_data.items() if v.get("errors")}
        passed_users = [k for k in all_user_data if k not in failed_users]
    
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        html = [
            "<!doctype html>",
            "<html><head><meta charset='utf-8'><title>Full Pipeline Report</title>",
            "<style>body{font-family:Arial,sans-serif} .pass{color:green} .fail{color:red} "
            "table{border-collapse:collapse;width:100%} th,td{border:1px solid #ccc;padding:4px;text-align:left} "
            "img{max-width:150px;max-height:150px} details{margin-bottom:10px} pre{background:#f4f4f4;padding:8px;"
            "white-space:pre-wrap;word-wrap:break-word}</style>",
            "</head><body>",
            f"<h1>Full Pipeline Report</h1><p>{timestamp}</p>",
            f"<p>Passed {len(passed_users)}/{total}, Failed {len(failed_users)}/{total}</p>"
        ]
    
        # -------------------- Passed users --------------------
        if passed_users:
            html.append("<h2>Passed users</h2>")
            for user in passed_users:
                html.append(f"<details><summary class='pass'>{user}</summary>")
                timings = all_user_data[user].get("timings", {})
                if timings:
                    html.append("<h3>Page Load Times (s)</h3><ul>")
                    for page_name, timing in timings.items():
                        html.append(f"<li>{page_name}: {timing}</li>")
                    html.append("</ul>")
                login_time = all_user_data[user].get("login_time")
                if login_time:
                    html.append(f"<p>Login Time: {login_time}s</p>")
                html.append("</details>")
    
        # -------------------- Failed users --------------------
        if failed_users:
            html.append("<h2>Failed users</h2>")
            for user, data in failed_users.items():
                html.append(f"<details><summary class='fail'>{user}</summary>")
    
                # Page timings
                if data.get("timings"):
                    html.append("<h3>Page Load Times (s)</h3><ul>")
                    for page_name, timing in data["timings"].items():
                        html.append(f"<li>{page_name}: {timing}</li>")
                    html.append("</ul>")
    
                if data.get("login_time"):
                    html.append(f"<p>Login Time: {data['login_time']}s</p>")
    
                # Errors
                if data.get("errors"):
                    html.append("<h3>Errors</h3><ul>")
                    for err in data["errors"]:
                        html.append(f"<li>{err}</li>")
                    html.append("</ul>")
    
                # Wrong prices
                if data.get("wrong_prices"):
                    html.append("<h3>Price Differences</h3><table><tr><th>Item</th><th>Expected</th><th>Actual</th></tr>")
                    for d in data["wrong_prices"]:
                        actual = d.get("actual", "")
                        if os.path.isfile(actual):
                            actual = f"<img src='{actual}'>"
                        html.append(f"<tr><td>{d['name']}</td><td>{d['expected']}</td><td>{actual}</td></tr>")
                    html.append("</table>")
    
                # Image diffs
                if data.get("image_diffs"):
                    html.append("<h3>Image Differences</h3><table><tr><th>Item</th><th>Expected</th><th>Actual</th></tr>")
                    for d in data["image_diffs"]:
                        actual_img = d.get("actual", "")
                        if os.path.isfile(actual_img):
                            actual_img = f"<img src='{actual_img}'>"
                        html.append(f"<tr><td>{d['name']}</td><td>{d['expected']}</td><td>{actual_img}</td></tr>")
                    html.append("</table>")
    
                # Description diffs
                if data.get("description_diffs"):
                    html.append("<h3>Description Differences</h3><pre>")
                    html.append(str(data["description_diffs"]))
                    html.append("</pre>")
    
                # Position diffs
                if data.get("position_diffs"):
                    html.append("<h3>Position Differences</h3><table><tr><th>Item</th><th>dx</th><th>dy</th></tr>")
                    for d in data["position_diffs"]:
                        html.append(f"<tr><td>{d['name']}</td><td>{d['dx']}</td><td>{d['dy']}</td></tr>")
                    html.append("</table>")
    
                # Screenshot
                if data.get("screenshot"):
                    screenshot_path = data["screenshot"]
                    if os.path.isfile(screenshot_path):
                        html.append("<h3>Screenshot</h3>")
                        html.append(f"<img src='{screenshot_path}' alt='screenshot'>")
    
                html.append("</details>")
    
        html.append("</body></html>")
    
        path = os.path.join(report_dir, "full_pipeline.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(html))
    
        print(f"HTML report generated: {path}")
        return report_dir
