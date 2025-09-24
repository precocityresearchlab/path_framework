# PATH Framework LLM Integration Guide

## Overview

The PATH Framework provides a unified LLM integration layer supporting multiple providers:
- **OpenAI** (GPT-4, GPT-3.5-turbo)
- **Anthropic** (Claude-3-sonnet, Claude-3-haiku)
- **OpenRouter** (Access to 200+ models including GPT-4, Claude, Llama, etc.)
- **Ollama** (Local LLMs like Llama2, CodeLlama)

## Quick Start

### 1. Set Up API Keys

```bash
# For OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# For Anthropic
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# For OpenRouter (recommended for multiple models)
export OPENROUTER_API_KEY="your-openrouter-api-key"

# For default provider selection
export PATH_LLM_PROVIDER="openrouter"  # or "openai" or "anthropic" or "ollama"
export PATH_LLM_MODEL="openai/gpt-4"   # OpenRouter model format: provider/model
```

### 2. Basic Usage

```python
import asyncio
from path_framework.core.llm_client import get_llm_client, LLMRequest

async def basic_example():
    # Get default client (uses environment variables)
    llm_client = get_llm_client()
    
    # Create a request
    request = LLMRequest(
        prompt="Explain microservices architecture in 3 key points",
        system_prompt="You are an expert software architect",
        temperature=0.1,
        max_tokens=500
    )
    
    # Generate response
    response = await llm_client.generate(request)
    
    print(f"Response: {response.content}")
    print(f"Tokens used: {response.tokens_used}")
    print(f"Model: {response.model_used}")
    print(f"Provider: {response.provider}")

# Run the example
asyncio.run(basic_example())
```

## Provider-Specific Configuration

### OpenAI Configuration

```python
from path_framework.core.llm_client import LLMClientFactory, LLMProvider

# Direct OpenAI client creation
openai_client = LLMClientFactory.create_client(
    provider=LLMProvider.OPENAI,
    api_key="your-openai-key",
    model="gpt-4",
    timeout=30
)

# Or using get_llm_client with explicit parameters
from path_framework.core.llm_client import get_llm_client

openai_client = get_llm_client(
    provider="openai",
    api_key="your-openai-key", 
    model="gpt-4"
)
```

### OpenRouter Configuration (Recommended)

OpenRouter provides access to 200+ AI models through a single API, including GPT-4, Claude, Llama, and many others.

```python
# Direct OpenRouter client creation
from path_framework.core.llm_client import LLMClientFactory, LLMProvider

openrouter_client = LLMClientFactory.create_client(
    provider=LLMProvider.OPENROUTER,
    api_key="your-openrouter-key",
    model="openai/gpt-4",  # Model format: provider/model
    timeout=30
)

# Available models include:
# - openai/gpt-4, openai/gpt-3.5-turbo
# - anthropic/claude-3-sonnet, anthropic/claude-3-haiku
# - meta-llama/llama-2-70b-chat
# - google/palm-2-chat-bison
# - And 200+ more...

# Or using environment variables
import os
os.environ["OPENROUTER_API_KEY"] = "your-openrouter-key"
os.environ["PATH_LLM_PROVIDER"] = "openrouter"
os.environ["PATH_LLM_MODEL"] = "anthropic/claude-3-sonnet"

openrouter_client = get_llm_client()
```

### Anthropic Configuration

```python
# Direct Anthropic client creation
anthropic_client = LLMClientFactory.create_client(
    provider=LLMProvider.ANTHROPIC,
    api_key="your-anthropic-key",
    model="claude-3-sonnet-20240229",
    timeout=30
)

# Or using environment variables
import os
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"

anthropic_client = get_llm_client(
    provider="anthropic",
    model="claude-3-sonnet-20240229"
)
```

### Ollama Configuration (Local LLMs)

