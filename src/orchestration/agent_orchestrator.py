"""Central orchestrator for agent coordination."""

from typing import Dict, Any, List, Optional
from src.core.base_agent import BaseAgent, AgentRequest
from src.communication.agent_messenger import AgentMessenger, AgentMessage, MessageType
from src.communication.event_bus import EventBus, EventType
from src.communication.work_queue import WorkQueue, WorkItem, WorkStatus
from src.knowledge.knowledge_base import SharedKnowledgeBase


class AgentOrchestrator:
    """Orchestrates agent interactions and workflows."""
    
    def __init__(self):
        self.knowledge_base = SharedKnowledgeBase()
        self.messenger = AgentMessenger()
        self.event_bus = EventBus()
        self.work_queue = WorkQueue()
        self.agents: Dict[str, BaseAgent] = {}
    
    def register_agent(self, agent_id: str, agent: BaseAgent) -> None:
        """Register agent with orchestrator."""
        self.agents[agent_id] = agent
    
    async def execute_user_story(self, user_story: Dict[str, Any]) -> Dict[str, Any]:
        """Execute complete user story through all phases."""
        
        # Phase 1: Software Engineering
        domain_result = await self._execute_agent_operation(
            "domain_analyst", "analyze_user_story", user_story
        )
        
        architecture_result = await self._execute_agent_operation(
            "system_architect", "design_architecture", domain_result
        )
        
        component_result = await self._execute_agent_operation(
            "component_designer", "design_components", architecture_result
        )
        
        integration_result = await self._execute_agent_operation(
            "integration_architect", "design_integrations", component_result
        )
        
        # Phase 2: TDD Implementation
        tdd_result = await self._execute_agent_operation(
            "tdd_orchestrator", "orchestrate_tdd_cycle", integration_result
        )
        
        # Phase 3: DevOps
        pipeline_result = await self._execute_agent_operation(
            "pipeline_architect", "design_pipeline", tdd_result
        )
        
        # Phase 4: Operations
        operations_result = await self._execute_agent_operation(
            "reliability_engineer", "monitor_reliability", pipeline_result
        )
        
        return {
            "story_id": user_story["story_id"],
            "status": "completed",
            "results": {
                "phase1": integration_result,
                "phase2": tdd_result,
                "phase3": pipeline_result,
                "phase4": operations_result
            }
        }
    
    async def _execute_agent_operation(self, agent_id: str, operation: str, 
                                     input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute operation on specific agent."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not registered")
        
        agent = self.agents[agent_id]
        request = AgentRequest(
            request_id=f"{agent_id}_{operation}",
            operation=operation,
            payload=input_data
        )
        
        result = await agent.execute(request, self.knowledge_base)
        
        # Store result in knowledge base for other agents
        await self.knowledge_base.store_agent_output(agent_id, operation, result)
        
        return result
    
    async def handle_agent_handoff(self, from_agent: str, to_agent: str, 
                                 work_product: Dict[str, Any]) -> None:
        """Handle work handoff between agents."""
        await self.messenger.handoff_to_next_phase(from_agent, to_agent, work_product)
        
        # Notify via event bus
        await self.event_bus.publish_work_completed(from_agent, work_product)