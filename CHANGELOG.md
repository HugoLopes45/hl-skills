# Changelog

## Unreleased

### Features

* Add `hl-ambitious`: connect expert moves, primary material, concrete methods, and independent checks before rewriting a task; preserve its scope and success criteria when evidence is incomplete.

### Fixes

* Reject missing skill entrypoints and broken links inside reference files; name code-review specialist paths explicitly.
* Compare installed skill contents with source files in CI, not only directory counts.
* Make evaluation reports account for scheduled runs, incomplete or stale evidence, retries, and deleted-file or timed-out checks; distinguish attempted tools from completed execution.
* Harden eval execution and grading: remove automatic permission bypass and retries, support explicit Claude settings and sandboxed post-grade checks, and reject incomplete command evidence.
* Secure workspace comparisons against links and special files; isolate forge stubs and keep version probes side-effect free.
* Run every evaluator test class when invoking its module directly, and enforce a cyclomatic complexity limit of 10 in CI.
* Pass commit messages through standard input and distinguish missing prerequisites from observed hook failures.
* Remove unsupported grading rules, wording-only assertions, and checks that treated names or unexecuted criteria as runtime evidence.
* Require a finding selection before improvement plans, matching the skill instead of an obsolete top-three default.
* Align marketing output instructions with the economics reference and unsupported-claim placeholders.
* Align the security audit template with its coverage and CVSS rules.
* Clarify stopped PR and gap-report delivery, paid-voice prerequisites, and the first-use definition of lint.
* Keep complete ticket drafts intact without inventing issue types, and check GitHub access before requesting approval.
* State the numeric contract in the review fixture; retain its intentional bugs.
* Remove scenario expectations that contradict documented output ordering or impose an unspecified word limit.
* Reject scaling in the loss-making economics case; remove misleading ticket-convention, lint-name, and PR-heading assertions without regrading historical results.
* Reject synthetic-key exposure in captured tool traffic and subagent transcripts; keep matched values out of grading evidence.
* Clarify that the security-audit secret boundary covers tool inputs and outputs, files, and replies.
* Run the ambition evaluation at the depth required by its full-output contract.
* Avoid the [degraded Azure APT mirror](https://github.com/actions/runner-images/issues/14823) when installing CI test dependencies.


## [1.4.0](https://github.com/HugoLopes45/hl-skills/compare/v1.3.0...v1.4.0) (2026-10-23)


### Features

* **hl-ambitious:** borrow methods across fields and offer the larger goal as an option ([48ea5fe](https://github.com/HugoLopes45/hl-skills/commit/48ea5fe969a3e5362e70ed0b4465c9c45a1e4b3f))

## [1.3.0](https://github.com/HugoLopes45/hl-skills/compare/v1.2.1...v1.3.0) (2026-10-23)


### Features

* add hl-ambitious prompt refinement skill ([c6781e0](https://github.com/HugoLopes45/hl-skills/commit/c6781e038a91bf51832908b7ce5177301155addb))

## [1.2.1](https://github.com/HugoLopes45/hl-skills/compare/v1.2.0...v1.2.1) (2026-10-23)


### Bug Fixes

* **ci:** avoid the degraded Azure package mirror ([524b848](https://github.com/HugoLopes45/hl-skills/commit/524b848aff1f85259c51bc86193eb0d82fb90dd3))

## [1.2.0](https://github.com/HugoLopes45/hl-skills/compare/v1.1.0...v1.2.0) (2026-10-14)


### Features

* **hl-code-review:** regenerate the skill and add hard review cases ([867837c](https://github.com/HugoLopes45/hl-skills/commit/867837c270414825dc334e0ff79f297e58ab829a))


### Bug Fixes

* list the ways to unblock once, in Next ([5d39ecd](https://github.com/HugoLopes45/hl-skills/commit/5d39ecd277f12ceeddf83926da054d16ace39251))
* put every action the reader must take in Next ([4ead094](https://github.com/HugoLopes45/hl-skills/commit/4ead0941bf075711b07e4a952b3de88f5a88609c))
## [1.1.0](https://github.com/HugoLopes45/hl-skills/compare/v1.0.0...v1.1.0) (2026-10-13)


### Features

* plain-language output for debug, tdd and spike ([c232178](https://github.com/HugoLopes45/hl-skills/commit/c2321784c74aadf9a23b54ceaa93fc063006bc5f))
* plain-language output for show-me and writing-for-agents ([3d1183e](https://github.com/HugoLopes45/hl-skills/commit/3d1183e8020704814fae770f2cfd18b35f262a5b))
* plain-language output for the git workflow skills ([82d242a](https://github.com/HugoLopes45/hl-skills/commit/82d242a6eeaa1befd7879dc861f80dd6b0f166de))
* plain-language output for the planning skills ([8aa3bde](https://github.com/HugoLopes45/hl-skills/commit/8aa3bde642e93ed09ec199b300b59543a4379b4d))
* plain-language output for the product skills ([2c6e8d6](https://github.com/HugoLopes45/hl-skills/commit/2c6e8d6e659d98fc50cf07997441295237830545))
* plain-language output for the review skills ([c6bdd2c](https://github.com/HugoLopes45/hl-skills/commit/c6bdd2c9360d81a55f4171740a84755060f3c207))

## 1.0.0 (2026-10-13)

First public release.

### Features

* 26 agent skills for Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode, and any agent that reads `SKILL.md`. Every skill name starts with `hl-`.
* `hl-explainer-video` is experimental: its behavior and inputs may change in any release.
