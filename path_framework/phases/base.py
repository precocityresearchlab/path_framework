"""
Base Phase class for PATH Framework.

All PATH Framework phases inherit from this base class.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from ..agents_base import BaseAgent, AgentTask, AgentStatus
from ..exceptions import PhaseError


class PhaseStatus(Enum):
    """Phase execution status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    WAITING_HUMAN = "waiting_human"
    COMPLETED = "completed"
    ERROR = "error"
    PAUSED = "paused"


@dataclass
class PhaseResult:
    """Result of phase execution."""
    phase_id: str
    status: PhaseStatus
    artifacts: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    execution_time: Optional[float] = None
    agent_results: Dict[str, Any] = field(default_factory=dict)


class BasePhase(ABC):
    """
    Abstract base class for all PATH Framework phases.
    
    Each phase orchestrates a group of specialized agents to accomplish
    a specific aspect of software development.
    """
    
    def __init__(
        self,
        phase_id: str,
        name: str,
        description: str,
        agent_registry,  # AgentRegistry type hint would create circular import
        config: Optional[Dict[str, Any]] = None
    ):
        self.phase_id = phase_id
        self.name = name
        self.description = description
        self.agent_registry = agent_registry
        self.config = config or {}
        
        # Runtime state
        self.status = PhaseStatus.NOT_STARTED
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.current_step = 0
        self.total_steps = 0
        
        # Results tracking
        self.artifacts: Dict[str, Any] = {}
        self.metrics: Dict[str, Any] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
        # Agent management
        self.required_agents: List[str] = []
        self.active_tasks: Dict[UUID, AgentTask] = {}
        
        # Setup logging
        self.logger = logging.getLogger(f"path.phase.{self.phase_id}")
        
        # Callbacks
        self.on_phase_started = None
        self.on_phase_completed = None
        self.on_step_completed = None
        self.on_human_input_required = None
        self.on_error = None
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> PhaseResult:
        """
        Execute this phase with the given input data.
        
        Args:
            input_data: Input data for the phase
            
        Returns:
            PhaseResult containing the phase execution results
            
        Raises:
            PhaseError: If phase execution fails
        """
        pass
    
    @abstractmethod
    def get_required_agents(self) -> List[str]:
        """
        Get the list of agent types required for this phase.
        
        Returns:
            List of required agent type identifiers
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate input data for this phase.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    async def start_phase(self, input_data: Dict[str, Any]) -> PhaseResult:
        """
        Start executing this phase.
        
        Args:
            input_data: Input data for the phase
            
        Returns:
            PhaseResult containing execution results
        """
        if self.status != PhaseStatus.NOT_STARTED:
            raise PhaseError(f"Phase {self.phase_id} already started (status: {self.status})")
            
        if not self.validate_input(input_data):
            raise PhaseError(f"Invalid input data for phase {self.phase_id}")
            
        # Check required agents are available
        await self._check_required_agents()
        
        self.status = PhaseStatus.IN_PROGRESS
        self.started_at = datetime.now()
        
        self.logger.info(f"Starting phase: {self.name}")
        
        if self.on_phase_started:
            await self.on_phase_started(self, input_data)
        
        try:
            result = await self.execute(input_data)
            await self._complete_phase(result)
            return result
            
        except Exception as e:
            await self._handle_phase_error(e)
            raise
    
    async def _check_required_agents(self):
        """Check that all required agents are available."""
        missing_agents = []
        
        for agent_type in self.get_required_agents():
            available_agents = [
                agent for agent in self.agent_registry.list_agents()
                if agent_type in agent.capabilities and agent.status == AgentStatus.IDLE
            ]
            
            if not available_agents:
                missing_agents.append(agent_type)
        
        if missing_agents:
            raise PhaseError(f"Missing required agents: {missing_agents}")
    
    async def assign_task_to_agent(self, agent_capability: str, task: AgentTask) -> UUID:
        """
        Assign a task to an agent with specific capability.
        
        Args:
            agent_capability: Required capability
            task: Task to assign
            
        Returns:
            Task ID
            
        Raises:
            PhaseError: If no suitable agent found
        """
        agent = await self.agent_registry.find_available_agent([agent_capability])
        
        if not agent:
            raise PhaseError(f"No available agent with capability: {agent_capability}")
        
        task_id = await self.agent_registry.assign_task(agent.agent_id, task)
        self.active_tasks[task_id] = task
        
        self.logger.debug(f"Assigned task {task.name} to agent {agent.agent_id}")
        return task_id
    
    async def wait_for_task_completion(self, task_id: UUID, timeout: Optional[float] = None) -> Dict[str, Any]:
        """
        Wait for a specific task to complete.
        
        Args:
            task_id: ID of the task to wait for
            timeout: Optional timeout in seconds
            
        Returns:
            Task results
            
        Raises:
            PhaseError: If task fails or times out
        """
        if task_id not in self.active_tasks:
            raise PhaseError(f"Unknown task ID: {task_id}")
        
        task = self.active_tasks[task_id]
        start_time = datetime.now()
        
        while task.status not in [AgentStatus.COMPLETED, AgentStatus.ERROR]:
            if timeout and (datetime.now() - start_time).total_seconds() > timeout:
                raise PhaseError(f"Task {task_id} timed out after {timeout} seconds")
            
            await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
        
        if task.status == AgentStatus.ERROR:
            raise PhaseError(f"Task {task.name} failed: {task.error_message}")
        
        del self.active_tasks[task_id]
        return task.output_data
    
    async def wait_for_all_tasks(self, timeout: Optional[float] = None) -> Dict[UUID, Dict[str, Any]]:
        """
        Wait for all active tasks to complete.
        
        Args:
            timeout: Optional timeout in seconds
            
        Returns:
            Dictionary mapping task IDs to their results
        """
        results = {}
        
        for task_id in list(self.active_tasks.keys()):
            try:
                result = await self.wait_for_task_completion(task_id, timeout)
                results[task_id] = result
            except PhaseError as e:
                self.errors.append(str(e))
                
        return results
    
    async def _complete_phase(self, result: PhaseResult):
        """Complete the phase successfully."""
        self.status = PhaseStatus.COMPLETED
        self.completed_at = datetime.now()
        
        if self.started_at:
            result.execution_time = (self.completed_at - self.started_at).total_seconds()
        
        result.artifacts = self.artifacts
        result.metrics = self.metrics
        result.errors = self.errors
        result.warnings = self.warnings
        
        self.logger.info(f"Phase completed: {self.name}")
        
        if self.on_phase_completed:
            await self.on_phase_completed(self, result)
    
    async def _handle_phase_error(self, error: Exception):
        """Handle phase execution error."""
        self.status = PhaseStatus.ERROR
        self.completed_at = datetime.now()
        
        error_msg = str(error)
        self.errors.append(error_msg)
        
        self.logger.error(f"Phase failed: {self.name} - {error_msg}")
        
        if self.on_error:
            await self.on_error(self, error)
    
    def add_artifact(self, name: str, content: Any):
        """Add an artifact to the phase results."""
        self.artifacts[name] = content
        self.logger.debug(f"Added artifact: {name}")
    
    def add_metric(self, name: str, value: Any):
        """Add a metric to the phase results."""
        self.metrics[name] = value
        self.logger.debug(f"Recorded metric: {name} = {value}")
    
    def add_warning(self, message: str):
        """Add a warning message."""
        self.warnings.append(message)
        self.logger.warning(message)
    
    def update_progress(self, current_step: int, total_steps: int):
        """Update phase progress."""
        self.current_step = current_step
        self.total_steps = total_steps
        
        progress = (current_step / total_steps * 100) if total_steps > 0 else 0
        self.logger.debug(f"Phase progress: {progress:.1f}% ({current_step}/{total_steps})")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current phase status."""
        progress = (self.current_step / self.total_steps * 100) if self.total_steps > 0 else 0
        
        return {
            "phase_id": self.phase_id,
            "name": self.name,
            "status": self.status.value,
            "progress": progress,
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "active_tasks": len(self.active_tasks),
            "artifacts_count": len(self.artifacts),
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __str__(self) -> str:
        return f"{self.name} ({self.phase_id}) - {self.status.value}"
    
    def __repr__(self) -> str:
        return f"BasePhase(id='{self.phase_id}', name='{self.name}', status='{self.status.value}')"
