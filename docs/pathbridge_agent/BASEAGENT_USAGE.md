# PATH Framework BaseAgent Usage Guide

This guide shows how to use the PATH Framework BaseAgent with sample data, following PATH Framework rule compliance requirements.

## Quick Start

```python
import asyncio
from src.core.base_agent import BaseAgent
from src.core.capability_interface import CapabilityRequest

# Initialize agent
agent = BaseAgent("development")

# Create and execute capability request
request = CapabilityRequest(
    request_id="example_001",
    capability="file_operations",
    method="write",
    params={
        "path": "/tmp/example.txt",
        "content": "Hello PATH Framework!"
    }
)

response = await agent.execute_capability(request)
print(f"Status: {response.status}")
```

## Core Concepts

### 1. BaseAgent Initialization

```python
# Initialize with profile name
agent = BaseAgent("development")

# Agent provides:
print(f"Agent ID: {agent.agent_id}")                    # PATH_DEVELOPMENT
print(f"Session UTC: {agent.session_utc}")              # 2024-01-16T15:30:45+00:00
print(f"Capabilities: {agent.list_capabilities()}")     # ['file_operations', ...]
```

### 2. Available Capabilities

The BaseAgent comes with four standard capabilities:

#### File Operations
- **Methods**: `read`, `write`, `create_directory`, `delete`, `list`, `move`, `copy`
- **Example**:
```python
request = CapabilityRequest(
    request_id="file_001",
    capability="file_operations",
    method="write",
    params={
        "path": "/tmp/config.json",
        "content": '{"app": "PATH Framework", "version": "1.0.0"}'
    }
)
```

#### Command Execution
- **Methods**: `execute`, `execute_async`, `stream_output`, `terminate`, `get_exit_code`
- **Example**:
```python
request = CapabilityRequest(
    request_id="cmd_001",
    capability="command_execution",
    method="execute",
    params={
        "command": "python --version"
    }
)
```

#### Code Generation
- **Methods**: `generate_source`, `generate_config`, `generate_docs`, `apply_templates`, `format_code`
- **Example**:
```python
request = CapabilityRequest(
    request_id="code_001",
    capability="code_generation",
    method="generate_source",
    params={
        "language": "python",
        "content": "class Example:\n    pass",
        "path": "/tmp/example.py",
        "user_story": {
            "format": "As a developer, I want to generate code, so that I can automate development"
        }
    }
)
```

#### Analysis Tools
- **Methods**: `static_analysis`, `parse_codebase`, `validate_config`, `assess_metrics`, `dependency_analysis`
- **Example**:
```python
request = CapabilityRequest(
    request_id="analysis_001",
    capability="analysis_tools",
    method="static_analysis",
    params={
        "path": "/path/to/code",
        "language": "python"
    }
)
```

### 3. PATH Framework Rule Compliance

The BaseAgent enforces PATH Framework rules automatically:

#### Mandatory Validation Gates

1. **GATE 1: Rule Loading Validation**
   - Ensures all capabilities are properly registered
   - Validates capability interface compliance

2. **GATE 2: UTC Time Validation**
   - Records session UTC timestamp
   - Tracks execution start/end times

3. **GATE 3: User Story Validation**
   - Required for code generation operations
   - Must follow "As a... I want... So that..." format

4. **GATE 4: Human Validation**
   - Required for critical operations
   - Auto-approved for demo purposes

5. **GATE 5: Completion Validation**
   - Records completion metadata
   - Updates rule compliance tracking

#### Rule Compliance Tracking

```python
# Check compliance status
for rule, status in agent.rule_compliance.items():
    print(f"{rule}: {status}")

# Output:
# tests_first: False
# story_ready: False  
# utc_tracking: True
# human_validation: False
# completion_format: True
# metadata_updated: True
# quality_gates: False
```

## Sample Data Examples

### User Data Example

```python
# Sample user data
user_data = {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "age": 28,
    "is_active": True,
    "created_at": "2024-01-16T15:30:00Z"
}

# Save to file
request = CapabilityRequest(
    request_id="user_001",
    capability="file_operations",
    method="write",
    params={
        "path": "/tmp/user.json",
        "content": json.dumps(user_data, indent=2)
    }
)

response = await agent.execute_capability(request)
```

### Configuration Example

```python
# Application configuration
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp"
    },
    "api": {
        "host": "0.0.0.0",
        "port": 8000,
        "debug": True
    },
    "features": {
        "logging": True,
        "monitoring": True,
        "caching": False
    }
}

# Generate config file
request = CapabilityRequest(
    request_id="config_001",
    capability="file_operations",
    method="write",
    params={
        "path": "/tmp/app_config.json",
        "content": json.dumps(config, indent=2)
    }
)
```

### Code Generation Example

```python
# Generate a data model class
user_story = {
    "format": "As a developer, I want to generate a User model class, so that I can represent user data consistently"
}

class_code = '''
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    email: str
    age: Optional[int] = None
    is_active: bool = True
    created_at: datetime = None
    
    def validate(self) -> bool:
        return "@" in self.email and len(self.username) >= 3
'''

request = CapabilityRequest(
    request_id="model_001",
    capability="code_generation",
    method="generate_source",
    params={
        "language": "python",
        "content": class_code,
        "path": "/tmp/user_model.py",
        "user_story": user_story
    }
)
```

