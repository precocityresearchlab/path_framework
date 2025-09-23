---
created_date: 2025-09-17
created_by: PATH Framework Team
last_modified: 2025-09-22
version: 3.0.0
purpose: Systematic rule execution with human validation gates for PATH Framework
framework_phase: N/A
dependencies: [all rule files]
status: active
tags: [rules, batch-read, execution, compliance, PATH Framework]
---

# PATH Framework Rule Execution Matrix

## Quick Start Prompt
```
Read all PATH Framework rule files systematically, then execute your task following all rules in priority order.
```

## ABSOLUTE ENFORCEMENT: MANDATORY VALIDATION GATES

**GATE 1: RULE LOADING VALIDATION**
- ❌ **IMMEDIATE STOP** if any PATH Framework rule files fail to load
- ❌ **IMMEDIATE STOP** if rule files are not read systematically first
- ❌ **IMMEDIATE STOP** if "file not found" errors occur
- ✅ **PROCEED ONLY** when all rule files successfully loaded

**GATE 2: UTC TIME VALIDATION**
- ❌ **IMMEDIATE STOP** if current UTC timestamp not obtained
- ❌ **IMMEDIATE STOP** if session UTC not cached
- ❌ **IMMEDIATE STOP** if start time not recorded before task execution
- ✅ **PROCEED ONLY** when UTC tracking is active

**GATE 3: USER STORY VALIDATION**
- ❌ **IMMEDIATE STOP** if task lacks "As a... I want... So that..." format
- ❌ **IMMEDIATE STOP** if acceptance criteria missing Given-When-Then format
- ❌ **IMMEDIATE STOP** if business value not clearly articulated
- ✅ **PROCEED ONLY** when user story is complete and validated

**GATE 4: HUMAN VALIDATION**
- ❌ **IMMEDIATE STOP** if human approval not obtained for critical decisions
- ❌ **IMMEDIATE STOP** if user story not validated by product owner/stakeholder
- ❌ **IMMEDIATE STOP** if architecture decisions not reviewed by human expert
- ✅ **PROCEED ONLY** when human validation gates passed

**GATE 5: COMPLETION VALIDATION**
- ❌ **IMMEDIATE STOP** if task marked complete without proper format
- ❌ **IMMEDIATE STOP** if file metadata not updated
- ❌ **IMMEDIATE STOP** if git commit not executed (when applicable)
- ✅ **PROCEED ONLY** when all completion steps validated

## MANDATORY: Read All Rules Systematically

Read these rule files in priority order:

### Phase 1: CRITICAL Rules (System & Core)
- system/conversation.rule.md
- system/time-tracking.rule.md
- path-framework/core/framework-definition.rule.md
- path-framework/quality/testing.rule.md
- path-framework/quality/quality-checkpoints.rule.md
- general/business-value.rule.md
- code/security-coding.rule.md
- code/error-handling.rule.md

### Phase 2: HIGH Priority Rules (Development & Process)
- path-framework/core/state-driven-development.rule.md
- path-framework/core/sequential-task-execution.rule.md
- path-framework/core/todo-execution.rule.md
- path-framework/core/minimal-development.rule.md
- general/functional-requirements-validation.rule.md
- path-framework/phases/atdd-bdd-integration.rule.md
- code/code-style.rule.md
- code/git-standards.rule.md

### Phase 3: MEDIUM Priority Rules (Implementation & Standards)
- code/python-standards.rule.md
- code/performance-optimization.rule.md
- path-framework/quality/complexity-based-refactoring.rule.md
- path-framework/quality/process-analytics.rule.md
- path-framework/collaboration/human-ai-patterns.rule.md
- path-framework/enterprise/implementation-strategy.rule.md
- path-framework/phases/phase1-architecture.rule.md
- path-framework/phases/phase3-devops.rule.md
- path-framework/phases/phase4-operations.rule.md

### Phase 4: Documentation Rules
- documentation/file-metadata.rule.md
- documentation/document-badges.rule.md
- documentation/mermaid-diagrams.rule.md
- documentation/path-framework-colors.rule.md

## MANDATORY: Rule Compliance Validation
After reading all files, confirm:
- [ ] All rule files read successfully
- [ ] No "file not found" errors
- [ ] Ready to apply PATH Framework rules systematically

