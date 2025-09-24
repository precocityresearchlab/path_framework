"""
Utility functions for PATH Framework.

Common utilities used across the framework.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Any

from .config import PathConfig
from .exceptions import ConfigurationError


def setup_logging(config: dict[str, Any] | None = None) -> logging.Logger:
    """
    Setup logging for PATH Framework.

    Args:
        config: Optional logging configuration

    Returns:
        Configured logger instance
    """
    # Default logging config
    default_config = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "handlers": ["console"],
    }

    if config:
        default_config.update(config)

    # Configure logging level
    level = getattr(logging, default_config["level"].upper(), logging.INFO)

    # Setup root logger
    root_logger = logging.getLogger("path")
    root_logger.setLevel(level)

    # Clear existing handlers
    root_logger.handlers.clear()

    # Setup formatter
    formatter = logging.Formatter(default_config["format"])

    # Add console handler if requested
    if "console" in default_config["handlers"]:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # Add file handler if configured
    if "file" in default_config["handlers"] and "file_path" in default_config:
        file_handler = logging.FileHandler(default_config["file_path"])
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    root_logger.info("PATH Framework logging configured")
    return root_logger


def load_config(config_path: str | None = None) -> PathConfig:
    """
    Load PATH Framework configuration.

    Args:
        config_path: Optional path to configuration file

    Returns:
        PathConfig instance

    Raises:
        ConfigurationError: If configuration loading fails
    """
    try:
        if config_path:
            return PathConfig.load_from_file(config_path)
        else:
            return PathConfig()
    except Exception as e:
        raise ConfigurationError(f"Failed to load configuration: {e}")


def validate_environment(config: PathConfig) -> bool:
    """
    Validate the environment for PATH Framework.

    Args:
        config: Configuration to validate against

    Returns:
        True if environment is valid

    Raises:
        ConfigurationError: If environment validation fails
    """
    # Check Python version

    # Check required environment variables
    required_env_vars = getattr(config, "required_env_vars", [])
    missing_vars = []

    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        raise ConfigurationError(
            f"Missing required environment variables: {missing_vars}"
        )

    # Check if working directory is writable
    try:
        test_file = Path.cwd() / ".path_test"
        test_file.touch()
        test_file.unlink()
    except Exception:
        raise ConfigurationError("Current directory is not writable")

    return True


def get_project_root() -> Path:
    """
    Get the project root directory.

    Returns:
        Path to project root
    """
    # Look for common project indicators
    current_path = Path.cwd()

    while current_path != current_path.parent:
        # Check for common project files
        for indicator in ["pyproject.toml", ".git", "setup.py", "requirements.txt"]:
            if (current_path / indicator).exists():
                return current_path
        current_path = current_path.parent

    # If no indicators found, return current directory
    return Path.cwd()


def ensure_directory(path: Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure

    Returns:
        The directory path
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_filename(filename: str) -> str:
    """
    Convert a string to a safe filename.

    Args:
        filename: Original filename

    Returns:
        Safe filename string
    """
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    safe_name = filename

    for char in unsafe_chars:
        safe_name = safe_name.replace(char, "_")

    # Remove leading/trailing spaces and dots
    safe_name = safe_name.strip(" .")

    # Limit length
    if len(safe_name) > 255:
        safe_name = safe_name[:255]

    return safe_name


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate a string to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix
