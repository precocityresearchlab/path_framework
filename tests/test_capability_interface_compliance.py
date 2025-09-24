"""Tests for PATH Framework rule-compliant capability interface."""

import pytest
from unittest.mock import Mock
from datetime import datetime, timezone
from src.core.base_agent import BaseAgent
from src.core.capability_interface import CapabilityRequest, CapabilityStatus


class TestCapabilityInterfaceCompliance:
    """Test capability interface PATH Framework rule compliance."""
    
    @pytest.fixture
    def agent(self):
        return BaseAgent("test_profile")
    
    def test_capability_registration_validation(self, agent):
        """Test capability registration follows PATH Framework rules."""
        # Valid capability should register
        mock_capability = Mock()
        mock_capability.get_capability_name.return_value = "test_capability"
        mock_capability.get_supported_methods.return_value = ["test_method"]
        mock_capability.validate_params = Mock()
        mock_capability.execute_capability = Mock()
        
        agent.register_capability(mock_capability)
        assert "test_capability" in agent.capabilities
        
    def test_capability_registration_invalid_interface(self, agent):
        """Test capability registration rejects invalid interfaces."""
        invalid_capability = "not_a_capability"
        
        with pytest.raises(ValueError, match="must implement AgentCapabilityInterface"):
            agent.register_capability(invalid_capability)
            
    def test_capability_registration_missing_methods(self, agent):
        """Test capability registration validates required methods."""
        mock_capability = Mock()
        mock_capability.get_capability_name.return_value = "invalid_capability"
        mock_capability.get_supported_methods.return_value = []
        # Missing validate_params and execute_capability methods
        
        with pytest.raises(ValueError, match="does not meet PATH Framework standards"):
            agent.register_capability(mock_capability)
            
    @pytest.mark.asyncio
    async def test_capability_execution_with_utc_tracking(self, agent):
        """Test capability execution includes UTC time tracking."""
        mock_capability = Mock()
        mock_capability.get_capability_name.return_value = "test_cap"
        mock_capability.get_supported_methods.return_value = ["test_method"]
        mock_capability.validate_params.return_value = True
        mock_capability.execute_capability = Mock(return_value={"result": "success"})
        
        agent.register_capability(mock_capability)
        
        request = CapabilityRequest(
            capability="test_cap",
            method="test_method",
            params={},
            request_id="test-001"
        )
        
        response = await agent.execute_capability(request)
        
        assert response.status == CapabilityStatus.SUCCESS
        assert "start_utc" in response.metadata
        assert "end_utc" in response.metadata
        assert "duration_seconds" in response.metadata
        assert "rule_compliance" in response.metadata
        
    @pytest.mark.asyncio
    async def test_capability_execution_user_story_validation(self, agent):
        """Test capability execution validates user story when required."""
        mock_capability = Mock()
        mock_capability.get_capability_name.return_value = "code_generation"
        mock_capability.get_supported_methods.return_value = ["generate_source"]
        mock_capability.validate_params.return_value = True
        
        agent.register_capability(mock_capability)
        
        # Request without user story should fail
        request = CapabilityRequest(
            capability="code_generation",
            method="generate_source",
            params={},
            request_id="test-002"
        )
        
        response = await agent.execute_capability(request)
        assert response.status == CapabilityStatus.ERROR
        assert "User story validation failed" in response.result["error"]
        
    @pytest.mark.asyncio
    async def test_capability_execution_human_validation_required(self, agent):
        """Test capability execution requires human validation for critical operations."""
        mock_capability = Mock()
        mock_capability.get_capability_name.return_value = "command_execution"
        mock_capability.get_supported_methods.return_value = ["execute"]
        mock_capability.validate_params.return_value = True
        
        agent.register_capability(mock_capability)
        
        request = CapabilityRequest(
            capability="command_execution",
            method="execute",
            params={"command": "rm -rf /"},
            request_id="test-003"
        )
        
        response = await agent.execute_capability(request)
        
        # Should succeed because _get_human_approval returns True for testing
        # In production, this would require actual human approval
        assert "Human approval requested" in str(agent.logger.handlers)
        
    @pytest.mark.asyncio
    async def test_capability_execution_rule_compliance_tracking(self, agent):
        """Test capability execution updates rule compliance tracking."""
        mock_capability = Mock()
        mock_capability.get_capability_name.return_value = "test_cap"
        mock_capability.get_supported_methods.return_value = ["test_method"]
        mock_capability.validate_params.return_value = True
        mock_capability.execute_capability = Mock(return_value={"result": "success"})
        
        agent.register_capability(mock_capability)
        
        request = CapabilityRequest(
            capability="test_cap",
            method="test_method",
            params={},
            request_id="test-004"
        )
        
        response = await agent.execute_capability(request)
        
        assert agent.rule_compliance["completion_format"] is True
        assert response.metadata["rule_compliance"]["completion_format"] is True