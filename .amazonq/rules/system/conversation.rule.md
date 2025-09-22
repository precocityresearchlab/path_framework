# Conversation

## Purpose
Defines how Amazon Q Developer should behave in conversations, including acknowledging rules when explicitly requested.

## Instructions
- Consider all active rules before responding. (ID: CHECK_RULES)
- When user asks about rule enforcement, acknowledge which rules are active. (ID: ACKNOWLEDGE_RULES)
- Apply rules systematically without explicit mention unless requested. (ID: APPLY_SILENTLY)
- If rule conflicts occur, follow priority hierarchy (Critical > High > Medium > Low). (ID: PRIORITY_RESOLUTION)

## Priority
Critical

## Error Handling
- If rule files are unreadable, continue but note the issue.
- If rule conflicts cannot be resolved by priority, ask user for clarification.