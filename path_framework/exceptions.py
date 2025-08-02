"""
PATH Framework exceptions.

Custom exception classes for the PATH Framework.
"""

class PathFrameworkError(Exception):
    """Base exception for PATH Framework."""
    pass


class ConfigurationError(PathFrameworkError):
    """Raised when there's a configuration issue."""
    pass


class AgentError(PathFrameworkError):
    """Raised when there's an agent-related error."""
    pass


class ValidationError(PathFrameworkError):
    """Raised when validation fails."""
    pass


class CommunicationError(PathFrameworkError):
    """Raised when agent communication fails."""
    pass


class PhaseError(PathFrameworkError):
    """Raised when there's a phase execution error."""
    pass


class LLMError(PathFrameworkError):
    """Raised when there's an LLM provider error."""
    pass


class AuthenticationError(PathFrameworkError):
    """Raised when authentication fails."""
    pass


class RateLimitError(PathFrameworkError):
    """Raised when rate limits are exceeded."""
    pass


class TemplateError(PathFrameworkError):
    """Raised when template processing fails."""
    pass
