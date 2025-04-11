"""
Anthropic Claude provider integration for element locator functionality.
"""

import os
from anthropic import Anthropic
import logging
from locatai.ai.providers.base_provider import BaseAIProvider
from locatai.ai.prompts.locator_prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class AnthropicProvider(BaseAIProvider):
    """Implements element finding using Anthropic's Claude"""
    
    def __init__(self):
        """Initialize Anthropic client with API key from environment"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.error("Anthropic API key not found in environment variables")
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = Anthropic(api_key=api_key)
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    
    def get_element(self, dom: str, element_description: str) -> str:
        """
        Uses Claude to find a suitable locator for the described element.
        
        Args:
            dom (str): HTML DOM content to analyze
            element_description (str): Natural language description of the element
            
        Returns:
            str: Locator in the format 'STRATEGY: value' or 'Element Not Found'
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                temperature=0.3,
                system=SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"Element Description: {element_description}\nHTML Snippet: {dom}"
                }]
            )
            
            result = message.content[0].text.strip()
            if not result:
                logger.error("Empty response from Claude")
                return "Element Not Found"
                
            logger.info(f"Claude ({self.model}) returned locator: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in Claude API call: {str(e)}")
            return "Element Not Found"