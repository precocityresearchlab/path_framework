"""Base agent architecture for PATH Framework.

Implements PATH Framework rule compliance according to rule-execution-priority-matrix.rule.md
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import logging
import time
from datetime import datetime, timezone

from ..communication.protocols import CommunicationLayer
from ..knowledge.knowledge_base import SharedKnowledgeBase
from ..validation.human_validation import HumanValidationInterface
from .system_adapter import SystemAdapter
from .capability_interface import (
    AgentCapabilityInterface, 
    CapabilityRequest, 
    CapabilityResponse, 
    CapabilityStatus
)


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
    """Base agent with PATH Framework rule compliance and standard capabilities.
    
    Implements mandatory validation gates from rule-execution-priority-matrix.rule.md:
    - UTC time tracking
    - User story validation
    - Human validation gates
    - Quality checkpoints
    - Completion validation
    """
    
    def __init__(self, profile_name: str):
        # GATE 2: UTC TIME VALIDATION - Get session UTC timestamp
        self.session_utc = datetime.now(timezone.utc)
        self.task_start_utc: Optional[datetime] = None
        self.task_end_utc: Optional[datetime] = None
        
        self.profile_name = profile_name
        self.agent_id = f"PATH_{profile_name.upper()}"
        self.logger = logging.getLogger(self.agent_id)
        
        # Core components
        self.knowledge_base = SharedKnowledgeBase()
        self.communication = CommunicationLayer()
        self.validation = HumanValidationInterface()
        self.system = SystemAdapter()
        
        # Single LLM interface for all agents
        from .llm_interface import UnifiedLLMInterface
        self.llm = UnifiedLLMInterface()
        
        # Rule compliance tracking - must be set before registering capabilities
        self.rule_compliance = {
            "tests_first": False,
            "story_ready": False,
            "utc_tracking": True,
            "human_validation": False,
            "completion_format": False,
            "metadata_updated": False,
            "quality_gates": False
        }
        
        # TDD cycle state tracking - implements Red-Green-Refactor discipline
        self.tdd_cycle_state = "RED"  # Always start in RED phase
        self.test_coverage = 0.0
        self.mutation_score = 0.0
        
        # Standard capabilities registry
        self.capabilities: Dict[str, AgentCapabilityInterface] = {}
        self._register_standard_capabilities()
        
        # Load profile
        self.profile = self._load_profile(profile_name)
        
        # Register profile-specific extended capabilities
        if self.profile:
            self.profile.register_extended_capabilities(self)
        
    def _register_standard_capabilities(self):
        """Register standard PATH Framework capabilities."""
        from .standard_capabilities import (
            StandardFileOperations,
            StandardCommandExecution,
            StandardCodeGeneration,
            StandardAnalysisTools
        )
        
        # Register core capabilities
        self.register_capability(StandardFileOperations(self.system))
        self.register_capability(StandardCommandExecution(self.system))
        self.register_capability(StandardCodeGeneration(self.system))
        self.register_capability(StandardAnalysisTools(self.system))
        
    def register_capability(self, capability: AgentCapabilityInterface):
        """Register capability with PATH Framework rule compliance validation."""
        # GATE 1: RULE LOADING VALIDATION - Validate capability interface
        if not isinstance(capability, AgentCapabilityInterface):
            raise ValueError("Capability must implement AgentCapabilityInterface")
            
        capability_name = capability.get_capability_name()
        
        # Validate capability follows PATH Framework standards
        if not self._validate_capability_compliance(capability):
            raise ValueError(f"Capability '{capability_name}' does not meet PATH Framework standards")
            
        # GATE 2: UTC TIME VALIDATION - Record registration time
        registration_utc = datetime.now(timezone.utc)
        
        self.capabilities[capability_name] = capability
        
        # Update rule compliance
        self.rule_compliance["metadata_updated"] = True
        
        self.logger.info(
            f"Registered capability: {capability_name} at {registration_utc.isoformat()}"
        )
        
    def _validate_capability_compliance(self, capability: AgentCapabilityInterface) -> bool:
        """Validate capability meets PATH Framework standards."""
        try:
            # Must have valid name
            name = capability.get_capability_name()
            if not name or not isinstance(name, str):
                return False
                
            # Must have supported methods
            methods = capability.get_supported_methods()
            if not methods or not isinstance(methods, list):
                return False
                
            # Must implement required methods
            required_methods = ["validate_params", "execute_capability"]
            for method in required_methods:
                if not hasattr(capability, method):
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Capability validation failed: {e}")
            return False
        
    def get_capability(self, name: str) -> Optional[AgentCapabilityInterface]:
        """Get capability implementation by name."""
        return self.capabilities.get(name)
        
    def list_capabilities(self) -> List[str]:
        """List all registered capabilities."""
        return list(self.capabilities.keys())
        
    async def execute_capability(self, request: CapabilityRequest) -> CapabilityResponse:
        """Execute capability with PATH Framework rule compliance.
        
        Implements mandatory validation gates from rule-execution-priority-matrix.rule.md
        """
        # GATE 1: RULE LOADING VALIDATION - Ensure capability exists
        capability = self.get_capability(request.capability)
        if not capability:
            self.logger.error(f"GATE 1 FAILURE: Capability '{request.capability}' not found")
            return self._create_error_response(request, "Capability not found")
            
        # GATE 2: UTC TIME VALIDATION - Record start time
        start_utc = datetime.now(timezone.utc)
        start_time = time.time()
        
        try:
            # GATE 3: USER STORY VALIDATION - Check if operation requires story
            if self._requires_user_story_validation(request.capability, request.method):
                user_story = request.params.get("user_story")
                if not self._validate_user_story(user_story):
                    self.logger.error("GATE 3 FAILURE: Invalid user story format")
                    return self._create_error_response(request, "User story validation failed")
                    
            # GATE 4: HUMAN VALIDATION - Check if operation requires human approval
            if self._requires_human_validation(request.capability, request.method):
                if not self._get_human_approval(request):
                    self.logger.error("GATE 4 FAILURE: Human validation required")
                    return self._create_error_response(request, "Human validation required")
                    
            # Parameter validation
            if not capability.validate_params(request.method, request.params):
                raise ValueError(f"Invalid parameters for {request.capability}.{request.method}")
                
            # Execute capability
            result = await capability.execute_capability(request.method, request.params)
            
            # GATE 5: COMPLETION VALIDATION - Record completion
            end_utc = datetime.now(timezone.utc)
            duration = (end_utc - start_utc).total_seconds()
            
            # Update rule compliance
            self.rule_compliance["completion_format"] = True
            
            return CapabilityResponse(
                request_id=request.request_id,
                status=CapabilityStatus.SUCCESS,
                result=result,
                metadata={
                    "agent_id": self.agent_id, 
                    "capability": request.capability,
                    "start_utc": start_utc.isoformat(),
                    "end_utc": end_utc.isoformat(),
                    "duration_seconds": duration
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error(f"Capability execution failed: {e}")
            return self._create_error_response(request, str(e))
    
    def _load_profile(self, profile_name: str):
        """Load agent profile by name."""
        try:
            if profile_name == "development":
                from ..profiles.development_profile import DevelopmentProfile
                return DevelopmentProfile()
            return None
        except Exception as e:
            self.logger.error(f"Failed to load profile {profile_name}: {e}")
            return None
    
    def _requires_user_story_validation(self, capability: str, method: str) -> bool:
        """Check if operation requires user story validation."""
        # Code generation operations require user stories
        return capability == "code_generation"
    
    def _validate_user_story(self, user_story) -> bool:
        """Validate user story format."""
        if not user_story or not isinstance(user_story, dict):
            return False
        
        story_format = user_story.get("format", "")
        if not story_format:
            return False
        
        # Check for "As a... I want... So that..." format
        required_parts = ["As a", "I want", "so that"]
        return all(part.lower() in story_format.lower() for part in required_parts)
    
    def _requires_human_validation(self, capability: str, method: str) -> bool:
        """Check if operation requires human validation."""
        # Critical operations that require human approval
        critical_ops = {
            "file_operations": ["delete_file", "modify_system_file"],
            "command_execution": ["execute_privileged", "system_modify"]
        }
        return method in critical_ops.get(capability, [])
    
    def _get_human_approval(self, request: CapabilityRequest) -> bool:
        """Get human approval for critical operations."""
        return self.validation.request_validation(
            f"{request.capability}.{request.method}",
            request.params
        )
    
    def _create_error_response(self, request: CapabilityRequest, error_msg: str) -> CapabilityResponse:
        """Create error response."""
        return CapabilityResponse(
            request_id=request.request_id,
            status=CapabilityStatus.ERROR,
            result={"error": error_msg},
            metadata={"agent_id": self.agent_id},
            execution_time=0.0
        )