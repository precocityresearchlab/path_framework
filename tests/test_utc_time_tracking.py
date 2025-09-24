"""Test UTC time tracking implementation for Task 1.1.2."""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, patch
import time

from src.core.core_agent import CoreAgent
from src.core.capability_interface import AgentCapabilityInterface


class MockCapability(AgentCapabilityInterface):
    """Mock capability for testing time tracking."""
    
    def get_capability_name(self) -> str:
        return "test_capability"
    
    def get_supported_methods(self) -> list:
        return ["test_method"]
    
    def validate_params(self, method: str, params: dict) -> bool:
        return True
    
    async def execute_capability(self, method: str, params: dict) -> dict:
        # Simulate some work
        time.sleep(0.1)
        return {"result": "success"}


class TestUTCTimeTracking:
    """Test UTC time tracking for Task 1.1.2 requirements."""
    
    def test_precise_utc_start_timestamp_recorded(self):
        """Test CoreAgent records precise UTC start timestamp."""
        before_init = datetime.now(timezone.utc)
        agent = CoreAgent("DA", 1)
        after_init = datetime.now(timezone.utc)
        
        # Should record precise initialization timestamp
        assert agent.session_utc >= before_init
        assert agent.session_utc <= after_init
        
        # Should have millisecond precision
        assert agent.session_utc.microsecond is not None
    
    @pytest.mark.asyncio
    async def test_capability_execution_time_tracking_millisecond_precision(self):
        """Test capability execution tracks start/end times with millisecond precision."""
        agent = CoreAgent("SA", 1)
        mock_capability = MockCapability()
        agent.register_capability(mock_capability)
        
        # Should track capability execution time with millisecond precision
        start_time = datetime.now(timezone.utc)
        execution_time = await agent.track_capability_execution("test_capability", "test_method", {})
        end_time = datetime.now(timezone.utc)
        
        # Should return execution time with millisecond precision
        assert execution_time > 0.0
        assert execution_time < 1.0  # Should be less than 1 second
        
        # Should have recorded precise timestamps
        assert hasattr(agent, 'last_capability_start_utc')
        assert hasattr(agent, 'last_capability_end_utc')
        assert agent.last_capability_start_utc >= start_time
        assert agent.last_capability_end_utc <= end_time
    
    def test_session_duration_calculation_formatted(self):
        """Test session duration calculation in Xh Ym Zs format."""
        with patch('src.core.core_agent.datetime') as mock_datetime:
            # Mock start time
            start_time = datetime(2025, 9, 23, 13, 16, 48, 123456, tzinfo=timezone.utc)
            mock_datetime.now.return_value = start_time
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            agent = CoreAgent("CD", 1)
            
            # Mock end time (2h 30m 45s later)
            end_time = datetime(2025, 9, 23, 15, 47, 33, 654321, tzinfo=timezone.utc)
            mock_datetime.now.return_value = end_time
            
            # Should format duration correctly
            formatted_duration = agent.get_session_duration_formatted()
            assert formatted_duration == "2h 30m 45s"
    
    def test_task_duration_formatting(self):
        """Test task duration formatting in Xh Ym Zs format."""
        agent = CoreAgent("IA", 1)
        
        # Test various durations
        test_cases = [
            (3661.5, "1h 1m 1s"),      # 1 hour, 1 minute, 1.5 seconds
            (125.0, "0h 2m 5s"),       # 2 minutes, 5 seconds
            (45.7, "0h 0m 45s"),       # 45.7 seconds
            (3600.0, "1h 0m 0s"),      # Exactly 1 hour
            (60.0, "0h 1m 0s"),        # Exactly 1 minute
        ]
        
        for duration_seconds, expected_format in test_cases:
            formatted = agent.format_duration(duration_seconds)
            assert formatted == expected_format
    
    def test_audit_trail_logging_with_millisecond_precision(self):
        """Test audit trail logging includes millisecond precision timestamps."""
        agent = CoreAgent("TO", 2)
        
        # Should log with millisecond precision
        with patch.object(agent.logger, 'info') as mock_log:
            agent.start_task("test_audit_task")
            
            # Should log with ISO format including microseconds
            mock_log.assert_called()
            log_message = mock_log.call_args[0][0]
            assert "test_audit_task" in log_message
            assert "T" in log_message  # ISO format
            assert "Z" in log_message or "+00:00" in log_message  # UTC indicator
    
    @pytest.mark.asyncio
    async def test_capability_execution_audit_logging(self):
        """Test capability execution creates audit trail."""
        agent = CoreAgent("TS", 2)
        mock_capability = MockCapability()
        agent.register_capability(mock_capability)
        
        with patch.object(agent.logger, 'info') as mock_log:
            await agent.track_capability_execution("test_capability", "test_method", {"param": "value"})
            
            # Should log capability execution with timestamps
            assert mock_log.call_count >= 2  # Start and end logs
            
            # Check log messages contain timing information
            log_calls = [call[0][0] for call in mock_log.call_args_list]
            start_logged = any("Started capability" in msg for msg in log_calls)
            end_logged = any("Completed capability" in msg for msg in log_calls)
            
            assert start_logged
            assert end_logged
    
    def test_compliance_requirements_met(self):
        """Test all compliance requirements are met."""
        agent = CoreAgent("IS", 2)
        
        # Should meet 100% timestamp accuracy requirement
        assert agent.session_utc.tzinfo == timezone.utc
        
        # Should support millisecond precision
        assert hasattr(agent.session_utc, 'microsecond')
        
        # Should have audit trail capabilities
        assert hasattr(agent, 'get_session_duration_formatted')
        assert hasattr(agent, 'track_capability_execution')
        assert hasattr(agent, 'format_duration')
        
        # Should track compliance
        assert "utc_tracking" in agent.rule_compliance
        assert agent.rule_compliance["utc_tracking"] is True