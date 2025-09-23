# Quality Checkpoints

## Purpose
Enforces quality validation at each PATH Framework phase transition with enhanced metrics and validation.

## Instructions
- Verify Story is Ready: proper format, testable criteria, clear business value. (ID: STORY_READY)
- Verify Design is Complete: technical approach planned, components defined, test strategy clear. (ID: DESIGN_COMPLETE)
- Verify Code is Done: acceptance tests pass, >90% coverage, clean and readable. (ID: CODE_DONE)
- Verify Ready for Production: automated deployment works, monitoring set up, security met. (ID: PRODUCTION_READY)
- Verify Successfully Operating: working in production, users using it, good metrics. (ID: OPERATING_SUCCESS)
- Validate Mutation Score: >80% mutation score for meaningful test validation. (ID: MUTATION_SCORE_GATE)
- Check Test Meaningfulness: >3 meaningful assertions per test, not trivial checks. (ID: TEST_MEANINGFULNESS_GATE)

## Priority
Critical

## Error Handling
- If quality checkpoint fails, document issues but allow phase progression for business value delivery.
- Provide specific remediation steps for each failed checkpoint as continuous improvement.
- If mutation score is <80%, regenerate tests with better behavioral coverage in next iteration.

- Quality gates serve as improvement targets, not delivery blockers.