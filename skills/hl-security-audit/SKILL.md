---
name: hl-security-audit
description: "Complete read-only security audit of a codebase or a path in it. Runs real scanners for evidence, traces untrusted input to dangerous sinks, scores by CWE/CVSS, writes a prioritized report. Use when the user asks for a security review or audit, or whether an attacker can abuse a repository, file, or endpoint. Not for reviewing a single diff (use `hl-code-review`)."
---
# Security Audit

Input: `[quick|standard|deep] [<path>] [--report]`

Audit a whole codebase for vulnerabilities. Assume the worst: the input is malicious, the auth check fails open, the secret is in the repo. Every value crossing a trust boundary is an attack until proven safe. Read-only on source; the report is the deliverable.

Two lanes: the mechanical lane runs real read-only scanners whose output is evidence; the review lane judges whether a hit is reachable and exploitable, after you open the code. A finding ships only when a scanner hit or a traced path backs it and you have read the cited line. There is no independent verifier; the verifier is you reading the code with the scanner output in hand. Confidence an LLM assigns itself is not evidence.

## Stance

- Every input is hostile. Trace each value from where it enters (request body, query param, header, upload, queue message, deserialized blob, webhook) to where it lands (SQL, shell, file path, template, `eval`, response HTML, redirect, auth decision).
- Hunt the unstated assumption: "user is always logged in", "this ID belongs to the caller", "this header is trusted".
- Silent failures fail open: swallowed exceptions, unawaited promises, unchecked null, ignored returns, auth that falls through to allow.

## Hard rules

1. Never modify source. The only file you may write is the report (Phase 5).
2. Read-only execution only. Run scanners, audits, `grep`, `tsc --noEmit`. Never install, build, write files other than the report, commit, or hit the network for side effects.
3. Never reproduce a secret value. Cite `file:line` and credential type, recommend rotation.
4. Vet before reporting. Scanners over-report; LLM traces hallucinate. For every CRITICAL and HIGH, open the cited code and confirm the path. Fix line numbers, drop false positives, merge cross-lane duplicates.
5. If `security-exceptions.json` exists, read it. Matching findings go to the Accepted risk section with rationale and expiry, not the main list.

## Phase 1, Recon and threat model

Read README, AGENTS.md or the equivalent instruction file, config, CI. Identify languages, frameworks, package managers. Find the trust boundaries: every place untrusted input enters. Note existing defenses (parameterized ORMs, framework auto-escaping) so you don't flag what is already safe. Name the crown jewels: auth, payment, PII, admin paths, key material.

Write a one-paragraph threat model; every later phase scopes to it. A `<path>` argument scopes the audit to that subtree.

## Phase 2, Mechanical pass

Detect the stack, run the read-only scanners that apply, capture raw output as evidence. Skip any tool not installed and record it in the report: a silent gap reads as "clean" when it isn't.

- Dependencies and CVEs: `npm audit --json`, `pnpm audit`, `pip-audit`, `composer audit`, `cargo audit`, `osv-scanner`, `govulncheck`. Group by severity; separate direct from transitive.
- Secrets: `gitleaks detect` or `trufflehog`, else grep key/token/password assignment patterns. Report `file:line` and type, never the value.
- SAST: `semgrep --config auto`, `bandit`, `gosec`, `brakeman`, eslint security plugins, whichever the stack supports.
- Pattern grep where no SAST covers it: string-built SQL, `exec`/`system` with variables, `eval`/`unserialize`/`pickle.load` on input, `dangerouslySetInnerHTML`, XML parse without entity restrictions, `md5`/`sha1` on passwords, `rand`/`mt_rand` for security values, file ops on user-controlled paths.

## Phase 3, Review pass

For each mechanical hit and each entry point, trace untrusted input to its sink and decide whether it is reachable and exploitable. A hit in dead code or behind a hard auth gate is not a finding.

For a full repo at `standard` or `deep`, fan out parallel read-only subagents, one per category, when the host supports them; otherwise review the categories yourself, one at a time. Subagents don't inherit this context: each prompt carries the threat model, the recon facts, and the category's mechanical hits, and returns candidate findings only (no fixes, no file dumps) as `file:line | <input → sink> | category | why exploitable | confidence H/M/L`.

Depth follows the level (default `standard`):

| | quick | standard | deep |
|---|---|---|---|
| Mechanical | deps + secrets | + SAST + pattern grep | + pattern grep on the whole tree |
| Review categories | injection, authn/authz, secrets | all 8 | all 8 |
| Breadth | entrypoints | input paths | everywhere |
| Findings | CRITICAL + HIGH | + MEDIUM | + MEDIUM, + Investigate |

