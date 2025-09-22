# Security Coding

## Purpose
Enforces secure coding practices to prevent vulnerabilities and protect sensitive data.

## Instructions
- Validate and sanitize all user inputs before processing. (ID: INPUT_VALIDATION)
- Use parameterized queries to prevent SQL injection attacks. (ID: PARAMETERIZED_QUERIES)
- Implement proper authentication and authorization checks. (ID: AUTH_CHECKS)
- Hash passwords using bcrypt or similar secure algorithms. (ID: SECURE_PASSWORD_HASHING)
- Use HTTPS for all external communications and API calls. (ID: HTTPS_REQUIRED)
- Implement rate limiting to prevent abuse and DoS attacks. (ID: RATE_LIMITING)
- Store secrets in secure vaults, never in code or environment variables. (ID: SECURE_SECRET_STORAGE)
- Implement CSRF protection for web applications. (ID: CSRF_PROTECTION)

## Priority
Critical

## Error Handling
- If input validation is missing, add validation before processing.
- If plain text passwords found, implement proper hashing immediately.
- If secrets are hardcoded, move to secure storage and rotate keys.