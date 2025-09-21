---
created_date: 2025-09-21
created_by: PATH Framework Team
last_modified: 2025-09-21
version: 1.0.0
purpose: Standardized color palette and styling guidelines for PATH Framework Mermaid diagrams
framework_phase: N/A
dependencies: [general.md rules, framework documentation]
status: approved
tags: [mermaid, colors, diagrams, styling, standards]
---

# Mermaid Color Standards

## PATH Framework Color Palette

### Phase Colors
- **Stage 0 (Story Foundation)**: `fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px` 🟣
- **Phase 1 (Software Engineering)**: `fill:#e3f2fd,stroke:#1976d2,stroke-width:2px` 🔵
- **Phase 2 (Test-Driven Development)**: `fill:#e8f5e8,stroke:#388e3c,stroke-width:2px` 🟢
- **Phase 3 (DevOps & Production)**: `fill:#fff3e0,stroke:#f57c00,stroke-width:2px` 🟠
- **Phase 4 (Operations & Maintenance)**: `fill:#fce4ec,stroke:#c2185b,stroke-width:2px` 🔴

### Functional Colors
- **Quality Gates**: `fill:#ffcdd2,stroke:#d32f2f,stroke-width:3px` 🔴
- **AI Agents**: `fill:#fce4ec,stroke:#c2185b,stroke-width:2px` 🔴
- **User Stories**: `fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px` 🟣
- **Tests (Acceptance)**: `fill:#e3f2fd,stroke:#1976d2,stroke-width:2px` 🔵
- **Tests (Unit)**: `fill:#e8f5e8,stroke:#388e3c,stroke-width:2px` 🟢
- **Implementation**: `fill:#fff3e0,stroke:#f57c00,stroke-width:2px` 🟠
- **Production**: `fill:#fce4ec,stroke:#c2185b,stroke-width:2px` 🔴
- **Knowledge Base**: `fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px` 🟣

### TDD Specific Colors
- **Red Phase**: `fill:#ffebee,stroke:#d32f2f,stroke-width:2px` 🔴
- **Green Phase**: `fill:#e8f5e8,stroke:#388e3c,stroke-width:2px` 🟢
- **Refactor Phase**: `fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px` 🟣

## Standard Box Sizing
- Mermaid automatically sizes rectangles based on text content
- Use consistent text formatting for uniform appearance
- Avoid width/height in classDef as they don't control visual sizing

## Usage Guidelines
- Use these exact color codes for consistency across all PATH Framework diagrams
- Apply appropriate emoji circles in legends: 🟣🔵🟢🟠🔴
- Maintain stroke-width:2px for standard elements, 3px for critical gates
- Always include legends when using multiple colors
- Apply standard box sizing for uniform appearance