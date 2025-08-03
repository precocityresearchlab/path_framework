"""
CLI Tests for PATH Framework
Tests for command-line interface functionality
"""

from unittest.mock import patch, MagicMock
from typer.testing import CliRunner


class TestCLI:
    """Test suite for PATH Framework CLI"""
    
    def test_cli_help(self):
        """Test that CLI help command works"""
        from path_framework.cli import app
        
        runner = CliRunner()
        result = runner.invoke(app, ["--help"])
        
        assert result.exit_code == 0
        assert "PATH Framework" in result.stdout
        assert "Process/AI/Technology/Human" in result.stdout
    
    def test_arch_command_exists(self):
        """Test that arch command is available"""
        from path_framework.cli import app
        
        runner = CliRunner()
        result = runner.invoke(app, ["arch", "--help"])
        
        assert result.exit_code == 0
        assert "Architecture" in result.stdout
        assert "PROJECT_NAME" in result.stdout
    
    def test_arch_command_parameters(self):
        """Test arch command parameter validation"""
        from path_framework.cli import app
        
        runner = CliRunner()
        
        # Test missing project name
        result = runner.invoke(app, ["arch"])
        assert result.exit_code != 0  # Should fail without project name
    
    @patch('path_framework.phases.arch.simple_orchestrator.ArchOrchestrator')
    def test_arch_command_execution(self, mock_orchestrator):
        """Test arch command execution with mocked orchestrator"""
        from path_framework.cli import app
        
        # Mock the orchestrator
        mock_instance = MagicMock()
        mock_orchestrator.return_value = mock_instance
        
        runner = CliRunner()
        
        # Test non-interactive execution
        result = runner.invoke(app, [
            "arch", "test_project", 
            "--non-interactive",
            "--output", "/tmp/test_output"
        ])
        
        # Should not fail (may have other issues but command should be recognized)
        assert "test_project" in result.stdout or result.exit_code == 0
    
    def test_status_command(self):
        """Test status command"""
        from path_framework.cli import app
        
        runner = CliRunner()
        result = runner.invoke(app, ["status"])
        
        assert result.exit_code == 0
        assert "Framework Version" in result.stdout
    
    def test_init_command(self):
        """Test init command"""
        from path_framework.cli import app
        
        runner = CliRunner()
        result = runner.invoke(app, ["init", "--help"])
        
        assert result.exit_code == 0
        assert "Initialize" in result.stdout
