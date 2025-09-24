# PATH Framework UV Quick Start Guide

This document explains how to use UV with the PATH Framework for faster package management and execution.

## Why UV?

UV is a fast Python package manager and project runner that:
- ⚡ **10-100x faster** than pip for package installation
- 🔄 **Better dependency resolution** with conflict detection
- 🎯 **Project isolation** with automatic virtual environments
- 🚀 **Direct script execution** without activation steps

## Installation

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

## Quick Start with PATH Framework

### 1. Environment Setup

```bash
# Set your environment variables
export OPENROUTER_API_KEY="your-openrouter-api-key"
export PATH_LLM_PROVIDER="openrouter"

# Phase-specific models (your configuration)
export PATH_LLM_MODEL_PHASE1="openai/gpt-4"
export PATH_LLM_MODEL_PHASE2="anthropic/claude-3-sonnet"
export PATH_LLM_MODEL_PHASE3="meta-llama/llama-2-70b-chat"  
export PATH_LLM_MODEL_PHASE4="openai/gpt-3.5-turbo"
```

### 2. Install Dependencies

```bash
# Install core PATH Framework dependencies
uv sync

# Install specific LLM providers
uv add openai anthropic aiohttp  # All providers

# Or install selectively
uv add openai          # OpenAI only
uv add anthropic       # Anthropic only
uv add aiohttp         # Ollama only
```

### 3. Run Examples

```bash
# Test phase-specific model configuration
uv run python examples/phase_models_demo.py

# Test OpenRouter integration
uv run python examples/openrouter_example.py

# Run configuration demo
uv run python examples/configuration_demo.py

# Run main LLM demo
uv run python demo_real_llm.py
```

### 4. Development Commands (Updated for Ruff)

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=path_framework --cov-report=html

# Format code with Ruff (replaces Black)
uv run ruff format

# Lint code with Ruff (replaces flake8)
uv run ruff check

# Lint and fix issues
uv run ruff check --fix

# Type checking (if needed)
uv run mypy path_framework/
```

## UV Scripts (Configured in pyproject.toml)

The PATH Framework includes predefined UV scripts for common tasks:

```bash
# LLM Testing Scripts
uv run --script test-llm              # Run LLM-specific tests
uv run --script demo-openrouter       # OpenRouter demo
uv run --script demo-phase-models     # Phase-specific models demo
uv run --script demo-config           # Configuration demo

# Development Scripts (Updated for Ruff)
uv run --script format                # Format code with Ruff
uv run --script lint                  # Lint with Ruff
uv run --script lint-fix              # Lint and fix with Ruff
uv run --script typecheck             # Type check with MyPy (optional)
uv run --script test                  # Run tests
uv run --script test-cov              # Run tests with coverage

# Setup Scripts
./scripts/setup_openrouter.sh         # OpenRouter setup
./scripts/setup_phase_models.sh       # Phase-specific model setup

# Install LLM Providers
uv run --script install-openai        # Install OpenAI
uv run --script install-anthropic     # Install Anthropic
uv run --script install-ollama        # Install Ollama support
uv run --script install-all-llm       # Install all providers
```

## Phase-Specific Model Usage with UV

Your environment variable configuration works perfectly with UV:

```bash
# Your current setup
export OPENROUTER_API_KEY="your-key"
export PATH_LLM_PROVIDER="openrouter"
export PATH_LLM_MODEL_PHASE1="openai/gpt-4"
export PATH_LLM_MODEL_PHASE2="anthropic/claude-3-sonnet" 
export PATH_LLM_MODEL_PHASE3="meta-llama/llama-2-70b-chat"
export PATH_LLM_MODEL_PHASE4="openai/gpt-3.5-turbo"

# Test phase-specific configuration
uv run python -c "
from path_framework.core.llm_client import get_llm_client
for phase in [1,2,3,4]:
    client = get_llm_client(phase=phase)
    print(f'Phase {phase}: {client.model}')
