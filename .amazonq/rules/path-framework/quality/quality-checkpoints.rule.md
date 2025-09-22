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
- Verify Behavioral Coverage: >90% specification coverage with behavioral assertions. (ID: BEHAVIORAL_COVERAGE_GATE)
- Check Test Meaningfulness: >3 meaningful assertions per test, not trivial checks. (ID: TEST_MEANINGFULNESS_GATE)
- Validate Business Value Delivery: 95% user story success rate maintained. (ID: BUSINESS_VALUE_GATE)
- Ensure ROI Tracking: Monitor 167-378% first-year ROI achievement. (ID: ROI_TRACKING_GATE)

## Priority
Critical

## Error Handling
- If quality checkpoint fails, do not proceed to next phase until resolved.
- Provide specific remediation steps for each failed checkpoint.
- If mutation score is <80%, regenerate tests with better behavioral coverage.
- If business value delivery is <95%, analyze and address story quality issues.