### Categories

1. Injection (CWE-89/78/611/90): SQLi, command injection, XXE, NoSQL/LDAP injection, template injection, path traversal.
2. Authn/authz (CWE-287/639/862): auth bypass, missing ownership check (IDOR), privilege escalation, session/JWT flaws, checks that fail open.
3. Crypto and secrets (CWE-798/327/338): hardcoded keys, weak algorithms, bad key storage, predictable randomness for security values, cert validation bypass.
4. Code execution and deserialization (CWE-502/94): RCE via unsafe deserialization (pickle, unsafe YAML, gadget chains, `phar://`), `eval` on untrusted input.
5. XSS (CWE-79): reflected, stored, DOM. React/Angular only via `dangerouslySetInnerHTML` or `bypassSecurityTrust*`.
6. Data exposure (CWE-200/532): secrets or PII logged or returned, debug leakage, over-exposed endpoints.
7. SSRF, host or protocol control only (CWE-918). Path-only control is not a finding.
8. Vulnerable dependencies: a CVE from Phase 2 is a finding only if its vulnerable code path is reachable from the app.

## Phase 4, Vet, score, filter

Vet per hard rule 4. Score each finding by impact times likelihood into CRITICAL, HIGH, or MEDIUM, and map its CWE; drop anything lower, and at `quick` drop MEDIUM too. Dedupe across lanes: a SAST hit and a manual trace of the same line are one finding. Apply the filter below; default to dropping when the path isn't concrete. A CRITICAL or HIGH finding not confirmed, or any finding below confidence H, goes to Investigate at `deep` and is dropped otherwise.

Drop automatically:

- DoS and resource exhaustion (memory, CPU, file descriptors).
- Secrets at rest on disk if otherwise secured.
- Rate limiting and overload.
- Missing validation on non-security-critical fields with no proven impact.
- GitHub Action workflow injection unless concretely triggerable by untrusted input.
- Absence of a hardening measure. Concrete vulns only.
- Theoretical race and timing issues. Concrete and exploitable only.
- Memory safety (overflow, use-after-free) in memory-safe languages (Rust, Go, JS, Python).
- Findings only in unit-test or fixture files.
- Log spoofing and logging unsanitized non-secret input.
- SSRF controlling only the path.
- User-controlled content in AI system prompts.
- Regex injection and regex DoS.
- Findings in documentation files.
- Absence of audit logging.

Precedents:

- Logging a high-value secret in plaintext is a vuln. Logging a URL is safe.
- UUIDs are unguessable; no need to validate them.
- Env vars and CLI flags are trusted. An attack that needs to control them is invalid.
- Tabnabbing, XS-Leaks, prototype pollution, and open redirect only at very high confidence.
- React and Angular are XSS-safe unless using the unsafe HTML methods above.
- Client-side missing authn/authz is not a vuln. The backend owns validation.
- Command injection in a shell script only with a concrete untrusted-input path.
- A MEDIUM ships only if obvious and concrete.

## Phase 5, Report

With `--report`, or for a whole-repository `standard` or `deep` run, write `security-audit.md` in the repository root, using the stored template below. The reply presents the same findings in the shape below and names that file in `**Changed:**`. Otherwise `**Changed:** none`.

Reader: a developer or security lead who decides what to fix first and whether to trust the audit. Define each term once in the reply, where it first appears: CWE-n is the public ID of a weakness type; assurance is how much of the code the checks covered, not how safe the code is; a sink is where untrusted input does harm; transitive means pulled in by another dependency.

Line 1, bold, one plain sentence, 100 characters at most: the risk in everyday words, or for a clean result, what the checks covered. Never open with a label, severity word, CWE ID, or count.

Under line 1, plain sentences without labels, in this order:
- Assurance, as one sentence that gives the level and names what did not run: "Assurance is medium: gitleaks ran, semgrep did not, and I did not review the PIN service."
- Each risk seen outside the requested scope, as one line that starts "Outside what you asked:", with its `file:line` and why it matters. Never a numbered point, never in the findings.

Then numbered points, worst first. Each point: a bold plain sentence that states the problem and its seriousness in words ("critical", "high", "medium"); one or two sentences on how an attacker reaches it and whether you read or ran it; a `text` view of the traced hops, only when it helps; the fix in one sentence.