"
```

## UV vs Traditional Python

| Task | Traditional | UV |
|------|-------------|-----|
| **Install deps** | `pip install -r requirements.txt` | `uv sync` |
| **Run script** | `python script.py` | `uv run python script.py` |
| **Add package** | `pip install package` | `uv add package` |
| **Virtual env** | `python -m venv .venv && source .venv/bin/activate` | Automatic |
| **Lock deps** | `pip freeze > requirements.txt` | `uv lock` |

## Advantages for PATH Framework

1. **⚡ Faster Installation**
   ```bash
   # Traditional (slow)
   pip install openai anthropic aiohttp  # 30-60 seconds
   
   # UV (fast)
   uv add openai anthropic aiohttp        # 3-5 seconds
   ```

2. **🔒 Better Dependency Management**
   ```bash
   # UV automatically resolves conflicts
   uv add openai==1.0.0 anthropic==0.25.0
   # Checks compatibility automatically
   ```

3. **🎯 Project Isolation**
   ```bash
   # No need to manage virtual environments manually
   uv run python examples/phase_models_demo.py
   # UV handles isolation automatically
   ```

4. **🚀 Direct Execution**
   ```bash
   # No activation needed
   uv run python -c "from path_framework.core.llm_client import get_llm_client; print('Works!')"
   ```

## Configuration File Integration

UV works seamlessly with your phase-specific environment variables and the PATH Framework configuration system:

```python
# path_framework/core/config.py automatically detects:
# - Environment variables (PATH_LLM_MODEL_PHASE1, etc.)
# - Configuration files
# - Function parameters
# - Fallback defaults

# UV execution respects all configuration sources
uv run python examples/phase_models_demo.py
```

## Best Practices with UV

1. **Always use uv run for scripts**
   ```bash
   # Good
   uv run python script.py
   
   # Avoid (requires manual env management)
   python script.py
   ```

2. **Use uv add for dependencies**
   ```bash
   # Good
   uv add openai anthropic
   
   # Slower
   pip install openai anthropic
   ```

3. **Leverage UV scripts**
   ```bash
   # Defined in pyproject.toml
   uv run --script demo-phase-models
   uv run --script test-llm
   ```

4. **Environment variable inheritance**
   ```bash
   # Your env vars work with UV
   export PATH_LLM_MODEL_PHASE1="openai/gpt-4"
   uv run python examples/phase_models_demo.py  # Uses phase 1 model
   ```

## Troubleshooting

### Common Issues

1. **UV not found**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source ~/.bashrc
   ```

2. **Environment variables not working**
   ```bash
   # Make sure variables are exported
   export OPENROUTER_API_KEY="your-key"
   uv run python -c "import os; print(os.getenv('OPENROUTER_API_KEY'))"
   ```

3. **Dependencies not found**
   ```bash
   # Sync dependencies first
   uv sync
   ```

4. **Script execution fails**
   ```bash
   # Use absolute path or ensure script is executable
   chmod +x scripts/setup_phase_models.sh
   ./scripts/setup_phase_models.sh
   ```

## Migration from pip/conda

```bash
# Old workflow
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python demo_real_llm.py

# New UV workflow  
uv run python demo_real_llm.py  # That's it!
```

UV automatically handles virtual environment creation, dependency installation, and script execution in a single command.

## Your Phase-Specific Setup Works Perfectly!

Your current environment variable configuration is optimal for UV:

```bash
export OPENROUTER_API_KEY="your-key"
export PATH_LLM_PROVIDER="openrouter"
export PATH_LLM_MODEL_PHASE1="openai/gpt-4"           # Best for analysis
export PATH_LLM_MODEL_PHASE2="anthropic/claude-3-sonnet"  # Good for planning  
export PATH_LLM_MODEL_PHASE3="meta-llama/llama-2-70b-chat"  # Fast for coding
export PATH_LLM_MODEL_PHASE4="openai/gpt-3.5-turbo"  # Efficient for testing

# Test your setup
uv run python examples/phase_models_demo.py
```

This configuration provides:
- 🎯 **Optimized model selection** per phase
- 💰 **Cost optimization** (cheaper models where appropriate)
- ⚡ **Performance tuning** (faster models for code generation)
- 🔧 **Easy experimentation** with different models

UV makes your existing configuration even better with faster execution and better dependency management!
