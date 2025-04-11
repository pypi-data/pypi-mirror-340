"""
This example demonstrates how to use LocatAI with the Sauce Demo website.
It showcases various features like finding elements using natural language,
handling multiple elements, and tracking AI usage.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from locatai import ElementFinder, AIUsageTracker

def setup_driver():
    """Set up and return a Chrome WebDriver instance"""
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    return webdriver.Chrome(options=chrome_options)

def login_to_sauce_demo(driver):
    """Demonstrate logging in using LocatAI"""
    print("\n=== Logging in to Sauce Demo ===")
    
    # Navigate to the website
    driver.get("https://www.saucedemo.com/v1/")
    
    # Find and fill the username field
    username = ElementFinder.FindElementByAI(driver, "username input field")
    username.send_keys("standard_user")
    
    # Find and fill the password field
    password = ElementFinder.FindElementByAI(driver, "password input field")
    password.send_keys("secret_sauce")
    
    # Find and click the login button
    login_button = ElementFinder.FindElementByAI(driver, "login button")
    login_button.click()
    
    print("Successfully logged in!")

def demonstrate_inventory_interactions(driver):
    """Demonstrate various LocatAI features on the inventory page"""
    print("\n=== Interacting with Inventory ===")
    
    # Find all product cards (demonstrating FindElementsByAI)
    products = ElementFinder.FindElementsByAI(driver, "product cards or items")
    print(f"Found {len(products)} products on the page")
    
    # Find the first 'Add to Cart' button
    add_button = ElementFinder.FindElementByAI(driver, "first Add to Cart button")
    add_button.click()
    print("Added first item to cart")
    
    # Find the shopping cart
    cart = ElementFinder.FindElementByAI(driver, "shopping cart link")
    print("Cart element found")
    
    # Get the cart badge number
    cart_badge = ElementFinder.FindElementByAI(driver, "shopping cart badge showing number of items")
    print(f"Items in cart: {cart_badge.text}")

def demonstrate_error_handling(driver):
    """Demonstrate how LocatAI handles non-existent elements"""
    print("\n=== Demonstrating Error Handling ===")
    
    try:
        # Try to find a non-existent element
        ElementFinder.FindElementByAI(driver, "non-existent mega menu", timeout=5)
    except Exception as e:
        print(f"Successfully caught error for non-existent element: {str(e)}")

def print_usage_stats():
    """Print the AI usage statistics"""
    print("\n=== AI Usage Statistics ===")
    report = AIUsageTracker.get_instance().get_report()
    print(f"Total API Calls: {report['api_calls']}")
    print(f"Cache Hit Rate: {report['cache_hit_rate']:.1%}")
    print(f"Success Rate: {report['element_success_rate']:.1%}")
    print(f"Estimated Cost: ${report['estimated_cost']:.4f}")

def main():
    """Main function to run the demo"""
    print("Starting LocatAI Sauce Demo example...")
    
    driver = setup_driver()
    
    try:
        login_to_sauce_demo(driver)
        time.sleep(2)  # Wait for inventory page to load
        
        demonstrate_inventory_interactions(driver)
        time.sleep(1)
        
        demonstrate_error_handling(driver)
        
        print_usage_stats()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print("\nClosing browser...")
        driver.quit()

if __name__ == "__main__":
    main()