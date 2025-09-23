"""Main entry point for PATH Framework agents."""

import asyncio
import logging
from typing import Dict, Any

from core.base_agent import BaseAgent, AgentRequest
from profiles.profile_loader import ProfileLoader


async def main():
    """Main function to demonstrate agent functionality."""
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("PATH_Framework")
    
    logger.info("Starting PATH Framework Agent System")
    
    # List available profiles
    profiles = ProfileLoader.list_profiles()
    logger.info(f"Available profiles: {profiles}")
    
    # Create Domain Analyst agent
    da_agent = BaseAgent("domain_analyst")
    
    # Create sample user story analysis request
    request = AgentRequest(
        request_id="req_001",
        operation="analyze_user_story",
        payload={
            "story_id": "story_001",
            "user_story": "As a customer, I want to place an order online so that I can purchase products conveniently from home."
        }
    )
    
    # Process request
    logger.info("Processing user story analysis request...")
    response = await da_agent.process_request(request)
    
    logger.info(f"Response status: {response.status}")
    logger.info(f"Analysis result: {response.result}")
    
    # Create System Architect agent
    sa_agent = BaseAgent("system_architect")
    
    # Create architecture generation request
    arch_request = AgentRequest(
        request_id="req_002",
        operation="generate_architecture",
        payload={
            "requirements": {
                "user_load": 1000,
                "data_volume": "medium",
                "complexity": "medium"
            },
            "constraints": {
                "team_size": 8,
                "budget": "medium",
                "timeline": "6_months"
            }
        }
    )
    
    # Process architecture request
    logger.info("Processing architecture generation request...")
    arch_response = await sa_agent.process_request(arch_request)
    
    logger.info(f"Architecture response status: {arch_response.status}")
    logger.info(f"Architecture options: {len(arch_response.result.get('options', []))}")
    
    logger.info("PATH Framework Agent System demonstration completed")


if __name__ == "__main__":
    asyncio.run(main())