## Error Handling

```python
try:
    response = await agent.execute_capability(request)
    
    if response.status == CapabilityStatus.SUCCESS:
        print("✅ Success:", response.result)
    else:
        print("❌ Error:", response.result.get("error"))
        
except Exception as e:
    print(f"❌ Exception: {e}")
```

## Response Format

All capability executions return a `CapabilityResponse`:

```python
@dataclass
class CapabilityResponse:
    request_id: str                    # Original request ID
    status: CapabilityStatus          # SUCCESS, ERROR, or TIMEOUT
    result: Dict[str, Any]            # Operation results
    metadata: Dict[str, Any]          # Execution metadata
    execution_time: float             # Execution time in seconds
```

Example response:
```python
CapabilityResponse(
    request_id="file_001",
    status=CapabilityStatus.SUCCESS,
    result={"success": True},
    metadata={
        "agent_id": "PATH_DEVELOPMENT",
        "capability": "file_operations", 
        "start_utc": "2024-01-16T15:30:45.123456+00:00",
        "end_utc": "2024-01-16T15:30:45.234567+00:00",
        "duration_seconds": 0.111111
    },
    execution_time=0.111
)
```

## Running the Examples

### Prerequisites

```bash
# Install dependencies
uv sync

# Ensure you're in the project root
cd path_framework
```

### Run Examples

```bash
# Simple usage guide
uv run python examples/simple_usage_guide.py

# Comprehensive example with all capabilities
uv run python examples/base_agent_usage_example.py
```

### Expected Output

```
🚀 PATH Framework BaseAgent Usage Example
==================================================
✅ Agent initialized: PATH_DEVELOPMENT
📅 Session UTC: 2024-01-16T15:30:45.123456+00:00
🔧 Available capabilities: ['file_operations', 'command_execution', 'code_generation', 'analysis_tools']

📁 Example 1: File Operations
------------------------------
✅ File operation result: CapabilityStatus.SUCCESS
📊 Metadata: {'agent_id': 'PATH_DEVELOPMENT', 'capability': 'file_operations', ...}

💻 Example 2: Code Generation
------------------------------
✅ Code generation result: CapabilityStatus.SUCCESS
📝 Generated code preview: ...

🔍 Example 3: Analysis Tools
------------------------------
✅ Analysis result: CapabilityStatus.SUCCESS
📊 Code metrics: {'lines': 0, 'complexity': 0}

⚡ Example 4: Command Execution
------------------------------
✅ Command 'echo': CapabilityStatus.SUCCESS
   Output: Hello from PATH Framework!

📋 PATH Framework Rule Compliance Status
----------------------------------------
✅ utc_tracking: True
✅ completion_format: True
✅ metadata_updated: True
❌ tests_first: False
❌ story_ready: False
❌ human_validation: False
❌ quality_gates: False

🎯 Example completed successfully!
```

## Best Practices

### 1. Always Use User Stories for Code Generation

```python
# ✅ Good - includes user story
user_story = {
    "format": "As a developer, I want to generate a config parser, so that I can handle application settings"
}

request = CapabilityRequest(
    capability="code_generation",
    method="generate_source",
    params={
        "user_story": user_story,
        # ... other params
    }
)
```

### 2. Handle Errors Gracefully

```python
# ✅ Good - proper error handling
try:
    response = await agent.execute_capability(request)
    if response.status == CapabilityStatus.SUCCESS:
        return response.result
    else:
        logger.error(f"Capability failed: {response.result.get('error')}")
        return None
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return None
```

### 3. Use Descriptive Request IDs

```python
# ✅ Good - descriptive IDs
request_id = f"user_data_save_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# ❌ Bad - generic IDs
request_id = "req_001"
```

### 4. Validate Parameters

```python
# ✅ Good - validate before sending
def create_file_request(path: str, content: str) -> CapabilityRequest:
    if not path or not content:
        raise ValueError("Path and content are required")
    
    return CapabilityRequest(
        request_id=f"file_{uuid.uuid4().hex[:8]}",
        capability="file_operations",
        method="write",
        params={"path": path, "content": content}
    )
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Solution: Ensure src is in Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```

2. **Missing Dependencies**
   ```bash
   # Solution: Install with uv
   uv sync
   ```

3. **Permission Errors**
   ```bash
   # Solution: Use writable directories
   # Use /tmp instead of system directories
   ```

4. **Capability Not Found**
   ```python
   # Solution: Check available capabilities
   print(agent.list_capabilities())
   ```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# This will show detailed execution logs
agent = BaseAgent("development")
```

## Next Steps

1. **Explore Agent Profiles**: Look at different profiles in `src/profiles/`
2. **Create Custom Capabilities**: Implement your own capabilities following the interface
3. **Build Applications**: Use BaseAgent as foundation for PATH Framework applications
4. **Study Rule Compliance**: Review how examples follow PATH Framework rules

## Support

- **Documentation**: Check the main PATH Framework documentation
- **Rules**: Review rule files in `.amazonq/rules/`
- **Tests**: Look at test files for additional usage patterns
- **Issues**: Create issues in the project repository