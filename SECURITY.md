# Security

## Report a vulnerability

Report it privately through [GitHub private vulnerability reporting](https://github.com/HugoLopes45/hl-skills/security/advisories/new). Do not open a public issue.

Include the skill, the agent and model, and the steps to reproduce.

## Scope

- A skill that makes an agent run a destructive command, leak secrets, or act on shared state without an explicit request.
- A skill that makes an agent follow instructions from untrusted content, such as files, web pages, or issue text.

The behavior of a model that ignores a skill is out of scope. Report it as a skill problem issue.
