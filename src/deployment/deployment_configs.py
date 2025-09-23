"""Deployment configurations for PATH Framework agents."""

from typing import Dict, List, Any
from enum import Enum


class DeploymentMode(Enum):
    """Deployment mode options."""
    SINGLE_CONTAINER = "single_container"
    PHASE_CONTAINERS = "phase_containers"


class DeploymentConfig:
    """Deployment configuration manager."""
    
    CONFIGURATIONS = {
        DeploymentMode.SINGLE_CONTAINER: {
            "containers": 1,
            "agents_per_container": 16,
            "resources": {"cpu": "4", "memory": "16Gi"},
            "scaling": {"min": 1, "max": 3},
            "use_case": "Small teams (5-10 developers)"
        },
        
        DeploymentMode.PHASE_CONTAINERS: {
            "containers": 4,
            "agents_per_container": 4,
            "resources": {"cpu": "2", "memory": "8Gi"},
            "scaling": {"min": 1, "max": 5},
            "use_case": "Medium teams (10-50 developers)"
        },
        

    }
    
    @classmethod
    def get_config(cls, mode: DeploymentMode) -> Dict[str, Any]:
        """Get deployment configuration."""
        return cls.CONFIGURATIONS[mode]
    
    @classmethod
    def recommend_deployment(cls, team_size: int) -> DeploymentMode:
        """Recommend deployment mode based on team size."""
        if team_size <= 10:
            return DeploymentMode.SINGLE_CONTAINER
        else:
            return DeploymentMode.PHASE_CONTAINERS