"""Main entry point for individual agent containers."""

import asyncio
import logging
import os
from core.base_agent import BaseAgent


async def main():
    """Run single agent based on AGENT_PROFILE environment variable."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("PATH_Individual_Agent")
    
    # Get agent profile from environment
    agent_profile = os.getenv("AGENT_PROFILE")
    if not agent_profile:
        raise ValueError("AGENT_PROFILE environment variable must be set")
    
    logger.info(f"Starting individual agent: {agent_profile}")
    
    # Create specialized agent
    agent = BaseAgent(agent_profile)
    
    # Start agent service (would include REST API, message handling, etc.)
    logger.info(f"Agent {agent_profile} ready and listening...")
    
    # Keep running
    while True:
        await asyncio.sleep(60)
        logger.info(f"Agent {agent_profile} heartbeat")


if __name__ == "__main__":
    asyncio.run(main())