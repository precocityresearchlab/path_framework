"""
PATH Framework Configuration Management

Handles configuration loading, validation, and environment-specific settings.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
import tomllib
import os


@dataclass
class LLMConfig:
    """LLM provider configuration."""
    provider: str = "openai"  # openai, anthropic, ollama
    api_key: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.1
    max_tokens: int = 4000
    timeout: int = 30


@dataclass
class AgentConfig:
    """Agent-specific configuration."""
    llm: LLMConfig = field(default_factory=LLMConfig)
    human_approval_required: bool = True
    audit_trail_enabled: bool = True
    decision_timeout: int = 300  # seconds
    retry_attempts: int = 3


@dataclass
class QualityGateConfig:
    """Quality gate configuration."""
    test_coverage_threshold: float = 90.0
    response_time_threshold: int = 200  # milliseconds
    security_scan_required: bool = True
    code_quality_threshold: float = 8.0
    documentation_required: bool = True


@dataclass
class EnvironmentConfig:
    """Environment-specific configuration."""
    development: str = "local"
    staging: str = "docker"
    production: str = "kubernetes"
    database_url: Optional[str] = None
    redis_url: Optional[str] = None


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "structured"  # structured, json, simple
    output: str = "logs/path.log"
    max_size: str = "100MB"
    backup_count: int = 5


@dataclass
class ProjectConfig:
    """Project-specific configuration."""
    name: str
    version: str = "0.1.0"
    description: str = ""
    domain: str = "general"
    complexity: str = "medium"  # simple, medium, complex
    team_size: int = 4
    timeline_weeks: int = 8


@dataclass
class FrameworkConfig:
    """Framework-level configuration."""
    version: str = "1.0.0"
    phases: List[str] = field(default_factory=lambda: [
        "software_engineering", "tdd", "devops", "operations"
    ])
    parallel_execution: bool = False
    emergency_mode: bool = False


@dataclass
class PathConfig:
    """Main PATH Framework configuration."""
    project: ProjectConfig
    framework: FrameworkConfig = field(default_factory=FrameworkConfig)
    agents: AgentConfig = field(default_factory=AgentConfig)
    quality_gates: QualityGateConfig = field(default_factory=QualityGateConfig)
    environments: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    @classmethod
    def from_file(cls, config_path: Path) -> "PathConfig":
        """Load configuration from a TOML file."""
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
        
        return cls.from_dict(data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PathConfig":
        """Create configuration from dictionary."""
        # Extract project config (required)
        project_data = data.get("project", {})
        if not project_data.get("name"):
            raise ValueError("Project name is required in configuration")
        
        project = ProjectConfig(
            name=project_data["name"],
            version=project_data.get("version", "0.1.0"),
            description=project_data.get("description", ""),
            domain=project_data.get("domain", "general"),
            complexity=project_data.get("complexity", "medium"),
            team_size=project_data.get("team_size", 4),
            timeline_weeks=project_data.get("timeline_weeks", 8),
        )
        
        # Framework config
        framework_data = data.get("framework", {})
        framework = FrameworkConfig(
            version=framework_data.get("version", "1.0.0"),
            phases=framework_data.get("phases", [
                "software_engineering", "tdd", "devops", "operations"
            ]),
            parallel_execution=framework_data.get("parallel_execution", False),
            emergency_mode=framework_data.get("emergency_mode", False),
        )
        
        # Agent config
        agents_data = data.get("agents", {})
        llm_data = agents_data.get("llm", {})
        llm = LLMConfig(
            provider=llm_data.get("provider", "openai"),
            api_key=llm_data.get("api_key") or os.getenv("OPENAI_API_KEY"),
            model=llm_data.get("model", "gpt-4"),
            temperature=llm_data.get("temperature", 0.1),
            max_tokens=llm_data.get("max_tokens", 4000),
            timeout=llm_data.get("timeout", 30),
        )
        
        agents = AgentConfig(
            llm=llm,
            human_approval_required=agents_data.get("human_approval_required", True),
            audit_trail_enabled=agents_data.get("audit_trail_enabled", True),
            decision_timeout=agents_data.get("decision_timeout", 300),
            retry_attempts=agents_data.get("retry_attempts", 3),
        )
        
        # Quality gates config
        quality_data = data.get("quality_gates", {})
        quality_gates = QualityGateConfig(
            test_coverage_threshold=quality_data.get("test_coverage_threshold", 90.0),
            response_time_threshold=quality_data.get("response_time_threshold", 200),
            security_scan_required=quality_data.get("security_scan_required", True),
            code_quality_threshold=quality_data.get("code_quality_threshold", 8.0),
            documentation_required=quality_data.get("documentation_required", True),
        )
        
        # Environment config
        env_data = data.get("environments", {})
        environments = EnvironmentConfig(
            development=env_data.get("development", "local"),
            staging=env_data.get("staging", "docker"),
            production=env_data.get("production", "kubernetes"),
            database_url=env_data.get("database_url") or os.getenv("DATABASE_URL"),
            redis_url=env_data.get("redis_url") or os.getenv("REDIS_URL"),
        )
        
        # Logging config
        logging_data = data.get("logging", {})
        logging = LoggingConfig(
            level=logging_data.get("level", "INFO"),
            format=logging_data.get("format", "structured"),
            output=logging_data.get("output", "logs/path.log"),
            max_size=logging_data.get("max_size", "100MB"),
            backup_count=logging_data.get("backup_count", 5),
        )
        
        return cls(
            project=project,
            framework=framework,
            agents=agents,
            quality_gates=quality_gates,
            environments=environments,
            logging=logging,
        )
    
    def validate(self) -> List[str]:
        """Validate configuration and return any errors."""
        errors = []
        
        # Validate project config
        if not self.project.name:
            errors.append("Project name cannot be empty")
        
        if self.project.complexity not in ["simple", "medium", "complex"]:
            errors.append("Project complexity must be 'simple', 'medium', or 'complex'")
        
        if self.project.team_size < 1:
            errors.append("Team size must be at least 1")
        
        if self.project.timeline_weeks < 1:
            errors.append("Timeline must be at least 1 week")
        
        # Validate LLM config
        if self.agents.llm.provider not in ["openai", "anthropic", "ollama"]:
            errors.append("LLM provider must be 'openai', 'anthropic', or 'ollama'")
        
        if self.agents.llm.provider in ["openai", "anthropic"] and not self.agents.llm.api_key:
            errors.append(f"API key required for {self.agents.llm.provider} provider")
        
        if self.agents.llm.temperature < 0 or self.agents.llm.temperature > 1:
            errors.append("LLM temperature must be between 0 and 1")
        
        # Validate quality gates
        if self.quality_gates.test_coverage_threshold < 0 or self.quality_gates.test_coverage_threshold > 100:
            errors.append("Test coverage threshold must be between 0 and 100")
        
        if self.quality_gates.response_time_threshold < 1:
            errors.append("Response time threshold must be at least 1ms")
        
        # Validate logging
        if self.logging.level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            errors.append("Logging level must be DEBUG, INFO, WARNING, ERROR, or CRITICAL")
        
        if self.logging.format not in ["structured", "json", "simple"]:
            errors.append("Logging format must be 'structured', 'json', or 'simple'")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "project": {
                "name": self.project.name,
                "version": self.project.version,
                "description": self.project.description,
                "domain": self.project.domain,
                "complexity": self.project.complexity,
                "team_size": self.project.team_size,
                "timeline_weeks": self.project.timeline_weeks,
            },
            "framework": {
                "version": self.framework.version,
                "phases": self.framework.phases,
                "parallel_execution": self.framework.parallel_execution,
                "emergency_mode": self.framework.emergency_mode,
            },
            "agents": {
                "llm": {
                    "provider": self.agents.llm.provider,
                    "model": self.agents.llm.model,
                    "temperature": self.agents.llm.temperature,
                    "max_tokens": self.agents.llm.max_tokens,
                    "timeout": self.agents.llm.timeout,
                },
                "human_approval_required": self.agents.human_approval_required,
                "audit_trail_enabled": self.agents.audit_trail_enabled,
                "decision_timeout": self.agents.decision_timeout,
                "retry_attempts": self.agents.retry_attempts,
            },
            "quality_gates": {
                "test_coverage_threshold": self.quality_gates.test_coverage_threshold,
                "response_time_threshold": self.quality_gates.response_time_threshold,
                "security_scan_required": self.quality_gates.security_scan_required,
                "code_quality_threshold": self.quality_gates.code_quality_threshold,
                "documentation_required": self.quality_gates.documentation_required,
            },
            "environments": {
                "development": self.environments.development,
                "staging": self.environments.staging,
                "production": self.environments.production,
            },
            "logging": {
                "level": self.logging.level,
                "format": self.logging.format,
                "output": self.logging.output,
                "max_size": self.logging.max_size,
                "backup_count": self.logging.backup_count,
            },
        }


def load_config(config_path: Optional[str] = None) -> PathConfig:
    """
    Load PATH Framework configuration from file or environment.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        PathConfig: Loaded configuration
        
    Raises:
        FileNotFoundError: If configuration file not found
        ValueError: If configuration is invalid
    """
    if config_path:
        path = Path(config_path)
    else:
        # Look for configuration in standard locations
        for candidate in [
            Path("path.toml"),
            Path("config/path.toml"),
            Path.home() / ".config" / "path" / "config.toml",
        ]:
            if candidate.exists():
                path = candidate
                break
        else:
            # Create default configuration
            return create_default_config()
    
    config = PathConfig.from_file(path)
    
    # Validate configuration
    errors = config.validate()
    if errors:
        raise ValueError(f"Configuration validation failed: {', '.join(errors)}")
    
    return config


def create_default_config() -> PathConfig:
    """Create a default configuration."""
    return PathConfig(
        project=ProjectConfig(
            name="default-project",
            description="Default PATH Framework project",
        )
    )


def save_config(config: PathConfig, config_path: Path):
    """Save configuration to file."""
    import tomli_w
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, "wb") as f:
        tomli_w.dump(config.to_dict(), f)
