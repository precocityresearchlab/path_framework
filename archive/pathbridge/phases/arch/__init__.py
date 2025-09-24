"""
Arch Phase: Software Engineering & Architecture - Complete PATH Implementation
PATH Framework - Process/AI/Technology/Human

This module implements the full PATH model for Architecture:

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

# Phase Orchestrator (coordinates all PATH components)
from .ai.orchestrator import ArchOrchestrator  # AI orchestrator with fixed imports

# Human Components
from .human import ApprovalGates, CreativeInput, HumanOversight
from .process.quality_gates import ArchQualityGates
from .process.validation import ArchValidation

# Process Components
from .process.workflows import ArchWorkflows

# Technology Components
from .technology import ArchitectureTools, DesignPatterns, ModelingFrameworks

# from .simple_orchestrator import ArchOrchestrator  # Fallback disabled

__all__ = [
    "ApprovalGates",
    # Phase Orchestrator
    "ArchOrchestrator",
    "ArchQualityGates",
    "ArchValidation",
    # Process Components
    "ArchWorkflows",
    # Technology Components
    "ArchitectureTools",
    "CreativeInput",
    "DesignPatterns",
    # Human Components
    "HumanOversight",
    "ModelingFrameworks",
]

# Complete PATH Registry for Arch Phase
ARCH_PATH_COMPONENTS = {
    "process": {
        "workflows": ArchWorkflows,
        "quality_gates": ArchQualityGates,
        "validation": ArchValidation,
    },
    "ai": {
        # AI components will be added when imports are fixed
    },
    "technology": {
        "architecture_tools": ArchitectureTools,
        "design_patterns": DesignPatterns,
        "modeling_frameworks": ModelingFrameworks,
    },
    "human": {
        "oversight": HumanOversight,
        "approval_gates": ApprovalGates,
        "creative_input": CreativeInput,
    },
}
