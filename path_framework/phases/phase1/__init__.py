"""
Phase 1: Software Engineering - Complete PATH Implementation
PATH Framework - Process/AI/Technology/Human

This module implements the full PATH model for Phase 1:

P - PROCESS: 7-step systematic workflow with quality gates
A - AI: 4 specialized AI agents for intelligent automation
T - TECHNOLOGY: Architecture tools, design patterns, validation frameworks
H - HUMAN: Oversight, creative decisions, quality validation, strategic direction

Components:
- PROCESS: Systematic workflows and quality gates
- AI: Domain Analyst, System Architect, Component Designer, Integration Architect
- TECHNOLOGY: Architecture tools, design patterns, modeling frameworks
- HUMAN: Human oversight, approval gates, creative architectural decisions
"""

# AI Components
from .ai.domain_analyst import AIDomainAnalyst
from .ai.system_architect import AISystemArchitect
from .ai.component_designer import AIComponentDesigner
from .ai.integration_architect import AIIntegrationArchitect
from .ai.phase1_orchestrator import Phase1Orchestrator

# Process Components
from .process.workflows import Phase1Workflows
from .process.quality_gates import Phase1QualityGates
from .process.validation import Phase1Validation

# Technology Components
from .technology.architecture_tools import ArchitectureTools
from .technology.design_patterns import DesignPatterns
from .technology.modeling_frameworks import ModelingFrameworks

# Human Components
from .human.oversight import HumanOversight
from .human.approval_gates import ApprovalGates
from .human.creative_input import CreativeInput

__all__ = [
    # AI Components
    "AIDomainAnalyst",
    "AISystemArchitect", 
    "AIComponentDesigner",
    "AIIntegrationArchitect",
    "Phase1Orchestrator",
    
    # Process Components
    "Phase1Workflows",
    "Phase1QualityGates", 
    "Phase1Validation",
    
    # Technology Components
    "ArchitectureTools",
    "DesignPatterns",
    "ModelingFrameworks",
    
    # Human Components
    "HumanOversight",
    "ApprovalGates",
    "CreativeInput"
]

# Complete PATH Registry for Phase 1
PHASE1_PATH_COMPONENTS = {
    "process": {
        "workflows": Phase1Workflows,
        "quality_gates": Phase1QualityGates,
        "validation": Phase1Validation
    },
    "ai": {
        "domain_analyst": AIDomainAnalyst,
        "system_architect": AISystemArchitect,
        "component_designer": AIComponentDesigner,
        "integration_architect": AIIntegrationArchitect,
        "orchestrator": Phase1Orchestrator
    },
    "technology": {
        "architecture_tools": ArchitectureTools,
        "design_patterns": DesignPatterns,
        "modeling_frameworks": ModelingFrameworks
    },
    "human": {
        "oversight": HumanOversight,
        "approval_gates": ApprovalGates,
        "creative_input": CreativeInput
    }
}
