---
name: hl-security-audit
description: "Read-only security audit of a codebase or a path in it. Runs real scanners for evidence, traces untrusted input to dangerous sinks, scores by CWE/CVSS, writes a prioritized report. Use when the user asks for a security review or audit, or whether an attacker can abuse a repository, file, or endpoint. Not for reviewing a single diff (use `hl-code-review`)."
---
# Security Audit

Input: `[quick|standard|deep] [<path>] [--report]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Lead with evidenced attacker impact and coverage. Keep exploit prerequisites and uncertainty with each finding; preserve the complete report and outside-scope warnings.

Audit a whole codebase for vulnerabilities. Treat external input as untrusted. Test whether defenses fail; do not assume a vulnerability before tracing its path. Read-only on source; the report is the deliverable.

Two lanes: the mechanical lane runs real read-only scanners whose output is evidence; the review lane judges whether a hit is reachable and exploitable, after you open the code. A finding ships only when a scanner hit or a traced path backs it and you have read the cited line. There is no independent verifier; the verifier is you reading the code with the scanner output in hand. Confidence an LLM assigns itself is not evidence.

## Stance

- Every input is hostile. Trace each value from where it enters (request body, query param, header, upload, queue message, deserialized blob, webhook) to where it lands (SQL, shell, file path, template, `eval`, response HTML, redirect, auth decision).
- Hunt the unstated assumption: "user is always logged in", "this ID belongs to the caller", "this header is trusted".
- Check whether swallowed exceptions, unawaited promises, unchecked null, ignored returns, or auth fallthrough bypass a security decision.

## Hard rules

1. Never modify source. The only file you may write is the report (Phase 5).
2. Read-only execution only. Run scanners, audits, `grep`, `tsc --noEmit`. Never install, build, write files other than the report, commit, or hit the network for side effects.
3. Never expose secret values in tool inputs or outputs, files, or replies. Before each scan, record the exact invocation and the permitted help or documentation proving redaction and allowed network behavior, including telemetry and version lookups. Local scanning or silence about networking is not proof of offline behavior. Inconclusive evidence: skip the scan and report the coverage gap; a sandbox does not replace this preflight. Skip forbidden files. External uploads need explicit approval. Cite `file:line` and credential type, recommend rotation.
4. Vet before reporting. Scanners over-report; LLM traces hallucinate. For every CRITICAL and HIGH, open the cited code and confirm the path. Fix line numbers, drop false positives, merge cross-lane duplicates.
5. If `security-exceptions.json` exists, read it. Matching findings go to the Accepted risk section with rationale and expiry, not the main list.

## Phase 1, Recon and threat model

Read README, AGENTS.md or the equivalent instruction file, config, CI. Identify languages, frameworks, package managers. Find the trust boundaries: every place untrusted input enters. Note existing defenses (parameterized ORMs, framework auto-escaping) so you don't flag what is already safe. Name the crown jewels: auth, payment, PII, admin paths, key material.

Write a one-paragraph threat model; every later phase scopes to it. A `<path>` argument scopes the audit to that subtree.

## Phase 2, Mechanical pass

Detect the stack, run the read-only scanners that apply, capture raw output as evidence. Skip any tool not installed and record it in the report: a silent gap reads as "clean" when it isn't.

- Dependencies and CVEs: `npm audit --json`, `pnpm audit`, `pip-audit`, `composer audit`, `cargo audit`, `osv-scanner`, `govulncheck`. Group by severity; separate direct from transitive.
- Secrets: an installed scanner such as `gitleaks` or `trufflehog`, configured to redact values before output. If no safe mode is available, report the scan unavailable; never print matching secret lines.
- SAST: `semgrep` with already-local rules, `bandit`, `gosec`, `brakeman`, eslint security plugins, whichever the stack supports. Apply the hard rules before executing any example; tool names do not authorize downloads or disallowed writes.
- Pattern grep where no SAST covers it: string-built SQL, `exec`/`system` with variables, `eval`/`unserialize`/`pickle.load` on input, `dangerouslySetInnerHTML`, XML parse without entity restrictions, `md5`/`sha1` on passwords, `rand`/`mt_rand` for security values, file ops on user-controlled paths.

## Phase 3, Review pass

For each mechanical hit and each entry point, trace untrusted input to its sink and decide whether it is reachable and exploitable. A hit in demonstrably unreachable code is not a finding. An auth gate alone does not prove the path safe.

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
5. XSS (CWE-79): reflected, stored, DOM. Check framework escaping, unsafe HTML methods, and DOM writes outside protected contexts.
6. Data exposure (CWE-200/532): secrets or PII logged or returned, debug leakage, over-exposed endpoints.
7. SSRF (CWE-918): trace attacker influence on requests, redirects, and reachable internal or privileged resources. A fixed host alone does not prove safety.
8. Vulnerable dependencies: a CVE from Phase 2 is a finding only if its vulnerable code path is reachable from the app.

## Phase 4, Vet, score, filter

Vet per hard rule 4. Classify each finding by evidenced impact and exploit prerequisites as CRITICAL, HIGH, or MEDIUM, and map its CWE. Use a checked scoring method for CVSS and report its version and inputs; otherwise mark CVSS unscored. Then drop anything lower, and at `quick` drop MEDIUM too. Dedupe across lanes: a SAST hit and a manual trace of the same line are one finding. Apply the filter below. Unconfirmed candidates are not findings; at `deep`, list them under Investigate. At every depth, record unresolved exposure that limits the conclusion as a coverage gap.

Filter by the traced threat model, not a blanket exemption:

- Close a candidate only when the path is unreachable, the relevant defense prevents it, or the traced behavior has no security impact. Record the reason.
- An authentication gate does not exclude authenticated attackers. Check roles, ownership, and affected data.
- Environment variables and CLI arguments are trusted only when their setters are trusted. Trace their origin.
- A UUID is not authorization. A URL can contain credentials. Framework escaping protects only the contexts it actually covers.
- Do not dismiss a concrete path solely because it concerns resource exhaustion, a race, a regular expression, a prompt, a fixture, documentation, or memory safety. Establish attacker control, execution context, and impact.
- Missing hardening alone is not an exploit. Unconfirmed paths remain explicit coverage gaps or Investigate candidates at `deep`, not confirmed findings.

## Phase 5, Report

With `--report`, or for a whole-repository `standard` or `deep` run, write `security-audit.md` in the repository root, using the stored template below. Keep its formal fields, fixes, traces, scanner evidence, coverage, and assurance complete. The reply presents the findings' consequences and decisive evidence, without repeating the report's fixes as body advice, and names that file in `**Changed:**`. Otherwise `**Changed:** none`.

Reader: a developer or security lead who decides what to fix first and whether to trust the audit. Use plain consequences and coverage in chat; the stored report retains formal classifications. Define a technical term only if the reply needs it.

Line 1, bold, one plain sentence: the risk in everyday words, or for a clean result, what the checks covered. A live credential or data-loss risk goes first, including outside scope. Never open with a label, severity word, CWE ID, or count.

Under line 1, plain sentences without labels, in this order:
- Name the checks that ran and what did not run or was not reviewed. Keep the scope and gaps explicit. Set the assurance level using the Coverage gate; the stored report records it formally.
- Each risk seen outside the requested scope, as one line that starts "Outside what you asked:", with its `file:line` and why it matters. Never a numbered point, never in the findings.

Then numbered points, worst first. Each point: a bold plain sentence that states the consequence and its seriousness in words ("critical", "high", "medium"); the decisive evidence, how an attacker reaches it, and whether you read or ran it; a `text` view of the traced hops, only when it helps. Keep uncertain exploit prerequisites explicit, such as attacker control of a loaded file. Fixes belong only in Next in chat.

Then the verdict line, `**Next:**`, and `**Changed:**`:
- `Verdict: Exploitable`: a critical or high finding with a traced path an attacker can use.
- `Verdict: Risks`: medium findings only.
- No confirmed findings: at HIGH assurance, `Verdict: No high-confidence exploitable vulnerabilities in <scope>`; otherwise, `Verdict: No vulnerabilities surfaced by the checks that ran`.
- `**Next:**`: every reader action, decision, prerequisite, and unblock route once. Credential response, including revoking or rotating exposed credentials, comes first, then other fixes in severity order, then the rerun. Include responses to outside-scope risks without treating them as audited findings.

````markdown
**Anyone can run shell commands through the class-booking email field.**
gitleaks and bandit ran; semgrep did not, and the door-lock service is outside this repository, so I did not review it.
Outside what you asked: `staff/payroll.py:8` writes salaries to a log file. I did not review it.

1. **Email text runs as a shell command, a critical risk.**
   I read the code from the form to the call; I did not run it. From that trace, `a@b.c; ls -la` would run a second command on the server.
   ```text
   booking/notify.py:9   addr = request.form["email"]   # typed by anyone
   booking/notify.py:14  os.system(f"sendmail {addr}")  # runs a shell command
   ```

2. **A failed door-code check leaves the door open, a high risk.**
   I read `gym/door.py:19` and did not run it. The check returns True when it fails.

Verdict: Exploitable

**Next:**
1. Pass the address as one argument at `booking/notify.py:14`: `subprocess.run(["sendmail", addr])`.
2. Make `gym/door.py:19` return False on a failed code, so the door stays locked.
3. Have the payroll owner assess salary logging at `staff/payroll.py:8`; it was outside this audit.
4. Install `semgrep` and rerun the audit, including `booking/`; the skipped check leaves coverage incomplete.

**Changed:** security-audit.md
````

A clean result reads the same way: line 1 says what the checks covered, the coverage sentence follows, and plain sentences state what was read. At HIGH assurance use `No high-confidence exploitable vulnerabilities in <scope>`; below HIGH use `No vulnerabilities surfaced by the checks that ran`.

The stored `security-audit.md` uses this template, with every section kept:

````markdown
**<line 1 of the reply>**
Verdict: <the reply's verdict>
Assurance: HIGH | MEDIUM | LOW; not checked: <the unchecked surface, or "nothing">
Out of scope: <risk, file:line, why it matters>

## Findings
| # | Severity | Finding (CWE) | Where | Fix |
|---|---|---|---|---|
| 1 | <severity justified by evidenced impact> | <finding (CWE)> | <file:line> | <fix> |

## 1. <finding>, <file:line>
<severity> · <CWE> · <confidence> · CVSS: <checked version and inputs, or unscored> · evidence: <checked evidence>
```text
<trace from attacker-controlled input to sink, with verified file:line anchors>
```
Exploit: <supported outcome, prerequisites, and whether observed or predicted>.
Fix: <grounded correction>.

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
| Tool | Exact command and directory | Executions | Status and evidence |
|---|---|---|---|
| <scanner> | <command; working directory> | <actual count> | <result or explicit coverage gap; offline/redaction preflight source> |

**Next:**
1. <credential response first, then other fixes in severity order>
2. <install and rerun the skipped scanners, when assurance is below HIGH>

Date: <date> · Commit: <short SHA> · Scope: <path / whole repo> · Depth: quick|standard|deep
````

## Coverage gate

Set Assurance from what actually ran, never implying safety you didn't verify.

- HIGH: SAST plus dependency and secret scans ran on the full scope, and you hand-vetted every CRITICAL and HIGH.
- MEDIUM: successful SAST or dependency coverage exists, but a required scan or scope is incomplete. Name what wasn't covered.
- LOW: neither SAST nor dependency coverage succeeded. No applicable targets does not establish coverage. Secret-only scans leave code findings unconfirmed by tooling. Name the missing coverage and the permitted rerun prerequisites.

Found nothing? You may only write `No high-confidence exploitable vulnerabilities in <scope>` at HIGH assurance. Below HIGH, write `No vulnerabilities surfaced by the checks that ran` and list the unchecked surface. Don't manufacture findings to look thorough, and don't let "found nothing" and "barely looked" read the same.
