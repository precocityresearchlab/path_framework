# General Rules

## Session Management
- At the start of each chat session, run the `date` command to get the current date. Cache and use this date in all future responses.


## Human-Side Requirements
- Add `user story` to drive proper feature implementation in all development work
- User stories must follow the format: "As a [user type], I want [functionality], so that [benefit]"
- Include 2-5 clear acceptance criteria using Given-When-Then format

## File Metadata Requirements
- Add metadata info to each file or document added to the folder
- Use the following template for metadata:

```yaml
---
# File Metadata Template
created_date: YYYY-MM-DD
created_by: [Author/Creator Name]
last_modified: YYYY-MM-DD
version: X.Y.Z
purpose: [Brief description of file purpose]
framework_phase: [1-4 or N/A]
dependencies: [List of related files/components]
status: [draft|review|approved|deprecated]
tags: [comma, separated, tags]
---
```

## Metadata Guidelines
- Place metadata at the top of each file using YAML front matter format
- Update `last_modified` and `version` when making changes
- Use semantic versioning (X.Y.Z) for version numbers
- Include relevant `framework_phase` (1-4) for PATH Framework files
- Add descriptive `tags` for easy categorization and search

## Document Badge Guidelines
- Add colored badge tags to document headers for key information
- Use shields.io badge format: `![Label](https://img.shields.io/badge/Label-Value-color?style=flat-square)`
- Include standard badges: Framework, Version, License, Status, Institution, Methodology
- Use consistent colors: Framework (orange), Version (blue), License (green), Status (brightgreen), Institution (purple), Methodology (red)

## Mermaid Diagram Guidelines
- Always add color coding to complex Mermaid diagrams for visual clarity
- Include a legend explaining color meanings when using multiple colors
- Use consistent color themes across related diagrams
- Apply proper styling with `classDef` and `class` declarations
- Use colored emoji circles in legends without color names (e.g., 🔵 Phase 1, not 🔵 **Blue**: Phase 1)
- Follow the standardized color palette defined in `mermaid_colors.md` for consistency