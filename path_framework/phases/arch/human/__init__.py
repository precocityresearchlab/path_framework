"""Human Components for Architecture Phase

This module provides comprehensive human oversight, approval workflows, and creative input
mechanisms for architecture decisions, ensuring human expertise guides the AI-driven process.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

from path_framework.models.arch_models import SystemArchitecture, RequirementAnalysis


class ApprovalStatus(Enum):
    """Status of human approval process"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"
    ESCALATED = "escalated"


class StakeholderRole(Enum):
    """Types of stakeholders in architecture decisions"""
    ARCHITECT = "architect"
    TECH_LEAD = "tech_lead"
    PRODUCT_OWNER = "product_owner"
    SECURITY_OFFICER = "security_officer"
    OPERATIONS = "operations"
    BUSINESS_ANALYST = "business_analyst"
    DEVELOPER = "developer"
    QA_ENGINEER = "qa_engineer"


class ReviewType(Enum):
    """Types of architecture reviews"""
    DESIGN_REVIEW = "design_review"
    SECURITY_REVIEW = "security_review"
    PERFORMANCE_REVIEW = "performance_review"
    SCALABILITY_REVIEW = "scalability_review"
    COMPLIANCE_REVIEW = "compliance_review"
    COST_REVIEW = "cost_review"


@dataclass
class Stakeholder:
    """Stakeholder definition"""
    id: str
    name: str
    role: StakeholderRole
    email: str
    expertise_areas: List[str] = field(default_factory=list)
    approval_authority: List[str] = field(default_factory=list)
    notification_preferences: Dict[str, bool] = field(default_factory=dict)
    timezone: str = "UTC"


@dataclass
class ApprovalRequest:
    """Human approval request"""
    request_id: str
    title: str
    description: str
    artifact_type: str  # "architecture", "requirements", "design"
    artifact_data: Dict[str, Any]
    requested_by: str
    stakeholders: List[str]  # Stakeholder IDs
    approval_criteria: List[str]
    priority: str = "medium"  # low, medium, high, critical
    deadline: Optional[datetime] = None
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    comments: List[Dict[str, Any]] = field(default_factory=list)
    attachments: List[str] = field(default_factory=list)


@dataclass
class CreativeSession:
    """Creative input session"""
    session_id: str
    title: str
    objective: str
    facilitator: str
    participants: List[str]
    duration_minutes: int
    session_type: str  # "brainstorming", "design_thinking", "architecture_review"
    techniques: List[str] = field(default_factory=list)
    outcomes: List[str] = field(default_factory=list)
    follow_up_actions: List[Dict[str, Any]] = field(default_factory=list)
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class QualityGate:
    """Quality gate definition"""
    gate_id: str
    name: str
    description: str
    criteria: List[Dict[str, Any]]
    required_approvers: List[str]
    automated_checks: List[str] = field(default_factory=list)
    manual_checks: List[str] = field(default_factory=list)
    blocking: bool = True  # Whether gate blocks progression


