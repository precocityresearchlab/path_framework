#!/bin/bash
# PATH Framework OpenRouter Setup Script

echo "🌐 PATH Framework - OpenRouter Configuration Setup"
echo "=================================================="

# Check if OpenRouter API key is already set
if [ -n "$OPENROUTER_API_KEY" ]; then
    echo "✅ OPENROUTER_API_KEY is already set"
    echo "🔑 Key: ${OPENROUTER_API_KEY:0:8}...${OPENROUTER_API_KEY: -8}"
else
    echo "❌ OPENROUTER_API_KEY is not set"
    echo ""
    echo "To get started with OpenRouter:"
    echo "1. Visit https://openrouter.ai/keys"
    echo "2. Sign up and create an API key"
    echo "3. Set your API key:"
    echo "   export OPENROUTER_API_KEY='your-api-key-here'"
    echo ""
    read -p "Enter your OpenRouter API key: " api_key
    
    if [ -n "$api_key" ]; then
        export OPENROUTER_API_KEY="$api_key"
        echo "✅ API key set for this session"
        echo ""
        echo "To make it permanent, add to your ~/.bashrc:"
        echo "echo 'export OPENROUTER_API_KEY=\"$api_key\"' >> ~/.bashrc"
    else
        echo "❌ No API key provided"
        exit 1
    fi
fi

# Set PATH Framework to use OpenRouter by default
export PATH_LLM_PROVIDER="openrouter"
export PATH_LLM_MODEL="openai/gpt-4"

echo ""
echo "🔧 PATH Framework Configuration:"
echo "   Provider: $PATH_LLM_PROVIDER"
echo "   Model: $PATH_LLM_MODEL"
echo ""

# Test connectivity
echo "🧪 Testing OpenRouter connectivity..."
uv run python -c "
import asyncio
import os
import sys
sys.path.append('.')

from path_framework.core.llm_client import get_llm_client, LLMRequest

async def test():
    try:
        client = get_llm_client()
        request = LLMRequest(
            prompt='Say Hello from PATH Framework via OpenRouter',
            temperature=0.1,
            max_tokens=50
        )
        response = await client.generate(request)
        print('✅ Connection successful!')
        print(f'Response: {response.content}')
        print(f'Model: {response.model_used}')
        print(f'Provider: {response.provider}')
    except Exception as e:
        print(f'❌ Connection failed: {e}')

asyncio.run(test())
"

echo ""
echo "🎉 OpenRouter setup complete!"
echo ""
echo "Available OpenRouter models include:"
echo "  • openai/gpt-4, openai/gpt-3.5-turbo"
echo "  • anthropic/claude-3-sonnet, anthropic/claude-3-haiku" 
echo "  • meta-llama/llama-2-70b-chat"
echo "  • google/palm-2-chat-bison"
echo "  • And 200+ more models!"
echo ""
echo "To test with examples:"
echo "  uv run python examples/openrouter_example.py"
echo "  uv run python demo_real_llm.py"
echo ""
echo "To change models:"
echo "  export PATH_LLM_MODEL='anthropic/claude-3-sonnet'"
echo "  export PATH_LLM_MODEL='meta-llama/llama-2-70b-chat'"
