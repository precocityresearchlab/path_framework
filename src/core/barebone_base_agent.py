"""Barebone BaseAgent with only essential shared capabilities for all 16 agents."""

from typing import Dict, List, Optional
import logging
from datetime import datetime, timezone

from ..knowledge.knowledge_base import SharedKnowledgeBase
from ..validation.human_validation import HumanValidationInterface
from .capability_interface import AgentCapabilityInterface


class BareboneBaseAgent:
    """Barebone base agent with only essential capabilities shared across all 16 agents.
    
    Essential shared capabilities ALL 16 agents need:
    1. Agent identity and logging
    2. Knowledge base access (agent-to-agent communication)
    3. Human validation interface (critical decisions)
    4. PATH Framework rule compliance tracking
    5. Capability registry (dynamic capability loading)
    """
    
    def __init__(self, agent_code: str, phase: int):
        # Essential agent identity
        self.agent_code = agent_code  # DA, SA, CD, IA, TO, TS, IS, CV, PA, IE, DS, MA, RE, OS, PerfA, SO
        self.phase = phase            # 1, 2, 3, or 4
        self.agent_id = f"PATH_{agent_code}"
        self.logger = logging.getLogger(self.agent_id)
        
        # Essential shared services ALL agents need
        self.knowledge_base = SharedKnowledgeBase()  # Agent-to-agent communication
        self.validation = HumanValidationInterface()  # Critical decision approval
        
        # Essential PATH Framework compliance (mandatory)
        self.session_utc = datetime.now(timezone.utc)
        self.rule_compliance = {
            "utc_tracking": True,
            "completion_format": False,
            "metadata_updated": False
        }
        
        # Essential capability registry (all agents have capabilities)
        self.capabilities: Dict[str, AgentCapabilityInterface] = {}
        
    def register_capability(self, capability: AgentCapabilityInterface):
        """Register capability - essential for all agents."""
        name = capability.get_capability_name()
        self.capabilities[name] = capability
        self.rule_compliance["metadata_updated"] = True
        self.logger.info(f"Registered capability: {name}")
        
    def get_capability(self, name: str) -> Optional[AgentCapabilityInterface]:
        """Get capability by name - essential for all agents."""
        return self.capabilities.get(name)
        
    def list_capabilities(self) -> List[str]:
        """List capabilities - essential for all agents."""
        return list(self.capabilities.keys())
        
    async def store_output(self, operation: str, result: dict):
        """Store agent output in knowledge base - essential for agent communication."""
        await self.knowledge_base.store_agent_output(self.agent_id, operation, result)
        
    async def get_previous_work(self, source_agent: str, operation: str) -> dict:
        """Get previous agent work - essential for agent communication."""
        return await self.knowledge_base.get_agent_output(source_agent, operation)
        
    def request_human_approval(self, operation: str, data: dict) -> bool:
        """Request human approval - essential for critical decisions."""
        return self.validation.request_validation(f"{self.agent_id}.{operation}", data)
        
    def mark_complete(self, operation: str, duration: float):
        """Mark operation complete - essential for PATH Framework compliance."""
        end_utc = datetime.now(timezone.utc)
        self.rule_compliance["completion_format"] = True
        self.logger.info(f"Completed {operation} in {duration:.2f}s at {end_utc.isoformat()}")
        
    def get_agent_info(self) -> dict:
        """Get agent information - essential for identification."""
        return {
            "agent_id": self.agent_id,
            "agent_code": self.agent_code,
            "phase": self.phase,
            "session_utc": self.session_utc.isoformat(),
            "capabilities": self.list_capabilities(),
            "rule_compliance": self.rule_compliance
        }