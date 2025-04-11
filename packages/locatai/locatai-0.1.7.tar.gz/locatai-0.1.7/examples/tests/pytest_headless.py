"""
Pytest plugin to enable headless Chrome mode when running tests in CI.
"""
import pytest

def pytest_addoption(parser):
    """Add the headless option to pytest command line."""
    parser.addoption("--headless", action="store_true", default=False, 
                     help="Run browser tests in headless mode for CI/CD pipelines")

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Register the plugin and mark flag."""
    config.addinivalue_line("markers", "headless: mark test to run in headless mode")