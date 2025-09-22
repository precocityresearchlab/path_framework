# Mermaid Diagrams

## Purpose
Ensures consistent visual styling and color coding for PATH Framework Mermaid diagrams.

## Instructions
- Always add color coding to complex Mermaid diagrams for visual clarity. (ID: ADD_COLOR_CODING)
- Include a legend explaining color meanings when using multiple colors. (ID: INCLUDE_LEGEND)
- Use consistent color themes across related diagrams. (ID: CONSISTENT_THEMES)
- Apply proper styling with `classDef` and `class` declarations. (ID: PROPER_STYLING)
- Use colored emoji circles in legends without color names (e.g., 🔵 Phase 1, not 🔵 **Blue**: Phase 1). (ID: EMOJI_LEGENDS)
- Follow the standardized color palette defined in `mermaid_colors.md` for consistency. (ID: STANDARD_PALETTE)

## Priority
Medium

## Error Handling
- If color palette is not followed, reference mermaid_colors.md for correct colors.
- If legend is missing from multi-color diagram, generate appropriate legend.