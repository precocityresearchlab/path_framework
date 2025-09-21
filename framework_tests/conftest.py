"""Test configuration for PATH Framework."""

import asyncio
import shutil
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        "project": {
            "name": "test-project",
            "version": "0.1.0",
            "description": "Test project",
        },
        "framework": {
            "version": "1.0.0",
            "phases": ["software_engineering", "tdd", "devops", "operations"],
        },
        "agents": {
            "llm_provider": "openai",
            "human_approval_required": True,
            "audit_trail_enabled": True,
        },
        "logging": {"level": "INFO", "format": "structured"},
    }


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""
    return {
        "choices": [
            {
                "message": {
                    "content": "This is a mock response from the LLM.",
                    "role": "assistant",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 15, "total_tokens": 25},
    }
