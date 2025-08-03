"""
Base Agent class for PATH Framework
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4


class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentTask:
    """Agent task definition"""
    task_id: str
    description: str
    parameters: Dict[str, Any]
    status: AgentStatus = AgentStatus.IDLE


class BaseAgent(ABC):
    """
    Base class for all PATH Framework agents
    """
    
    def __init__(self, agent_id: str, name: str, specialization: str, 
                 decision_authority: str, phase: int, config: Optional[Dict[str, Any]] = None):
        self.agent_id = agent_id
        self.name = name
        self.specialization = specialization
        self.decision_authority = decision_authority
        self.phase = phase
        self.config = config or {}
        self.logger = logging.getLogger(f"path.agent.{agent_id}")
        self.current_task: Optional[AgentTask] = None
        self.status = AgentStatus.IDLE
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an agent task"""
        pass
    
    @abstractmethod
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate agent output"""
        pass
