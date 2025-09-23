"""LLM interface for PATH Framework agents."""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import logging
import os
from .llm_adapters import LLMAdapterFactory, LLMAdapter


class LLMInterface(ABC):
    """Abstract interface for LLM providers."""
    
    @abstractmethod
    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate response from LLM."""
        pass
    
    @abstractmethod
    async def analyze_text(self, text: str, analysis_type: str) -> Dict[str, Any]:
        """Analyze text using LLM."""
        pass


class OpenAIInterface(LLMInterface):
    """OpenAI GPT interface."""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.logger = logging.getLogger("OpenAIInterface")
    
    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate response using OpenAI API."""
        # Implementation would use OpenAI client
        self.logger.info(f"Generating response with {self.model}")
        return f"Generated response for: {prompt[:50]}..."
    
    async def analyze_text(self, text: str, analysis_type: str) -> Dict[str, Any]:
        """Analyze text using OpenAI."""
        self.logger.info(f"Analyzing text: {analysis_type}")
        return {"analysis_type": analysis_type, "result": "analysis_result"}


class AnthropicInterface(LLMInterface):
    """Anthropic Claude interface."""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet"):
        self.api_key = api_key
        self.model = model
        self.logger = logging.getLogger("AnthropicInterface")
    
    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate response using Anthropic API."""
        self.logger.info(f"Generating response with {self.model}")
        return f"Generated response for: {prompt[:50]}..."
    
    async def analyze_text(self, text: str, analysis_type: str) -> Dict[str, Any]:
        """Analyze text using Claude."""
        self.logger.info(f"Analyzing text: {analysis_type}")
        return {"analysis_type": analysis_type, "result": "analysis_result"}


class LLMFactory:
    """Factory for creating LLM interfaces."""
    
    @staticmethod
    def create_llm(provider: str, **kwargs) -> LLMInterface:
        """Create LLM interface based on provider."""
        if provider.lower() == "openai":
            return OpenAIInterface(**kwargs)
        elif provider.lower() == "anthropic":
            return AnthropicInterface(**kwargs)
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")


class UnifiedLLMInterface:
    """Single LLM interface for all PATH Framework agents."""
    
    def __init__(self, provider: Optional[str] = None, **kwargs):
        # Get provider from environment or default to openai
        provider = provider or os.getenv("LLM_PROVIDER", "openai")
        
        self.adapter = LLMAdapterFactory.create_adapter(provider, **kwargs)
        self.logger = logging.getLogger("UnifiedLLM")
        self.logger.info(f"Initialized with {self.adapter.get_provider_name()} adapter")
    
    async def process_agent_request(self, agent_code: str, operation: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process any agent request using appropriate LLM prompts."""
        
        if agent_code == "DA":
            return await self._handle_domain_analyst(operation, payload)
        elif agent_code == "SA":
            return await self._handle_system_architect(operation, payload)
        elif agent_code == "TS":
            return await self._handle_test_strategist(operation, payload)
        elif agent_code == "PA":
            return await self._handle_pipeline_architect(operation, payload)
        else:
            return await self._handle_generic_request(agent_code, operation, payload)
    
    async def _handle_domain_analyst(self, operation: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Domain Analyst operations."""
        if operation == "analyze_user_story":
            prompt = f"Analyze user story: {payload.get('user_story', '')}. Extract: user type, functionality, benefit, entities, rules, edge cases"
        else:
            prompt = f"Domain analysis for {operation}: {payload}"
        
        response = await self.adapter.generate_response(prompt)
        return {"llm_result": response}
    
    async def _handle_system_architect(self, operation: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle System Architect operations."""
        if operation == "generate_architecture":
            prompt = f"Generate 3 architecture options for: {payload.get('requirements', '')}. Include patterns, components, trade-offs, scalability"
        else:
            prompt = f"Architecture design for {operation}: {payload}"
        
        response = await self.adapter.generate_response(prompt)
        return {"llm_result": response}
    
    async def _handle_test_strategist(self, operation: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Test Strategist operations."""
        if operation == "generate_tests":
            prompt = f"Generate tests for: {payload.get('acceptance_criteria', '')}. Include BDD scenarios, unit tests, edge cases"
        else:
            prompt = f"Test strategy for {operation}: {payload}"
        
        response = await self.adapter.generate_response(prompt)
        return {"llm_result": response}
    
    async def _handle_pipeline_architect(self, operation: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Pipeline Architect operations."""
        if operation == "design_pipeline":
            prompt = f"Design CI/CD pipeline for: {payload.get('code_and_tests', '')}. Include quality gates, deployment strategies"
        else:
            prompt = f"Pipeline design for {operation}: {payload}"
        
        response = await self.adapter.generate_response(prompt)
        return {"llm_result": response}
    
    async def _handle_generic_request(self, agent_code: str, operation: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generic agent requests."""
        prompt = f"Agent {agent_code} operation {operation}: {payload}"
        response = await self.adapter.generate_response(prompt)
        return {"llm_result": response}