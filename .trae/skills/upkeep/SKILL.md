---
name: "upkeep"
description: "Maintain documentation-code consistency. Find outdated docs, verify code matches docs. Invoke when user asks to check docs or maintain consistency."
---

# Upkeep Skill

## Check Criteria

### Config Consistency
- Every config param in docs must exist in code; Defaults must match; Undocumented params flagged

### Flow Consistency
- Upgrade steps in docs must match actual code; Key mappings must match; Error messages must match

### File Path Consistency
- All paths in docs must exist; Directory structures must match actual

### Feature Completeness
- New features must be documented; Removed features must not appear in docs

## Output Format
```
## Upkeep Report
| # | File | Line | Type | Issue | Fix |
|---|------|------|------|-------|-----|
```