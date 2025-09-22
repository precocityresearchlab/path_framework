# ATDD/BDD Integration

## Purpose
Enforces proper integration of Acceptance Test-Driven Development and Behavior-Driven Development practices.

## Instructions
- Convert acceptance criteria into executable tests using Gherkin format. (ID: EXECUTABLE_ACCEPTANCE_TESTS)
- Implement nested loop structure: ATDD outer loop, TDD inner loop. (ID: NESTED_LOOP_STRUCTURE)
- Use Given-When-Then format for all acceptance criteria. (ID: GIVEN_WHEN_THEN_FORMAT)
- Ensure acceptance tests drive unit test creation in TDD cycles. (ID: ACCEPTANCE_DRIVES_UNIT)
- Maintain traceability between user stories, acceptance tests, and unit tests. (ID: TEST_TRACEABILITY)
- Block merge if any acceptance criterion fails in CI pipeline. (ID: ACCEPTANCE_GATE)
- Generate test automation framework for continuous validation. (ID: TEST_AUTOMATION_FRAMEWORK)

## Priority
High

## Error Handling
- If acceptance criteria are not in Given-When-Then format, provide template correction.
- If traceability is broken, regenerate links between stories and tests.
- If acceptance tests don't drive TDD, restructure development workflow.