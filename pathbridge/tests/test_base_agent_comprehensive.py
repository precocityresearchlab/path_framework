"""Comprehensive tests for BaseAgent to achieve >90% coverage."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timezone
from src.core.base_agent import BaseAgent, AgentRequest, AgentResponse
from src.core.capability_interface import CapabilityRequest, CapabilityStatus


class TestBaseAgentComprehensive:
    """Comprehensive test coverage for BaseAgent."""
    
    @pytest.fixture
    def agent(self):
        return BaseAgent("test_profile")
    
    @pytest.fixture
    def sample_request(self):
        return AgentRequest(
            request_id="test-001",
            operation="test_operation",
            payload={"user_story": "As a user, I want functionality, So that I benefit"}
        )
    
    def test_agent_initialization(self, agent):
        """Test agent initialization and components."""
        assert agent.profile_name == "test_profile"
        assert agent.agent_id == "PATH_TEST_PROFILE"
        assert agent.session_utc is not None
        assert agent.tdd_cycle_state == "RED"
        assert len(agent.capabilities) == 4  # Standard capabilities
        
    def test_capability_registration(self, agent):
        """Test capability registration and retrieval."""
        mock_capability = Mock()
        mock_capability.get_capability_name.return_value = "test_capability"
        
        agent.register_capability(mock_capability)
        assert "test_capability" in agent.capabilities
        assert agent.get_capability("test_capability") == mock_capability
        
    def test_list_capabilities(self, agent):
        """Test listing all capabilities."""
        capabilities = agent.list_capabilities()
        expected = ["file_operations", "command_execution", "code_generation", "analysis_tools"]
        assert all(cap in capabilities for cap in expected)
        
    @pytest.mark.asyncio
    async def test_execute_capability_success(self, agent):
        """Test successful capability execution."""
        mock_capability = Mock()
        mock_capability.get_capability_name.return_value = "test_cap"
        mock_capability.validate_params.return_value = True
        mock_capability.execute_capability = AsyncMock(return_value={"result": "success"})
        
        agent.register_capability(mock_capability)
        
        request = CapabilityRequest(
            capability="test_cap",
            method="test_method",
            params={"param": "value"},
            request_id="cap-001"
        )
        
        response = await agent.execute_capability(request)
        assert response.status == CapabilityStatus.SUCCESS
        assert response.result == {"result": "success"}
        
    @pytest.mark.asyncio
    async def test_execute_capability_not_found(self, agent):
        """Test capability execution with unknown capability."""
        request = CapabilityRequest(
            capability="unknown",
            method="test",
            params={},
            request_id="cap-002"
        )
        
        response = await agent.execute_capability(request)
        assert response.status == CapabilityStatus.ERROR
        assert "not found" in response.result["error"]
        
    @pytest.mark.asyncio
    async def test_execute_capability_invalid_params(self, agent):
        """Test capability execution with invalid parameters."""
        mock_capability = Mock()
        mock_capability.get_capability_name.return_value = "test_cap"
        mock_capability.validate_params.return_value = False
        
        agent.register_capability(mock_capability)
        
        request = CapabilityRequest(
            capability="test_cap",
            method="test_method",
            params={},
            request_id="cap-003"
        )
        
        response = await agent.execute_capability(request)
        assert response.status == CapabilityStatus.ERROR
        assert "Invalid parameters" in response.result["error"]
        
    def test_validate_user_story_valid(self, agent):
        """Test user story validation with valid format."""
        story = "As a user, I want functionality, So that I benefit"
        assert agent._validate_user_story(story) is True
        
    def test_validate_user_story_invalid(self, agent):
        """Test user story validation with invalid format."""
        story = "Invalid story format"
        assert agent._validate_user_story(story) is False
        
    def test_validate_user_story_empty(self, agent):
        """Test user story validation with empty story."""
        assert agent._validate_user_story("") is False
        assert agent._validate_user_story(None) is False
        
    def test_validate_pre_task_checklist_success(self, agent):
        """Test pre-task validation success."""
        story = "As a user, I want functionality, So that I benefit"
        assert agent.validate_pre_task_checklist(story) is True
        
    def test_validate_pre_task_checklist_failure(self, agent):
        """Test pre-task validation failure."""
        assert agent.validate_pre_task_checklist("invalid story") is False
        
    def test_record_task_timing(self, agent):
        """Test task timing recording."""
        agent.record_task_start()
        assert agent.task_start_utc is not None
        
        duration = agent.record_task_end()
        assert agent.task_end_utc is not None
        assert "s" in duration
        
    def test_validate_post_task_checklist(self, agent):
        """Test post-task validation."""
        agent.record_task_start()
        agent.record_task_end()
        
        checklist = agent.validate_post_task_checklist()
        assert checklist["task_completed"] is True
        assert checklist["duration_calculated"] is True
        
    def test_generate_rule_compliance_report(self, agent):
        """Test rule compliance report generation."""
        agent.record_task_start()
        agent.record_task_end()
        
        report = agent.generate_rule_compliance_report()
        assert "agent_id" in report
        assert "session_utc" in report
        assert "rule_compliance" in report
        
    def test_tdd_cycle_progression(self, agent):
        """Test TDD cycle state progression."""
        assert agent.tdd_cycle_state == "RED"
        
        agent.advance_to_green_phase()
        assert agent.tdd_cycle_state == "GREEN"
        
        agent.advance_to_refactor_phase()
        assert agent.tdd_cycle_state == "REFACTOR"
        
        agent.complete_tdd_cycle()
        assert agent.tdd_cycle_state == "RED"
        
    def test_tdd_cycle_invalid_progression(self, agent):
        """Test invalid TDD cycle progression."""
        agent.tdd_cycle_state = "GREEN"
        with pytest.raises(Exception, match="Must complete RED phase first"):
            agent.advance_to_green_phase()
            
    def test_validate_test_coverage_success(self, agent):
        """Test test coverage validation success."""
        agent.validate_test_coverage(95.0)
        assert agent.test_coverage == 95.0
        assert agent.rule_compliance["quality_gates"] is True
        
    def test_validate_test_coverage_failure(self, agent):
        """Test test coverage validation failure."""
        with pytest.raises(Exception, match="Coverage must be >90%"):
            agent.validate_test_coverage(85.0)
            
    def test_validate_mutation_score_success(self, agent):
        """Test mutation score validation success."""
        agent.validate_mutation_score(85.0)
        assert agent.mutation_score == 85.0
        
    def test_validate_mutation_score_failure(self, agent):
        """Test mutation score validation failure."""
        with pytest.raises(Exception, match="Mutation score must be >80%"):
            agent.validate_mutation_score(75.0)
            
    def test_tests_exist_for_feature(self, agent):
        """Test feature test existence check."""
        # Always returns False to enforce test-first
        assert agent._tests_exist_for_feature("any_feature") is False
        
    @pytest.mark.asyncio
    async def test_process_request_success(self, agent, sample_request):
        """Test successful request processing."""
        with patch.object(agent.profile, 'execute', new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = {"status": "completed"}
            
            response = await agent.process_request(sample_request)
            assert response.status == "success"
            assert response.result == {"status": "completed"}
            assert "execution_duration" in response.metadata
            
    @pytest.mark.asyncio
    async def test_process_request_validation_failure(self, agent):
        """Test request processing with validation failure."""
        invalid_request = AgentRequest(
            request_id="test-002",
            operation="test_op",
            payload={"user_story": "invalid story"}
        )
        
        response = await agent.process_request(invalid_request)
        assert response.status == "validation_failed"
        assert "Pre-task validation failed" in response.result["error"]
        
    @pytest.mark.asyncio
    async def test_process_request_execution_error(self, agent, sample_request):
        """Test request processing with execution error."""
        with patch.object(agent.profile, 'execute', new_callable=AsyncMock) as mock_execute:
            mock_execute.side_effect = Exception("Execution failed")
            
            response = await agent.process_request(sample_request)
            assert response.status == "error"
            assert "Execution failed" in response.result["error"]