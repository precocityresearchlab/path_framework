# Code Style

## Purpose
Ensures consistent code formatting and style across all PATH Framework projects.

## Instructions
- Follow PEP8 standards for Python code formatting. (ID: PEP8_COMPLIANCE)
- Use snake_case for variables and functions, PascalCase for classes. (ID: NAMING_CONVENTIONS)
- Organize imports: standard library, third-party, local imports with blank lines between. (ID: IMPORT_ORGANIZATION)
- Add type hints to all function parameters and return values. (ID: TYPE_HINTS_REQUIRED)
- Use descriptive variable names that explain purpose, avoid abbreviations. (ID: DESCRIPTIVE_NAMES)
- Keep line length under 88 characters (Black formatter standard). (ID: LINE_LENGTH_LIMIT)
- Use docstrings for all public functions, classes, and modules. (ID: DOCSTRING_REQUIREMENT)

## Priority
High

## Error Handling
- If PEP8 violations exist, run automated formatter (black, ruff) to fix.
- If type hints are missing, add them before code review.
- If naming is unclear, refactor to use descriptive names.