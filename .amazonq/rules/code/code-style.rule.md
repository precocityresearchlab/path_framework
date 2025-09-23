# Code Style

## Purpose
Ensures consistent code formatting and style across all PATH Framework projects.

## Instructions
- Use language-specific formatters: Python (Ruff), JavaScript/TypeScript (Prettier), Go (gofmt), Java (Google Java Format), C# (dotnet format). (ID: LANGUAGE_FORMATTERS)
- Use snake_case for variables and functions, PascalCase for classes in Python. (ID: NAMING_CONVENTIONS)
- Organize imports: standard library, third-party, local imports with blank lines between. (ID: IMPORT_ORGANIZATION)
- Add type hints to all function parameters and return values where supported. (ID: TYPE_HINTS_REQUIRED)
- Use descriptive variable names that explain purpose, avoid abbreviations. (ID: DESCRIPTIVE_NAMES)
- Keep line length under 88 characters for Python, follow language standards for others. (ID: LINE_LENGTH_LIMIT)
- Use docstrings/comments for all public functions, classes, and modules for code clarity. (ID: DOCUMENTATION_REQUIREMENT)

## Priority
High

## Error Handling
- If formatting violations exist, run appropriate language formatter to fix.
- If type hints are missing, add them before code review.
- If naming is unclear, refactor to use descriptive names.