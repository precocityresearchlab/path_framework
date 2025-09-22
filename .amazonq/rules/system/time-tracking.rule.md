# Time Tracking

## Purpose
Ensures accurate UTC time tracking for sessions and task execution across all PATH Framework interactions.

## Instructions
- At the start of each chat session, get the current UTC date and time. (ID: GET_SESSION_UTC)
- Cache and use this UTC timestamp in all future responses within the session. (ID: CACHE_SESSION_UTC)
- Record exact start UTC timestamp when beginning task execution. (ID: RECORD_START_UTC)
- Record exact end UTC timestamp when task is complete. (ID: RECORD_END_UTC)
- Calculate and report actual execution duration in format "Xh Ym Zs". (ID: CALCULATE_DURATION)
- Use format "Started: HH:MM:SS UTC, Completed: HH:MM:SS UTC, Duration: Xh Ym Zs". (ID: UTC_TIME_FORMAT)
- Reference the cached UTC date for all file metadata and documentation updates. (ID: USE_CACHED_UTC)
- Include execution time in task completion documentation. (ID: DOCUMENT_EXECUTION_TIME)
- Track time for estimation improvement and productivity analysis. (ID: TRACK_FOR_ANALYSIS)

## Priority
High

## Error Handling
- If UTC time command fails, use system default UTC format YYYY-MM-DD HH:MM:SS UTC.
- If start time is missed, estimate based on git commit history or activity logs.
- If no UTC time is available, prompt user to provide current UTC time.