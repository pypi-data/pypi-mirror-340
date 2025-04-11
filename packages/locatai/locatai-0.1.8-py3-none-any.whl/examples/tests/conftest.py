"""Pytest configuration and shared fixtures."""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from locatai import AIUsageTracker

def pytest_addoption(parser):
    """Add command line options to pytest."""
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run browser tests in headless mode")

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "login: mark test as login test")
    config.addinivalue_line("markers", "inventory: mark test as inventory test")

@pytest.fixture(scope="function")
def chrome_options(request):
    """Chrome options for WebDriver with headless support for CI."""
    options = Options()
    options.add_argument('--start-maximized')
    
    # Enable headless mode if --headless flag is passed
    if request.config.getoption("--headless", False):
        options.add_argument('--headless=new')  # Using the new headless mode
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
    
    return options

@pytest.fixture(scope="function")
def driver(chrome_options):
    """Provide a new WebDriver instance for each test."""
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()  # Ensure driver is closed after each test

@pytest.fixture(scope="session")
def base_url():
    """Provide base URL for the application."""
    return "https://www.saucedemo.com/v1/"

@pytest.fixture(scope="session")
def test_data():
    """Provide test data for the application."""
    return {
        "valid_user": {
            "username": "standard_user",
            "password": "secret_sauce"
        },
        "invalid_user": {
            "username": "locked_out_user",
            "password": "wrong_password"
        }
    }

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print AI usage statistics in the terminal summary after all tests finish."""
    tracker = AIUsageTracker.get_instance()
    report = tracker.get_report()
    
    terminalreporter.section("AI Usage Statistics")
    terminalreporter.line("\n=== AI Usage Statistics ===")
    terminalreporter.line(f"Total API Calls: {report['api_calls']}")
    terminalreporter.line(f"Cache Hit Rate: {report['cache_hit_rate']:.1%}")
    terminalreporter.line(f"Success Rate: {report['element_success_rate']:.1%}")
    terminalreporter.line(f"Estimated Cost: ${report['estimated_cost']:.4f}")
    terminalreporter.line(f"Runtime: {report['runtime_seconds']:.2f} seconds")