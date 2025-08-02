"""
PATH Framework Base Agent

This module provides the base class for all PATH Framework agents.
All specialized agents inherit from this base class to ensure consistent
behavior, communication protocols, and quality assurance.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
import uuid
import asyncio
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class AgentPhase(Enum):
    """PATH Framework phases"""
    SOFTWARE_ENGINEERING = "phase1_software_engineering"
    TDD = "phase2_tdd"
    DEVOPS = "phase3_devops"
    OPERATIONS = "phase4_operations"


class DecisionAuthority(Enum):
    """Agent decision authority levels"""
    AUTONOMOUS = "autonomous"  # Agent decides independently
    HUMAN_APPROVAL = "human_approval"  # Requires human approval
    COLLABORATIVE = "collaborative"  # Joint human-AI decision


@dataclass
class AgentRequest:
    """Standard request format for agent communication"""
    id: str
    timestamp: datetime
    from_agent: str
    to_agent: str
    request_type: str
    data: Dict[str, Any]
    priority: str = "normal"  # low, normal, high, critical
    requires_human_input: bool = False


@dataclass
class AgentResponse:
    """Standard response format for agent communication"""
    id: str
    request_id: str
    timestamp: datetime
    from_agent: str
    to_agent: str
    response_type: str
    data: Dict[str, Any]
    status: str  # success, error, partial, requires_approval
    human_approval_required: bool = False
    confidence_score: float = 0.0
    reasoning: str = ""


@dataclass
class ValidationResult:
    """Result of agent output validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    confidence_score: float
    recommendations: List[str]


