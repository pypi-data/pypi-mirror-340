"""
OpenAI provider integration for element locator functionality.
"""

import os
from openai import OpenAI
import logging
from locatai.ai.providers.base_provider import BaseAIProvider
from locatai.ai.prompts.locator_prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class OpenAIProvider(BaseAIProvider):
    """Implements element finding using OpenAI"""
    
    def __init__(self):
        """Initialize OpenAI client with API key from environment"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OpenAI API key not found in environment variables")
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")  # Default to gpt-4 if not specified
    
    def get_element(self, dom: str, element_description: str) -> str:
        """
        Uses OpenAI to find a suitable locator for the described element.
        
        Args:
            dom (str): HTML DOM content to analyze
            element_description (str): Natural language description of the element
            
        Returns:
            str: Locator in the format 'STRATEGY: value' or 'Element Not Found'
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }, {
                    "role": "user",
                    "content": f"Element Description: {element_description}\nHTML Snippet: {dom}"
                }],
                max_tokens=100,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            if not result:
                logger.error("Empty response from OpenAI")
                return "Element Not Found"
                
            logger.info(f"OpenAI ({self.model}) returned locator: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in OpenAI API call: {str(e)}")
            return "Element Not Found"

# For backwards compatibility
def GetElementUsingAI(dom: str, element_description: str) -> str:
    """Legacy function that uses OpenAI provider"""
    provider = OpenAIProvider()
    return provider.get_element(dom, element_description)