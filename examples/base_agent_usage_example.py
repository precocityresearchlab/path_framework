#!/usr/bin/env python3
"""
Example: Using BaseAgent with Sample Data

Demonstrates PATH Framework BaseAgent usage with real sample data following
rule-execution-priority-matrix.rule.md compliance requirements.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
os.chdir(project_root)

from src.core.base_agent import BaseAgent
from src.core.capability_interface import CapabilityRequest


async def main():
    """Main example demonstrating BaseAgent usage with sample data."""
    
    print("🚀 PATH Framework BaseAgent Usage Example")
    print("=" * 50)
    
    # Initialize BaseAgent with sample profile
    agent = BaseAgent("development")
    
    print(f"✅ Agent initialized: {agent.agent_id}")
    print(f"📅 Session UTC: {agent.session_utc.isoformat()}")
    print(f"🔧 Available capabilities: {agent.list_capabilities()}")
    print()
    
    # Example 1: File Operations with Sample Data
    print("📁 Example 1: File Operations")
    print("-" * 30)
    
    # Sample user story for file operations
    sample_user_story = {
        "format": "As a developer, I want to create configuration files, so that I can store application settings",
        "acceptance_criteria": [
            "Given a configuration template, When I create a config file, Then it should contain valid JSON",
            "Given file path and content, When I write the file, Then it should be created successfully"
        ]
    }
    
    # Sample configuration data
    sample_config = {
        "app_name": "PATH Framework Demo",
        "version": "1.0.0",
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "path_demo"
        },
        "features": {
            "logging": True,
            "monitoring": True,
            "caching": False
        }
    }
    
    # Create file operation request
    file_request = CapabilityRequest(
        request_id="file_001",
        capability="file_operations",
        method="write",
        params={
            "path": "/tmp/sample_config.json",
            "content": str(sample_config).replace("'", '"'),
            "user_story": sample_user_story
        }
    )
    
    try:
        response = await agent.execute_capability(file_request)
        print(f"✅ File operation result: {response.status}")
        print(f"📊 Metadata: {response.metadata}")
    except Exception as e:
        print(f"❌ File operation failed: {e}")
    
    print()
    
    # Example 2: Code Generation with Sample Data
    print("💻 Example 2: Code Generation")
    print("-" * 30)
    
    # Sample user story for code generation
    code_user_story = {
        "format": "As a developer, I want to generate a data model class, so that I can represent user data consistently",
        "acceptance_criteria": [
            "Given field specifications, When I generate a class, Then it should have proper type hints",
            "Given validation rules, When I create the model, Then it should include validation methods"
        ]
    }
    
    # Sample data model specification
    sample_model_spec = {
        "class_name": "User",
        "fields": [
            {"name": "id", "type": "int", "required": True},
            {"name": "username", "type": "str", "required": True, "min_length": 3},
            {"name": "email", "type": "str", "required": True, "pattern": r"^[^@]+@[^@]+\.[^@]+$"},
            {"name": "age", "type": "int", "required": False, "min_value": 0},
            {"name": "is_active", "type": "bool", "default": True}
        ],
        "methods": ["validate", "__str__", "__repr__"]
    }
    
    # Create code generation request
    code_request = CapabilityRequest(
        request_id="code_001",
        capability="code_generation",
        method="generate_source",
        params={
            "language": "python",
            "content": f"# Generated from specification: {sample_model_spec['class_name']}",
            "path": "/tmp/generated_model.py",
            "user_story": code_user_story
        }
    )
    
    try:
        response = await agent.execute_capability(code_request)
        print(f"✅ Code generation result: {response.status}")
        if response.result:
            print("📝 Generated code preview:")
            print(response.result.get("code", "")[:200] + "...")
    except Exception as e:
        print(f"❌ Code generation failed: {e}")
    
    print()
    
    # Example 3: Analysis Tools with Sample Data
    print("🔍 Example 3: Analysis Tools")
    print("-" * 30)
    
    # Sample code for analysis
    sample_code = '''
def calculate_user_score(user_data):
    if not user_data:
        return 0
    
    score = 0
    if user_data.get("age", 0) > 18:
        score += 10
    
    if user_data.get("is_premium", False):
        score *= 2
    
    return score

def process_users(users):
    results = []
    for user in users:
        score = calculate_user_score(user)
        results.append({"user": user, "score": score})
    return results
'''
    
    # Create analysis request
    analysis_request = CapabilityRequest(
        request_id="analysis_001",
        capability="analysis_tools",
        method="static_analysis",
        params={
            "path": "/tmp",
            "language": "python"
        }
    )
    
    try:
        response = await agent.execute_capability(analysis_request)
        print(f"✅ Analysis result: {response.status}")
        if response.result:
            metrics = response.result.get("metrics", {})
            print(f"📊 Code metrics: {metrics}")
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
    
    print()
    
    # Example 4: Command Execution with Sample Data
    print("⚡ Example 4: Command Execution")
    print("-" * 30)
    
    # Sample system commands
    sample_commands = [
        {"command": "echo", "args": ["Hello from PATH Framework!"]},
        {"command": "date", "args": ["+%Y-%m-%d %H:%M:%S UTC"]},
        {"command": "python", "args": ["--version"]}
    ]
    
    for i, cmd_spec in enumerate(sample_commands):
        cmd_request = CapabilityRequest(
            request_id=f"cmd_{i:03d}",
            capability="command_execution",
            method="execute",
            params={
                "command": f"{cmd_spec['command']} {' '.join(cmd_spec['args'])}"
            }
        )
        
        try:
            response = await agent.execute_capability(cmd_request)
            print(f"✅ Command '{cmd_spec['command']}': {response.status}")
            if response.result:
                output = response.result.get("stdout", "").strip()
                if output:
                    print(f"   Output: {output}")
        except Exception as e:
            print(f"❌ Command '{cmd_spec['command']}' failed: {e}")
    
    print()
    
    # Display final rule compliance status
    print("📋 PATH Framework Rule Compliance Status")
    print("-" * 40)
    for rule, status in agent.rule_compliance.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {rule}: {status}")
    
    print()
    print("🎯 Example completed successfully!")
    print(f"⏱️  Session duration: {(agent.session_utc - agent.session_utc).total_seconds():.2f}s")


if __name__ == "__main__":
    asyncio.run(main())