```python
# First, start Ollama server locally
# ollama serve

# Then create Ollama client (no API key needed)
ollama_client = LLMClientFactory.create_client(
    provider=LLMProvider.OLLAMA,
    api_key="",  # Not needed for Ollama
    model="llama2",
    base_url="http://localhost:11434",  # Default Ollama port
    timeout=60  # Longer timeout for local processing
)

# Or using get_llm_client
ollama_client = get_llm_client(
    provider="ollama",
    model="llama2"
)
```

## Advanced Usage Examples

### 1. Structured JSON Generation

```python
async def structured_example():
    llm_client = get_llm_client()
    
    # Define JSON schema
    schema = {
        "type": "object",
        "properties": {
            "requirements": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                        "description": {"type": "string"}
                    }
                }
            }
        }
    }
    
    request = LLMRequest(
        prompt="Extract requirements for a simple todo app",
        system_prompt="You are a business analyst extracting software requirements",
        temperature=0.1,
        max_tokens=1000
    )
    
    # Generate structured response
    result = await llm_client.generate_structured(request, schema)
    
    print("Structured result:", result)
    # Returns parsed JSON matching the schema
```

### 2. Configuration-Based Client Creation

```python
from path_framework.core.llm_client import LLMClientFactory

# Create client from configuration dictionary
config = {
    "provider": "openai",
    "api_key": "your-api-key",
    "model": "gpt-4",
    "timeout": 30
}

client = LLMClientFactory.create_from_config(config)
```

### 3. Multi-Provider Comparison

```python
async def compare_providers():
    providers = [
        {"provider": "openai", "model": "gpt-4"},
        {"provider": "anthropic", "model": "claude-3-sonnet-20240229"},
        {"provider": "openrouter", "model": "openai/gpt-4"},
        {"provider": "openrouter", "model": "anthropic/claude-3-sonnet"},
        {"provider": "openrouter", "model": "meta-llama/llama-2-70b-chat"},
        {"provider": "ollama", "model": "llama2"}
    ]
    
    prompt = "Explain the benefits of microservices architecture"
    
    for provider_config in providers:
        try:
            client = get_llm_client(**provider_config)
            request = LLMRequest(prompt=prompt, temperature=0.1)
            response = await client.generate(request)
            
            print(f"\n{provider_config['provider'].upper()} ({provider_config['model']}):")
            print(f"Response: {response.content[:200]}...")
            print(f"Tokens: {response.tokens_used}")
            
        except Exception as e:
            print(f"Error with {provider_config['provider']}: {e}")
```

## Integration with PATH Framework Agents

### Using LLM Integration in Custom Agents

```python
from path_framework.agents_base import BaseAgent
from path_framework.core.llm_client import get_llm_client, LLMRequest

class CustomAnalysisAgent(BaseAgent):
    def __init__(self, config=None):
        super().__init__(
            agent_id="custom_analyst",
            name="Custom Analysis Agent",
            specialization="Custom analysis tasks",
            decision_authority="autonomous",
            phase=1,
            config=config
        )
        
        # Initialize LLM client
        self.llm_client = get_llm_client()
    
    async def execute(self, task):
        """Execute analysis task using LLM"""
        
        system_prompt = """You are an expert analyst specializing in requirement analysis.
        Provide detailed, actionable insights based on the input provided."""
        
        request = LLMRequest(
            prompt=task.get("input_text", ""),
            system_prompt=system_prompt,
            temperature=0.1,
            max_tokens=2000
        )
        
        response = await self.llm_client.generate(request)
        
        return {
            "agent_id": self.agent_id,
            "analysis_result": response.content,
            "confidence_score": 0.85,
            "tokens_used": response.tokens_used,
            "model_used": response.model_used
        }
    
    def validate_output(self, output):
        """Validate agent output"""
        required_fields = ["agent_id", "analysis_result", "confidence_score"]
        return all(field in output for field in required_fields)
```

## Error Handling and Best Practices

