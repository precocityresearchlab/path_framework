"""Human validation interface for critical decisions."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime


class ValidationStatus(Enum):
    """Validation status options."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


@dataclass
class ValidationRequest:
    """Human validation request."""
    request_id: str
    agent_id: str
    decision_type: str
    context: Dict[str, Any]
    options: List[Dict[str, Any]]
    recommendation: str
    urgency: str = "normal"
    approver_role: str = "product_owner"


@dataclass
class ValidationResponse:
    """Human validation response."""
    request_id: str
    status: ValidationStatus
    selected_option: Optional[str]
    feedback: str
    approver_id: str
    timestamp: str


class HumanValidationInterface:
    """Interface for human validation workflows."""
    
    def __init__(self):
        self.logger = logging.getLogger("HumanValidationInterface")
        self.pending_requests = {}
        self.validation_history = {}
        self.approvers = {}
    
    async def request_validation(self, request: ValidationRequest) -> str:
        """Submit validation request to human approver."""
        self.pending_requests[request.request_id] = {
            **request.__dict__,
            "submitted_at": datetime.utcnow().isoformat(),
            "status": ValidationStatus.PENDING.value
        }
        
        # In real implementation, this would send notifications
        self.logger.info(f"Validation requested: {request.request_id} for {request.decision_type}")
        
        # Simulate notification to approver
        await self._notify_approver(request)
        
        return request.request_id
    
    async def submit_validation_response(self, response: ValidationResponse) -> None:
        """Submit human validation response."""
        if response.request_id not in self.pending_requests:
            raise ValueError(f"Unknown validation request: {response.request_id}")
        
        # Update request status
        self.pending_requests[response.request_id]["status"] = response.status.value
        self.pending_requests[response.request_id]["response"] = response.__dict__
        
        # Store in history
        self.validation_history[response.request_id] = {
            "request": self.pending_requests[response.request_id],
            "response": response.__dict__,
            "completed_at": datetime.utcnow().isoformat()
        }
        
        # Remove from pending
        del self.pending_requests[response.request_id]
        
        self.logger.info(f"Validation completed: {response.request_id} - {response.status.value}")
    
    async def get_pending_validations(self, approver_role: str = None) -> List[Dict[str, Any]]:
        """Get pending validation requests."""
        pending = []
        for request_id, request in self.pending_requests.items():
            if approver_role is None or request.get("approver_role") == approver_role:
                pending.append({
                    "request_id": request_id,
                    **request
                })
        
        # Sort by urgency and submission time
        pending.sort(key=lambda x: (
            0 if x.get("urgency") == "high" else 1,
            x.get("submitted_at", "")
        ))
        
        return pending
    
    async def get_validation_status(self, request_id: str) -> Optional[str]:
        """Get validation status."""
        if request_id in self.pending_requests:
            return self.pending_requests[request_id]["status"]
        elif request_id in self.validation_history:
            return self.validation_history[request_id]["response"]["status"]
        else:
            return None
    
    async def get_validation_history(self, agent_id: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get validation history."""
        history = []
        for request_id, record in self.validation_history.items():
            if agent_id is None or record["request"]["agent_id"] == agent_id:
                history.append({
                    "request_id": request_id,
                    **record
                })
        
        # Sort by completion time
        history.sort(key=lambda x: x.get("completed_at", ""), reverse=True)
        return history[:limit]
    
    async def register_approver(self, approver_id: str, role: str, capabilities: List[str]) -> None:
        """Register human approver."""
        self.approvers[approver_id] = {
            "role": role,
            "capabilities": capabilities,
            "registered_at": datetime.utcnow().isoformat(),
            "active": True
        }
        self.logger.info(f"Registered approver: {approver_id} with role {role}")
    
    async def get_approvers(self, role: str = None) -> List[Dict[str, Any]]:
        """Get available approvers."""
        approvers = []
        for approver_id, approver in self.approvers.items():
            if approver.get("active", True) and (role is None or approver.get("role") == role):
                approvers.append({
                    "approver_id": approver_id,
                    **approver
                })
        return approvers
    
    async def escalate_validation(self, request_id: str, reason: str) -> None:
        """Escalate validation to higher authority."""
        if request_id not in self.pending_requests:
            raise ValueError(f"Unknown validation request: {request_id}")
        
        request = self.pending_requests[request_id]
        
        # Update urgency and approver role
        request["urgency"] = "high"
        request["escalation_reason"] = reason
        request["escalated_at"] = datetime.utcnow().isoformat()
        
        # Determine escalation target
        current_role = request.get("approver_role", "product_owner")
        if current_role == "product_owner":
            request["approver_role"] = "senior_architect"
        elif current_role == "senior_architect":
            request["approver_role"] = "engineering_manager"
        
        self.logger.info(f"Escalated validation: {request_id} to {request['approver_role']}")
        
        # Notify new approver
        await self._notify_approver(ValidationRequest(**{
            k: v for k, v in request.items() 
            if k in ValidationRequest.__annotations__
        }))
    
    async def _notify_approver(self, request: ValidationRequest) -> None:
        """Send notification to approver."""
        # In real implementation, this would send email, Slack, etc.
        self.logger.info(f"Notifying {request.approver_role} for validation: {request.request_id}")
    
    def create_validation_request(
        self,
        agent_id: str,
        decision_type: str,
        context: Dict[str, Any],
        options: List[Dict[str, Any]],
        recommendation: str,
        urgency: str = "normal",
        approver_role: str = "product_owner"
    ) -> ValidationRequest:
        """Create validation request."""
        request_id = f"val_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{agent_id}"
        
        return ValidationRequest(
            request_id=request_id,
            agent_id=agent_id,
            decision_type=decision_type,
            context=context,
            options=options,
            recommendation=recommendation,
            urgency=urgency,
            approver_role=approver_role
        )
    
    def create_validation_response(
        self,
        request_id: str,
        status: ValidationStatus,
        selected_option: Optional[str],
        feedback: str,
        approver_id: str
    ) -> ValidationResponse:
        """Create validation response."""
        return ValidationResponse(
            request_id=request_id,
            status=status,
            selected_option=selected_option,
            feedback=feedback,
            approver_id=approver_id,
            timestamp=datetime.utcnow().isoformat()
        )