"""Enhanced profile with extended capabilities."""

from typing import Dict, Any
from ..core.base_agent import AgentProfile, AgentRequest, BaseAgent
from ..knowledge.knowledge_base import SharedKnowledgeBase


class EnhancedProfile(AgentProfile):
    """Profile with extended capabilities."""
    
    @property
    def agent_code(self) -> str:
        return "EP"
    
    @property
    def phase(self) -> int:
        return 2
    
    async def execute(self, request: AgentRequest, knowledge_base: SharedKnowledgeBase) -> Dict[str, Any]:
        return {"status": "enhanced_executed"}
    
    def get_capabilities(self) -> Dict[str, str]:
        return {
            "network": "Network operations",
            "version_control": "Git operations"
        }
    
    def get_performance_metrics(self) -> Dict[str, str]:
        return {"enhanced_metric": "100%"}
        
    def register_extended_capabilities(self, agent: BaseAgent):
        """Register extended capabilities."""
        from ..core.extended_capability_implementations import (
            StandardNetworkOperations,
            StandardVersionControl
        )
        
        # Register extended capabilities
        agent.register_capability(StandardNetworkOperations(agent.system))
        agent.register_capability(StandardVersionControl(agent.system))