"""
PATH Framework - People-Agent Teams/Process/Technology

A comprehensive framework for systematic software engineering through
human-AI collaboration.

This package provides:
- 16 specialized AI agents across 4 development phases
- Human-AI collaboration protocols
- Quality assurance and validation systems
- Complete project orchestration
- Real-world implementation examples
"""

__version__ = "1.0.0"
__author__ = "Precocity Research Lab"
__email__ = "contact@precocityresearch.com"
__license__ = "MIT"

# Core components - imported lazily to avoid circular imports
__all__ = [
    "__author__",
    "__email__",
    "__license__",
    "__version__",
    "get_agent_count",
    "get_phase_count",
    "get_version",
]


def get_version() -> str:
    """Get the current version of PATH Framework."""
    return __version__


def get_agent_count() -> int:
    """Get the total number of specialized agents."""
    return 16


def get_phase_count() -> int:
    """Get the total number of development phases."""
    return 4


# Lazy imports to prevent circular dependencies
def get_config():
    """Get PATH configuration loader."""
    from .config import PathConfig

    return PathConfig


def get_cli_app():
    """Get the CLI application."""
    from .cli import app

    return app


def initialize_framework(config_path: str | None = None):
    """
    Initialize the PATH Framework with configuration.

    Args:
        config_path: Optional path to configuration file

    Returns:
        Configured framework instance
    """
    try:
        config_class = get_config()
        config = (
            config_class.load_from_file(config_path) if config_path else config_class()
        )
        return {"config": config, "status": "initialized"}
    except ImportError as e:
        return {
            "error": f"Framework components not yet implemented: {e}",
            "status": "partial",
        }