### 1. Error Handling

```python
from path_framework.exceptions import PathFrameworkError

async def robust_llm_call():
    try:
        llm_client = get_llm_client()
        request = LLMRequest(prompt="Your prompt here")
        response = await llm_client.generate(request)
        return response
        
    except PathFrameworkError as e:
        print(f"PATH Framework error: {e}")
        # Handle framework-specific errors
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        # Handle other errors
```

### 2. Best Practices

```python
# Good: Use appropriate temperature settings
request = LLMRequest(
    prompt="Extract structured data from this text",
    temperature=0.1,  # Low temperature for structured tasks
    max_tokens=2000
)

# Good: Use system prompts for role-based instructions
request = LLMRequest(
    prompt="Analyze this architecture design",
    system_prompt="You are an expert software architect with 15 years of experience",
    temperature=0.2
)

# Good: Use structured generation for JSON responses
schema = {"type": "object", "properties": {"key": {"type": "string"}}}
result = await client.generate_structured(request, schema)

# Good: Handle token limits appropriately
request = LLMRequest(
    prompt="Very long prompt...",
    max_tokens=4000,  # Adjust based on expected response length
    temperature=0.1
)
```

## Environment Configuration

### Development Environment

```bash
# .env file
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
OPENROUTER_API_KEY=your-openrouter-key
PATH_LLM_PROVIDER=openrouter
PATH_LLM_MODEL=openai/gpt-4
```

### Production Environment

```bash
# Production settings with OpenRouter
export OPENROUTER_API_KEY="prod-openrouter-key"
export PATH_LLM_PROVIDER="openrouter"
export PATH_LLM_MODEL="openai/gpt-4"
export PATH_LLM_TIMEOUT=60

# Or direct OpenAI
export OPENAI_API_KEY="prod-openai-key"
export PATH_LLM_PROVIDER="openai"
export PATH_LLM_MODEL="gpt-4"
export PATH_LLM_TIMEOUT=60
```

### Local Development with Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull a model
ollama pull llama2

# Configure PATH to use Ollama
export PATH_LLM_PROVIDER=ollama
export PATH_LLM_MODEL=llama2
```

## Testing LLM Integration

### Basic Connectivity Test

```python
import asyncio
from path_framework.core.llm_client import get_llm_client, LLMRequest

async def test_connectivity():
    """Test basic LLM connectivity"""
    try:
        client = get_llm_client()
        
        test_request = LLMRequest(
            prompt="Respond with 'Connection successful' to confirm API connectivity",
            temperature=0.1,
            max_tokens=20
        )
        
        response = await client.generate(test_request)
        
        print("✅ LLM Connection Test Passed")
        print(f"Provider: {response.provider}")
        print(f"Model: {response.model_used}")
        print(f"Response: {response.content}")
        print(f"Tokens: {response.tokens_used}")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM Connection Test Failed: {e}")
        return False

# Run connectivity test
asyncio.run(test_connectivity())
```

## Troubleshooting

### Common Issues

1. **Missing API Keys**
   ```
   Error: PathFrameworkError: API key required for openai
   Solution: Set OPENAI_API_KEY environment variable
   ```

2. **Provider Not Found**
   ```
   Error: PathFrameworkError: Unsupported LLM provider: unknown
   Solution: Use 'openai', 'anthropic', or 'ollama'
   ```

3. **Ollama Connection Failed**
   ```
   Error: Ollama API error: 11434
   Solution: Start Ollama server with 'ollama serve'
   ```

4. **JSON Parsing Error**
   ```
   Error: Invalid JSON response from LLM
   Solution: Adjust prompt or use lower temperature for structured responses
   ```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("path.llm")

# Now run your LLM calls to see detailed logs
```

This guide covers all the essential aspects of using the PATH Framework's LLM integration. The system is designed to be flexible, supporting multiple providers while maintaining a consistent interface for all AI agents in the framework.
