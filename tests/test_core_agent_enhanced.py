"""Test enhanced CoreAgent implementation for Task 1.1.1."""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, patch
import uuid

from src.core.core_agent import CoreAgent
from src.core.capability_interface import AgentCapabilityInterface


class MockCapability(AgentCapabilityInterface):
    """Mock capability for testing."""
    
    def get_capability_name(self) -> str:
        return "test_capability"
    
    def get_supported_methods(self) -> list:
        return ["test_method"]
    
    def validate_params(self, method: str, params: dict) -> bool:
        return True
    
    async def execute_capability(self, method: str, params: dict) -> dict:
        return {"result": "success"}


class TestCoreAgentEnhanced:
    """Test enhanced CoreAgent for Task 1.1.1 requirements."""
    
    def test_core_agent_initialization_with_unique_id(self):
        """Test CoreAgent generates unique agent ID."""
        agent1 = CoreAgent("DA", 1)
        agent2 = CoreAgent("DA", 1)
        
        # Should have different unique IDs
        assert agent1.agent_id != agent2.agent_id
        assert "PATH_DA" in agent1.agent_id
        assert "PATH_DA" in agent2.agent_id
    
    def test_five_essential_services_present(self):
        """Test all 5 essential services are present."""
        agent = CoreAgent("SA", 1)
        
        # 1. Agent identity
        assert hasattr(agent, 'agent_code')
        assert hasattr(agent, 'phase')
        assert hasattr(agent, 'agent_id')
        assert hasattr(agent, 'logger')
        
        # 2. Knowledge base access
        assert hasattr(agent, 'knowledge_base')
        
        # 3. Human validation interface
        assert hasattr(agent, 'validation')
        
        # 4. PATH Framework compliance tracking
        assert hasattr(agent, 'rule_compliance')
        assert hasattr(agent, 'session_utc')
        
        # 5. Capability registry
        assert hasattr(agent, 'capabilities')
        assert hasattr(agent, 'register_capability')
    
    def test_dynamic_capability_loading(self):
        """Test dynamic capability loading functionality."""
        agent = CoreAgent("CD", 1)
        mock_capability = MockCapability()
        
        # Should be able to register capability dynamically
        agent.register_capability(mock_capability)
        
        # Should be able to retrieve capability
        retrieved = agent.get_capability("test_capability")
        assert retrieved is mock_capability
        
        # Should appear in capability list
        assert "test_capability" in agent.list_capabilities()
    
    def test_utc_time_tracking_enhanced(self):
        """Test enhanced UTC time tracking."""
        with patch('src.core.core_agent.datetime') as mock_datetime:
            mock_utc = datetime(2025, 9, 23, 13, 16, 48, tzinfo=timezone.utc)
            mock_datetime.now.return_value = mock_utc
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            agent = CoreAgent("IA", 1)
            
            # Should track session start time
            assert agent.session_utc == mock_utc
            
            # Should have task timing methods
            assert hasattr(agent, 'start_task')
            assert hasattr(agent, 'end_task')
    
    def test_inheritance_compatibility(self):
        """Test TypeAgent can inherit all services without configuration."""
        
        class TestTypeAgent(CoreAgent):
            def __init__(self):
                super().__init__("TEST", 2)
        
        agent = TestTypeAgent()
        
        # Should automatically have all 5 services
        assert agent.knowledge_base is not None
        assert agent.validation is not None
        assert agent.rule_compliance is not None
        assert agent.capabilities is not None
        assert agent.logger is not None
    
    def test_path_framework_compliance_tracking(self):
        """Test PATH Framework compliance tracking."""
        agent = CoreAgent("TO", 2)
        
        # Should track compliance status
        assert "utc_tracking" in agent.rule_compliance
        assert "completion_format" in agent.rule_compliance
        assert "metadata_updated" in agent.rule_compliance
        
        # Should update compliance when capabilities registered
        mock_capability = MockCapability()
        agent.register_capability(mock_capability)
        assert agent.rule_compliance["metadata_updated"] is True
    
    def test_task_timing_functionality(self):
        """Test task timing methods work correctly."""
        agent = CoreAgent("CV", 2)
        
        # Start task
        agent.start_task("test_task")
        assert agent.task_start_utc is not None
        
        # End task
        duration = agent.end_task("test_task")
        assert agent.task_end_utc is not None
        assert duration >= 0.0
    
    def test_agent_communication_methods(self):
        """Test agent-to-agent communication methods."""
        agent = CoreAgent("PA", 3)
        
        # Test async methods exist and are callable
        import asyncio
        
        async def test_communication():
            # Store output
            await agent.store_output("test_op", {"result": "success"})
            
            # Get previous work
            result = await agent.get_previous_work("PATH_DA", "analysis")
            assert isinstance(result, dict)
        
        asyncio.run(test_communication())
    
    def test_human_validation_integration(self):
        """Test human validation integration."""
        agent = CoreAgent("IE", 3)
        
        # Should be able to request human approval
        with patch.object(agent.validation, 'request_validation', return_value=True):
            result = agent.request_human_approval("critical_operation", {"data": "test"})
            assert result is True
    
    def test_completion_tracking(self):
        """Test operation completion tracking."""
        agent = CoreAgent("DS", 3)
        
        # Mark operation complete
        agent.mark_complete("deployment", 5.5)
        assert agent.rule_compliance["completion_format"] is True
    
    def test_agent_info_retrieval(self):
        """Test agent information retrieval."""
        agent = CoreAgent("MA", 3)
        mock_capability = MockCapability()
        agent.register_capability(mock_capability)
        
        info = agent.get_agent_info()
        
        assert info["agent_code"] == "MA"
        assert info["phase"] == 3
        assert "PATH_MA" in info["agent_id"]
        assert "test_capability" in info["capabilities"]
        assert "session_utc" in info
        assert "rule_compliance" in info