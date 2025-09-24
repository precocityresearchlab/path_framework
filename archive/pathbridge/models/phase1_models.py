"""
Phase 1 Data Models
PATH Framework - Process/AI/Technology/Human

Data models for Phase 1: Software Engineering agents
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


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
    acceptance_criteria: list[str] = field(default_factory=list)
    business_value: str = ""
    complexity_score: float = 0.0
    dependencies: list[str] = field(default_factory=list)
    stakeholders: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class DomainEntity:
    """Domain entity model"""

    name: str
    description: str
    attributes: dict[str, str] = field(default_factory=dict)
    behaviors: list[str] = field(default_factory=list)
    relationships: dict[str, str] = field(default_factory=dict)
    business_rules: list[str] = field(default_factory=list)


@dataclass
class BusinessRule:
    """Business rule specification"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    condition: str = ""
    action: str = ""
    priority: RequirementPriority = RequirementPriority.MEDIUM
    affected_entities: list[str] = field(default_factory=list)


@dataclass
class DomainModel:
    """Complete domain model"""

    name: str
    description: str
    entities: list[DomainEntity] = field(default_factory=list)
    value_objects: list[dict[str, Any]] = field(default_factory=list)
    aggregates: list[dict[str, Any]] = field(default_factory=list)
    bounded_contexts: list[str] = field(default_factory=list)
    domain_services: list[str] = field(default_factory=list)


@dataclass
class RequirementAnalysis:
    """Complete requirement analysis result"""

    project_name: str
    description: str
    requirements: list[Requirement] = field(default_factory=list)
    business_rules: list[BusinessRule] = field(default_factory=list)
    domain_model: DomainModel | None = None
    compliance_requirements: dict[str, str] = field(default_factory=dict)
    risk_assessment: dict[str, str] = field(default_factory=dict)
    analysis_confidence: float = 0.0


@dataclass
class StakeholderAnalysis:
    """Stakeholder analysis and mapping"""

    primary_stakeholders: list[str] = field(default_factory=list)
    secondary_stakeholders: list[str] = field(default_factory=list)
    stakeholder_concerns: dict[str, list[str]] = field(default_factory=dict)
    communication_plan: dict[str, str] = field(default_factory=dict)


@dataclass
class TechnologyStack:
    """Technology stack specification"""

    languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    databases: list[str] = field(default_factory=list)
    infrastructure: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    justification: dict[str, str] = field(default_factory=dict)


@dataclass
class SystemArchitecture:
    """System architecture specification"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    pattern: ArchitecturePattern = ArchitecturePattern.LAYERED
    technology_stack: TechnologyStack = field(default_factory=TechnologyStack)
    components: list[dict[str, Any]] = field(default_factory=list)
    interfaces: list[dict[str, Any]] = field(default_factory=list)
    quality_attributes: dict[str, str] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)


@dataclass
class ComponentDesign:
    """Component design specification"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    responsibilities: list[str] = field(default_factory=list)
    interfaces: list[dict[str, Any]] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    design_patterns: list[str] = field(default_factory=list)
    solid_compliance: dict[str, bool] = field(default_factory=dict)
    quality_metrics: dict[str, float] = field(default_factory=dict)


@dataclass
class IntegrationDesign:
    """Integration design specification"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    integration_patterns: list[str] = field(default_factory=list)
    api_specifications: list[dict[str, Any]] = field(default_factory=list)
    data_formats: list[str] = field(default_factory=list)
    security_requirements: list[str] = field(default_factory=list)
    error_handling: dict[str, str] = field(default_factory=dict)


@dataclass
class Phase1Output:
    """Complete Phase 1 output package"""

    project_name: str
    generated_at: datetime = field(default_factory=datetime.now)
    requirement_analysis: RequirementAnalysis | None = None
    domain_model: DomainModel | None = None
    system_architecture: SystemArchitecture | None = None
    component_designs: list[ComponentDesign] = field(default_factory=list)
    integration_design: IntegrationDesign | None = None
    validation_results: dict[str, bool] = field(default_factory=dict)
    human_approvals: dict[str, bool] = field(default_factory=dict)
    next_phase_inputs: dict[str, Any] = field(default_factory=dict)
