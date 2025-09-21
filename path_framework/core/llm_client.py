"""
LLM Client Interface for PATH Framework
Supports multiple LLM providers: OpenAI, Anthropic, Ollama, etc.
"""

import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any

from ..exceptions import PathFrameworkError

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    AZURE_OPENAI = "azure_openai"
    OPENROUTER = "openrouter"


@dataclass
class LLMRequest:
    """Request structure for LLM calls"""

    prompt: str
    system_prompt: str | None = None
    temperature: float = 0.1
    max_tokens: int = 4000
    model: str | None = None
    response_format: str = "text"  # text, json


@dataclass
class LLMResponse:
    """Response structure from LLM calls"""

    content: str
    tokens_used: int
    model_used: str
    provider: str
    finish_reason: str
    metadata: dict[str, Any] = None


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients"""

    def __init__(self, api_key: str, model: str, timeout: int = 30):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate response from LLM"""

    @abstractmethod
    async def generate_structured(
        self, request: LLMRequest, schema: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate structured response (JSON) from LLM"""


class OpenAIClient(BaseLLMClient):
    """OpenAI LLM Client"""

    def __init__(self, api_key: str, model: str = "gpt-4", timeout: int = 30):
        super().__init__(api_key, model, timeout)
        self.base_url = "https://api.openai.com/v1"

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate response using OpenAI API"""
        try:
            # Import here to avoid hard dependency
            import openai

            client = openai.AsyncOpenAI(api_key=self.api_key, timeout=self.timeout)

            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})

            response = await client.chat.completions.create(
                model=request.model or self.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                response_format=(
                    {"type": "json_object"}
                    if request.response_format == "json"
                    else {"type": "text"}
                ),
            )

            return LLMResponse(
                content=response.choices[0].message.content,
                tokens_used=response.usage.total_tokens,
                model_used=response.model,
                provider="openai",
                finish_reason=response.choices[0].finish_reason,
                metadata={"usage": response.usage.model_dump()},
            )

        except ImportError:
            raise PathFrameworkError(
                "OpenAI library not installed. Run: pip install openai"
            )
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise PathFrameworkError(f"OpenAI generation failed: {e!s}")

    async def generate_structured(
        self, request: LLMRequest, schema: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate structured JSON response"""
        # Add JSON format instruction to prompt
        json_prompt = f"""{request.prompt}

Please respond with valid JSON that matches this schema:
{json.dumps(schema, indent=2)}

Ensure your response is valid JSON only, no additional text."""

        structured_request = LLMRequest(
            prompt=json_prompt,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            model=request.model,
            response_format="json",
        )

        response = await self.generate(structured_request)

        try:
            return json.loads(response.content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response.content}")
            raise PathFrameworkError(f"Invalid JSON response from LLM: {e!s}")


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude LLM Client"""

    def __init__(
        self, api_key: str, model: str = "claude-3-sonnet-20240229", timeout: int = 30
    ):
        super().__init__(api_key, model, timeout)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate response using Anthropic API"""
        try:
            # Import here to avoid hard dependency
            import anthropic

            client = anthropic.AsyncAnthropic(
                api_key=self.api_key, timeout=self.timeout
            )

            # Combine system and user prompts for Anthropic
            full_prompt = ""
            if request.system_prompt:
                full_prompt = f"System: {request.system_prompt}\n\nHuman: {request.prompt}\n\nAssistant:"
            else:
                full_prompt = f"Human: {request.prompt}\n\nAssistant:"

            response = await client.messages.create(
                model=request.model or self.model,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                messages=[{"role": "user", "content": full_prompt}],
            )

            return LLMResponse(
                content=response.content[0].text,
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                model_used=response.model,
                provider="anthropic",
                finish_reason=response.stop_reason,
                metadata={
                    "usage": {
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens,
                    }
                },
            )

        except ImportError:
            raise PathFrameworkError(
                "Anthropic library not installed. Run: pip install anthropic"
            )
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise PathFrameworkError(f"Anthropic generation failed: {e!s}")

    async def generate_structured(
        self, request: LLMRequest, schema: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate structured JSON response"""
        json_prompt = f"""{request.prompt}

Please respond with valid JSON that matches this schema:
{json.dumps(schema, indent=2)}

Return only valid JSON, no additional text or formatting."""

        structured_request = LLMRequest(
            prompt=json_prompt,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            model=request.model,
        )

        response = await self.generate(structured_request)

        try:
            return json.loads(response.content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response.content}")
            raise PathFrameworkError(f"Invalid JSON response from LLM: {e!s}")


class OllamaClient(BaseLLMClient):
    """Ollama Local LLM Client"""

    def __init__(
        self,
        api_key: str = "",
        model: str = "llama2",
        base_url: str = "http://localhost:11434",
        timeout: int = 60,
    ):
        super().__init__(api_key, model, timeout)
        self.base_url = base_url

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate response using Ollama API"""
        try:
            import aiohttp

            prompt = request.prompt
            if request.system_prompt:
                prompt = f"System: {request.system_prompt}\n\nUser: {request.prompt}"

            payload = {
                "model": request.model or self.model,
                "prompt": prompt,
                "options": {
                    "temperature": request.temperature,
                    "num_predict": request.max_tokens,
                },
                "stream": False,
            }

            async with (
                aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as session,
                session.post(f"{self.base_url}/api/generate", json=payload) as response,
            ):
                if response.status != 200:
                    raise PathFrameworkError(f"Ollama API error: {response.status}")

                result = await response.json()

                return LLMResponse(
                    content=result["response"],
                    tokens_used=result.get("eval_count", 0)
                    + result.get("prompt_eval_count", 0),
                    model_used=result["model"],
                    provider="ollama",
                    finish_reason="stop",
                    metadata=result,
                )

        except ImportError:
            raise PathFrameworkError(
                "aiohttp library not installed. Run: pip install aiohttp"
            )
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise PathFrameworkError(f"Ollama generation failed: {e!s}")

    async def generate_structured(
        self, request: LLMRequest, schema: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate structured JSON response"""
        json_prompt = f"""{request.prompt}

Respond with valid JSON matching this schema:
{json.dumps(schema, indent=2)}

JSON only, no other text:"""

        structured_request = LLMRequest(
            prompt=json_prompt,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            model=request.model,
        )

        response = await self.generate(structured_request)

        try:
            # Clean up response - Ollama sometimes adds extra text
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]

            return json.loads(content.strip())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response.content}")
            raise PathFrameworkError(f"Invalid JSON response from LLM: {e!s}")


