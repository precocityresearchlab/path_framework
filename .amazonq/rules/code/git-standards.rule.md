# Git Standards

## Purpose
Defines consistent Git workflow and commit standards for collaborative development.

## Instructions
- Use conventional commit format: type(scope): description. (ID: CONVENTIONAL_COMMITS)
- Write clear, descriptive commit messages explaining what and why. (ID: DESCRIPTIVE_COMMITS)
- Use branch naming: feature/task-description, bugfix/issue-description. (ID: BRANCH_NAMING)
- Keep commits atomic - one logical change per commit. (ID: ATOMIC_COMMITS)
- Squash feature branch commits before merging to main. (ID: SQUASH_BEFORE_MERGE)
- Require code review approval before merging pull requests. (ID: REQUIRE_CODE_REVIEW)
- Include tests and documentation updates in the same PR. (ID: COMPLETE_PR_CHANGES)
- Reference issue numbers in commit messages and PR descriptions. (ID: REFERENCE_ISSUES)

## Priority
High

## Error Handling
- If commit messages are unclear, provide examples of good commit format.
- If branch names don't follow convention, rename before merging.
- If PR lacks tests or docs, request completion before approval.