class BaseAgent(ABC):
    """
    Base class for all PATH Framework agents.
    
    Provides common functionality for:
    - Agent configuration and initialization
    - Communication with other agents
    - Human collaboration protocols
    - Quality assurance and validation
    - Audit trail and logging
    """
    
    def __init__(self, config: Dict[str, Any], llm_provider=None):
        """
        Initialize base agent with configuration
        
        Args:
            config: Agent configuration dictionary
            llm_provider: LLM provider instance for AI capabilities
        """
        self.config = config
        self.llm_provider = llm_provider
        self.agent_id = config.get('agent_id', str(uuid.uuid4()))
        self.name = config.get('name', self.__class__.__name__)
        self.phase = AgentPhase(config.get('phase'))
        self.capabilities = config.get('capabilities', [])
        self.decision_authority = config.get('decision_authority', {})
        self.quality_gates = config.get('quality_gates', [])
        
        # Initialize logging
        self.logger = logging.getLogger(f"agent.{self.name}")
        self.audit_trail = []
        
        # Initialize agent state
        self.is_active = False
        self.current_task = None
        self.context_memory = {}
        
        self.logger.info(f"Initialized agent {self.name} for {self.phase.value}")
    
    @abstractmethod
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """
        Process an incoming request and return a response.
        
        This is the main method that each agent must implement to define
        their specialized behavior.
        
        Args:
            request: Incoming agent request
            
        Returns:
            AgentResponse: Response containing results or requesting approval
        """
        pass
    
    @abstractmethod
    async def validate_output(self, output: Any) -> ValidationResult:
        """
        Validate agent output for quality assurance.
        
        Args:
            output: Output to validate
            
        Returns:
            ValidationResult: Validation results with errors/warnings
        """
        pass
    
    async def send_message(self, to_agent: str, message_type: str, 
                          data: Dict[str, Any], 
                          requires_human_approval: bool = False) -> AgentResponse:
        """
        Send a message to another agent.
        
        Args:
            to_agent: Target agent identifier
            message_type: Type of message being sent
            data: Message payload
            requires_human_approval: Whether message requires human approval
            
        Returns:
            AgentResponse: Response from target agent
        """
        request = AgentRequest(
            id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            from_agent=self.agent_id,
            to_agent=to_agent,
            request_type=message_type,
            data=data,
            requires_human_input=requires_human_approval
        )
        
        self._log_communication("OUTGOING", request)
        
        # TODO: Implement actual message routing
        # This would route the message to the appropriate agent
        return await self._route_message(request)
    
    async def request_human_approval(self, decision: Dict[str, Any], 
                                   context: str) -> bool:
        """
        Request human approval for a decision.
        
        Args:
            decision: Decision requiring approval
            context: Context explaining why approval is needed
            
        Returns:
            bool: Whether approval was granted
        """
        approval_request = {
            "agent": self.name,
            "phase": self.phase.value,
            "decision": decision,
            "context": context,
            "timestamp": datetime.utcnow().isoformat(),
            "reasoning": self._generate_reasoning(decision)
        }
        
        self.logger.info(f"Requesting human approval: {context}")
        self._add_to_audit_trail("APPROVAL_REQUEST", approval_request)
        
        # TODO: Implement actual human approval interface
        # This would present the decision to human team members
        return await self._request_approval_from_human(approval_request)
    
    def has_decision_authority(self, decision_type: str) -> DecisionAuthority:
        """
        Check agent's decision authority for a specific type of decision.
        
        Args:
            decision_type: Type of decision being made
            
        Returns:
            DecisionAuthority: Level of authority for this decision
        """
        authority = self.decision_authority.get(
            decision_type, 
            DecisionAuthority.HUMAN_APPROVAL
        )
        return DecisionAuthority(authority)
    
    async def execute_quality_gate(self, gate_name: str, 
                                  data: Any) -> ValidationResult:
        """
        Execute a quality gate validation.
        
        Args:
            gate_name: Name of the quality gate
            data: Data to validate
            
        Returns:
            ValidationResult: Results of quality gate validation
        """
        if gate_name not in self.quality_gates:
            return ValidationResult(
                is_valid=True,
                errors=[],
                warnings=[f"Quality gate {gate_name} not configured"],
                confidence_score=1.0,
                recommendations=[]
            )
        
        self.logger.info(f"Executing quality gate: {gate_name}")
        
        # Execute the quality gate
        result = await self._execute_quality_gate(gate_name, data)
        
        self._add_to_audit_trail("QUALITY_GATE", {
            "gate_name": gate_name,
            "result": result,
            "data_summary": self._summarize_data(data)
        })
        
        return result
    
    def update_context(self, key: str, value: Any):
        """
        Update agent context memory.
        
        Args:
            key: Context key
            value: Context value
        """
        self.context_memory[key] = {
            "value": value,
            "timestamp": datetime.utcnow(),
            "agent": self.agent_id
        }
        
        self.logger.debug(f"Updated context: {key}")
    
    def get_context(self, key: str) -> Optional[Any]:
        """
        Get value from agent context memory.
        
        Args:
            key: Context key
            
        Returns:
            Context value or None if not found
        """
        context_entry = self.context_memory.get(key)
        return context_entry["value"] if context_entry else None
    
    def _add_to_audit_trail(self, action: str, data: Dict[str, Any]):
        """Add entry to audit trail"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": self.agent_id,
            "action": action,
            "data": data
        }
        self.audit_trail.append(entry)
        
        # Limit audit trail size to prevent memory issues
        if len(self.audit_trail) > 1000:
            self.audit_trail = self.audit_trail[-500:]
    
    def _log_communication(self, direction: str, message: AgentRequest):
        """Log agent communication"""
        self.logger.info(
            f"{direction} message: {message.request_type} "
            f"{'to' if direction == 'OUTGOING' else 'from'} {message.to_agent}"
        )
        
        self._add_to_audit_trail("COMMUNICATION", {
            "direction": direction,
            "message_type": message.request_type,
            "target_agent": message.to_agent,
            "message_id": message.id
        })
    
    def _generate_reasoning(self, decision: Dict[str, Any]) -> str:
        """Generate human-readable reasoning for a decision"""
        # This would use the LLM to generate clear reasoning
        # For now, return a placeholder
        return f"Decision made by {self.name} based on {self.phase.value} methodology"
    
    def _summarize_data(self, data: Any) -> str:
        """Create a summary of data for audit purposes"""
        if isinstance(data, dict):
            return f"Dictionary with {len(data)} keys"
        elif isinstance(data, list):
            return f"List with {len(data)} items"
        else:
            return f"{type(data).__name__}: {str(data)[:100]}..."
    
    async def _route_message(self, request: AgentRequest) -> AgentResponse:
        """Route message to target agent (placeholder implementation)"""
        # TODO: Implement actual message routing system
        return AgentResponse(
            id=str(uuid.uuid4()),
            request_id=request.id,
            timestamp=datetime.utcnow(),
            from_agent=request.to_agent,
            to_agent=request.from_agent,
            response_type="acknowledgment",
            data={"status": "received"},
            status="success"
        )
    
    async def _request_approval_from_human(self, approval_request: Dict[str, Any]) -> bool:
        """Request approval from human team members (placeholder implementation)"""
        # TODO: Implement actual human approval interface
        # For now, simulate approval based on decision complexity
        return True
    
    async def _execute_quality_gate(self, gate_name: str, data: Any) -> ValidationResult:
        """Execute specific quality gate (placeholder implementation)"""
        # TODO: Implement actual quality gate execution
        return ValidationResult(
            is_valid=True,
            errors=[],
            warnings=[],
            confidence_score=0.95,
            recommendations=[]
        )


class AgentError(Exception):
    """Base exception for agent errors"""
    pass


class ValidationError(AgentError):
    """Exception raised when validation fails"""
    pass


class CommunicationError(AgentError):
    """Exception raised when agent communication fails"""
    pass


class ApprovalTimeoutError(AgentError):
    """Exception raised when human approval times out"""
    pass