class OpenRouterClient(BaseLLMClient):
    """OpenRouter LLM Client - Access to multiple models through OpenRouter API"""

    def __init__(self, api_key: str, model: str = "openai/gpt-4", timeout: int = 30):
        super().__init__(api_key, model, timeout)
        self.base_url = "https://openrouter.ai/api/v1"

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate response using OpenRouter API"""
        try:
            # OpenRouter uses OpenAI-compatible API
            import openai

            client = openai.AsyncOpenAI(
                api_key=self.api_key, base_url=self.base_url, timeout=self.timeout
            )

            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})

            response = await client.chat.completions.create(
                model=request.model or self.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                response_format=(
                    {"type": "json_object"}
                    if request.response_format == "json"
                    else {"type": "text"}
                ),
            )

            return LLMResponse(
                content=response.choices[0].message.content,
                tokens_used=response.usage.total_tokens if response.usage else 0,
                model_used=response.model,
                provider="openrouter",
                finish_reason=response.choices[0].finish_reason,
                metadata={
                    "usage": response.usage.model_dump() if response.usage else {},
                    "openrouter_model": response.model,
                },
            )

        except ImportError:
            raise PathFrameworkError(
                "OpenAI library not installed. Run: pip install openai"
            )
        except Exception as e:
            logger.error(f"OpenRouter API error: {e}")
            raise PathFrameworkError(f"OpenRouter generation failed: {e!s}")

    async def generate_structured(
        self, request: LLMRequest, schema: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate structured JSON response"""
        # Add JSON format instruction to prompt
        json_prompt = f"""{request.prompt}

Please respond with valid JSON that matches this schema:
{json.dumps(schema, indent=2)}

Ensure your response is valid JSON only, no additional text."""

        structured_request = LLMRequest(
            prompt=json_prompt,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            model=request.model,
            response_format="json",
        )

        response = await self.generate(structured_request)

        try:
            return json.loads(response.content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response.content}")
            raise PathFrameworkError(f"Invalid JSON response from LLM: {e!s}")


