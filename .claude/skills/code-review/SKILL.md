---
name: code-review
description: Structured 4-dimension code review
---

# /code-review — Structured Code Review

## Usage
```
/code-review                    # Review uncommitted changes
/code-review <file> [file...]   # Review specific files
/code-review <commit-range>     # Review commits (e.g., HEAD~3..HEAD)
/code-review <branch>           # Review branch diff vs main
```

## Review Dimensions

### 1. Security (OWASP Top 10)
- Injection vulnerabilities (SQL, command, XSS)
- Authentication/authorization flaws
- Sensitive data exposure (hardcoded secrets, logging PII)
- Insecure deserialization
- Missing input validation at boundaries

### 2. Performance
- N+1 queries, unnecessary loops
- Missing caching opportunities
- Large allocations or memory leaks
- Blocking operations that should be async
- Unindexed database queries

### 3. Code Quality (DRY / SOLID)
- Code duplication
- Single responsibility violations
- Overly complex functions (cyclomatic complexity)
- Poor naming or unclear intent
- Missing or misleading comments
- Dead code

### 4. Test Coverage
- New code paths without tests
- Edge cases not covered
- Test quality (meaningful assertions, not just "runs without error")
- Integration test gaps

## Output Format

For each issue found:
```
[DIMENSION] severity: HIGH | MEDIUM | LOW
file:line — description
Suggestion: how to fix
```

## Verdict
End with one of:
- **APPROVE** — No blocking issues. May include LOW suggestions.
- **REQUEST CHANGES** — Has HIGH or multiple MEDIUM issues that must be fixed.
- **NEEDS DISCUSSION** — Architectural concerns that need team input.

## Process
1. Determine the diff to review (uncommitted, files, commits, branch)
2. Read all changed files in full (not just the diff — context matters)
3. Analyze each dimension
4. Group findings by severity
5. Deliver verdict with actionable feedback
