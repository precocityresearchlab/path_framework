"""Minimal BaseAgent with only core shared capabilities.

Implements PATH Framework rule compliance with minimal shared functionality.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import logging
from datetime import datetime, timezone

from ..knowledge.knowledge_base import SharedKnowledgeBase
from ..validation.human_validation import HumanValidationInterface
from .capability_interface import (
    AgentCapabilityInterface, 
    CapabilityRequest, 
    CapabilityResponse, 
    CapabilityStatus
)


class MinimalBaseAgent:
    """Minimal base agent with only core shared capabilities.
    
    Core shared capabilities ALL agents need:
    - PATH Framework rule compliance
    - UTC time tracking
    - Knowledge base access
    - Human validation interface
    - Capability registry
    """
    
    def __init__(self, profile_name: str):
        # Core identity
        self.profile_name = profile_name
        self.agent_id = f"PATH_{profile_name.upper()}"
        self.logger = logging.getLogger(self.agent_id)
        
        # Core shared services ALL agents need
        self.knowledge_base = SharedKnowledgeBase()
        self.validation = HumanValidationInterface()
        
        # PATH Framework rule compliance (mandatory for all agents)
        self.session_utc = datetime.now(timezone.utc)
        self.rule_compliance = {
            "utc_tracking": True,
            "story_ready": False,
            "human_validation": False,
            "completion_format": False,
            "metadata_updated": False
        }
        
        # Capability registry (all agents have capabilities)
        self.capabilities: Dict[str, AgentCapabilityInterface] = {}
        
        # Load profile (adds specialized capabilities)
        self.profile = self._load_profile(profile_name)
        if self.profile:
            self.profile.register_capabilities(self)
        
    def register_capability(self, capability: AgentCapabilityInterface):
        """Register capability with validation."""
        if not isinstance(capability, AgentCapabilityInterface):
            raise ValueError("Must implement AgentCapabilityInterface")
            
        name = capability.get_capability_name()
        self.capabilities[name] = capability
        self.rule_compliance["metadata_updated"] = True
        
        self.logger.info(f"Registered capability: {name}")
        
    def get_capability(self, name: str) -> Optional[AgentCapabilityInterface]:
        """Get capability by name."""
        return self.capabilities.get(name)
        
    def list_capabilities(self) -> List[str]:
        """List all capabilities."""
        return list(self.capabilities.keys())
        
    async def execute_capability(self, request: CapabilityRequest) -> CapabilityResponse:
        """Execute capability with PATH Framework compliance."""
        start_utc = datetime.now(timezone.utc)
        
        capability = self.get_capability(request.capability)
        if not capability:
            return self._create_error_response(request, "Capability not found")
            
        try:
            # Validate parameters
            if not capability.validate_params(request.method, request.params):
                raise ValueError(f"Invalid parameters for {request.capability}.{request.method}")
                
            # Execute capability
            result = await capability.execute_capability(request.method, request.params)
            
            # Record completion
            end_utc = datetime.now(timezone.utc)
            duration = (end_utc - start_utc).total_seconds()
            self.rule_compliance["completion_format"] = True
            
            return CapabilityResponse(
                request_id=request.request_id,
                status=CapabilityStatus.SUCCESS,
                result=result,
                metadata={
                    "agent_id": self.agent_id,
                    "start_utc": start_utc.isoformat(),
                    "end_utc": end_utc.isoformat(),
                    "duration_seconds": duration
                },
                execution_time=duration
            )
            
        except Exception as e:
            self.logger.error(f"Capability execution failed: {e}")
            return self._create_error_response(request, str(e))
    
    def _load_profile(self, profile_name: str):
        """Load agent profile."""
        # Profiles register their own specialized capabilities
        try:
            if profile_name == "domain_analyst":
                from ..profiles.domain_analyst_profile import DomainAnalystProfile
                return DomainAnalystProfile()
            elif profile_name == "system_architect":
                from ..profiles.system_architect_profile import SystemArchitectProfile
                return SystemArchitectProfile()
            # Add other profiles as needed
            return None
        except Exception as e:
            self.logger.error(f"Failed to load profile {profile_name}: {e}")
            return None
    
    def _create_error_response(self, request: CapabilityRequest, error_msg: str) -> CapabilityResponse:
        """Create error response."""
        return CapabilityResponse(
            request_id=request.request_id,
            status=CapabilityStatus.ERROR,
            result={"error": error_msg},
            metadata={"agent_id": self.agent_id},
            execution_time=0.0
        )