## CRITICAL: Pre-Task Execution Checklist
Before starting any task, MUST validate:
- [ ] **HUMAN_VALIDATION**: Required human approvals obtained for current phase
- [ ] **TESTS_FIRST**: Will write tests before implementation code
- [ ] **STORY_READY**: User story follows "As a... I want... So that..." format with Given-When-Then acceptance criteria
- [ ] **REQUIRE_USER_STORY**: Task has proper user story with business value
- [ ] **GET_SESSION_UTC**: Current UTC timestamp obtained and cached
- [ ] **EXECUTABLE_ACCEPTANCE_TESTS**: Acceptance criteria converted to executable tests
- [ ] **ADD_FILE_METADATA**: Will update file metadata with current session UTC

## CRITICAL: Post-Task Completion Checklist
After completing any task, MUST validate:
- [ ] **HUMAN_REVIEW**: Present results to human for validation before marking complete
- [ ] **MARK_COMPLETE**: Used required completion format with detailed reporting
- [ ] **RECORD_END_UTC**: Recorded exact completion timestamp
- [ ] **CALCULATE_DURATION**: Calculated and reported execution duration
- [ ] **TEST_COVERAGE**: Achieved >90% test coverage
- [ ] **QUALITY_GATES**: All quality checkpoints passed
- [ ] **UPDATE_METADATA**: Updated file metadata with completion details

## Rule Application Enforcement
**STOP EXECUTION** if any checklist item fails validation.
**DO NOT PROCEED** to next task until all rules are properly applied.
**DOCUMENT COMPLIANCE** for each rule application during execution.

## MANDATORY: Task Completion Validation
Before marking any task complete, MUST execute this validation sequence:

```
1. VALIDATE PRE-TASK CHECKLIST ✅
2. EXECUTE TASK WITH TDD ✅  
3. VALIDATE POST-TASK CHECKLIST ✅
4. UPDATE FILE METADATA ✅
5. COMMIT WITH CONVENTIONAL FORMAT ✅ (if applicable)
6. MARK TASK AS ✅ COMPLETE ✅
7. DOCUMENT RULE COMPLIANCE ✅
```

**IF ANY STEP FAILS**: STOP and fix before proceeding.
**NO EXCEPTIONS**: All 7 steps must be completed for each task.

## Execution Order
1. **CRITICAL** (Phase 1) - Must execute first, blocks all work
2. **HIGH** (Phase 2) - Execute before main work
3. **MEDIUM** (Phase 3) - Execute during main work  
4. **Documentation** (Phase 4) - Execute during/after implementation

## CRITICAL: Human Validation Breakpoints

### Phase 0: Story Validation (HUMAN LEADS - Pattern 1)
**MANDATORY HUMAN APPROVAL** before Phase 1:
- [ ] **User Story Validation**: Product owner confirms "As a... I want... So that..." format
- [ ] **Business Value Confirmation**: Stakeholder validates measurable benefits and ROI
- [ ] **Acceptance Criteria Review**: Human expert approves Given-When-Then scenarios
- [ ] **Priority Assessment**: Human decision on implementation priority vs other features

**AI PRESENTS TO HUMAN**:
- Generated user story options with business value analysis
- Risk assessment and implementation complexity estimates
- Alternative approaches with trade-off analysis
- Resource requirements and timeline estimates

### Phase 1: Architecture Decisions (COLLABORATE - Pattern 3)
**MANDATORY HUMAN APPROVAL** before Phase 2:
- [ ] **Technology Stack Approval**: Human architect validates technology choices
- [ ] **System Design Review**: Human expert approves component architecture
- [ ] **Integration Strategy**: Human validation of external system connections
- [ ] **Security Architecture**: Human security expert approves security design

**AI PRESENTS TO HUMAN**:
- Multiple architecture options with pros/cons analysis
- Technology recommendations with justification
- Risk mitigation strategies for each approach
- Performance and scalability implications

### Phase 2: Implementation Quality Gates (AI LEADS - Pattern 2)
**HUMAN OVERSIGHT CHECKPOINTS**:
- [ ] **Test Strategy Review**: Human validates comprehensive test approach
- [ ] **Code Quality Spot Check**: Human reviews critical algorithm implementations
- [ ] **Security Code Review**: Human security expert validates sensitive code paths
- [ ] **Performance Validation**: Human approves performance test results

**AI PRESENTS TO HUMAN**:
- Test coverage reports and quality metrics
- Code complexity analysis and refactoring recommendations
- Security vulnerability scan results
- Performance benchmarks and optimization suggestions

### Phase 3: Production Readiness (COLLABORATE - Pattern 3)
**MANDATORY HUMAN APPROVAL** before deployment:
- [ ] **Deployment Strategy**: Human DevOps expert approves deployment plan
- [ ] **Monitoring Setup**: Human validates alerting and monitoring configuration
- [ ] **Rollback Plan**: Human approves emergency rollback procedures
- [ ] **Go-Live Decision**: Human stakeholder makes final deployment authorization

