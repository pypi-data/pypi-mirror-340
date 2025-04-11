"""Login page object for Sauce Demo site."""
from locatai import ElementFinder

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def navigate(self, base_url):
        """Navigate to the login page."""
        self.driver.get(base_url)

    def login(self, username, password):
        """Login with the given credentials."""
        username_field = ElementFinder.FindElementByAI(self.driver, "username input field")
        password_field = ElementFinder.FindElementByAI(self.driver, "password input field")
        login_button = ElementFinder.FindElementByAI(self.driver, "login button")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

    def get_error_message(self):
        """Get the error message if login fails."""
        try:
            error = ElementFinder.FindElementByAI(self.driver, "error message with text 'Epic sadface'", timeout=5)
            return error.text
        except:
            return None