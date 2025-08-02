"""Tests for the base agent functionality."""

import pytest
import asyncio
from uuid import uuid4
from datetime import datetime

from path_framework.agents.base import (
    BaseAgent, 
    AgentStatus, 
    AgentTask, 
    AgentMessage, 
    Priority
)
from path_framework.exceptions import AgentError, ValidationError


class TestAgent(BaseAgent):
    """Test agent implementation."""
    
    async def execute_task(self, task):
        """Simple test task execution."""
        return {"result": f"Task {task.name} completed"}
    
    def validate_input(self, input_data):
        """Simple validation."""
        return "required_field" in input_data


@pytest.mark.asyncio
async def test_agent_creation():
    """Test agent creation and basic properties."""
    agent = TestAgent(
        agent_id="test-agent-1",
        name="Test Agent",
        description="A test agent",
        phase="testing",
        capabilities=["test_execution", "validation"]
    )
    
    assert agent.agent_id == "test-agent-1"
    assert agent.name == "Test Agent"
    assert agent.status == AgentStatus.IDLE
    assert "test_execution" in agent.capabilities


@pytest.mark.asyncio 
async def test_task_execution():
    """Test successful task execution."""
    agent = TestAgent(
        agent_id="test-agent-2",
        name="Test Agent 2", 
        description="Another test agent",
        phase="testing",
        capabilities=["test_execution"]
    )
    
    task = AgentTask(
        name="test-task",
        description="A test task",
        agent_id="test-agent-2",
        input_data={"required_field": "test_value"}
    )
    
    task_id = await agent.start_task(task)
    
    assert task_id == task.id
    assert task.status == AgentStatus.COMPLETED
    assert "result" in task.output_data


@pytest.mark.asyncio
async def test_validation_error():
    """Test task validation failure."""
    agent = TestAgent(
        agent_id="test-agent-3",
        name="Test Agent 3",
        description="Test validation agent", 
        phase="testing",
        capabilities=["validation"]
    )
    
    task = AgentTask(
        name="invalid-task",
        description="Task with invalid input",
        agent_id="test-agent-3", 
        input_data={"wrong_field": "test_value"}  # Missing required_field
    )
    
    with pytest.raises(ValidationError):
        await agent.start_task(task)


@pytest.mark.asyncio
async def test_agent_busy_error():
    """Test error when agent is already busy."""
    agent = TestAgent(
        agent_id="test-agent-4",
        name="Test Agent 4",
        description="Busy test agent",
        phase="testing", 
        capabilities=["test_execution"]
    )
    
    # Set agent to working status
    agent.status = AgentStatus.WORKING
    
    task = AgentTask(
        name="test-task",
        description="A test task",
        agent_id="test-agent-4",
        input_data={"required_field": "test_value"}
    )
    
    with pytest.raises(AgentError):
        await agent.start_task(task)


def test_agent_status():
    """Test agent status reporting."""
    agent = TestAgent(
        agent_id="test-agent-5",
        name="Status Test Agent",
        description="Agent for testing status",
        phase="testing",
        capabilities=["status_reporting"]
    )
    
    status = agent.get_status()
    
    assert status["agent_id"] == "test-agent-5"
    assert status["name"] == "Status Test Agent"
    assert status["status"] == "idle"
    assert status["current_task"] is None
    assert status["task_count"] == 0


@pytest.mark.asyncio
async def test_message_sending():
    """Test agent message sending."""
    agent = TestAgent(
        agent_id="sender-agent",
        name="Sender Agent", 
        description="Agent that sends messages",
        phase="testing",
        capabilities=["messaging"]
    )
    
    message_id = await agent.send_message(
        recipient="receiver-agent",
        message_type="test_message",
        content={"test": "data"},
        priority=Priority.HIGH
    )
    
    assert message_id is not None


def test_agent_string_representation():
    """Test agent string representations."""
    agent = TestAgent(
        agent_id="string-test",
        name="String Test Agent",
        description="Agent for string testing",
        phase="testing",
        capabilities=["string_ops"]
    )
    
    str_repr = str(agent)
    assert "String Test Agent" in str_repr
    assert "string-test" in str_repr
    assert "idle" in str_repr
    
    repr_str = repr(agent)
    assert "BaseAgent" in repr_str
    assert "string-test" in repr_str
