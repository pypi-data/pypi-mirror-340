"""
Base class for AI providers in LocatAI.
"""

from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def get_element(self, dom: str, element_description: str) -> str:
        """
        Uses AI to find a suitable locator for the described element.
        
        Args:
            dom (str): HTML DOM content to analyze
            element_description (str): Natural language description of the element
            
        Returns:
            str: Locator in the format 'STRATEGY: value' (e.g., 'ID: login-button') 
                 or 'Element Not Found' if no suitable element could be identified
        """
        pass