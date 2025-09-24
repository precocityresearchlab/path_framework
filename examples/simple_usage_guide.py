#!/usr/bin/env python3
"""
Simple Usage Guide: PATH Framework BaseAgent

Shows the essential steps to use BaseAgent with sample data.
"""

import asyncio
import sys
from pathlib import Path

# Setup imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from src.core.base_agent import BaseAgent
from src.core.capability_interface import CapabilityRequest


async def simple_example():
    """Simple example showing BaseAgent usage."""
    
    print("🚀 Simple PATH Framework BaseAgent Example")
    print("=" * 45)
    
    # Step 1: Initialize BaseAgent
    agent = BaseAgent("development")
    print(f"✅ Agent created: {agent.agent_id}")
    print(f"🔧 Capabilities: {', '.join(agent.list_capabilities())}")
    print()
    
    # Step 2: Create a file with sample data
    sample_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "active": True
    }
    
    # User story for file operation (required for code generation)
    user_story = {
        "format": "As a developer, I want to save user data to a file, so that I can persist user information"
    }
    
    # Create file request
    file_request = CapabilityRequest(
        request_id="simple_001",
        capability="file_operations", 
        method="write",
        params={
            "path": "/tmp/user_data.json",
            "content": str(sample_data).replace("'", '"'),
            "user_story": user_story
        }
    )
    
    # Execute file operation
    response = await agent.execute_capability(file_request)
    print(f"📁 File operation: {response.status}")
    print(f"⏱️  Execution time: {response.execution_time:.3f}s")
    print()
    
    # Step 3: Execute a simple command
    cmd_request = CapabilityRequest(
        request_id="simple_002",
        capability="command_execution",
        method="execute", 
        params={
            "command": "ls -la /tmp/user_data.json"
        }
    )
    
    response = await agent.execute_capability(cmd_request)
    print(f"⚡ Command execution: {response.status}")
    if response.result.get("stdout"):
        print(f"📄 File created: {response.result['stdout'].strip()}")
    print()
    
    # Step 4: Generate some code
    code_request = CapabilityRequest(
        request_id="simple_003",
        capability="code_generation",
        method="generate_source",
        params={
            "language": "python",
            "content": "class User:\n    def __init__(self, name, email):\n        self.name = name\n        self.email = email",
            "path": "/tmp/user_model.py",
            "user_story": {
                "format": "As a developer, I want to generate a User class, so that I can model user data consistently"
            }
        }
    )
    
    response = await agent.execute_capability(code_request)
    print(f"💻 Code generation: {response.status}")
    print(f"📝 Generated file: {response.result.get('path', 'N/A')}")
    print()
    
    # Step 5: Show rule compliance
    print("📋 Rule Compliance Status:")
    for rule, status in agent.rule_compliance.items():
        icon = "✅" if status else "❌"
        print(f"  {icon} {rule}: {status}")
    
    print("\n🎯 Simple example completed!")


if __name__ == "__main__":
    asyncio.run(simple_example())