class HumanOversight:
    """Human oversight for architecture decisions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stakeholders: Dict[str, Stakeholder] = {}
        self.pending_requests: Dict[str, ApprovalRequest] = {}
        self.quality_gates: Dict[str, QualityGate] = {}
        self._setup_default_stakeholders()
        self._setup_default_quality_gates()
    
    def _setup_default_stakeholders(self):
        """Setup default stakeholder roles"""
        default_stakeholders = [
            Stakeholder(
                id="lead_architect",
                name="Lead Architect",
                role=StakeholderRole.ARCHITECT,
                email="architect@company.com",
                expertise_areas=["system_design", "scalability", "patterns"],
                approval_authority=["architecture", "design_patterns", "technology_stack"],
                notification_preferences={"email": True, "slack": True}
            ),
            Stakeholder(
                id="tech_lead",
                name="Technical Lead",
                role=StakeholderRole.TECH_LEAD,
                email="techlead@company.com",
                expertise_areas=["implementation", "code_quality", "team_coordination"],
                approval_authority=["implementation_approach", "code_standards"],
                notification_preferences={"email": True, "slack": True}
            ),
            Stakeholder(
                id="security_officer",
                name="Security Officer",
                role=StakeholderRole.SECURITY_OFFICER,
                email="security@company.com",
                expertise_areas=["security", "compliance", "data_protection"],
                approval_authority=["security_architecture", "data_handling"],
                notification_preferences={"email": True, "phone": True}
            ),
            Stakeholder(
                id="product_owner",
                name="Product Owner",
                role=StakeholderRole.PRODUCT_OWNER,
                email="po@company.com",
                expertise_areas=["business_requirements", "user_experience"],
                approval_authority=["feature_requirements", "user_stories"],
                notification_preferences={"email": True, "slack": True}
            )
        ]
        
        for stakeholder in default_stakeholders:
            self.stakeholders[stakeholder.id] = stakeholder
    
    def _setup_default_quality_gates(self):
        """Setup default quality gates"""
        self.quality_gates = {
            "architecture_review": QualityGate(
                gate_id="architecture_review",
                name="Architecture Design Review",
                description="Comprehensive review of system architecture",
                criteria=[
                    {"type": "scalability", "threshold": "handles_expected_load"},
                    {"type": "maintainability", "threshold": "follows_solid_principles"},
                    {"type": "security", "threshold": "passes_security_review"},
                    {"type": "performance", "threshold": "meets_performance_requirements"}
                ],
                required_approvers=["lead_architect", "tech_lead"],
                automated_checks=["dependency_analysis", "pattern_compliance"],
                manual_checks=["design_coherence", "business_alignment"]
            ),
            "security_gate": QualityGate(
                gate_id="security_gate",
                name="Security Review Gate",
                description="Security and compliance validation",
                criteria=[
                    {"type": "authentication", "threshold": "multi_factor_enabled"},
                    {"type": "authorization", "threshold": "rbac_implemented"},
                    {"type": "data_encryption", "threshold": "encryption_at_rest_and_transit"},
                    {"type": "vulnerability", "threshold": "no_high_severity_issues"}
                ],
                required_approvers=["security_officer"],
                automated_checks=["security_scan", "dependency_vulnerability_check"],
                manual_checks=["architecture_security_review", "compliance_check"]
            )
        }
    
    def add_stakeholder(self, stakeholder: Stakeholder):
        """Add a new stakeholder"""
        self.stakeholders[stakeholder.id] = stakeholder
        self.logger.info(f"Added stakeholder: {stakeholder.name} ({stakeholder.role.value})")
    
    def request_approval(self, 
                        title: str,
                        description: str,
                        artifact_type: str,
                        artifact_data: Dict[str, Any],
                        stakeholder_roles: List[StakeholderRole],
                        priority: str = "medium") -> str:
        """Request approval from specified stakeholders"""
        
        # Find stakeholders by roles
        stakeholder_ids = [
            sid for sid, stakeholder in self.stakeholders.items()
            if stakeholder.role in stakeholder_roles
        ]
        
        request = ApprovalRequest(
            request_id=f"approval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=title,
            description=description,
            artifact_type=artifact_type,
            artifact_data=artifact_data,
            requested_by="system",
            stakeholders=stakeholder_ids,
            approval_criteria=self._get_approval_criteria(artifact_type),
            priority=priority,
            deadline=datetime.now() + timedelta(days=3)  # Default 3-day deadline
        )
        
        self.pending_requests[request.request_id] = request
        self.logger.info(f"Created approval request: {request.request_id}")
        
        # Notify stakeholders
        self._notify_stakeholders(request)
        
        return request.request_id
    
    def _get_approval_criteria(self, artifact_type: str) -> List[str]:
        """Get approval criteria based on artifact type"""
        criteria_map = {
            "architecture": [
                "Meets scalability requirements",
                "Follows architectural principles",
                "Security considerations addressed",
                "Performance requirements considered",
                "Maintainability ensured"
            ],
            "requirements": [
                "Business objectives aligned",
                "Functional requirements complete",
                "Non-functional requirements specified",
                "Acceptance criteria defined"
            ],
            "design": [
                "Design patterns appropriate",
                "Component interfaces well-defined",
                "Data flow clearly specified",
                "Error handling considered"
            ]
        }
        return criteria_map.get(artifact_type, ["General approval required"])
    
    def _notify_stakeholders(self, request: ApprovalRequest):
        """Notify stakeholders about approval request"""
        for stakeholder_id in request.stakeholders:
            stakeholder = self.stakeholders.get(stakeholder_id)
            if stakeholder:
                self.logger.info(f"Notifying {stakeholder.name} about approval request {request.request_id}")
                # In real implementation, send email/slack notification
    
    def provide_approval(self, 
                        request_id: str, 
                        stakeholder_id: str, 
                        decision: ApprovalStatus,
                        comments: str = "",
                        suggestions: List[str] = None) -> bool:
        """Provide approval decision"""
        
        if request_id not in self.pending_requests:
            self.logger.error(f"Approval request {request_id} not found")
            return False
        
        request = self.pending_requests[request_id]
        
        if stakeholder_id not in request.stakeholders:
            self.logger.error(f"Stakeholder {stakeholder_id} not authorized for request {request_id}")
            return False
        
        # Add comment with decision
        comment = {
            "stakeholder_id": stakeholder_id,
            "decision": decision.value,
            "comments": comments,
            "suggestions": suggestions or [],
            "timestamp": datetime.now().isoformat()
        }
        request.comments.append(comment)
        
        # Check if all required approvals received
        if self._check_approval_completion(request):
            request.status = ApprovalStatus.APPROVED
            self.logger.info(f"Approval request {request_id} fully approved")
        elif decision == ApprovalStatus.REJECTED:
            request.status = ApprovalStatus.REJECTED
            self.logger.info(f"Approval request {request_id} rejected by {stakeholder_id}")
        
        return True
    
    def _check_approval_completion(self, request: ApprovalRequest) -> bool:
        """Check if all required approvals are received"""
        approved_stakeholders = {
            comment["stakeholder_id"] 
            for comment in request.comments 
            if comment["decision"] == ApprovalStatus.APPROVED.value
        }
        
        return len(approved_stakeholders) >= len(request.stakeholders)
    
    def get_pending_approvals(self, stakeholder_id: str = None) -> List[ApprovalRequest]:
        """Get pending approval requests"""
        requests = [req for req in self.pending_requests.values() 
                   if req.status == ApprovalStatus.PENDING]
        
        if stakeholder_id:
            requests = [req for req in requests if stakeholder_id in req.stakeholders]
        
        return requests
    
    def escalate_request(self, request_id: str, reason: str) -> bool:
        """Escalate approval request"""
        if request_id not in self.pending_requests:
            return False
        
        request = self.pending_requests[request_id]
        request.status = ApprovalStatus.ESCALATED
        
        # Add escalation comment
        comment = {
            "type": "escalation",
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }
        request.comments.append(comment)
        
        self.logger.warning(f"Approval request {request_id} escalated: {reason}")
        return True


class ApprovalGates:
    """Human approval gates for architecture workflow"""
    
    def __init__(self, oversight: HumanOversight):
        self.oversight = oversight
        self.logger = logging.getLogger(__name__)
    
    def validate_quality_gate(self, gate_id: str, artifact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate artifact against quality gate"""
        
        if gate_id not in self.oversight.quality_gates:
            return {"status": "error", "message": f"Quality gate {gate_id} not found"}
        
        gate = self.oversight.quality_gates[gate_id]
        results = {
            "gate_id": gate_id,
            "status": "pending",
            "automated_results": {},
            "manual_checks_required": gate.manual_checks,
            "approval_required": len(gate.required_approvers) > 0
        }
        
        # Run automated checks
        for check in gate.automated_checks:
            results["automated_results"][check] = self._run_automated_check(check, artifact_data)
        
        # Check if automated checks pass
        automated_passed = all(
            result.get("passed", False) 
            for result in results["automated_results"].values()
        )
        
        if automated_passed and not gate.manual_checks and not gate.required_approvers:
            results["status"] = "passed"
        elif not automated_passed and gate.blocking:
            results["status"] = "failed"
        else:
            results["status"] = "requires_human_review"
            
            # Request human approval if needed
            if gate.required_approvers:
                approval_request_id = self.oversight.request_approval(
                    title=f"Quality Gate: {gate.name}",
                    description=gate.description,
                    artifact_type="quality_gate_validation",
                    artifact_data=artifact_data,
                    stakeholder_roles=[
                        self.oversight.stakeholders[approver].role 
                        for approver in gate.required_approvers 
                        if approver in self.oversight.stakeholders
                    ]
                )
                results["approval_request_id"] = approval_request_id
        
        return results
    
    def _run_automated_check(self, check_name: str, artifact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run automated quality check"""
        # Simulate automated checks
        check_results = {
            "dependency_analysis": {"passed": True, "message": "No circular dependencies found"},
            "pattern_compliance": {"passed": True, "message": "Follows architectural patterns"},
            "security_scan": {"passed": True, "message": "No security vulnerabilities detected"},
            "dependency_vulnerability_check": {"passed": True, "message": "All dependencies are secure"}
        }
        
        return check_results.get(check_name, {"passed": False, "message": f"Unknown check: {check_name}"})


class CreativeInput:
    """Human creative input mechanisms"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.creative_sessions: Dict[str, CreativeSession] = {}
        self.techniques = self._load_creative_techniques()
    
    def _load_creative_techniques(self) -> Dict[str, Dict[str, Any]]:
        """Load creative techniques for architecture sessions"""
        return {
            "brainstorming": {
                "description": "Generate creative ideas without judgment",
                "duration": 30,
                "facilitator_guide": [
                    "Start with clear problem statement",
                    "Encourage wild ideas",
                    "Build on others' ideas", 
                    "Stay focused on the topic",
                    "No criticism during ideation"
                ],
                "tools": ["sticky notes", "whiteboard", "timer"]
            },
            
            "design_thinking": {
                "description": "Human-centered design approach",
                "duration": 120,
                "phases": ["empathize", "define", "ideate", "prototype", "test"],
                "facilitator_guide": [
                    "Focus on user needs and pain points",
                    "Define clear problem statements",
                    "Generate multiple solution options",
                    "Create low-fidelity prototypes",
                    "Test with real users or stakeholders"
                ],
                "tools": ["personas", "journey maps", "prototyping materials"]
            },
            
            "architecture_review": {
                "description": "Collaborative architecture assessment",
                "duration": 90,
                "facilitator_guide": [
                    "Present architecture overview",
                    "Review against quality attributes",
                    "Identify risks and trade-offs",
                    "Discuss alternative approaches",
                    "Document decisions and rationale"
                ],
                "tools": ["architecture diagrams", "checklists", "decision matrix"]
            },
            
            "scenario_planning": {
                "description": "Explore different future scenarios",
                "duration": 60,
                "facilitator_guide": [
                    "Define key uncertainties",
                    "Create scenario matrices",
                    "Develop detailed scenarios",
                    "Assess architecture robustness",
                    "Identify adaptation strategies"
                ],
                "tools": ["scenario templates", "impact assessment", "contingency plans"]
            }
        }
    
    def schedule_creative_session(self,
                                title: str,
                                objective: str,
                                facilitator: str,
                                participants: List[str],
                                session_type: str,
                                scheduled_at: datetime = None) -> str:
        """Schedule a creative input session"""
        
        if session_type not in self.techniques:
            raise ValueError(f"Unknown session type: {session_type}")
        
        technique = self.techniques[session_type]
        session = CreativeSession(
            session_id=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=title,
            objective=objective,
            facilitator=facilitator,
            participants=participants,
            duration_minutes=technique.get("duration", 60),
            session_type=session_type,
            techniques=[session_type],
            scheduled_at=scheduled_at or datetime.now() + timedelta(days=1)
        )
        
        self.creative_sessions[session.session_id] = session
        self.logger.info(f"Scheduled creative session: {session.session_id}")
        
        return session.session_id
    
    def conduct_session(self, session_id: str) -> Dict[str, Any]:
        """Conduct creative session and capture outcomes"""
        
        if session_id not in self.creative_sessions:
            return {"error": "Session not found"}
        
        session = self.creative_sessions[session_id]
        technique = self.techniques[session.session_type]
        
        # Simulate session outcomes
        session.outcomes = self._generate_session_outcomes(session.session_type, session.objective)
        session.follow_up_actions = self._generate_follow_up_actions(session.outcomes)
        session.completed_at = datetime.now()
        
        results = {
            "session_id": session_id,
            "technique_used": session.session_type,
            "outcomes": session.outcomes,
            "follow_up_actions": session.follow_up_actions,
            "participants": session.participants,
            "duration": session.duration_minutes,
            "facilitator_notes": technique.get("facilitator_guide", [])
        }
        
        self.logger.info(f"Completed creative session: {session_id}")
        return results
    
    def _generate_session_outcomes(self, session_type: str, objective: str) -> List[str]:
        """Generate sample outcomes based on session type"""
        outcomes_map = {
            "brainstorming": [
                "Identified 5 alternative architecture patterns",
                "Generated 12 innovative integration approaches", 
                "Proposed 3 novel caching strategies",
                "Suggested 4 user experience improvements"
            ],
            "design_thinking": [
                "Defined 3 key user personas",
                "Mapped critical user journeys",
                "Identified 6 pain points in current system",
                "Prototyped 2 alternative interfaces"
            ],
            "architecture_review": [
                "Validated scalability approach",
                "Identified 3 potential risks",
                "Recommended security enhancements",
                "Agreed on technology choices"
            ],
            "scenario_planning": [
                "Developed 4 future scenarios",
                "Assessed architecture flexibility",
                "Identified adaptation points",
                "Created contingency plans"
            ]
        }
        
        return outcomes_map.get(session_type, ["Session completed successfully"])
    
    def _generate_follow_up_actions(self, outcomes: List[str]) -> List[Dict[str, Any]]:
        """Generate follow-up actions from session outcomes"""
        actions = []
        for i, outcome in enumerate(outcomes[:3]):  # Limit to top 3 outcomes
            actions.append({
                "action_id": f"action_{i+1}",
                "description": f"Implement solution from: {outcome}",
                "assigned_to": "architecture_team",
                "due_date": (datetime.now() + timedelta(weeks=2)).isoformat(),
                "priority": "medium"
            })
        
        return actions
    
    def get_session_report(self, session_id: str) -> Dict[str, Any]:
        """Get detailed session report"""
        if session_id not in self.creative_sessions:
            return {"error": "Session not found"}
        
        session = self.creative_sessions[session_id]
        
        return {
            "session_info": {
                "id": session.session_id,
                "title": session.title,
                "objective": session.objective,
                "type": session.session_type,
                "facilitator": session.facilitator,
                "participants": session.participants,
                "scheduled_at": session.scheduled_at.isoformat() if session.scheduled_at else None,
                "completed_at": session.completed_at.isoformat() if session.completed_at else None,
                "duration_minutes": session.duration_minutes
            },
            "outcomes": session.outcomes,
            "follow_up_actions": session.follow_up_actions,
            "techniques_used": session.techniques,
            "status": "completed" if session.completed_at else "scheduled"
        }