class LLMClientFactory:
    """Factory for creating LLM clients"""

    @staticmethod
    def create_client(
        provider: LLMProvider, api_key: str, model: str, **kwargs
    ) -> BaseLLMClient:
        """Create LLM client based on provider"""

        if provider == LLMProvider.OPENAI:
            return OpenAIClient(api_key=api_key, model=model, **kwargs)
        elif provider == LLMProvider.ANTHROPIC:
            return AnthropicClient(api_key=api_key, model=model, **kwargs)
        elif provider == LLMProvider.OLLAMA:
            return OllamaClient(api_key=api_key, model=model, **kwargs)
        elif provider == LLMProvider.OPENROUTER:
            return OpenRouterClient(api_key=api_key, model=model, **kwargs)
        else:
            raise PathFrameworkError(f"Unsupported LLM provider: {provider}")

    @staticmethod
    def create_from_config(config: dict[str, Any]) -> BaseLLMClient:
        """Create LLM client from configuration"""
        provider = LLMProvider(config.get("provider", "openai"))
        api_key = (
            config.get("api_key")
            or os.getenv("OPENAI_API_KEY")
            or os.getenv("ANTHROPIC_API_KEY")
            or os.getenv("OPENROUTER_API_KEY")
        )
        model = config.get("model", "gpt-4")

        if not api_key and provider in [
            LLMProvider.OPENAI,
            LLMProvider.ANTHROPIC,
            LLMProvider.OPENROUTER,
        ]:
            raise PathFrameworkError(f"API key required for {provider.value}")

        return LLMClientFactory.create_client(
            provider=provider,
            api_key=api_key,
            model=model,
            timeout=config.get("timeout", 30),
        )


# Convenience function for getting default client
def get_llm_client(
    provider: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
    phase: int | None = None,
    **kwargs,
) -> BaseLLMClient:
    """
    Get default LLM client with flexible configuration

    Priority order:
    1. Function parameters (highest priority)
    2. Environment variables (including phase-specific models)
    3. Configuration file
    4. Default values (lowest priority)

    Args:
        provider: LLM provider ("openai", "anthropic", "openrouter", "ollama")
        api_key: API key for the provider
        model: Model name/identifier
        phase: PATH Framework phase (1-4) for phase-specific model selection
        **kwargs: Additional configuration options

    Returns:
        Configured LLM client instance

    Environment Variables:
        PATH_LLM_PROVIDER: Default provider
        PATH_LLM_MODEL: Default model for all phases
        PATH_LLM_MODEL_PHASE1: Phase 1 specific model (Architecture)
        PATH_LLM_MODEL_PHASE2: Phase 2 specific model (Development Planning)
        PATH_LLM_MODEL_PHASE3: Phase 3 specific model (Implementation)
        PATH_LLM_MODEL_PHASE4: Phase 4 specific model (Testing/Deployment)
        OPENROUTER_API_KEY: OpenRouter API key
    """

    # Try to use enhanced config if available
    try:
        from .config import get_config

        config_manager = get_config()
        config = config_manager.get_llm_config(
            provider=provider, api_key=api_key, model=model, phase=phase, **kwargs
        )
    except ImportError:
        # Fallback to environment variables if config module not available
        config = _get_fallback_config(provider, api_key, model, phase, **kwargs)

    return LLMClientFactory.create_client(
        provider=LLMProvider(config["provider"]),
        api_key=config["api_key"],
        model=config["model"],
        timeout=config.get("timeout", 30),
    )


def _get_fallback_config(
    provider: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
    phase: int | None = None,
    **kwargs,
) -> dict[str, Any]:
    """Fallback configuration using environment variables only"""

    provider = provider or os.getenv("PATH_LLM_PROVIDER", "openai")
    api_key = (
        api_key
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("ANTHROPIC_API_KEY")
        or os.getenv("OPENROUTER_API_KEY")
    )

    # Phase-specific model selection
    if not model and phase:
        model = os.getenv(f"PATH_LLM_MODEL_PHASE{phase}")

    # Fallback to general model if no phase-specific model
    if not model:
        model = os.getenv("PATH_LLM_MODEL")

    # Provider-specific defaults if still no model
    if not model:
        if provider == "openai":
            model = "gpt-4"
        elif provider == "anthropic":
            model = "claude-3-sonnet-20240229"
        elif provider == "ollama":
            model = "llama2"
            api_key = ""  # Ollama doesn't need API key
        elif provider == "openrouter":
            model = "openai/gpt-4"

    # Special handling for Ollama
    if provider == "ollama":
        api_key = ""

    return {
        "provider": provider,
        "api_key": api_key,
        "model": model,
        "timeout": int(os.getenv("PATH_LLM_TIMEOUT", "30")),
        **kwargs,
    }