Then the verdict line, `**Next:**`, and `**Changed:**`:
- `Verdict: Exploitable`: a critical or high finding with a traced path an attacker can use.
- `Verdict: Risks`: medium findings only.
- `Verdict: No high-confidence exploitable vulnerabilities in <scope>`: HIGH assurance only. Set the assurance first; it picks this wording. Below HIGH: `Verdict: No vulnerabilities surfaced by the checks that ran`.
- `**Next:**`: each step to act on, in severity order, then the rerun.

````markdown
**Anyone can run shell commands through the class-booking email field.**
Assurance is medium: gitleaks and bandit ran, semgrep did not, and the door-lock service is outside this repository, so I did not review it.
Outside what you asked: `staff/payroll.py:8` writes salaries to a log file (CWE-532). I did not review it.

1. **Email text runs as a shell command, a critical risk (CWE-78).**
   I read the code from the form to the call. Typing `a@b.c; ls -la` runs a second command on the server.
   ```text
   booking/notify.py:9   addr = request.form["email"]   # typed by anyone
   booking/notify.py:14  os.system(f"sendmail {addr}")  # runs a shell command
   ```
   Pass the address as one argument: `subprocess.run(["sendmail", addr])`.

2. **A failed door-code check leaves the door open, a high risk (CWE-287).**
   I read `gym/door.py:19` and did not run it. The check returns True when it fails.
   Return False on error, so the door stays locked.

Verdict: Exploitable

**Next:**
1. Fix `booking/notify.py:14` as shown, then rerun the audit on `booking/`.
2. Make `gym/door.py:19` return False on a failed code.
3. Install `semgrep` and rerun the audit; assurance stays medium until then.

**Changed:** security-audit.md
````

A clean result reads the same way: line 1 says what the checks covered, the assurance sentence follows, plain sentences state what was read, and the verdict is `No vulnerabilities surfaced by the checks that ran`.

The stored `security-audit.md` uses this template, with every section kept:

````markdown
**<line 1 of the reply>**
Verdict: <the reply's verdict>
Assurance: HIGH | MEDIUM | LOW; not checked: <the unchecked surface, or "nothing">
Out of scope: <risk, file:line, why it matters>

## Findings
| # | Severity | Finding (CWE) | Where | Fix |
|---|---|---|---|---|
| 1 | CRITICAL | SQLi (CWE-89) | clinic/search.py:42 | Whitelist sort columns |

## 1. SQL injection, clinic/search.py:42
CRITICAL · CWE-89 · confidence H · evidence: semgrep + traced path
```text
clinic/search.py:38  sort = request.args["sort"]    # untrusted: query param
clinic/search.py:42  f"... ORDER BY {sort}"         # SINK: string-built SQL
clinic/db.py:17         cursor.execute(query)          # runs on the production database
```
Exploit: `?sort=id;DROP TABLE users--` runs attacker SQL.
Fix: whitelist the sort columns, as `clinic/schedule.py:88` does.

## Dependencies
| Package | CVE (severity) | Direct/Transitive | Reachable | Fix version |
|---|---|---|---|---|

## Accepted risk
Findings matched by security-exceptions.json, with rationale and expiry.

## Investigate
`deep` only. Candidates not confirmed or below confidence H, with what would confirm each.

## Considered and dismissed
Closed candidates only, with the reason, so the next audit doesn't re-raise them.

## Scanners
| Tool | Status |
|---|---|
| semgrep | ran |
| npm audit | ran, nothing to check (no lockfile) |
| bandit | skipped: not installed |

**Next:**
1. <the fix for the highest finding, then the rest in severity order>
2. <install and rerun the skipped scanners, when assurance is below HIGH>

Date: <date> · Commit: <short SHA> · Scope: <path / whole repo> · Depth: quick|standard|deep
````

## Coverage gate

Set Assurance from what actually ran, never implying safety you didn't verify.

- HIGH: SAST plus dependency and secret scans ran on the full scope, and you hand-vetted every CRITICAL and HIGH.
- MEDIUM: some scanners ran, or scope was partial. Name what wasn't covered.
- LOW: no SAST or dependency scanner was available, so the audit is LLM-only and unconfirmed by tooling. List the tools to install (`semgrep`, the stack's dependency auditor, `gitleaks`) and rerun.

Found nothing? You may only write `No high-confidence exploitable vulnerabilities in <scope>` at HIGH assurance. Below HIGH, write `No vulnerabilities surfaced by the checks that ran` and list the unchecked surface. Don't manufacture findings to look thorough, and don't let "found nothing" and "barely looked" read the same.