**AI PRESENTS TO HUMAN**:
- Deployment risk analysis and mitigation plans
- Infrastructure capacity and scaling recommendations
- Monitoring dashboard and alert configuration
- Disaster recovery and business continuity plans

### Phase 4: Operations Decisions (HUMAN LEADS - Pattern 1)
**HUMAN DECISION POINTS**:
- [ ] **Performance Issues**: Human decides on optimization priorities
- [ ] **Feature Requests**: Human product owner prioritizes new requirements
- [ ] **Incident Response**: Human incident commander directs critical issue resolution
- [ ] **Capacity Planning**: Human management approves infrastructure scaling

**AI PRESENTS TO HUMAN**:
- Production metrics and trend analysis
- User feedback analysis and feature usage patterns
- Incident reports with root cause analysis
- Cost optimization recommendations

## Human Validation Protocol

### MANDATORY: Present Options Format
When presenting to humans, AI MUST use this format:

```
📊 DECISION REQUIRED: [Decision Type]

🎯 CONTEXT:
- Current situation and requirements
- Business impact and constraints

📋 OPTIONS:
1. **Option A**: [Description]
   - Pros: [Benefits]
   - Cons: [Risks/Limitations]
   - Effort: [Time/Resources]

2. **Option B**: [Description]
   - Pros: [Benefits]
   - Cons: [Risks/Limitations]
   - Effort: [Time/Resources]

📈 RECOMMENDATION: [AI Recommendation with rationale]

❓ HUMAN INPUT NEEDED:
- [ ] Approve recommended option
- [ ] Select alternative option
- [ ] Request additional analysis
- [ ] Provide additional requirements
```

### ENFORCEMENT: No Bypass Protocol
- **ABSOLUTE PROHIBITION**: AI cannot bypass human validation gates
- **ESCALATION REQUIRED**: If human unavailable, escalate to backup decision maker
- **DOCUMENTATION MANDATORY**: Record all human decisions with rationale
- **AUDIT TRAIL**: Maintain complete decision history for compliance

## Rule Compliance Tracking
For each task execution, document:
```
✅ RULE COMPLIANCE REPORT
- Tests First: [YES/NO] - [Evidence]
- Story Ready: [YES/NO] - [Evidence] 
- UTC Tracking: [YES/NO] - [Start/End times]
- Human Validation: [YES/NO] - [Decision Points]
- Completion Format: [YES/NO] - [Evidence]
- Metadata Updated: [YES/NO] - [Evidence]
- Quality Gates: [YES/NO] - [Evidence]
```

## Prevention Strategy

### MANDATORY: Pre-Execution Validation
Before starting ANY task, MUST execute this validation checklist:

```
🔍 PRE-TASK VALIDATION CHECKLIST
□ All PATH Framework rule files read successfully (no "file not found" errors)
□ Current UTC timestamp obtained and cached for session
□ Task has proper user story with "As a... I want... So that..." format
□ Acceptance criteria defined in Given-When-Then format
□ Business value clearly articulated and validated
□ Test strategy planned (tests will be written first)
□ Ready to apply TDD methodology (red-green-refactor)
```

**CRITICAL ENFORCEMENT**: 
- **IMMEDIATELY STOP** if ANY checklist item is unchecked
- **DO NOT ANALYZE** or discuss task details until ALL items pass
- **GENERATE MISSING ITEMS** using appropriate rules before proceeding
- **VALIDATE COMPLETION** of each item before moving to next
- **NO EXCEPTIONS** - every task must pass complete validation

### MANDATORY: During-Execution Monitoring
While executing task, continuously validate:

```
⚡ EXECUTION MONITORING CHECKLIST
□ Following TDD discipline (tests first, then implementation)
□ Recording exact start/end UTC timestamps
□ Writing real business logic (no placeholder code)
□ Maintaining >90% test coverage
□ Following minimal development principles
□ Applying security and error handling patterns
```

### MANDATORY: Post-Execution Validation
After completing task, MUST validate ALL steps:

```
✅ POST-TASK VALIDATION CHECKLIST
□ Task marked complete with detailed reporting format
□ All changes committed using conventional commit format (if applicable)
□ Execution duration calculated and documented
□ Quality gates passed (>90% coverage, real business logic)
□ File metadata updated with completion details
□ Next task identified and ready for execution
□ Rule compliance documented and validated
```

### CRITICAL: Failure Prevention Measures

