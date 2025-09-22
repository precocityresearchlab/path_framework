# Error Handling

## Purpose
Defines consistent error handling patterns and logging standards for robust applications.

## Instructions
- Use specific exception types instead of generic Exception catches. (ID: SPECIFIC_EXCEPTIONS)
- Log errors with context: timestamp, user ID, operation, error details. (ID: CONTEXTUAL_LOGGING)
- Return meaningful error messages to users, log technical details separately. (ID: USER_FRIENDLY_ERRORS)
- Implement circuit breaker pattern for external service calls. (ID: CIRCUIT_BREAKER_PATTERN)
- Use structured logging with JSON format for production systems. (ID: STRUCTURED_LOGGING)
- Handle timeouts and retries with exponential backoff. (ID: TIMEOUT_RETRY_HANDLING)
- Never expose sensitive data in error messages or logs. (ID: NO_SENSITIVE_DATA_EXPOSURE)

## Priority
Critical

## Error Handling
- If generic exceptions are used, replace with specific exception types.
- If error context is missing, add relevant debugging information.
- If sensitive data appears in logs, implement data masking.