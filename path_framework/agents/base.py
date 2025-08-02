"""
Base Agent class for PATH Framework.

All PATH Framework agents inherit from this base class.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from ..exceptions import AgentError, ValidationError


class AgentStatus(Enum):
    """Agent execution status."""
    IDLE = "idle"
    WORKING = "working"
    WAITING_HUMAN = "waiting_human"
    COMPLETED = "completed"
    ERROR = "error"
    PAUSED = "paused"


class Priority(Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class AgentMessage:
    """Message exchanged between agents."""
    id: UUID = field(default_factory=uuid4)
    sender: str = ""
    recipient: str = ""
    message_type: str = "info"
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    priority: Priority = Priority.MEDIUM
    requires_response: bool = False
    parent_id: Optional[UUID] = None


@dataclass  
class AgentTask:
    """Task assigned to an agent."""
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str = ""
    agent_id: str = ""
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    status: AgentStatus = AgentStatus.IDLE
    priority: Priority = Priority.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    progress: float = 0.0
    requires_human_approval: bool = False
    human_approved: bool = False


class BaseAgent(ABC):
    """
    Abstract base class for all PATH Framework agents.
    
    This class provides common functionality for:
    - Task execution and management
    - Communication with other agents  
    - Human approval workflows
    - Error handling and logging
    - Progress tracking
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        description: str,
        phase: str,
        capabilities: List[str],
        llm_provider: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.phase = phase
        self.capabilities = capabilities
        self.llm_provider = llm_provider or "openai"
        self.config = config or {}
        
        # Runtime state
        self.status = AgentStatus.IDLE
        self.current_task: Optional[AgentTask] = None
        self.message_queue: List[AgentMessage] = []
        self.task_history: List[AgentTask] = []
        
        # Setup logging
        self.logger = logging.getLogger(f"path.agent.{self.agent_id}")
        
        # Callbacks for external integration
        self.on_task_started = None
        self.on_task_completed = None
        self.on_human_approval_required = None
        self.on_error = None
        
    @abstractmethod
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a specific task assigned to this agent.
        
        Args:
            task: The task to execute
            
        Returns:
            Dict containing the task results
            
        Raises:
            AgentError: If task execution fails
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate input data for this agent.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValidationError: If validation fails
        """
        pass
    
    async def start_task(self, task: AgentTask) -> UUID:
        """
        Start executing a task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task ID
        """
        if self.status != AgentStatus.IDLE:
            raise AgentError(f"Agent {self.agent_id} is not idle (status: {self.status})")
            
        if not self.validate_input(task.input_data):
            raise ValidationError(f"Invalid input data for task {task.id}")
            
        self.current_task = task
        self.status = AgentStatus.WORKING
        task.status = AgentStatus.WORKING
        task.started_at = datetime.now()
        
        self.logger.info(f"Starting task: {task.name}")
        
        if self.on_task_started:
            await self.on_task_started(self, task)
            
        try:
            # Execute the task
            result = await self.execute_task(task)
            
            # Check if human approval is required
            if task.requires_human_approval and not task.human_approved:
                await self._request_human_approval(task, result)
                return task.id
                
            # Complete the task
            await self._complete_task(task, result)
            
        except Exception as e:
            await self._handle_task_error(task, e)
            
        return task.id
    
    async def _request_human_approval(self, task: AgentTask, result: Dict[str, Any]):
        """Request human approval for task results."""
        task.status = AgentStatus.WAITING_HUMAN
        self.status = AgentStatus.WAITING_HUMAN
        task.output_data = result
        
        self.logger.info(f"Requesting human approval for task: {task.name}")
        
        if self.on_human_approval_required:
            await self.on_human_approval_required(self, task, result)
    
    async def approve_task(self, task_id: UUID, approved: bool, feedback: str = ""):
        """
        Handle human approval response.
        
        Args:
            task_id: ID of the task being approved
            approved: Whether the task was approved
            feedback: Optional feedback from human
        """
        if not self.current_task or self.current_task.id != task_id:
            raise AgentError(f"No active task with ID {task_id}")
            
        task = self.current_task
        task.human_approved = approved
        
        if approved:
            self.logger.info(f"Task approved: {task.name}")
            await self._complete_task(task, task.output_data)
        else:
            self.logger.info(f"Task rejected: {task.name} - {feedback}")
            # Could implement retry logic here
            await self._handle_task_error(task, AgentError(f"Task rejected: {feedback}"))
    
    async def _complete_task(self, task: AgentTask, result: Dict[str, Any]):
        """Complete a task successfully."""
        task.status = AgentStatus.COMPLETED
        task.completed_at = datetime.now()
        task.output_data = result
        task.progress = 100.0
        
        self.status = AgentStatus.IDLE
        self.task_history.append(task)
        self.current_task = None
        
        self.logger.info(f"Task completed: {task.name}")
        
        if self.on_task_completed:
            await self.on_task_completed(self, task, result)
    
    async def _handle_task_error(self, task: AgentTask, error: Exception):
        """Handle task execution error."""
        task.status = AgentStatus.ERROR
        task.error_message = str(error)
        task.completed_at = datetime.now()
        
        self.status = AgentStatus.IDLE
        self.task_history.append(task)
        self.current_task = None
        
        self.logger.error(f"Task failed: {task.name} - {error}")
        
        if self.on_error:
            await self.on_error(self, task, error)
    
    async def send_message(self, recipient: str, message_type: str, content: Dict[str, Any], 
                          priority: Priority = Priority.MEDIUM, requires_response: bool = False) -> UUID:
        """
        Send a message to another agent.
        
        Args:
            recipient: ID of the recipient agent
            message_type: Type of message
            content: Message content
            priority: Message priority
            requires_response: Whether a response is required
            
        Returns:
            Message ID
        """
        message = AgentMessage(
            sender=self.agent_id,
            recipient=recipient,
            message_type=message_type,
            content=content,
            priority=priority,
            requires_response=requires_response
        )
        
        self.logger.debug(f"Sending message to {recipient}: {message_type}")
        
        # In a real implementation, this would route through a message broker
        # For now, we just log it
        return message.id
    
    async def receive_message(self, message: AgentMessage):
        """
        Receive a message from another agent.
        
        Args:
            message: The received message
        """
        self.message_queue.append(message)
        self.logger.debug(f"Received message from {message.sender}: {message.message_type}")
        
        # Process message based on type
        await self._process_message(message)
    
    async def _process_message(self, message: AgentMessage):
        """Process a received message."""
        # Override in subclasses for specific message handling
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status.value,
            "current_task": self.current_task.id if self.current_task else None,
            "task_count": len(self.task_history),
            "message_count": len(self.message_queue)
        }
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities."""
        return self.capabilities.copy()
    
    def __str__(self) -> str:
        return f"{self.name} ({self.agent_id}) - {self.status.value}"
    
    def __repr__(self) -> str:
        return f"BaseAgent(id='{self.agent_id}', name='{self.name}', status='{self.status.value}')"
