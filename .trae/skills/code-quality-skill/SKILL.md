---
name: "code-quality-skill"
description: "Check Python code quality: naming, type hints, exception handling, security, logging, best practices. Invoke when user asks for code review or quality check."
---

# Code Quality Skill

## Check Criteria

### Naming (PEP8)
- Class: CapWords; Function/variable: snake_case; Constant: UPPER_CASE; Private: _leading_underscore

### Type Hints
- All function params and return values must have type hints
- Use typing module (List, Dict, Optional) for complex types

### Exception Handling
- No bare `except:`; No silent error swallowing; Context managers for resources

### Security
- No hardcoded passwords; No eval/exec on user input; SSH creds from config only

### Logging
- Use logger not print; Appropriate levels; No sensitive data in logs

### Code Quality
- Functions under 50 lines; No duplicated code; No unused imports; Docstrings on public API

## Output Format
```
## Code Quality Report
| # | File | Line | Severity | Category | Issue | Suggestion |
|---|------|------|----------|----------|-------|------------|
```