**IMMEDIATE STOP EXECUTION** if any validation step fails:
- **Missing Human Validation**: **STOP** - Present decision options to human using mandatory format
- **Missing Rule Files**: Re-read rule files systematically until all files loaded
- **No UTC Timestamp**: Execute time tracking command and cache result
- **Invalid User Story**: **STOP** - Generate proper "As a... I want... So that..." format using Business Value rule
- **Missing Acceptance Criteria**: **STOP** - Generate Given-When-Then format from task requirements
- **Missing Business Value**: **STOP** - Extract and validate measurable benefits
- **Missing Tests**: **STOP** - Write tests first before any implementation code
- **Placeholder Code**: **STOP** - Replace with real business logic and algorithms
- **Missing Metadata**: **STOP** - Update with comprehensive task details
- **No Git Commit**: **STOP** - Commit all changes with conventional format (if applicable)

**ABSOLUTE PROHIBITION**: 
- **NO TASK ANALYSIS** until validation complete
- **NO CODE DISCUSSION** until user story exists
- **NO IMPLEMENTATION PLANNING** until acceptance criteria defined
- **NO EXCEPTIONS** - validation is mandatory gate

**ENFORCEMENT SEQUENCE**:
1. **CHECK** each validation item
2. **STOP IMMEDIATELY** on first failure
3. **GENERATE/FIX** the missing item
4. **VALIDATE** the fix is complete
5. **CONTINUE** only when ALL items pass

### Compliance Enforcement Protocol

1. **VALIDATE BEFORE START**: Execute pre-task checklist
2. **MONITOR DURING EXECUTION**: Check execution monitoring points
3. **VALIDATE BEFORE COMPLETE**: Execute post-task checklist
4. **DOCUMENT COMPLIANCE**: Record all validation results
5. **COMMIT CHANGES**: Use conventional commit format (if applicable)
6. **UPDATE TRACKING**: Mark task complete in task list
7. **PREPARE NEXT**: Validate readiness for next task

**ZERO TOLERANCE**: Any missing step requires immediate correction before proceeding.

## ENFORCEMENT AUTOMATION

### MANDATORY: Pre-Task Execution Sequence
**EXECUTE IN EXACT ORDER - NO EXCEPTIONS:**

```
1. EXECUTE: Get current UTC timestamp and cache
2. EXECUTE: Batch read all PATH Framework rule files (4 phases)
3. VALIDATE: All files loaded successfully
4. VALIDATE: Task has complete user story
5. VALIDATE: Acceptance criteria in Given-When-Then format
6. VALIDATE: Business value clearly articulated
7. RECORD: Task start UTC timestamp
8. PROCEED: Begin task execution with TDD
```

### MANDATORY: Post-Task Completion Sequence
**EXECUTE IN EXACT ORDER - NO EXCEPTIONS:**

```
1. RECORD: Task end UTC timestamp
2. CALCULATE: Execution duration
3. UPDATE: File metadata with session UTC
4. UPDATE: Task list with completion status (if applicable)
5. EXECUTE: Git commit with conventional format (if applicable)
6. VALIDATE: All completion steps executed
7. MARK: Task as ✅ COMPLETE
8. DOCUMENT: Rule compliance report
```

### CRITICAL: Failure Response Protocol
**IF ANY STEP FAILS:**
- **STOP IMMEDIATELY** - Do not proceed to next step
- **IDENTIFY ROOT CAUSE** - Determine why step failed
- **EXECUTE CORRECTION** - Fix the specific issue
- **VALIDATE FIX** - Confirm correction is complete
- **RESUME SEQUENCE** - Continue from corrected step
- **DOCUMENT ISSUE** - Log failure and resolution

**NO BYPASSING ALLOWED** - Every step must be completed successfully.

## PATH Framework Integration

### Four-Phase Lifecycle Support
- **Phase 1 (Architecture)**: Apply architecture and design rules
- **Phase 2 (TDD)**: Enforce testing-first development
- **Phase 3 (DevOps)**: Apply deployment and production rules
- **Phase 4 (Operations)**: Apply monitoring and maintenance rules

### Human-AI Collaboration Patterns
- **Pattern 1 (Human Leads)**: Strategic decisions, creative problem-solving
- **Pattern 2 (AI Leads)**: Routine tasks, systematic execution (default)
- **Pattern 3 (Collaborate)**: Critical decisions requiring both perspectives

### Business Value Enforcement
- Every task must deliver measurable business value
- 95% user story success rate maintained
- ROI tracking with 167-378% first-year return target
- 3-6 month break-even timeline validation

## Success Metrics
- **Rule Compliance**: 100% validation gate passage
- **Quality**: >90% test coverage, >80% mutation score
- **Business Value**: 95% story success rate
- **Efficiency**: Minimal code with maximum value delivery