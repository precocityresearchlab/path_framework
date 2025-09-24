# Table of Contents

## Purpose
Ensures all markdown documents have consistent navigation through standardized Table of Contents.

## Instructions
- Add Table of Contents (ToC) to all markdown documents longer than 500 words. (ID: ADD_TOC_LONG_DOCS)
- Place ToC immediately after document header and badges, before main content. (ID: TOC_PLACEMENT)
- Use markdown link format: `- [Section Name](#section-name)` with proper anchor links. (ID: MARKDOWN_LINK_FORMAT)
- Include all major sections (##) and subsections (###) in ToC. (ID: INCLUDE_MAJOR_SECTIONS)
- Use nested bullet points to show document hierarchy. (ID: NESTED_BULLET_POINTS)
- Update ToC when document structure changes. (ID: UPDATE_TOC_CHANGES)
- Generate ToC automatically using markdown tools when possible. (ID: AUTOMATIC_TOC_GENERATION)

## Priority
Medium

## Error Handling
- If ToC is missing from long documents, generate one based on existing headers.
- If ToC links are broken, fix anchor references to match actual headers.
- If document structure changes, update ToC to reflect new organization.