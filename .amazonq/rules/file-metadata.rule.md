# File Metadata

## Purpose
Ensures all files in PATH Framework have consistent metadata for tracking and documentation.

## Instructions
- Add metadata info to each file or document added to the folder. (ID: ADD_FILE_METADATA)
- Use YAML front matter format at the top of each file. (ID: YAML_FRONTMATTER)
- Include required fields: created_date, created_by, last_modified, version, purpose, framework_phase, dependencies, status, tags. (ID: REQUIRED_METADATA_FIELDS)
- Update `last_modified` and `version` when making changes. (ID: UPDATE_METADATA)
- Use semantic versioning (X.Y.Z) for version numbers. (ID: SEMANTIC_VERSIONING)
- Include relevant `framework_phase` (1-4) for PATH Framework files. (ID: FRAMEWORK_PHASE)
- Add descriptive `tags` for easy categorization and search. (ID: DESCRIPTIVE_TAGS)

## Priority
High

## Error Handling
- If metadata is missing, create it using the template with current session date.
- If version is missing, start with 1.0.0 for new files.