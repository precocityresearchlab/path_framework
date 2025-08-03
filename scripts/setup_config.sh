#!/bin/bash
# PATH Framework Configuration Setup

echo "⚙️  PATH Framework Configuration Setup"
echo "====================================="

# Function to update .bashrc with environment variables
setup_bashrc() {
    local provider="$1"
    local model="$2" 
    local api_key="$3"
    
    echo ""
    echo "📝 Setting up .bashrc configuration..."
    
    # Backup existing .bashrc
    cp ~/.bashrc ~/.bashrc.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backed up .bashrc"
    
    # Remove any existing PATH Framework config
    grep -v "PATH_LLM\|OPENROUTER_API_KEY\|OPENAI_API_KEY\|ANTHROPIC_API_KEY" ~/.bashrc > ~/.bashrc.tmp
    mv ~/.bashrc.tmp ~/.bashrc
    
    # Add new configuration
    echo "" >> ~/.bashrc
    echo "# PATH Framework Configuration" >> ~/.bashrc
    echo "export PATH_LLM_PROVIDER=\"$provider\"" >> ~/.bashrc
    echo "export PATH_LLM_MODEL=\"$model\"" >> ~/.bashrc
    
    if [ "$provider" = "openrouter" ]; then
        echo "export OPENROUTER_API_KEY=\"$api_key\"" >> ~/.bashrc
    elif [ "$provider" = "openai" ]; then
        echo "export OPENAI_API_KEY=\"$api_key\"" >> ~/.bashrc  
    elif [ "$provider" = "anthropic" ]; then
        echo "export ANTHROPIC_API_KEY=\"$api_key\"" >> ~/.bashrc
    fi
    
    echo "✅ Updated .bashrc with PATH Framework configuration"
    echo "💡 Run 'source ~/.bashrc' to apply changes"
}

# Function to create configuration file
create_config_file() {
    local provider="$1"
    local model="$2"
    
    echo ""
    echo "📄 Creating configuration file..."
    
    mkdir -p ~/.path_framework
    
    cat > ~/.path_framework/config.json << EOF
{
  "llm": {
    "provider": "$provider",
    "model": "$model",
    "timeout": 30,
    "temperature": 0.1,
    "max_tokens": 4000
  },
  "agents": {
    "domain_analyst": {
      "confidence_threshold": 0.8
    },
    "system_architect": {
      "technology_preference": "cloud_native"
    }
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  }
}
EOF

    echo "✅ Created config file: ~/.path_framework/config.json"
}

echo ""
echo "Choose your LLM provider:"
echo "1. OpenRouter (recommended - access to 200+ models)"
echo "2. OpenAI (direct)"
echo "3. Anthropic (direct)"
echo "4. Ollama (local)"

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        provider="openrouter"
        echo ""
        echo "OpenRouter Models:"
        echo "• openai/gpt-4"
        echo "• openai/gpt-3.5-turbo"
        echo "• anthropic/claude-3-sonnet"
        echo "• anthropic/claude-3-haiku"
        echo "• meta-llama/llama-2-70b-chat"
        echo "• google/palm-2-chat-bison"
        
        read -p "Enter model [openai/gpt-4]: " model
        model=${model:-"openai/gpt-4"}
        
        read -p "Enter OpenRouter API key: " api_key
        ;;
    2)
        provider="openai"
        read -p "Enter model [gpt-4]: " model
        model=${model:-"gpt-4"}
        
        read -p "Enter OpenAI API key: " api_key
        ;;
    3)
        provider="anthropic"
        read -p "Enter model [claude-3-sonnet-20240229]: " model
        model=${model:-"claude-3-sonnet-20240229"}
        
        read -p "Enter Anthropic API key: " api_key
        ;;
    4)
        provider="ollama"
        echo ""
        echo "Ollama Models (local):"
        echo "• llama2"
        echo "• codellama"
        echo "• mistral"
        
        read -p "Enter model [llama2]: " model
        model=${model:-"llama2"}
        
        echo "Note: Make sure Ollama is running with 'ollama serve'"
        api_key=""
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "📋 Configuration Summary:"
echo "   Provider: $provider"
echo "   Model: $model"
if [ -n "$api_key" ]; then
    echo "   API Key: ${api_key:0:8}...${api_key: -4}"
else
    echo "   API Key: Not required (local)"
fi

echo ""
read -p "Continue with this configuration? (y/N): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ Configuration cancelled"
    exit 1
fi

# Setup methods
echo ""
echo "Choose configuration method:"
echo "1. Environment variables in .bashrc (persistent)"
echo "2. Configuration file only"
echo "3. Both (recommended)"

read -p "Enter choice (1-3): " method

case $method in
    1)
        setup_bashrc "$provider" "$model" "$api_key"
        ;;
    2)
        create_config_file "$provider" "$model"
        if [ -n "$api_key" ]; then
            echo "⚠️  Don't forget to set your API key environment variable:"
            if [ "$provider" = "openrouter" ]; then
                echo "   export OPENROUTER_API_KEY=\"$api_key\""
            elif [ "$provider" = "openai" ]; then
                echo "   export OPENAI_API_KEY=\"$api_key\""
            elif [ "$provider" = "anthropic" ]; then
                echo "   export ANTHROPIC_API_KEY=\"$api_key\""
            fi
        fi
        ;;
    3)
        setup_bashrc "$provider" "$model" "$api_key"
        create_config_file "$provider" "$model"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

# Test configuration
echo ""
echo "🧪 Testing configuration..."

# Export for current session
export PATH_LLM_PROVIDER="$provider"
export PATH_LLM_MODEL="$model"

if [ "$provider" = "openrouter" ] && [ -n "$api_key" ]; then
    export OPENROUTER_API_KEY="$api_key"
elif [ "$provider" = "openai" ] && [ -n "$api_key" ]; then
    export OPENAI_API_KEY="$api_key"
elif [ "$provider" = "anthropic" ] && [ -n "$api_key" ]; then
    export ANTHROPIC_API_KEY="$api_key"
fi

# Test with Python
python3 -c "
import sys
sys.path.append('.')

try:
    from path_framework.core.llm_client import get_llm_client
    client = get_llm_client()
    print('✅ Configuration test passed!')
    print(f'🔧 Provider: {client.__class__.__name__}')
    print(f'🤖 Model: {client.model}')
except Exception as e:
    print(f'❌ Configuration test failed: {e}')
    print('💡 Check your API key and internet connection')
"

echo ""
echo "🎉 PATH Framework Configuration Complete!"
echo ""
echo "📖 Usage Examples:"
echo "   # Use default configuration"
echo "   python3 examples/configuration_demo.py"
echo ""
echo "   # Test OpenRouter specifically"  
echo "   python3 examples/openrouter_example.py"
echo ""
echo "   # Override at runtime"
echo "   python3 -c \"
echo "   from path_framework.core.llm_client import get_llm_client"
echo "   client = get_llm_client(model='anthropic/claude-3-haiku')"
echo "   \""
echo ""
echo "💡 Configuration Priority:"
echo "   1. Function parameters (highest)"
echo "   2. Environment variables"
echo "   3. Configuration file"
echo "   4. Default values (lowest)"
