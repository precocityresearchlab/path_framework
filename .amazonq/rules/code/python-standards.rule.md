# Python Standards

## Purpose
Defines Python-specific coding standards and best practices for PATH Framework projects.

## Instructions
- Use f-strings for string formatting instead of .format() or % formatting. (ID: USE_F_STRINGS)
- Prefer pathlib.Path over os.path for file system operations. (ID: USE_PATHLIB)
- Use dataclasses or Pydantic models for structured data. (ID: USE_DATACLASSES)
- Implement context managers (with statements) for resource management. (ID: USE_CONTEXT_MANAGERS)
- Use list/dict comprehensions for simple transformations. (ID: USE_COMPREHENSIONS)
- Follow Python's "batteries included" philosophy - use standard library first. (ID: PREFER_STDLIB)
- Use uv for Python package management and virtual environments. (ID: USE_UV_PACKAGE_MANAGER)
- Always run ruff check and ruff format before committing code. (ID: ALWAYS_USE_RUFF)
- Use pyproject.toml for project configuration with uv. (ID: USE_PYPROJECT_TOML)
- Run uv sync to install dependencies, uv add to add new packages. (ID: UV_DEPENDENCY_MANAGEMENT)
- Use uv run for executing scripts and commands in virtual environment. (ID: UV_RUN_COMMANDS)
- Configure ruff in pyproject.toml for consistent linting and formatting. (ID: CONFIGURE_RUFF)
- Implement proper __str__ and __repr__ methods for custom classes. (ID: IMPLEMENT_STR_REPR)

## Priority
Medium

## Error Handling
- If old string formatting found, refactor to use f-strings.
- If os.path used, migrate to pathlib.Path for better readability.
- If resource leaks detected, implement proper context managers.
- If pip or poetry found, migrate to uv for package management.
- If ruff checks fail, fix all issues before proceeding with development.