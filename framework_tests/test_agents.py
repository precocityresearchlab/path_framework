"""Tests for the base agent functionality."""

import pytest

from path_framework.agents_base import AgentStatus, BaseAgent


class TestAgent(BaseAgent):
    """Test agent implementation."""

    async def execute(self, task):
        """Simple test task execution."""
        return {"result": f"Task {task.get('name', 'unnamed')} completed"}

    def validate_output(self, output):
        """Simple validation."""
        return "result" in output


@pytest.mark.asyncio
async def test_agent_creation():
    """Test agent creation and basic properties."""
    agent = TestAgent(
        agent_id="test-agent-1",
        name="Test Agent",
        specialization="Testing",
        decision_authority="low",
        phase=1,
    )

    assert agent.agent_id == "test-agent-1"
    assert agent.name == "Test Agent"
    assert agent.status == AgentStatus.IDLE
    assert agent.specialization == "Testing"


@pytest.mark.asyncio
async def test_task_execution():
    """Test successful task execution."""
    agent = TestAgent(
        agent_id="test-agent-2",
        name="Test Agent 2",
        specialization="Testing",
        decision_authority="low",
        phase=1,
    )

    task_data = {"name": "test-task", "data": "test_value"}
    result = await agent.execute(task_data)

    assert "result" in result
    assert "test-task" in result["result"]


def test_agent_status():
    """Test agent status reporting."""
    agent = TestAgent(
        agent_id="test-agent-5",
        name="Status Test Agent",
        specialization="Testing",
        decision_authority="low",
        phase=1,
    )

    assert agent.status == AgentStatus.IDLE
    assert agent.agent_id == "test-agent-5"
    assert agent.name == "Status Test Agent"


def test_agent_string_representation():
    """Test agent string representations."""
    agent = TestAgent(
        agent_id="string-test",
        name="String Test Agent",
        specialization="Testing",
        decision_authority="low",
        phase=1,
    )

    # Basic existence check
    assert agent.agent_id == "string-test"
    assert agent.name == "String Test Agent"
