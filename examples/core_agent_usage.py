#!/usr/bin/env python3
"""
Example: Using CoreAgent and specialized agents

Demonstrates the CoreAgent foundation with specialized agent implementations.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from src.agents.domain_analyst_agent import DomainAnalystAgent
from src.agents.tdd_orchestrator_agent import TDDOrchestratorAgent


async def main():
    """Demonstrate CoreAgent with specialized agents."""
    
    print("🎯 CoreAgent + Specialized Agents Example")
    print("=" * 50)
    
    # Create specialized agents
    da_agent = DomainAnalystAgent()
    to_agent = TDDOrchestratorAgent()
    
    print(f"✅ Created agents:")
    print(f"   📋 {da_agent.agent_id} (Phase {da_agent.phase})")
    print(f"   🧪 {to_agent.agent_id} (Phase {to_agent.phase})")
    print()
    
    # Show agent info
    print("📊 Agent Information:")
    da_info = da_agent.get_agent_info()
    to_info = to_agent.get_agent_info()
    
    print(f"DA Agent: {da_info['agent_code']} - Phase {da_info['phase']}")
    print(f"TO Agent: {to_info['agent_code']} - Phase {to_info['phase']}")
    print()
    
    # Phase 1: Domain Analysis
    print("🔵 Phase 1: Domain Analysis")
    print("-" * 30)
    
    user_story = "As a customer, I want to place an order, so that I can purchase products"
    da_result = await da_agent.analyze_user_story(user_story)
    
    print(f"✅ Domain analysis complete")
    print(f"📋 Requirements: {da_result['requirements']}")
    print(f"🏗️ Domain model: {da_result['domain_model']}")
    print()
    
    # Phase 2: TDD Orchestration
    print("🟢 Phase 2: TDD Orchestration")
    print("-" * 30)
    
    # TO agent gets DA's work from knowledge base
    da_work = await to_agent.get_previous_work("PATH_DA", "analyze_user_story")
    print(f"📥 Retrieved DA work: {da_work.get('requirements', 'None')}")
    
    to_result = await to_agent.orchestrate_tdd_cycle(da_work)
    
    print(f"✅ TDD orchestration complete")
    print(f"🔄 TDD cycle: {to_result['tdd_cycle']}")
    print(f"🧪 Tests: {to_result['tests_created']}")
    print()
    
    # Show rule compliance
    print("📋 Rule Compliance Status:")
    print(f"DA Agent: {da_agent.rule_compliance}")
    print(f"TO Agent: {to_agent.rule_compliance}")
    
    print("\n🎯 CoreAgent example completed!")


if __name__ == "__main__":
    asyncio.run(main())