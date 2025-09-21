"""
PATH Framework exceptions.

Custom exception classes for the PATH Framework.
"""


class PathFrameworkError(Exception):
    """Base exception for PATH Framework."""


class ConfigurationError(PathFrameworkError):
    """Raised when there's a configuration issue."""


class AgentError(PathFrameworkError):
    """Raised when there's an agent-related error."""


class ValidationError(PathFrameworkError):
    """Raised when validation fails."""


class CommunicationError(PathFrameworkError):
    """Raised when agent communication fails."""


class PhaseError(PathFrameworkError):
    """Raised when there's a phase execution error."""


class LLMError(PathFrameworkError):
    """Raised when there's an LLM provider error."""


class AuthenticationError(PathFrameworkError):
    """Raised when authentication fails."""


class RateLimitError(PathFrameworkError):
    """Raised when rate limits are exceeded."""


class TemplateError(PathFrameworkError):
    """Raised when template processing fails."""
