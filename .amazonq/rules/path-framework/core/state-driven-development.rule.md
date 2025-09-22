# State-Driven Development

## Purpose
Ensures decisions are based on current system state rather than assumptions, reducing rework and integration issues.

## Instructions
- Always refresh project state analysis before making architectural or implementation decisions. (ID: REFRESH_STATE_ANALYSIS)
- Use current codebase analysis for impact assessment of proposed changes. (ID: IMPACT_ASSESSMENT)
- Make decisions based on fresh system state, not outdated assumptions or documentation. (ID: FRESH_STATE_DECISIONS)
- Update state documentation after significant changes to maintain accuracy. (ID: UPDATE_STATE_DOCS)
- Validate state consistency before proceeding to next development phase. (ID: VALIDATE_STATE_CONSISTENCY)

## Priority
High

## Error Handling
- If state analysis is unavailable, document assumptions and validate them before proceeding.
- If state inconsistencies are found, resolve them before making dependent changes.
- If state refresh fails, use most recent available state with explicit risk acknowledgment.