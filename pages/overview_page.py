from playwright.sync_api import Page
from utils.helpers import parse_price


class OverviewPage:
    def __init__(self, page: Page):
        self.page = page
        self.finish_btn = page.locator('#finish')
        self.item_total = page.locator('.summary_subtotal_label')
        self.tax = page.locator('.summary_tax_label')
        self.total = page.locator('.summary_total_label')
    
    
    def get_item_total(self) -> float:
        return parse_price(self.item_total.inner_text())
    
    
    def get_tax(self) -> float:
        return parse_price(self.tax.inner_text())
    
    
    def get_total(self) -> float:
        return parse_price(self.total.inner_text())
    
    
    def finish(self):
        self.finish_btn.click()