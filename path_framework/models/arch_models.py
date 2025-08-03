"""
Phase 1 Data Models
PATH Framework - Process/AI/Technology/Human

Data models for Phase 1: Software Engineering agents
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from datetime import datetime
import uuid


class RequirementType(Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    BUSINESS = "business"
    TECHNICAL = "technical"
    COMPLIANCE = "compliance"


class RequirementPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ArchitecturePattern(Enum):
    MICROSERVICES = "microservices"
    MONOLITHIC = "monolithic"
    LAYERED = "layered"
    HEXAGONAL = "hexagonal"
    EVENT_DRIVEN = "event_driven"
    SERVERLESS = "serverless"


@dataclass
class Requirement:
    """Individual requirement specification"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    type: RequirementType = RequirementType.FUNCTIONAL
    priority: RequirementPriority = RequirementPriority.MEDIUM
    acceptance_criteria: List[str] = field(default_factory=list)
    business_value: str = ""
    complexity_score: float = 0.0
    dependencies: List[str] = field(default_factory=list)
    stakeholders: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class DomainEntity:
    """Domain entity model"""
    name: str
    description: str
    attributes: Dict[str, str] = field(default_factory=dict)
    behaviors: List[str] = field(default_factory=list)
    relationships: Dict[str, str] = field(default_factory=dict)
    business_rules: List[str] = field(default_factory=list)


@dataclass
class BusinessRule:
    """Business rule specification"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    condition: str = ""
    action: str = ""
    priority: RequirementPriority = RequirementPriority.MEDIUM
    affected_entities: List[str] = field(default_factory=list)


@dataclass
class DomainModel:
    """Complete domain model"""
    name: str
    description: str
    entities: List[DomainEntity] = field(default_factory=list)
    value_objects: List[Dict[str, Any]] = field(default_factory=list)
    aggregates: List[Dict[str, Any]] = field(default_factory=list)
    bounded_contexts: List[str] = field(default_factory=list)
    domain_services: List[str] = field(default_factory=list)


@dataclass
class RequirementAnalysis:
    """Complete requirement analysis result"""
    project_name: str
    description: str
    requirements: List[Requirement] = field(default_factory=list)
    business_rules: List[BusinessRule] = field(default_factory=list)
    domain_model: Optional[DomainModel] = None
    compliance_requirements: Dict[str, str] = field(default_factory=dict)
    risk_assessment: Dict[str, str] = field(default_factory=dict)
    analysis_confidence: float = 0.0


@dataclass
class StakeholderAnalysis:
    """Stakeholder analysis and mapping"""
    primary_stakeholders: List[str] = field(default_factory=list)
    secondary_stakeholders: List[str] = field(default_factory=list)
    stakeholder_concerns: Dict[str, List[str]] = field(default_factory=dict)
    communication_plan: Dict[str, str] = field(default_factory=dict)


@dataclass
class TechnologyStack:
    """Technology stack specification"""
    languages: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    databases: List[str] = field(default_factory=list)
    infrastructure: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    justification: Dict[str, str] = field(default_factory=dict)


@dataclass
class SystemArchitecture:
    """System architecture specification"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    pattern: ArchitecturePattern = ArchitecturePattern.LAYERED
    technology_stack: TechnologyStack = field(default_factory=TechnologyStack)
    components: List[Dict[str, Any]] = field(default_factory=list)
    interfaces: List[Dict[str, Any]] = field(default_factory=list)
    quality_attributes: Dict[str, str] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)


@dataclass
class ComponentDesign:
    """Component design specification"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    responsibilities: List[str] = field(default_factory=list)
    interfaces: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    design_patterns: List[str] = field(default_factory=list)
    solid_compliance: Dict[str, bool] = field(default_factory=dict)
    quality_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class IntegrationDesign:
    """Integration design specification"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    integration_patterns: List[str] = field(default_factory=list)
    api_specifications: List[Dict[str, Any]] = field(default_factory=list)
    data_formats: List[str] = field(default_factory=list)
    security_requirements: List[str] = field(default_factory=list)
    error_handling: Dict[str, str] = field(default_factory=dict)


@dataclass
class Phase1Output:
    """Complete Phase 1 output package"""
    project_name: str
    generated_at: datetime = field(default_factory=datetime.now)
    requirement_analysis: Optional[RequirementAnalysis] = None
    domain_model: Optional[DomainModel] = None
    system_architecture: Optional[SystemArchitecture] = None
    component_designs: List[ComponentDesign] = field(default_factory=list)
    integration_design: Optional[IntegrationDesign] = None
    validation_results: Dict[str, bool] = field(default_factory=dict)
    human_approvals: Dict[str, bool] = field(default_factory=dict)
    next_phase_inputs: Dict[str, Any] = field(default_factory=dict)
