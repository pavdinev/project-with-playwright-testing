import config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

class UserValidator:
    """
    Validates a user's inventory against a cached standard_user reference.
    Caches:
      - Prices (literal strings)
      - Image URLs (exact list/order)
      - Layout metrics (column count, vertical ordering, typical vertical gap)
    """

    _standard_prices_cache = None
    _standard_images_cache = None
    _standard_layout_cache = None  # {"columns": int, "medianGap": float, "total": int}

    def __init__(self, page):
        self.page = page

    def get_all_product_images(self):
        return self.page.locator(".inventory_item_img img").evaluate_all(
            "els => els.map(e => e.src)"
        )

    def wait_for_inventory_loaded(self, timeout=5000) -> bool:
        """Wait until at least one inventory card is present; return False on timeout."""
        try:
            self.page.locator(".inventory_item").first.wait_for(timeout=timeout)
            return True
        except Exception:
            return False

    # ---------- internal helpers ----------
    def _collect_layout_metrics(self):
        """
        Collect simple, robust layout metrics:
          - number of visual columns (by rounding each card's left x to 10px buckets)
          - for each item: check vertical order name->desc->price and measure gap (price.top - name.top)
          - median vertical gap across items (robust to outliers)
        """
        return self.page.evaluate("""
() => {
  const items = Array.from(document.querySelectorAll('.inventory_item'));
  const lefts = items.map(el => el.getBoundingClientRect().left);
  const rounded = lefts.map(x => Math.round(x / 10) * 10);
  const columns = Array.from(new Set(rounded)).length;

  const perItem = items.map(el => {
    const name = el.querySelector('.inventory_item_name')?.getBoundingClientRect();
    const desc = el.querySelector('.inventory_item_desc')?.getBoundingClientRect();
    const price = el.querySelector('.inventory_item_price')?.getBoundingClientRect();
    const okOrder = !!(name && desc && price && name.top <= desc.top && desc.top <= price.top);
    const gap = (name && price) ? (price.top - name.top) : null;
    return { okOrder, gap };
  });

  const gaps = perItem.map(p => p.gap).filter(g => g != null).sort((a,b) => a - b);
  const medianGap = gaps.length ? gaps[Math.floor(gaps.length/2)] : null;
  const okCount = perItem.filter(p => p.okOrder).length;

  return {
    columns,
    medianGap,
    okCount,
    total: items.length
  };
}
""")

    # ---------- caching standard ----------
    def cache_standard_user_data(self):
        """Login as standard_user once and cache reference prices/images/layout."""
        if (self._standard_prices_cache is not None and
            self._standard_images_cache is not None and
            self._standard_layout_cache is not None):
            return

        login_page = LoginPage(self.page)
        login_page.navigate()
        login_page.login(
            config.USERS["standard_user"]["username"],
            config.USERS["standard_user"]["password"]
        )

        # Make sure inventory is up
        if not self.wait_for_inventory_loaded(timeout=8000):
            raise RuntimeError("standard_user inventory did not load; cannot cache reference data")

        inventory = InventoryPage(self.page)
        self._standard_prices_cache = inventory.item_prices()
        self._standard_images_cache = self.get_all_product_images()
        self._standard_layout_cache = self._collect_layout_metrics()

    # ---------- checks against cached standard ----------
    def has_wrong_prices(self) -> bool:
        current_prices = [el.inner_text() for el in self.page.locator(".inventory_item_price").all()]
        return current_prices != self._standard_prices_cache

    def has_bad_images(self) -> bool:
        """Exact image list comparison with standard + basic sanity (non-empty, jpg/png)."""
        current_images = self.get_all_product_images()
        basic_sanity = all(img and (img.endswith(".jpg") or img.endswith(".png")) for img in current_images)
        if not basic_sanity:
            return True
        return current_images != self._standard_images_cache

    def has_layout_issues(self) -> bool:
        """Compare column count, per-item vertical order, and typical spacing to standard."""
        std = self._standard_layout_cache
        cur = self._collect_layout_metrics()

        if cur["total"] != std["total"]:
            return True  # different number of cards

        if cur["columns"] != std["columns"]:
            return True  # different grid layout

        # Require most items obey vertical name->desc->price order (match standard proportion)
        if cur["okCount"] < std["okCount"]:
            return True

        # Spacing tolerance (allow ~20px drift from standard median)
        if std["medianGap"] is not None and cur["medianGap"] is not None:
            if abs(cur["medianGap"] - std["medianGap"]) > 20:
                return True

        return False
