"""LLM provider adapters for PATH Framework."""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import os
import logging


class LLMAdapter(ABC):
    """Abstract adapter for LLM providers."""
    
    @abstractmethod
    async def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate response from LLM provider."""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get provider name."""
        pass


class OpenAIAdapter(LLMAdapter):
    """OpenAI GPT adapter."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.logger = logging.getLogger("OpenAIAdapter")
    
    async def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate response using OpenAI API."""
        # Real implementation would use openai client
        self.logger.info(f"OpenAI {self.model} request")
        return f"OpenAI response for: {prompt[:50]}..."
    
    def get_provider_name(self) -> str:
        return "openai"


class AnthropicAdapter(LLMAdapter):
    """Anthropic Claude adapter."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.logger = logging.getLogger("AnthropicAdapter")
    
    async def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate response using Anthropic API."""
        # Real implementation would use anthropic client
        self.logger.info(f"Anthropic {self.model} request")
        return f"Claude response for: {prompt[:50]}..."
    
    def get_provider_name(self) -> str:
        return "anthropic"


class AzureOpenAIAdapter(LLMAdapter):
    """Azure OpenAI adapter."""
    
    def __init__(self, endpoint: Optional[str] = None, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.model = model
        self.logger = logging.getLogger("AzureOpenAIAdapter")
    
    async def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate response using Azure OpenAI."""
        self.logger.info(f"Azure OpenAI {self.model} request")
        return f"Azure OpenAI response for: {prompt[:50]}..."
    
    def get_provider_name(self) -> str:
        return "azure_openai"


class BedrockAdapter(LLMAdapter):
    """AWS Bedrock adapter."""
    
    def __init__(self, region: str = "us-east-1", model: str = "anthropic.claude-3-sonnet"):
        self.region = region
        self.model = model
        self.logger = logging.getLogger("BedrockAdapter")
    
    async def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate response using AWS Bedrock."""
        self.logger.info(f"Bedrock {self.model} request")
        return f"Bedrock response for: {prompt[:50]}..."
    
    def get_provider_name(self) -> str:
        return "bedrock"


class LocalLLMAdapter(LLMAdapter):
    """Local LLM adapter (Ollama, etc.)."""
    
    def __init__(self, endpoint: str = "http://localhost:11434", model: str = "llama2"):
        self.endpoint = endpoint
        self.model = model
        self.logger = logging.getLogger("LocalLLMAdapter")
    
    async def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate response using local LLM."""
        self.logger.info(f"Local LLM {self.model} request")
        return f"Local LLM response for: {prompt[:50]}..."
    
    def get_provider_name(self) -> str:
        return "local"


class LLMAdapterFactory:
    """Factory for creating LLM adapters."""
    
    ADAPTERS = {
        "openai": OpenAIAdapter,
        "anthropic": AnthropicAdapter,
        "azure_openai": AzureOpenAIAdapter,
        "bedrock": BedrockAdapter,
        "local": LocalLLMAdapter
    }
    
    @classmethod
    def create_adapter(cls, provider: str, **kwargs) -> LLMAdapter:
        """Create LLM adapter for provider."""
        if provider not in cls.ADAPTERS:
            raise ValueError(f"Unknown LLM provider: {provider}. Available: {list(cls.ADAPTERS.keys())}")
        
        adapter_class = cls.ADAPTERS[provider]
        return adapter_class(**kwargs)
    
    @classmethod
    def get_available_providers(cls) -> list:
        """Get list of available providers."""
        return list(cls.ADAPTERS.keys())