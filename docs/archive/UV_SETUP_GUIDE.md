# PATH Framework - UV Setup Guide

This guide shows how to set up and use the PATH Framework with UV package manager for optimal Python dependency management.

## Prerequisites

1. **Install UV** (if not already installed):
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Via pip
pip install uv

# Via conda
conda install -c conda-forge uv
```

2. **Verify installation**:
```bash
uv --version
```

## Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/precocityresearchlab/path_framework.git
cd path_framework

# Install all dependencies including development tools
uv sync

# Or install only production dependencies
uv sync --no-dev
```

### 2. Verify Installation
```bash
# Run tests to verify everything works
uv run pytest

# Check PATH Framework CLI
uv run path --help

# List available agents
uv run path agents list
```

### 3. Create Your First Project
```bash
# Initialize a new PATH Framework project
uv run path init my-awesome-project --template api

# Navigate to the project
cd my-awesome-project

# Install project dependencies
uv sync

# Start development
uv run path run --phase 1
```

## UV Usage Patterns

### Development Workflow

```bash
# Install development dependencies
make install-dev
# or
uv sync

# Run tests
make test
# or
uv run pytest

# Format code
make format
# or
uv run black path_framework tests
uv run isort path_framework tests

# Type checking
make type-check
# or
uv run mypy path_framework

# Complete development setup
make dev-setup
```

### Dependency Management

```bash
# Add a new dependency
uv add requests

# Add a development dependency
uv add --dev pytest-mock

# Add optional dependency group
uv add --optional llm openai anthropic

# Update all dependencies
uv sync --upgrade

# Show dependency tree
uv tree

# Show outdated packages
uv pip list --outdated
```

### Virtual Environment Management

```bash
# UV automatically manages virtual environments
# but you can also manage them manually:

# Create a new virtual environment
uv venv

# Activate virtual environment (if needed)
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies in specific environment
uv pip install -r requirements.txt

# Python version management
uv python install 3.11
uv python install 3.12
uv python list
```

### Running Commands

```bash
# Run PATH Framework CLI
uv run path --help

# Run specific agent
uv run path agents status

# Run tests with specific Python version
uv run --python 3.11 pytest

# Run with environment variables
uv run --env OPENAI_API_KEY=sk-... path run

# Run example project
cd examples/task_management_api
uv run python run_full_cycle.py
```

## Advanced UV Features

### Lock File Management

```bash
# Generate lock file (uv.lock)
uv lock

# Sync from lock file (exact versions)
uv sync --frozen

# Update lock file
uv lock --upgrade

# Check for security vulnerabilities
uv audit
```

### Multiple Python Versions

```bash
# Install specific Python versions
uv python install 3.10 3.11 3.12

# Use specific version for project
uv python pin 3.11

# Run tests on multiple versions
uv run --python 3.10 pytest
uv run --python 3.11 pytest
uv run --python 3.12 pytest
```

### Environment Variables and Configuration

```bash
# Set environment variables for UV
export UV_CACHE_DIR=/path/to/cache
export UV_PYTHON_PREFERENCE=only-managed

# Use configuration file (.uvrc)
echo "python-preference = 'only-managed'" > .uvrc
echo "resolution = 'highest'" >> .uvrc
```

### Publishing and Building

```bash
# Build distribution packages
uv build

# Publish to PyPI
uv publish

# Publish to Test PyPI
uv publish --repository testpypi

# Build specific formats
uv build --wheel
uv build --sdist
```

## Project Structure with UV

```
path_framework/
├── pyproject.toml          # Main project configuration
├── uv.toml                 # UV-specific configuration
├── uv.lock                 # Lock file (auto-generated)
├── Makefile                # Build automation
├── path_framework/         # Source code
├── tests/                  # Test suite
├── examples/               # Example projects
├── docs/                   # Documentation
└── .venv/                  # Virtual environment (auto-created)
```

## Environment-Specific Setups

### Development Environment
```bash
# Complete development setup
make dev-setup

# Or manually:
uv sync
uv run pre-commit install
make docs
```

### Production Environment
```bash
# Install only production dependencies
uv sync --no-dev --frozen

# Or using specific group
uv sync --only-group prod
```

### CI/CD Environment
```bash
# Fast, reproducible CI setup
uv sync --frozen --no-dev
uv run pytest --junitxml=results.xml
```

### Docker Environment
```dockerfile
# Dockerfile example
FROM python:3.11-slim

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY path_framework ./path_framework

# Run application
CMD ["uv", "run", "path", "run"]
```

## Integration with IDEs

### VS Code

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.terminal.activateEnvironment": false,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black"
}
```

### PyCharm
1. Open project
2. Go to Settings → Project → Python Interpreter
3. Select "Add Interpreter" → "Existing environment"
4. Point to `.venv/bin/python`

## Troubleshooting

### Common Issues

1. **UV not found**:
```bash
# Add UV to PATH
export PATH="$HOME/.cargo/bin:$PATH"
```

2. **Python version conflicts**:
```bash
# Use specific Python version
uv python pin 3.11
uv sync
```

3. **Dependency conflicts**:
```bash
# Clear cache and reinstall
uv cache clean
uv sync --refresh
```

4. **Lock file issues**:
```bash
# Regenerate lock file
rm uv.lock
uv lock
uv sync
```

### Performance Tips

1. **Use lock files** for reproducible builds
2. **Enable parallel installs** (default in UV)
3. **Use dependency groups** for different environments
4. **Cache dependencies** for faster CI/CD

### Getting Help

```bash
# UV help
uv --help
uv sync --help

# PATH Framework help
uv run path --help
uv run path agents --help

# Community support
# - GitHub Issues: https://github.com/precocityresearchlab/path_framework/issues
# - Documentation: https://path-framework.readthedocs.io/
```

## Comparison with Other Tools

| Feature | UV | pip + venv | Poetry | Pipenv |
|---------|----|-----------:|--------:|--------:|
| Speed | ⚡⚡⚡ | ⚡ | ⚡⚡ | ⚡ |
| Lock files | ✅ | ❌ | ✅ | ✅ |
| Dependency resolution | ✅ | ❌ | ✅ | ✅ |
| Python version management | ✅ | ❌ | ❌ | ✅ |
| Built in Rust | ✅ | ❌ | ❌ | ❌ |
| PEP 621 support | ✅ | ❌ | ✅ | ❌ |

## Best Practices

1. **Always use lock files** in production
2. **Pin Python version** in pyproject.toml
3. **Use dependency groups** for organization
4. **Regular updates** with `uv sync --upgrade`
5. **Cache optimization** for CI/CD pipelines
6. **Environment isolation** for different projects

This setup provides a modern, fast, and reliable Python development experience for the PATH Framework! 🚀
