# Performance Optimization

## Purpose
Ensures optimal performance through efficient coding practices and resource management.

## Instructions
- Use database indexes for frequently queried columns. (ID: DATABASE_INDEXING)
- Implement caching for expensive operations and frequently accessed data. (ID: IMPLEMENT_CACHING)
- Use async/await for I/O operations to prevent blocking. (ID: ASYNC_IO_OPERATIONS)
- Optimize database queries to avoid N+1 problems. (ID: OPTIMIZE_DB_QUERIES)
- Implement pagination for large data sets. (ID: IMPLEMENT_PAGINATION)
- Use connection pooling for database and external service connections. (ID: CONNECTION_POOLING)
- Profile code to identify bottlenecks before optimizing. (ID: PROFILE_BEFORE_OPTIMIZE)
- Implement lazy loading for expensive resources. (ID: LAZY_LOADING)

## Priority
Medium

## Error Handling
- If performance issues detected, profile to identify root cause.
- If database queries are slow, analyze and add appropriate indexes.
- If memory usage is high, implement proper resource cleanup.