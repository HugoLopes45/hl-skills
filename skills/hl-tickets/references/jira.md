# Jira

Jira specifics for steps 1 and 2 of the skill.

## Grounding

- **Reference issue**: fetch it in full (`GET /rest/api/2/issue/<KEY>`, no `fields` param) for the raw description.
- **Flavor**: use the instance URL as a clue, not proof of its API version or stored markup. Confirm the flavor and markup against the instance and a raw description before recording them as observed. A requested project key proves neither.
- **Required fields**: `GET /rest/api/2/issue/createmeta?projectKeys=<KEY>&issuetypeNames=<Type>&expand=projects.issuetypes.fields`; on 404, `GET /rest/api/3/issue/createmeta/<KEY>/issuetypes`.
- **No API** (SSO wall, no token): read the reference in the editor source view, and the required-field markers on the create dialog.

## Markup

Convert when the instance stores wiki markup:

| Markdown | Jira wiki markup |
|---|---|
| `## H2` | `h2.` |
| `**bold**` · `*italic*` | `*bold*` · `_italic_` |
| `` `code` `` | `{{code}}` |
| ` ```bash ... ``` ` | `{code:bash} … {code}` |
| `- item` · `1. item` | `* item` · `# item` |
| `- [ ] item` | no native checkbox: `(/)` / `(x)`, or real Sub-tasks |
| `[text](url)` | `[text\|url]` |
| table | `\|\|A\|\|B\|\|` header, then `\|a\|b\|` |
| `> quote` | `{quote} … {quote}` |
| `#1149` | full URL, Jira has no GitHub cross-reference |

Confirm the editor's Markdown paste behavior before converting: converting twice leaves literal `h2.` in the body. When the reader must validate the editor or references, put that prerequisite only in Next, with its owner and the delivery step it blocks; leave unobserved markup explicit in the draft.
