"""
LocatAI - AI-powered element locator for Selenium WebDriver

A robust library that uses AI to find web elements based on natural language descriptions,
making Selenium tests more reliable and easier to maintain.

## Key Components

- ElementFinder: Core class providing AI-powered element finding capabilities
- AIUsageTracker: Utility for tracking AI API usage and performance metrics

## Basic Usage

```python
from selenium import webdriver
from locatai import ElementFinder

driver = webdriver.Chrome()
driver.get("https://example.com")

# Find element using natural language
element = ElementFinder.FindElementByAI(driver, "login button")
element.click()
```

## Environment Setup

Before using this package, create a `.env` file in your project root with:
```
OPENAI_API_KEY=your_openai_api_key
```

For more information, see the README.md or visit:
https://github.com/Divyarajsinh-Dodia/locatai
"""

__version__ = '0.1.0'

from locatai.finder.element_finder import ElementFinder
from locatai.utils.analytics import AIUsageTracker

__all__ = ['ElementFinder', 'AIUsageTracker']