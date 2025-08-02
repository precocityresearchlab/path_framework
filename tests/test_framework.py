"""Basic tests for PATH Framework core functionality."""

import pytest
from path_framework import get_version, get_agent_count, get_phase_count
from path_framework.exceptions import PathFrameworkError


def test_framework_metadata():
    """Test framework metadata functions."""
    assert get_version() == "1.0.0"
    assert get_agent_count() == 16
    assert get_phase_count() == 4


def test_exception_hierarchy():
    """Test that custom exceptions inherit from base."""
    with pytest.raises(PathFrameworkError):
        raise PathFrameworkError("Test error")


def test_framework_import():
    """Test that the framework can be imported."""
    import path_framework
    assert path_framework.__version__ == "1.0.0"
    assert path_framework.__author__ == "Precocity Research Lab"


def test_lazy_imports():
    """Test that lazy imports work."""
    from path_framework import get_config, get_cli_app
    
    # These should not raise ImportError
    config_class = get_config()
    cli_app = get_cli_app()
    
    assert config_class is not None
    assert cli_app is not None
