### Recommended Structure for Amazon Q Developer Rules
A suggested format for rule files, which are stored as Markdown documents in the `.amazonq/rules` folder, includes the following sections to enhance clarity and optimization:
- **Rule Name**: A descriptive title, such as "Monitoring" or "Frontend - React."
- **Purpose**: A concise explanation of the rule's intent, e.g., "Ensures consistent monitoring coverage for new features."
- **Instructions**: Actionable directives, ideally with unique identifiers (e.g., "ID: CHECK_MONITORING_PLAN") for traceability. This allows Amazon Q to reference applied rules explicitly if configured to do so.
- **Priority**: Levels like Critical, High, Medium, or Low to handle conflicts between rules.
- **Error Handling**: Strategies for edge cases, e.g., "If a required file is missing, create it with a basic structure."

This structure optimizes rules by making them modular, easier to maintain, and more effective in guiding Amazon Q's responses without requiring manual repetition in prompts.

### Sample Rules as Templates
Several examples are available that can be adapted as starting points:
1. **Monitoring Rule**:
   ```
   # Monitoring
   ## Purpose
   This rule ensures that monitoring coverage is maintained when major features are added.
   ## Instructions
   - When implementing a major feature, ALWAYS check if MONITORING_PLAN.md needs updates. (ID: CHECK_MONITORING_PLAN)
   - Major features include: new microservices, AI integrations, WebSocket endpoints. (ID: MAJOR_FEATURE_CRITERIA)
   - After updating MONITORING_PLAN.md, output "📊 Updated monitoring plan for: [feature]". (ID: ANNOUNCE_MONITORING_UPDATE)
   ## Priority
   High
   ## Error Handling
   - If MONITORING_PLAN.md doesn't exist, create it with basic monitoring structure.
   ```
   Save as `monitoring.rule.md`. This template optimizes for feature development by enforcing checks on documentation.

2. **Conversation Rule** (for transparency in responses):
   ```
   # Conversation
   ## Purpose
   This rule defines how Amazon Q Developer should behave in conversations, including acknowledging rules.
   ## Instructions
   - ALWAYS consider your rules before responding. (ID: CHECK_RULES)
   - When acting based on a rule, ALWAYS print "Rule used: `filename` (ID)" at the start. (ID: PRINT_RULES)
   - If multiple rules apply, list all rules used. (ID: PRINT_MULTIPLE)
   ## Priority
   Critical
   ## Error Handling
   - If rule files are unreadable, continue but note the issue.
   ```
   This can optimize usage by making Amazon Q explicitly acknowledge applied rules, aiding debugging.

3. **AWS Resource Rule** (from official documentation):
   ```
   All Amazon S3 buckets must have encryption enabled, enforce SSL, and block public access.
   All Amazon DynamoDB Streams tables must have encryption enabled.
   All Amazon SNS topics must have encryption enabled and enforce SSL.
   All Amazon SNS queues must enforce SSL.
   ```
   Save as `cdk-rules.md`. This simple template focuses on security best practices for AWS services.

Additional samples for time handling, frontend development (e.g., React), and Git operations are detailed in AWS resources, emphasizing unique IDs and priorities for better optimization.

### Best Practices for Optimization
To maximize the effectiveness of these rules:
- Organize files in subdirectories (e.g., `.amazonq/rules/frontend/react.rule.md`) for better scalability.
- Use descriptive filenames and focused instructions to reduce ambiguity.
- Verify rule activation in the Amazon Q chat panel, where you can toggle them for sessions.
- In CLI contexts, rules (or "scaffolds") provide additional context to steer responses, with commands like `/context` to confirm loading.
- Start with rules addressing common team pain points, such as code style or security, to ensure persistent application without per-prompt reminders.
