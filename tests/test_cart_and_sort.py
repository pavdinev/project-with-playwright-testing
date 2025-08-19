from config import DEFAULT_USER
from utils.helpers import parse_price, is_sorted
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from tests.base_test import BaseTest


class TestCartAndSort(BaseTest):
    def setUp(self):
        super().setUp()
        # login once per test for isolation
        login = LoginPage(self.page)
        login.goto()
        login.login(DEFAULT_USER["username"], DEFAULT_USER["password"])
    
    
    def test_sorting_and_add_to_cart(self):
        inv = InventoryPage(self.page)
        self.assertTrue(inv.is_loaded())
        
        
        # Verify default A→Z sort
        names = inv.item_names()
        self.assertTrue(is_sorted(names), "Default should be A→Z sorted")
        
        
        # Sort by price low→high
        inv.set_sort("lohi")
        prices = [parse_price(p) for p in inv.item_prices()]
        self.assertTrue(is_sorted(prices), "Prices should be low→high after sort")
        
        
        # Add two items by name
        inv.add_to_cart_by_name("Sauce Labs Backpack")
        inv.add_to_cart_by_name("Sauce Labs Bike Light")
        self.assertEqual(inv.get_cart_count(), 2)
        
        
        # Go to cart and verify
        inv.open_cart()
        cart = CartPage(self.page)
        items = cart.get_item_names()
        self.assertIn("Sauce Labs Backpack", items)
        self.assertIn("Sauce Labs Bike Light", items)