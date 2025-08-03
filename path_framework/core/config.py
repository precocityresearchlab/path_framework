"""
PATH Framework Configuration Management
Supports multiple configuration sources with priority hierarchy
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PathConfig:
    """
    Configuration manager for PATH Framework
    
    Priority order (highest to lowest):
    1. Explicit parameters
    2. Environment variables
    3. Config file
    4. Default values
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or self._find_config_file()
        self.file_config = self._load_config_file()
        
    def _find_config_file(self) -> Optional[str]:
        """Find configuration file in standard locations"""
        possible_paths = [
            "path_config.json",
            "config/path_config.json",
            os.path.expanduser("~/.path_framework/config.json"),
            "/etc/path_framework/config.json"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found config file: {path}")
                return path
        
        return None
    
    def _load_config_file(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_file or not os.path.exists(self.config_file):
            return {}
            
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                logger.info(f"Loaded config from {self.config_file}")
                return config
        except Exception as e:
            logger.warning(f"Failed to load config file {self.config_file}: {e}")
            return {}
    
    def get_llm_config(self, 
                      provider: Optional[str] = None,
                      api_key: Optional[str] = None, 
                      model: Optional[str] = None,
                      **kwargs) -> Dict[str, Any]:
        """
        Get LLM configuration with priority hierarchy
        
        Args:
            provider: Explicit provider override
            api_key: Explicit API key override
            model: Explicit model override
            **kwargs: Additional configuration options
            
        Returns:
            Configuration dictionary with resolved values
        """
        
        # Default values
        defaults = {
            "provider": "openai",
            "model": "gpt-4",
            "timeout": 30,
            "temperature": 0.1,
            "max_tokens": 4000
        }
        
        # File configuration
        file_llm_config = self.file_config.get("llm", {})
        
        # Environment variables with phase-specific model support
        env_config = {
            "provider": os.getenv("PATH_LLM_PROVIDER"),
            "model": self._get_phase_specific_model(kwargs.get("phase")), 
            "api_key": (os.getenv("OPENROUTER_API_KEY") or 
                       os.getenv("OPENAI_API_KEY") or 
                       os.getenv("ANTHROPIC_API_KEY")),
            "timeout": self._get_env_int("PATH_LLM_TIMEOUT"),
            "temperature": self._get_env_float("PATH_LLM_TEMPERATURE"),
            "max_tokens": self._get_env_int("PATH_LLM_MAX_TOKENS")
        }
        
        # Remove None values
        env_config = {k: v for k, v in env_config.items() if v is not None}
        
        # Explicit parameters
        explicit_config = {
            "provider": provider,
            "api_key": api_key,
            "model": model,
            **kwargs
        }
        
        # Remove None values
        explicit_config = {k: v for k, v in explicit_config.items() if v is not None}
        
        # Merge with priority: explicit > env > file > defaults
        final_config = {**defaults}
        final_config.update(file_llm_config)
        final_config.update(env_config)
        final_config.update(explicit_config)
        
        # Set provider-specific defaults for model if not specified
        if not explicit_config.get("model") and not env_config.get("model"):
            provider_val = final_config.get("provider", "openai")
            if provider_val == "openai":
                final_config["model"] = final_config.get("model", "gpt-4")
            elif provider_val == "anthropic":
                final_config["model"] = final_config.get("model", "claude-3-sonnet-20240229")
            elif provider_val == "openrouter":
                final_config["model"] = final_config.get("model", "openai/gpt-4")
            elif provider_val == "ollama":
                final_config["model"] = final_config.get("model", "llama2")
        
        # Validate required fields
        if not final_config.get("api_key") and final_config.get("provider") != "ollama":
            logger.warning(f"No API key found for provider: {final_config.get('provider')}")
        
        logger.debug(f"Final LLM config: {self._mask_sensitive(final_config)}")
        return final_config
    
    def _get_phase_specific_model(self, phase: Optional[int] = None) -> Optional[str]:
        """
        Get phase-specific model from environment variables
        
        Supports:
        - PATH_LLM_MODEL_PHASE1 (Architecture/Requirements)
        - PATH_LLM_MODEL_PHASE2 (Development Planning)  
        - PATH_LLM_MODEL_PHASE3 (Implementation)
        - PATH_LLM_MODEL_PHASE4 (Testing/Deployment)
        - PATH_LLM_MODEL (fallback for all phases)
        
        Args:
            phase: Phase number (1-4), if None uses general model
            
        Returns:
            Model name or None if not configured
        """
        if phase:
            phase_model = os.getenv(f"PATH_LLM_MODEL_PHASE{phase}")
            if phase_model:
                logger.debug(f"Using phase {phase} specific model: {phase_model}")
                return phase_model
        
        # Fallback to general model
        general_model = os.getenv("PATH_LLM_MODEL")
        if general_model:
            logger.debug(f"Using general model: {general_model}")
            return general_model
        
        return None
    
    def _get_env_int(self, key: str) -> Optional[int]:
        """Get integer value from environment variable"""
        value = os.getenv(key)
        if value:
            try:
                return int(value)
            except ValueError:
                logger.warning(f"Invalid integer value for {key}: {value}")
        return None
    
    def _get_env_float(self, key: str) -> Optional[float]:
        """Get float value from environment variable"""
        value = os.getenv(key)
        if value:
            try:
                return float(value)
            except ValueError:
                logger.warning(f"Invalid float value for {key}: {value}")
        return None
    
    def _mask_sensitive(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Mask sensitive information for logging"""
        masked = config.copy()
        if "api_key" in masked and masked["api_key"]:
            masked["api_key"] = f"{masked['api_key'][:8]}...{masked['api_key'][-4:]}"
        return masked
    
    def create_config_file(self, path: str, template: bool = True) -> None:
        """Create a configuration file template"""
        config_template = {
            "llm": {
                "provider": "openrouter",
                "model": "openai/gpt-4",  # Default fallback model
                "timeout": 30,
                "temperature": 0.1,
                "max_tokens": 4000,
                "phase_models": {
                    "phase1": "openai/gpt-4",  # Architecture & Requirements - Best reasoning
                    "phase2": "anthropic/claude-3-sonnet",  # Development Planning - Good planning
                    "phase3": "meta-llama/llama-2-70b-chat",  # Implementation - Fast coding
                    "phase4": "openai/gpt-3.5-turbo"  # Testing & Deployment - Cost efficient
                }
            },
            "agents": {
                "domain_analyst": {
                    "confidence_threshold": 0.8,
                    "phase": 1
                },
                "system_architect": {
                    "technology_preference": "cloud_native",
                    "phase": 1
                },
                "component_designer": {
                    "solid_principles": True,
                    "phase": 1
                },
                "integration_architect": {
                    "pattern_preference": "microservices",
                    "phase": 1
                }
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(config_template, f, indent=2)
        
        logger.info(f"Created config template: {path}")
        print(f"📝 Created configuration template: {path}")
        print("💡 Edit this file to customize your PATH Framework settings")


# Global config instance
_config_instance = None

def get_config() -> PathConfig:
    """Get global configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = PathConfig()
    return _config_instance

def set_config_file(config_file: str) -> None:
    """Set custom configuration file"""
    global _config_instance
    _config_instance = PathConfig(config_file)
