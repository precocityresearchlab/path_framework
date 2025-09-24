#!/usr/bin/env python3
"""
Minimal example of interfacing with PATH Framework agents.
"""

import asyncio
from src.core.base_agent import AgentRequest
from src.profiles.phase1.domain_analyst import DomainAnalystProfile
from src.knowledge.knowledge_base import SharedKnowledgeBase


async def main():
    """Example agent interaction."""
    
    # Initialize
    agent = DomainAnalystProfile()
    knowledge_base = SharedKnowledgeBase()
    
    # Analyze user story
    request = AgentRequest(
        request_id="example-001",
        operation="analyze_user_story",
        payload={
            "story_id": "US-001",
            "user_story": "As a customer, I want to search for products, so that I can find what I need"
        }
    )
    
    result = await agent.execute(request, knowledge_base)
    
    print("Analysis Result:")
    print(f"- Entities: {result.get('analysis', {}).get('domain_entities', [])}")
    print(f"- Completeness: {result.get('completeness_score', 0)}")
    print(f"- Recommendations: {result.get('recommendations', [])}")


if __name__ == "__main__":
    asyncio.run(main())