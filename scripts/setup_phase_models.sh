#!/bin/bash
# PATH Framework Phase-Specific Model Setup for OpenRouter

echo "🎯 PATH Framework - Phase-Specific Model Configuration"
echo "===================================================="

# Function to validate OpenRouter API key
validate_api_key() {
    local api_key="$1"
    if [ ${#api_key} -lt 20 ]; then
        echo "❌ API key seems too short. Please check your OpenRouter API key."
        return 1
    fi
    return 0
}

echo ""
echo "This script will set up your environment variables for:"
echo "• OPENROUTER_API_KEY"
echo "• PATH_LLM_PROVIDER" 
echo "• PATH_LLM_MODEL_PHASE1 (Architecture & Requirements)"
echo "• PATH_LLM_MODEL_PHASE2 (Development Planning)"
echo "• PATH_LLM_MODEL_PHASE3 (Implementation)"
echo "• PATH_LLM_MODEL_PHASE4 (Testing & Deployment)"

# Check if already configured
if [ -n "$OPENROUTER_API_KEY" ]; then
    echo ""
    echo "✅ Current Configuration:"
    echo "   OPENROUTER_API_KEY: ${OPENROUTER_API_KEY:0:8}...${OPENROUTER_API_KEY: -4}"
    echo "   PATH_LLM_PROVIDER: ${PATH_LLM_PROVIDER:-'Not set'}"
    echo "   PATH_LLM_MODEL_PHASE1: ${PATH_LLM_MODEL_PHASE1:-'Not set'}"
    echo "   PATH_LLM_MODEL_PHASE2: ${PATH_LLM_MODEL_PHASE2:-'Not set'}"
    echo "   PATH_LLM_MODEL_PHASE3: ${PATH_LLM_MODEL_PHASE3:-'Not set'}"
    echo "   PATH_LLM_MODEL_PHASE4: ${PATH_LLM_MODEL_PHASE4:-'Not set'}"
    
    echo ""
    read -p "Reconfigure? (y/N): " reconfigure
    if [ "$reconfigure" != "y" ] && [ "$reconfigure" != "Y" ]; then
        echo "Keeping current configuration."
        exit 0
    fi
fi

echo ""
echo "🔑 OpenRouter API Key Setup"
echo "Get your API key from: https://openrouter.ai/keys"

if [ -n "$OPENROUTER_API_KEY" ]; then
    read -p "Enter OpenRouter API key [current: ${OPENROUTER_API_KEY:0:8}...]: " api_key
    api_key=${api_key:-$OPENROUTER_API_KEY}
else
    read -p "Enter OpenRouter API key: " api_key
fi

if ! validate_api_key "$api_key"; then
    exit 1
fi

echo ""
echo "🤖 Phase-Specific Model Configuration"
echo "Choose from OpenRouter's available models:"

# Phase 1: Architecture & Requirements
echo ""
echo "📋 Phase 1 - Architecture & Requirements Analysis"
echo "   Recommended: openai/gpt-4 (best reasoning for complex analysis)"
echo "   Options: openai/gpt-4, anthropic/claude-3-opus, openai/gpt-4-turbo"

read -p "Phase 1 model [openai/gpt-4]: " phase1_model
phase1_model=${phase1_model:-"openai/gpt-4"}

# Phase 2: Development Planning  
echo ""
echo "📊 Phase 2 - Development Planning & Design"
echo "   Recommended: anthropic/claude-3-sonnet (excellent for structured planning)"
echo "   Options: anthropic/claude-3-sonnet, openai/gpt-4, anthropic/claude-3-opus"

read -p "Phase 2 model [anthropic/claude-3-sonnet]: " phase2_model
phase2_model=${phase2_model:-"anthropic/claude-3-sonnet"}

# Phase 3: Implementation
echo ""
echo "💻 Phase 3 - Implementation & Code Generation" 
echo "   Recommended: meta-llama/llama-2-70b-chat (fast and cost-effective for coding)"
echo "   Options: meta-llama/llama-2-70b-chat, openai/gpt-3.5-turbo, anthropic/claude-3-haiku"

read -p "Phase 3 model [meta-llama/llama-2-70b-chat]: " phase3_model
phase3_model=${phase3_model:-"meta-llama/llama-2-70b-chat"}

# Phase 4: Testing & Deployment
echo ""
echo "🧪 Phase 4 - Testing & Deployment"
echo "   Recommended: openai/gpt-3.5-turbo (efficient for test generation)"
echo "   Options: openai/gpt-3.5-turbo, anthropic/claude-3-haiku, google/palm-2-chat-bison"

read -p "Phase 4 model [openai/gpt-3.5-turbo]: " phase4_model
phase4_model=${phase4_model:-"openai/gpt-3.5-turbo"}

echo ""
echo "📋 Configuration Summary:"
echo "   Provider: openrouter"
echo "   API Key: ${api_key:0:8}...${api_key: -4}"
echo "   Phase 1 Model: $phase1_model"
echo "   Phase 2 Model: $phase2_model" 
echo "   Phase 3 Model: $phase3_model"
echo "   Phase 4 Model: $phase4_model"

echo ""
read -p "Apply this configuration? (y/N): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ Configuration cancelled"
    exit 1
fi

echo ""
echo "💾 Applying Configuration..."

# Export for current session
export OPENROUTER_API_KEY="$api_key"
export PATH_LLM_PROVIDER="openrouter"
export PATH_LLM_MODEL_PHASE1="$phase1_model"
export PATH_LLM_MODEL_PHASE2="$phase2_model" 
export PATH_LLM_MODEL_PHASE3="$phase3_model"
export PATH_LLM_MODEL_PHASE4="$phase4_model"

echo "✅ Environment variables set for current session"

# Option to persist to .bashrc
echo ""
read -p "Save to .bashrc for persistence? (y/N): " save_bashrc

if [ "$save_bashrc" = "y" ] || [ "$save_bashrc" = "Y" ]; then
    # Backup .bashrc
    cp ~/.bashrc ~/.bashrc.backup.$(date +%Y%m%d_%H%M%S)
    
    # Remove existing PATH Framework config
    grep -v "PATH_LLM\|OPENROUTER_API_KEY" ~/.bashrc > ~/.bashrc.tmp
    mv ~/.bashrc.tmp ~/.bashrc
    
    # Add new configuration
    echo "" >> ~/.bashrc
    echo "# PATH Framework Phase-Specific Configuration" >> ~/.bashrc
    echo "export OPENROUTER_API_KEY=\"$api_key\"" >> ~/.bashrc
    echo "export PATH_LLM_PROVIDER=\"openrouter\"" >> ~/.bashrc
    echo "export PATH_LLM_MODEL_PHASE1=\"$phase1_model\"" >> ~/.bashrc
    echo "export PATH_LLM_MODEL_PHASE2=\"$phase2_model\"" >> ~/.bashrc
    echo "export PATH_LLM_MODEL_PHASE3=\"$phase3_model\"" >> ~/.bashrc
    echo "export PATH_LLM_MODEL_PHASE4=\"$phase4_model\"" >> ~/.bashrc
    
    echo "✅ Configuration saved to .bashrc"
    echo "💡 Run 'source ~/.bashrc' to apply in new terminals"
fi

# Test configuration
echo ""
echo "🧪 Testing Configuration..."

uv run python -c "
import sys
sys.path.append('.')

try:
    from path_framework.core.llm_client import get_llm_client
    
    # Test each phase
    phases = [1, 2, 3, 4]
    for phase in phases:
        client = get_llm_client(phase=phase)
        print(f'✅ Phase {phase}: {client.model} ({client.__class__.__name__})')
    
    print()
    print('🎯 Phase-specific configuration working correctly!')
    
except Exception as e:
    print(f'❌ Configuration test failed: {e}')
    print('💡 Check your setup and try again')
"

echo ""
echo "🎉 Phase-Specific Model Configuration Complete!"
echo ""
echo "📖 Usage Examples:"
echo "   # Phase 1 (Architecture) - uses $phase1_model"
echo "   uv run python examples/phase_models_demo.py"
echo ""
echo "   # Test phase-specific models"
echo "   uv run python -c \"
echo "   from path_framework.core.llm_client import get_llm_client"
echo "   client1 = get_llm_client(phase=1)  # $phase1_model"
echo "   client3 = get_llm_client(phase=3)  # $phase3_model"
echo "   print(f'Phase 1: {client1.model}');"
echo "   print(f'Phase 3: {client3.model}')"
echo "   \""
echo ""
echo "💰 Cost Optimization Benefits:"
echo "   • Phase 1: Premium model for critical analysis"
echo "   • Phase 2: Balanced model for planning"  
echo "   • Phase 3: Cost-effective model for coding"
echo "   • Phase 4: Efficient model for testing"
