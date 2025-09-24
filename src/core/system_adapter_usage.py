#!/usr/bin/env python3
"""Example of using SystemAdapter in agents."""

import asyncio
from src.core.system_adapter import SystemAdapter


async def demo_system_adapter():
    """Demonstrate SystemAdapter capabilities."""
    
    system = SystemAdapter()
    
    # File operations
    await system.write_file("test_config.json", '{"name": "test", "version": "1.0"}')
    config = await system.read_json("test_config.json")
    print(f"Config: {config}")
    
    # Command execution
    result = await system.execute_command("ls -la")
    print(f"Command result: {result['success']}")
    
    # Code generation
    await system.generate_file_from_template(
        "templates/agent.py.template",
        "generated_agent.py",
        {"agent_name": "TestAgent", "phase": "1"}
    )
    
    # Analysis
    metrics = await system.analyze_file_metrics("test_config.json")
    print(f"File metrics: {metrics}")


class ExampleAgent:
    """Example agent using SystemAdapter."""
    
    def __init__(self):
        self.system = SystemAdapter()
    
    async def create_documentation(self, agent_name: str, specs: dict):
        """Create agent documentation using system adapter."""
        
        # Generate design document
        doc_content = f"""# {agent_name} Design
        
## Purpose
{specs.get('purpose', 'Agent purpose')}

## Operations
{specs.get('operations', 'Agent operations')}
"""
        
        await self.system.write_file(f"docs/{agent_name.lower()}_design.md", doc_content)
        
        # Create configuration
        config = {
            "agent_name": agent_name,
            "capabilities": specs.get('capabilities', []),
            "phase": specs.get('phase', 1)
        }
        
        await self.system.write_json(f"config/{agent_name.lower()}.json", config)
        
        # Execute validation
        result = await self.system.execute_command(f"python validate_agent.py {agent_name}")
        
        return {
            "documentation_created": True,
            "config_created": True,
            "validation_result": result['success']
        }


if __name__ == "__main__":
    asyncio.run(demo_system_adapter())