"""
AI provider integrations for LocatAI.
"""

import os
from typing import Type
from locatai.ai.providers.base_provider import BaseAIProvider
from locatai.ai.providers.openai_provider import OpenAIProvider, GetElementUsingAI
from locatai.ai.providers.anthropic_provider import AnthropicProvider

def get_provider() -> BaseAIProvider:
    """
    Factory function to get the configured AI provider.
    Uses AI_PROVIDER environment variable to determine which provider to use.
    Defaults to OpenAI if not specified.
    """
    provider_name = os.getenv("AI_PROVIDER", "openai").lower()
    
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider
    }
    
    provider_class = providers.get(provider_name, OpenAIProvider)
    return provider_class()

__all__ = ['get_provider', 'GetElementUsingAI', 'BaseAIProvider', 'OpenAIProvider', 'AnthropicProvider']