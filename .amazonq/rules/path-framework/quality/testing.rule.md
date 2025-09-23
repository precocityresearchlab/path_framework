# Testing

## Purpose
Comprehensive testing strategy combining TDD, meaningful AI test generation, and impact-based testing optimization.

## Instructions
- Write tests first, then write code to pass those tests. (ID: TESTS_FIRST)
- Maintain >90% test coverage for all code. (ID: TEST_COVERAGE)
- Generate specification-driven tests based on functional specification, not assumptions, with diverse scenarios including boundary conditions. (ID: SPECIFICATION_DRIVEN_TESTS)
- Create behavioral assertions that validate functionality, not just return values. (ID: BEHAVIORAL_ASSERTIONS)
- Validate test meaningfulness through mutation testing with >80% mutation score. (ID: MUTATION_TESTING_VALIDATION)
- Target tests based on actual code changes and affected components. (ID: TARGET_AFFECTED_TESTS)
- Use dependency analysis to determine minimum required test scope. (ID: DEPENDENCY_TEST_SCOPE)
- Run full test suite only for complex changes affecting core components. (ID: FULL_SUITE_COMPLEX_ONLY)
- Include comprehensive edge case coverage and invariant testing. (ID: COMPREHENSIVE_EDGE_CASES)
- Ensure tests trace back to functional specifications and requirements. (ID: SPECIFICATION_TRACEABILITY)
- Focus on one component at a time for unit tests, maintain cross-component traceability at acceptance level. (ID: COMPONENT_FOCUSED_TDD)
- Write unit tests immediately before implementing each component. (ID: IMMEDIATE_TEST_IMPLEMENTATION)
- Add integration tests after component stabilization, not before. (ID: INTEGRATION_AFTER_STABILITY)
- Evolve towards system tests as components mature and integrate. (ID: EVOLVE_TO_SYSTEM_TESTS)
- Use bulk testing only for acceptance criteria, compliance, or shared test data. (ID: LIMITED_BULK_TESTING)
- Start with clear specification understanding before writing any test. (ID: SPECIFICATION_FIRST)
- Break requirements into small, testable behaviors with input-output examples. (ID: TESTABLE_BEHAVIORS)
- Follow strict Red-Green-Refactor cycle: failing test, minimal code, improve design. (ID: RED_GREEN_REFACTOR)
- Write behavior-driven tests that verify what code should do, not how it does it. (ID: BEHAVIOR_DRIVEN_TESTS)
- Use descriptive test names that explain behavior clearly. (ID: DESCRIPTIVE_TEST_NAMES)
- Structure tests with Arrange-Act-Assert (AAA) pattern for clarity. (ID: AAA_STRUCTURE)
- Include boundary value testing for input range limits. (ID: BOUNDARY_VALUE_TESTING)
- Implement negative testing for invalid input handling. (ID: NEGATIVE_TESTING)
- Write minimal, focused tests with one purpose per test. (ID: MINIMAL_FOCUSED_TESTS)
- Ensure tests are deterministic and fast for continuous feedback. (ID: DETERMINISTIC_FAST_TESTS)
- Refactor both code and tests without changing functionality. (ID: REFACTOR_TESTS_AND_CODE)
- Ensure tests fail first before any implementation exists. (ID: FAIL_FIRST_REQUIREMENT)
- Cover normal cases, edge cases, and error/invalid input cases comprehensively. (ID: COMPREHENSIVE_CASE_COVERAGE)
- Write non-trivial assertions that validate meaningful behavior, not constants. (ID: NON_TRIVIAL_ASSERTIONS)
- Provide at least one test per functional requirement with extras for boundaries. (ID: ONE_TEST_PER_REQUIREMENT)
- Ensure tests are independent and do not depend on execution order. (ID: TEST_INDEPENDENCE)

## Priority
Critical

## Error Handling
- If tests are not written first, remind about TDD discipline.
- If coverage is below 90%, identify missing test cases.
- If mutation score is <80%, regenerate tests with better behavioral coverage.
- If impact analysis is unclear, default to broader test scope for safety.
- If tests are trivial (asserting hardcoded constants), rewrite with meaningful behavior validation.
- If tests check implementation details, refactor to test behavior instead.
- If multiple tests overlap unnecessarily, consolidate or remove duplicates.
- If refactoring is skipped, enforce cleanup phase before next Red cycle.
- If tests are not deterministic, identify and fix environmental dependencies.
- If bulk tests are written prematurely, refactor to component-focused approach.
- If component boundaries are unclear, define service boundaries before TDD.
- If cross-component traceability is lost, maintain it at acceptance test level while keeping unit tests component-focused.
- If tests don't fail first, stop and fix the test before implementing code.
- If normal case coverage is missing, add tests for typical usage scenarios.
- If requirements lack test coverage, create at least one test per requirement.
- If tests depend on execution order, refactor to ensure independence.