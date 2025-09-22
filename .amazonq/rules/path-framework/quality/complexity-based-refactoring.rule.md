# Complexity-Based Refactoring

## Purpose
Guides refactoring decisions based on code complexity and business criticality to optimize development velocity while maintaining quality.

## Instructions
- Refactor only for complex or business-critical components to maximize impact. (ID: REFACTOR_COMPLEX_CRITICAL)
- Skip refactoring for simple, stable components to maintain development velocity. (ID: SKIP_SIMPLE_STABLE)
- Use complexity metrics (cyclomatic, cognitive) to guide refactoring priorities. (ID: USE_COMPLEXITY_METRICS)
- Prioritize refactoring for components with high change frequency and complexity. (ID: PRIORITIZE_HIGH_CHANGE_COMPLEX)
- Defer refactoring for low-complexity components unless quality gates fail. (ID: DEFER_LOW_COMPLEXITY)
- Document refactoring decisions with complexity rationale for future reference. (ID: DOCUMENT_REFACTORING_RATIONALE)

## Priority
Medium

## Error Handling
- If complexity metrics are unavailable, use code review judgment for refactoring decisions.
- If quality gates fail, refactor regardless of complexity to meet standards.
- If refactoring scope is unclear, start with smallest viable improvement.