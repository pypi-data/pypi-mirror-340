# LocatAI

AI-powered element locator for Selenium WebDriver.

## Overview

LocatAI is an innovative Python package that uses AI to find web elements based on natural language descriptions, making your Selenium tests more reliable and easier to maintain. Instead of brittle CSS selectors or XPath expressions, you can use natural language to describe the elements you want to interact with.

## Features

- **Natural Language Element Finding**: Locate elements using plain English descriptions
- **Multiple AI Providers**: Support for OpenAI GPT-4 and Anthropic Claude
- **Smart Caching**: Reduces API calls and improves performance
- **Automatic Timeout Management**: Dynamically adjusts timeouts based on historical performance
- **Detailed Error Diagnostics**: Helps debug element location failures
- **Usage Analytics**: Tracks API usage, cache efficiency, and success rates

## Installation

Install the package using pip:

```bash
pip install locatai
```

## Environment Setup

LocatAI supports both OpenAI and Anthropic Claude for element location. You need to set up your API keys and configure which provider and model to use:

1. Create a `.env` file in your project's root directory
2. Add your configuration to the file:

```
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Provider Configuration
# Uncomment the provider you want to use (default is OpenAI)
AI_PROVIDER=openai
# AI_PROVIDER=anthropic

# Model Configuration
# OpenAI Models (default: gpt-4)
OPENAI_MODEL=gpt-4
# Other options: gpt-4-turbo-preview, gpt-3.5-turbo, etc.

# Anthropic Models (default: claude-3-opus-20240229)
ANTHROPIC_MODEL=claude-3-opus-20240229
# Other options: claude-3-sonnet-20240229, claude-3-haiku-20240307, etc.
```

3. **Important**: Add the `.env` file to your `.gitignore` to prevent accidentally committing your API keys

The package uses the `python-dotenv` library to automatically load these settings when needed.

## Basic Usage

```python
from selenium import webdriver
from locatai import ElementFinder

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://example.com")

# Find an element using natural language
login_button = ElementFinder.FindElementByAI(driver, "Login button")
login_button.click()

# Find multiple elements
item_cards = ElementFinder.FindElementsByAI(driver, "product cards")
print(f"Found {len(item_cards)} products")
```

## Advanced Usage

### Choosing an AI Provider

LocatAI supports two AI providers:
- OpenAI (GPT-4) - Default provider
- Anthropic (Claude) - Alternative provider with different capabilities

You can switch providers by setting the `AI_PROVIDER` environment variable in your `.env` file:

```
# Use OpenAI
AI_PROVIDER=openai

# Use Anthropic Claude
AI_PROVIDER=anthropic
```

### Smart Timeouts

LocatAI automatically adjusts wait times based on historical performance:

```python
# Default timeout will be used (smart timeout based on element history)
submit_button = ElementFinder.FindElementByAI(driver, "Submit button") 

# Override with a custom timeout in seconds
menu_item = ElementFinder.FindElementByAI(driver, "Settings menu item", timeout=15)
```

### Tracking API Usage

Monitor your AI API usage and performance metrics:

```python
from locatai import AIUsageTracker

# Get usage statistics
report = AIUsageTracker.get_instance().get_report()
print(f"API Calls: {report['api_calls']}")
print(f"Cache Hit Rate: {report['cache_hit_rate']:.1%}")
print(f"Estimated Cost: ${report['estimated_cost']:.4f}")
```

See the examples directory for more advanced usage patterns.

## How It Works

LocatAI analyzes the current DOM of your web page and uses AI (either OpenAI's GPT-4 or Anthropic's Claude) to determine the most reliable selector strategy for your element description. It prioritizes the most stable selectors (ID, name) when available, and falls back to CSS selectors or XPath when needed.

The package includes:
- Smart caching to reduce API calls for previously seen elements
- Automatic retries with different locator strategies
- Detailed error diagnostics when elements can't be found
- Performance tracking to optimize timeouts

## Troubleshooting

### API Key Issues
- Ensure your `.env` file is in the correct location (project root directory)
- Verify your API keys are valid for your chosen provider
- Check that the environment variable names are exactly `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY`
- Verify the `AI_PROVIDER` setting matches your intended provider

### Element Not Found Issues
- Try using more specific element descriptions
- Ensure the element is visible in the DOM when the finder method is called
- Check if the element is inside an iframe (switch to it first)
- Increase the timeout for elements that take longer to load
- Try switching AI providers as they may have different capabilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request to https://github.com/Divyarajsinh-Dodia/locatai.

## License

MIT