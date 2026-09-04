# Find Skills

## Description
Search and discover AI agent skills from the skills.sh registry. Use this skill when the user wants to find, discover, or install new skills for the project.

## How to Use

### Search for skills
```bash
npx skills find <keyword>
```

### Install a skill (requires git)
```bash
npx skills add <owner/repo> --skill <skill-name> --agent trae --yes
```

### List installed skills
```bash
npx skills list
```

## Tips
- `skills find` works without git
- `skills add` requires git installed on the system
- Browse skills at https://skills.sh
- Popular categories: python, testing, code-review, documentation, security