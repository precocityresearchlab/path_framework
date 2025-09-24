# PATH Framework BaseAgent Usage Examples

This directory contains comprehensive examples showing how to use the PATH Framework BaseAgent with realistic sample data.

## Files

- **`base_agent_usage_example.py`** - Main example demonstrating all BaseAgent capabilities
- **`sample_data.py`** - Comprehensive sample data provider with realistic examples
- **`README.md`** - This documentation file

## Quick Start

```bash
# Navigate to the examples directory
cd examples

# Run the main usage example
python base_agent_usage_example.py
```

## Example Coverage

### 1. File Operations
- Creating configuration files with JSON data
- Writing and reading application settings
- Error handling for invalid file paths

### 2. Code Generation
- Generating data model classes with type hints
- Creating validation methods
- Supporting different programming languages and styles

### 3. Analysis Tools
- Code quality analysis with metrics
- Complexity analysis
- Issue identification and reporting

### 4. Command Execution
- System command execution with parameters
- Timeout handling
- Output capture and processing

## Sample Data Types

The examples use realistic sample data including:

- **User Stories**: Following PATH Framework "As a... I want... So that..." format
- **Configuration Data**: Application settings, database configs, API settings
- **Model Specifications**: Data class definitions with validation rules
- **Test Data**: Users, products, orders for testing scenarios
- **Code Samples**: Functions, classes, and algorithms for analysis

## PATH Framework Rule Compliance

All examples demonstrate proper PATH Framework rule compliance:

- ✅ UTC time tracking for all operations
- ✅ User story validation for code generation operations
- ✅ Human validation gates for critical operations
- ✅ Completion validation with detailed reporting
- ✅ Rule compliance tracking and audit trails

## Running the Examples

### Prerequisites

```bash
# Ensure you're in the project root
cd path_framework

# Install dependencies
uv sync

# Add src to Python path (if needed)
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Execute Examples

```bash
# Run the main example
python examples/base_agent_usage_example.py

# Expected output:
# 🚀 PATH Framework BaseAgent Usage Example
# ==================================================
# ✅ Agent initialized: PATH_DEVELOPMENT
# 📅 Session UTC: 2024-01-16T15:30:45.123456+00:00
# 🔧 Available capabilities: ['file_operations', 'command_execution', 'code_generation', 'analysis_tools']
# ...
```

## Understanding the Output

The example will show:

1. **Agent Initialization**: Agent ID, session UTC timestamp, available capabilities
2. **File Operations**: Creating and writing configuration files
3. **Code Generation**: Generating Python classes from specifications
4. **Analysis Tools**: Analyzing code quality and metrics
5. **Command Execution**: Running system commands with output capture
6. **Rule Compliance**: Final status of all PATH Framework rule compliance checks

## Customizing Examples

### Adding New Sample Data

Edit `sample_data.py` to add new sample data:

```python
@staticmethod
def get_custom_data() -> Dict[str, Any]:
    return {
        "your_data": "here"
    }
```

### Creating New Examples

Follow the pattern in `base_agent_usage_example.py`:

```python
# Create capability request
request = CapabilityRequest(
    request_id="unique_id",
    capability="capability_name",
    method="method_name",
    params={
        "param1": "value1",
        "user_story": sample_user_story  # Required for code generation
    }
)

# Execute with error handling
try:
    response = await agent.execute_capability(request)
    print(f"✅ Result: {response.status}")
except Exception as e:
    print(f"❌ Failed: {e}")
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `src` is in Python path
2. **Missing Dependencies**: Run `uv sync` to install all dependencies
3. **Permission Errors**: Check file system permissions for `/tmp` directory
4. **Command Not Found**: Some command examples may not work on all systems

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Next Steps

After running these examples:

1. **Explore Agent Profiles**: Look at different agent profiles in `src/profiles/`
2. **Create Custom Capabilities**: Implement your own capabilities following the interface
3. **Build Applications**: Use BaseAgent as foundation for your PATH Framework applications
4. **Study Rule Compliance**: Review how examples follow PATH Framework rules

## Support

For questions or issues:

1. Check the main PATH Framework documentation
2. Review the rule files in `.amazonq/rules/`
3. Look at test files for additional usage patterns
4. Create issues in the project repository