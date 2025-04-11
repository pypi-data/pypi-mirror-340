"""Inventory page object for Sauce Demo site."""
from locatai import ElementFinder
import time

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

    def get_all_products(self):
        """Get all product elements on the page."""
        return ElementFinder.FindElementsByAI(self.driver, "inventory items with class 'inventory_item'")

    def add_item_to_cart(self, index=0):
        """Add a specific item to cart by index."""
        add_buttons = ElementFinder.FindElementsByAI(self.driver, "buttons containing text 'ADD TO CART'")
        if index < len(add_buttons):
            add_buttons[index].click()
            # Add a small wait for the cart badge to appear
            time.sleep(1)
            return True
        return False

    def get_cart_count(self):
        """Get the number of items in cart."""
        try:
            badge = ElementFinder.FindElementByAI(self.driver, "shopping cart badge with class 'shopping_cart_badge'")
            return int(badge.text)
        except:
            return 0

    def open_cart(self):
        """Click on the shopping cart link."""
        cart = ElementFinder.FindElementByAI(self.driver, "shopping cart link with class 'shopping_cart_link'")
        cart.click()

    def is_loaded(self):
        """Check if inventory page is loaded."""
        try:
            ElementFinder.FindElementByAI(self.driver, "inventory container with id 'inventory_container'", timeout=5)
            return True
        except:
            return False