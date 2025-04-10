"""
OpenAI provider integration for element locator functionality.

This module handles the communication with the OpenAI API to generate
element locators based on natural language descriptions and HTML content.

It includes:
- API key loading and validation from environment variables
- Error handling for API calls
- Formatting of prompts and responses for element finding

Environment Setup:
    Create a .env file in your project root with: OPENAI_API_KEY=your-api-key
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import logging
from locatai.ai.prompts.locator_prompts import SYSTEM_PROMPT

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

def get_api_key():
    """
    Get the OpenAI API key from environment variables.
    
    Returns:
        str: The OpenAI API key
        
    Raises:
        ValueError: If the API key is not found in environment variables
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("API key not found in environment variables")
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable in a .env file.")
    return api_key

def GetElementUsingAI(dom, elementDescription):
    """
    Uses OpenAI to find a suitable locator for the described element.
    
    The function:
    1. Sends the HTML DOM and element description to OpenAI
    2. Receives a locator strategy and value in response
    3. Returns the locator in a standardized format
    
    Args:
        dom (str): HTML DOM content to analyze
        elementDescription (str): Natural language description of the element
        
    Returns:
        str: Locator in the format 'STRATEGY: value' (e.g., 'ID: login-button') 
             or 'Element Not Found' if no suitable element could be identified
             
    Examples:
        >>> locator = GetElementUsingAI(driver.page_source, "Login button")
        >>> print(locator)
        'ID: login-button'
    """
    try:
        # Get API key
        api_key = get_api_key()
        
        # Initialize OpenAI client with explicit API key
        client = OpenAI(api_key=api_key)

        logger.info(f"Sending request to OpenAI for element: '{elementDescription}'")

        # Prepare the messages for the API call
        messages = [{
            "role": "system",
            "content": SYSTEM_PROMPT
        }, {
            "role": "user",
            "content": f"Element Description: {elementDescription}\nHTML Snippet: {dom}"
        }]

        # Make the API call with optimized parameters
        response = client.chat.completions.create(
            model="gpt-4o", # Using the standard GPT-4o model name for better compatibility
            messages=messages,
            max_tokens=100,  # Limit response size for efficiency
            temperature=0.3  # Lower temperature for more deterministic results
        )

        # Process the response
        result = response.choices[0].message.content.strip() if response.choices else ""
        if not result:
            logger.error("OpenAI response was empty")
            return "Element Not Found"

        logger.info(f"AI returned locator: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in GetElementUsingAI: {str(e)}")
        return "Element Not Found"  # Fallback for all errors