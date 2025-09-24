"""Tests for BaseAgent TDD implementation - RED phase first."""

import pytest
from datetime import datetime, timezone
from src.core.base_agent import BaseAgent, AgentRequest


class TestBaseAgentTDD:
    """Test TDD enforcement in BaseAgent."""
    
    def test_agent_enforces_tests_first_rule(self):
        """RED: Test that agent enforces tests-first rule."""
        # This test will fail until we implement TDD enforcement
        agent = BaseAgent("test_profile")
        
        request = AgentRequest(
            request_id="test-001",
            operation="implement_feature",
            payload={
                "user_story": "As a developer, I want TDD enforcement, so that tests are written first",
                "feature": "user_authentication"
            }
        )
        
        # Should fail if no tests exist for the feature
        with pytest.raises(Exception, match="Tests must be written first"):
            agent.enforce_tdd_discipline(request)
    
    def test_agent_validates_red_green_refactor_cycle(self):
        """RED: Test Red-Green-Refactor cycle validation."""
        agent = BaseAgent("test_profile")
        
        # Should track TDD cycle state
        assert hasattr(agent, 'tdd_cycle_state')
        assert agent.tdd_cycle_state == "RED"  # Start in RED phase
        
        # Should allow progression from RED to GREEN
        agent.advance_to_green_phase()
        assert agent.tdd_cycle_state == "GREEN"
        
        # Should enforce cycle progression - can't advance from GREEN without completing
        with pytest.raises(Exception, match="Must complete RED phase first"):
            agent.tdd_cycle_state = "GREEN"
            agent.advance_to_green_phase()
    
    def test_agent_tracks_test_coverage(self):
        """RED: Test coverage tracking >90%."""
        agent = BaseAgent("test_profile")
        
        # Should fail if coverage below 90%
        with pytest.raises(Exception, match="Coverage must be >90%"):
            agent.validate_test_coverage(85.0)
    
    def test_agent_validates_mutation_score(self):
        """RED: Test mutation score validation >80%."""
        agent = BaseAgent("test_profile")
        
        # Should fail if mutation score below 80%
        with pytest.raises(Exception, match="Mutation score must be >80%"):
            agent.validate_mutation_score(75.0)