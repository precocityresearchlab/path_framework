"""Dynamic profile loader for agent specialization."""

from typing import Dict, Type
from ..core.base_agent import AgentProfile

# Phase 1 profiles
from .phase1.domain_analyst import DomainAnalystProfile
from .phase1.system_architect import SystemArchitectProfile
from .phase1.component_designer import ComponentDesignerProfile
from .phase1.integration_architect import IntegrationArchitectProfile

# Phase 2 profiles
from .phase2.tdd_orchestrator import TDDOrchestratorProfile
from .phase2.test_strategist import TestStrategistProfile
from .phase2.implementation_specialist import ImplementationSpecialistProfile
from .phase2.coverage_validator import CoverageValidatorProfile

# Phase 3 profiles
from .phase3.pipeline_architect import PipelineArchitectProfile
from .phase3.infrastructure_engineer import InfrastructureEngineerProfile
from .phase3.deployment_specialist import DeploymentSpecialistProfile
from .phase3.monitoring_analyst import MonitoringAnalystProfile

# Phase 4 profiles
from .phase4.reliability_engineer import ReliabilityEngineerProfile
from .phase4.operations_specialist import OperationsSpecialistProfile
from .phase4.performance_analyst import PerformanceAnalystProfile
from .phase4.security_operator import SecurityOperatorProfile


class ProfileLoader:
    """Loads agent profiles dynamically."""
    
    PROFILES: Dict[str, Type[AgentProfile]] = {
        # Phase 1: Software Engineering
        "domain_analyst": DomainAnalystProfile,
        "system_architect": SystemArchitectProfile,
        "component_designer": ComponentDesignerProfile,
        "integration_architect": IntegrationArchitectProfile,
        
        # Phase 2: Test-Driven Development
        "tdd_orchestrator": TDDOrchestratorProfile,
        "test_strategist": TestStrategistProfile,
        "implementation_specialist": ImplementationSpecialistProfile,
        "coverage_validator": CoverageValidatorProfile,
        
        # Phase 3: DevOps & Production Readiness
        "pipeline_architect": PipelineArchitectProfile,
        "infrastructure_engineer": InfrastructureEngineerProfile,
        "deployment_specialist": DeploymentSpecialistProfile,
        "monitoring_analyst": MonitoringAnalystProfile,
        
        # Phase 4: Production Operations
        "reliability_engineer": ReliabilityEngineerProfile,
        "operations_specialist": OperationsSpecialistProfile,
        "performance_analyst": PerformanceAnalystProfile,
        "security_operator": SecurityOperatorProfile,
    }
    
    @classmethod
    def load(cls, profile_name: str) -> AgentProfile:
        """Load profile by name."""
        if profile_name not in cls.PROFILES:
            raise ValueError(f"Unknown profile: {profile_name}")
        
        profile_class = cls.PROFILES[profile_name]
        return profile_class()
    
    @classmethod
    def list_profiles(cls) -> Dict[str, str]:
        """List available profiles with their agent codes."""
        return {
            name: profile_class().agent_code 
            for name, profile_class in cls.PROFILES.items()
        }