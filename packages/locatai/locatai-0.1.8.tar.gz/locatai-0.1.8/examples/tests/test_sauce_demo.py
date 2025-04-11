"""
Test suite for Sauce Demo website using LocatAI with pytest.
"""
import pytest
from .pages.login_page import LoginPage
from .pages.inventory_page import InventoryPage

@pytest.mark.login
class TestLogin:
    def test_successful_login(self, driver, base_url, test_data):
        """Test successful login with valid credentials."""
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        
        login_page.navigate(base_url)
        login_page.login(
            test_data["valid_user"]["username"],
            test_data["valid_user"]["password"]
        )
        
        assert inventory_page.is_loaded(), "Login failed - inventory page not loaded"

    def test_failed_login(self, driver, base_url, test_data):
        """Test login failure with invalid credentials."""
        login_page = LoginPage(driver)
        
        login_page.navigate(base_url)
        login_page.login(
            test_data["invalid_user"]["username"],
            test_data["invalid_user"]["password"]
        )
        
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed for invalid login"

# @pytest.mark.inventory
# class TestInventory:
#     @pytest.fixture(autouse=True)
#     def setup(self, driver, base_url, test_data):
#         """Setup for inventory tests - login first."""
#         # Initialize pages
#         self.login_page = LoginPage(driver)
#         self.inventory_page = InventoryPage(driver)
        
#         # Perform login before each inventory test
#         self.login_page.navigate(base_url)
#         self.login_page.login(
#             test_data["valid_user"]["username"],
#             test_data["valid_user"]["password"]
#         )
        
#         # Wait for inventory page to load
#         assert self.inventory_page.is_loaded(), "Inventory page failed to load after login"
        
#         # Make the driver available to test methods
#         self.driver = driver

#     def test_product_listing(self, driver):
#         """Test that products are displayed on the inventory page."""
#         products = self.inventory_page.get_all_products()
#         assert len(products) > 0, "No products found on inventory page"

#     def test_add_to_cart(self, driver):
#         """Test adding an item to the cart."""
#         initial_count = self.inventory_page.get_cart_count()
        
#         # Add first item to cart
#         assert self.inventory_page.add_item_to_cart(0), "Failed to add item to cart"
        
#         # Verify cart count increased
#         new_count = self.inventory_page.get_cart_count()
#         assert new_count == initial_count + 1, "Cart count did not increase after adding item"
