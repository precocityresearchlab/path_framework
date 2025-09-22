# Testing

## Purpose
Comprehensive testing strategy combining TDD, meaningful AI test generation, and impact-based testing optimization.

## Instructions
- Write tests first, then write code to pass those tests. (ID: TESTS_FIRST)
- Follow red-green-refactor cycle: failing test, minimal code, clean refactor. (ID: RED_GREEN_REFACTOR)
- Maintain >90% test coverage for all code. (ID: TEST_COVERAGE)
- Generate specification-driven tests with diverse scenarios including boundary conditions. (ID: SPECIFICATION_DRIVEN_TESTS)
- Create behavioral assertions that validate functionality, not just return values. (ID: BEHAVIORAL_ASSERTIONS)
- Validate test meaningfulness through mutation testing with >80% mutation score. (ID: MUTATION_TESTING_VALIDATION)
- Target tests based on actual code changes and affected components. (ID: TARGET_AFFECTED_TESTS)
- Use dependency analysis to determine minimum required test scope. (ID: DEPENDENCY_TEST_SCOPE)
- Run full test suite only for complex changes affecting core components. (ID: FULL_SUITE_COMPLEX_ONLY)
- Include comprehensive edge case coverage and invariant testing. (ID: COMPREHENSIVE_EDGE_CASES)
- Ensure tests trace back to functional specifications and requirements. (ID: SPECIFICATION_TRACEABILITY)

## Priority
Critical

## Error Handling
- If tests are not written first, remind about TDD discipline.
- If coverage is below 90%, identify missing test cases.
- If mutation score is <80%, regenerate tests with better behavioral coverage.
- If impact analysis is unclear, default to broader test scope for safety.