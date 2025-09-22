# Session Management

## Purpose
Ensures consistent session initialization and date tracking across all PATH Framework interactions.

## Instructions
- At the start of each chat session, run the `date` command to get the current date. (ID: GET_SESSION_DATE)
- Cache and use this date in all future responses within the session. (ID: CACHE_SESSION_DATE)
- Reference the cached date for all file metadata and documentation updates. (ID: USE_CACHED_DATE)

## Priority
High

## Error Handling
- If date command fails, use system default date format YYYY-MM-DD.
- If no date is available, prompt user to provide current date.