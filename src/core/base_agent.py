"""Base agent architecture for PATH Framework."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass
import logging

from ..communication.protocols import CommunicationLayer
from ..knowledge.knowledge_base import SharedKnowledgeBase
from ..validation.human_validation import HumanValidationInterface


@dataclass
class AgentRequest:
    """Standard agent request format."""
    request_id: str
    operation: str
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None
    priority: str = "normal"


@dataclass
class AgentResponse:
    """Standard agent response format."""
    request_id: str
    status: str
    result: Dict[str, Any]
    metadata: Dict[str, Any]


class BaseAgent:
    """Base agent with profile-based specialization."""
    
    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        self.agent_id = f"PATH_{profile_name.upper()}"
        self.logger = logging.getLogger(self.agent_id)
        
        # Core components
        self.knowledge_base = SharedKnowledgeBase()
        self.communication = CommunicationLayer()
        self.validation = HumanValidationInterface()
        
        # Single LLM interface for all agents
        from .llm_interface import UnifiedLLMInterface
        self.llm = UnifiedLLMInterface()
        
        # Load profile
        self.profile = self._load_profile(profile_name)
        
    def _load_profile(self, profile_name: str):
        """Load agent profile dynamically."""
        from ..profiles.profile_loader import ProfileLoader
        return ProfileLoader.load(profile_name)
    
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process request using profile-specific logic."""
        try:
            self.logger.info(f"Processing {request.operation} for {self.profile_name}")
            
            # Use profile to execute request with LLM access
            result = await self.profile.execute(request, self.knowledge_base, self.llm)
            
            return AgentResponse(
                request_id=request.request_id,
                status="success",
                result=result,
                metadata={"agent_id": self.agent_id, "profile": self.profile_name}
            )
            
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return AgentResponse(
                request_id=request.request_id,
                status="error",
                result={"error": str(e)},
                metadata={"agent_id": self.agent_id, "profile": self.profile_name}
            )


class AgentProfile(ABC):
    """Abstract base class for agent profiles."""
    
    @property
    @abstractmethod
    def agent_code(self) -> str:
        """Two-letter agent code."""
        pass
    
    @property
    @abstractmethod
    def phase(self) -> int:
        """PATH Framework phase (1-4)."""
        pass
    
    @abstractmethod
    async def execute(self, request: AgentRequest, knowledge_base: SharedKnowledgeBase) -> Dict[str, Any]:
        """Execute profile-specific logic."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> Dict[str, str]:
        """Get profile capabilities."""
        pass
    
    @abstractmethod
    def get_performance_metrics(self) -> Dict[str, str]:
        """Get performance metrics."""
        pass