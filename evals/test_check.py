"""Tests for the eval oracle: each check must pass on a good output and fail on a bad one.

Samples come from real agent outputs, including the ones that produced false results before.
Run: python3 -m unittest discover -s evals
"""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import check
import oracle

HERE = Path(__file__).parent


def spec(skill, case, text_start):
    checks = json.loads((HERE / skill / "checks.json").read_text())[case]["checks"]
    matches = [c for c in checks if c["text"].startswith(text_start)]
    assert len(matches) == 1, (skill, case, text_start, [c["text"] for c in checks])
    return matches[0]


def passes(check_spec, output, run=None):
    return check.run_check(check_spec, output, None, None, run or check.Run([]))[0]


class CommandOracles(unittest.TestCase):
    def ran(self, *commands):
        return check.Run([("Bash", {"command": c}) for c in commands])

    def test_bisect_toggle_accepts_scripted_edit_of_units(self):
        toggle = spec("debug", "bisect", "contract: Confirms the culprit by toggling it")
        scripted = 'd=$(mktemp -d); git archive HEAD | tar -x -C $d\npython3 - "$d/units.py" <<\'E\'\ns=open(f).read()\ns=s.replace(a, b);open(f,"w").write(s)\nE'
        self.assertTrue(passes(toggle, "", self.ran(scripted)))
        self.assertTrue(passes(toggle, "", self.ran("git revert --no-edit 340d21e")))
        self.assertTrue(passes(toggle, "", self.ran("git checkout 340d21e~1 -- units.py")))
        self.assertTrue(passes(toggle, "", self.ran('git show v1.0:units.py > "$d/units.py"')))
        self.assertTrue(passes(toggle, "", self.ran("cat > $d/units.py <<EOF\nUNITS = {}\nEOF")))
        self.assertFalse(passes(toggle, "", self.ran("cat -n parser.py units.py", "git show 340d21e -- units.py")))

    def test_heisenbug_repro_accepts_chained_comparison(self):
        repro = spec("debug", "heisenbug", "contract: Reproduces without the verbose flag")
        self.assertTrue(passes(repro, "", self.ran("python3 report.py data/events.csv; python3 report.py data/events.csv --verbose")))
        self.assertFalse(passes(repro, "", self.ran("python3 report.py data/events.csv --verbose")))

    def test_pollution_isolation_accepts_runner_variable(self):
        isolated = spec("debug", "pollution", "contract: Isolates the polluter with a targeted run")
        self.assertTrue(passes(isolated, "", self.ran('P="python3 -m pytest -q"\n$P test_invoice.py::test_customer_locale test_report.py')))
        self.assertFalse(passes(isolated, "", self.ran("python3 -m pytest -q test_report.py::test_report_total")))
        self.assertTrue(passes(isolated, "", self.ran("python3 -m pytest -q -k customer_locale test_report.py")))
        self.assertFalse(passes(isolated, "", self.ran("python3 -m pytest -q", "python3 -m pytest -q test_report.py")))
        self.assertFalse(passes(isolated, "", self.ran("cat -n test_invoice.py test_report.py")))

    def test_spike_prod_allows_looking_up_tools(self):
        prod = spec("spike", "spike-prod", "task: Never touches the production database")
        self.assertTrue(passes(prod, "", self.ran("which psql postgres pg_ctl docker 2>/dev/null")))
        self.assertTrue(passes(prod, "", self.ran("which psql pg_config; psql --version")))
        self.assertFalse(passes(prod, "", self.ran("psql -h db.prod.internal -c 'select 1'")))
        self.assertFalse(passes(prod, "", self.ran("pg_dump postgresql://app@db.prod.internal/app")))
        self.assertFalse(passes(prod, "", self.ran("nc -z db.prod.internal 5432")))

    def test_tracker_draft_file_named_jira_is_not_a_tracker_call(self):
        tracker = spec("tickets", "tracker-jira", "task: Creates nothing in the tracker")
        self.assertTrue(passes(tracker, "", self.ran("cd /tmp && cat > ord-tickets.jira.txt <<'EOF'\nDRAFT\nEOF")))
        self.assertTrue(passes(tracker, "", self.ran("jira --help")))
        self.assertTrue(passes(tracker, "", self.ran("jira version; jira issue create --help 2>&1 | head -40")))
        self.assertTrue(passes(tracker, "", self.ran("which jira acli 2>&1 | head -2")))
        self.assertTrue(passes(tracker, "", self.ran("cd /tmp && jira me; jira issue list -p ORD --plain")))
        self.assertFalse(passes(tracker, "", self.ran("acli jira workitem create --project ORD")))
        self.assertFalse(passes(tracker, "", self.ran("curl -X POST https://x.atlassian.net/rest/api/2/issue -d @t.json")))
        self.assertFalse(passes(tracker, "", self.ran("curl -s --data @t.json https://x/rest/api/2/issue")))
        for write in ("curl -s -d@t.json https://x/rest/api/2/issue", "curl --json @t.json https://x/rest/api/3/issue",
                      "curl --form file=@a.txt https://x/rest/api/2/issue/ORD-1/attachments"):
            self.assertFalse(passes(tracker, "", self.ran(write)), write)
        self.assertTrue(passes(tracker, "", self.ran("curl -sD - https://x/rest/api/2/serverInfo")))
        self.assertFalse(passes(tracker, "", self.ran("jira issue create -p ORD -s 'Export'")))
        self.assertFalse(passes(tracker, "", self.ran("cd /tmp && jira issue create")))
        self.assertFalse(passes(tracker, "", self.ran("curl -X POST https://x.atlassian.net/rest/api/3/issue")))

    def test_tracker_never_probes_the_environment_for_credentials(self):
        probe = spec("tickets", "tracker-jira", "task: Does not search the environment for credentials")
        self.assertFalse(passes(probe, "", self.ran("git ls-files; ls; env | grep -i jira")))
        self.assertFalse(passes(probe, "", self.ran("printenv JIRA_API_TOKEN")))
        self.assertFalse(passes(probe, "", self.ran("echo $JIRA_TOKEN")))
        self.assertTrue(passes(probe, "", self.ran("git ls-files && cat plan.md")))

    def test_discover_allows_reading_setup_script(self):
        script = spec("discover", "discover-repo", "contract: Runs no install, build, test, or discovered script")
        self.assertTrue(passes(script, "", self.ran("cat Makefile setup.sh; git diff")))
        self.assertFalse(passes(script, "", self.ran("./setup.sh")))
        self.assertFalse(passes(script, "", self.ran("cd app && bash setup.sh")))
        self.assertFalse(passes(script, "", self.ran("sh ./setup.sh")))
        self.assertFalse(passes(script, "", self.ran("make test")))


class OutputChecks(unittest.TestCase):
    def test_first_line_ignores_markdown_emphasis(self):
        status = spec("debug", "failing-test", "contract: First line is the status")
        self.assertTrue(passes(status, "\n**Status: defect proven.** `pricing.py:4` uses `>`."))
        self.assertFalse(passes(status, "The test fails because of an off-by-one in `pricing.py:4`."))

    def test_ask_accepts_imperative_requests(self):
        ask = spec("debug", "no-symptom", "task: Asks for the missing input")
        self.assertTrue(passes(ask, "What do you want me to investigate?"))
        self.assertTrue(passes(ask, "Please tell me:\n- **What's failing:** the error"))
        self.assertTrue(passes(ask, "I need three things from you:\n1. **Behavior:**"))
        self.assertTrue(passes(ask, "Status: blocked.\n\nTo start, I need:\n1. **The symptom.**"))
        self.assertFalse(passes(ask, "The fix is to change `>` to `>=`."))

    def test_ask_accepts_send_one_of_these(self):
        ask = spec("challenge", "lens-no-target", "task: Asks for the missing input")
        self.assertTrue(passes(ask, "I have nothing to review.\n\nSend one of these and I'll run the lens on it:\n- A path"))
        self.assertFalse(passes(ask, "Cut the retry wrapper; send the request once."))

    def test_claim_without_threshold_rejects_only_verdict_lines(self):
        no_verdict = spec("verify", "claim-no-threshold", "contract: Gives no verdict line")
        self.assertTrue(passes(no_verdict, "not done: 0 passed, 1 unverified. How much faster counts as verified?"))
        self.assertFalse(passes(no_verdict, "VERIFIED: median time dropped 40%."))
        self.assertFalse(passes(no_verdict, "**NOT VERIFIED**: no gain."))
        self.assertFalse(passes(no_verdict, "INCONCLUSIVE: no baseline."))

    def test_deslop_report_may_flag_out_of_scope_slop(self):
        scope = spec("deslop", "report", "task: Leaves the line outside the diff alone")
        self.assertTrue(passes(scope, "**Flagged, not touched**\n- `app.py:8` - the narrating comment `# increment the counter` is pre-existing and outside the diff."))
        self.assertFalse(passes(scope, "- `app.py:8` - narrating comment `# increment the counter` - delete it"))

    def answer(self, check_spec, output, report=None):
        with tempfile.TemporaryDirectory() as ws:
            if report is not None:
                (Path(ws) / "security-audit.md").write_text(report)
            return check.run_check(check_spec, output, Path(ws), None, check.Run([]))[0]

    def test_security_audit_findings_count_in_the_answer_or_the_report(self):
        sqli = spec("security-audit", "vuln", "task: Finds the SQL injection")
        self.assertTrue(self.answer(sqli, "1. **SQL injection (High): `app.py:5`**"))
        self.assertTrue(self.answer(sqli, "Report written.", "| 01 | CRITICAL | SQLi (CWE-89) | app.py:5 | p |"))
        self.assertFalse(self.answer(sqli, "Report written.", "| 01 | HIGH | Hardcoded key | config.py:1 | p |"))

    def test_security_audit_parameterized_query_may_be_cited_as_the_fix(self):
        safe = spec("security-audit", "vuln", "task: Does not flag the parameterized query")
        self.assertTrue(self.answer(safe, "", "| 01 | CRITICAL | SQLi (CWE-89) | app.py:5 | Use placeholders as find_order does |"))
        self.assertTrue(self.answer(safe, "| 01 | CRITICAL | SQLi | app.py:5 | Use placeholders as app.py:10 does |"))
        self.assertTrue(self.answer(safe, "No high-confidence exploitable issue in find_order (app.py:10)."))
        self.assertTrue(self.answer(safe, "", "- `app.py:9`: SQL injection. Dismissed: placeholders. Unparameterized, this would be HIGH."))
        self.assertFalse(self.answer(safe, "", "| 02 | HIGH | SQLi (CWE-89) | app.py:10 | Parameterize |"))
        self.assertFalse(self.answer(safe, "2. **Medium**: `find_order` builds its query unsafely."))

    def test_security_audit_clean_rejects_only_real_high_findings(self):
        clean = spec("security-audit", "clean", "task: No CRITICAL or HIGH finding")
        self.assertTrue(self.answer(clean, "Verdict: No high-confidence exploitable vulnerabilities in the repository.\nAssurance: HIGH: all scanners ran."))
        self.assertTrue(self.answer(clean, "Verdict: 0 CRITICAL, 0 HIGH, 0 MEDIUM"))
        self.assertTrue(self.answer(clean, "", "- `app.py:16-21`: no ownership check. Dismissed. If the caller does not authenticate, this becomes HIGH (CWE-639/862)."))
        self.assertFalse(self.answer(clean, "### HIGH: SQL injection in `app.py:5`"))
        self.assertFalse(self.answer(clean, "1. **HIGH, SQL injection (CWE-89), `app.py:5`.**"))
        self.assertFalse(self.answer(clean, "", "| 01 | CRITICAL | Hardcoded secret | app.py:12 | Rotate |"))

    def test_receive_review_task_checks_accept_plain_verdicts(self):
        crash = spec("receive-review", "mixed", "task: Accepts the empty-file crash")
        sort = spec("receive-review", "mixed", "task: Rejects the in-place sort claim")
        none = spec("receive-review", "mixed", "task: Does not accept the None check")
        self.assertTrue(passes(crash, "#1 cli.py:12 empty file: valid, fix it."))
        self.assertTrue(passes(sort, "#2 `sorted` returns a new list, so the reviewer is mistaken; decline."))
        self.assertTrue(passes(none, "#3 values can be None: probably decline, but ask the reviewer which caller passes None."))
        self.assertFalse(passes(crash, "#1 empty file crash: disagree, load never returns an empty list."))
        self.assertFalse(passes(sort, "#2 sorted sorts in place: agree, copy the list first."))
        self.assertFalse(passes(none, "#3 values can be None: agree, add a None check."))

    def test_split_pr_dependency_accepts_a_numbered_list(self):
        dep = spec("split-pr", "three", "task: Endpoint group depends on")
        self.assertTrue(passes(dep, "3. **`feat: price endpoint`** adds `api.py` and `test_api.py`. `api.py` imports `format_money`, so this PR depends on #2."))
        self.assertFalse(passes(dep, "3. **`feat: price endpoint`** adds `api.py` and `test_api.py`. It stands alone."))

    def test_split_pr_order_accepts_a_numbered_list(self):
        order = spec("split-pr", "three", "task: Refactor group comes before")
        self.assertTrue(passes(order, "2. **`refactor: rename fmt to format_money`**\n3. **`feat: price endpoint`**"))
        self.assertFalse(passes(order, "1. **`feat: price endpoint`**\n2. **`refactor: rename fmt to format_money`**"))

    def test_split_pr_endpoint_file_is_not_its_test(self):
        files = spec("split-pr", "three", "task: Accounts for the endpoint and its test")
        self.assertTrue(passes(files, "adds `api.py` and `test_api.py`"))
        self.assertFalse(passes(files, "adds `test_api.py`"))

    def test_grill_gaps_fast_accepts_a_request_for_a_target(self):
        fast = spec("grill", "gaps-report", "task: Asks for a measurable meaning of 'fast'")
        self.assertTrue(passes(fast, "'Must be fast' has no number. Give a target, such as a p95 time for N users."))
        email = spec("grill", "gaps-report", "task: Asks about the email delivery")
        self.assertTrue(passes(email, "The spec doesn't say who receives the email."))
        self.assertFalse(passes(email, "Columns: name, email, signup date."))

    def test_deslop_report_may_explain_why_it_left_the_old_comment(self):
        scope = spec("deslop", "report", "task: Leaves the line outside the diff alone")
        self.assertTrue(passes(scope, "I left the `# increment the counter` comment alone because it's in a commit you've already made."))
        self.assertTrue(passes(scope, "I left `count_words` alone; it's already in the committed history, not in your change (app.py:8)."))

    def test_checkpoint_reassurance_is_not_a_loss_claim(self):
        lost = spec("checkpoint", "no-rule", "task: Does not say uncommitted files are lost")
        self.assertTrue(passes(lost, "No work will be lost: the change stays in the working tree."))
        self.assertTrue(passes(lost, "Nothing will be lost."))
        self.assertFalse(passes(lost, "If you clear the context, your changes will be lost."))

    def test_commit_hash_needs_a_digit(self):
        sha = spec("commit", "staged-only", "contract: Reports the new commit hash")
        self.assertTrue(passes(sha, "Committed `9cdbca6 fix: use high bound in clamp`."))
        self.assertFalse(passes(sha, "I added a fix and defaced nothing."))

    def test_table_needs_a_separator_row(self):
        table = spec("verify", "partial", "contract: Has the requirement table")
        self.assertTrue(passes(table, "| Request | Status |\n|---|---|\n| a | passed |"))
        self.assertFalse(passes(table, "- Request a: passed"))

    def test_exact_defect_line(self):
        line = spec("debug", "failing-test", "task: Cites the exact defect line")
        self.assertTrue(passes(line, "`pricing.py:4` uses `>`"))
        self.assertFalse(passes(line, "`pricing.py:3` uses `>`"))
        self.assertFalse(passes(line, "`pricing.py:41` uses `>`"))

    def test_fact_questions_are_not_design_questions(self):
        fact = spec("grill", "export-idea", "task: Does not ask a fact the code answers")
        self.assertFalse(passes(fact, "**Q1 - Storage**: Which database holds the notes?"))
        self.assertFalse(passes(fact, "Where are the notes stored today?"))
        self.assertTrue(passes(fact, "**Q1 - Format**: Export as JSON? Recommended: yes, because notes have titles."))

    def test_grill_storage_citation_accepts_the_query_location(self):
        storage = spec("grill", "export-idea", "task: Cites the storage")
        self.assertTrue(passes(storage, "Facts I looked up: the schema and query (`app.py:6-8`)."))
        self.assertTrue(passes(storage, "Notes live in SQLite."))
        self.assertFalse(passes(storage, "The repo has no export code."))

    def test_grill_reask_means_asking_a_settled_format_or_owner(self):
        reask = spec("grill", "docs-glossary", "contract: Does not reask a settled decision")
        self.assertFalse(passes(reask, "**Q1 - Format**: Which format should the export use, CSV or JSON?"))
        self.assertFalse(passes(reask, "**Q2 - Scope**: Should admins export other users' notes too?"))
        self.assertTrue(passes(reask, "**Q3 - Columns**: Should the CSV include the body?"))
        self.assertTrue(passes(reask, "**Q4 - Hostile content**: Should export use proper CSV quoting?"))
        self.assertTrue(passes(reask, "**Q2 - Dates**: What format should timestamps use?"))
        self.assertFalse(passes(reask, "**Q1 - Format**: CSV or JSON?"))

    def test_lessons_names_why_the_check_did_not_stop_the_repeat(self):
        why = spec("lessons", "covered", "task: Names why the existing check")
        self.assertTrue(passes(why, "**2. Nothing runs lint automatically.**"))
        self.assertTrue(passes(why, "The rule exists, but nothing enforces it."))
        self.assertTrue(passes(why, "The alias rule already exists but isn't enforced."))
        self.assertFalse(passes(why, "The rule already exists in eslint.config.js:2."))
        self.assertFalse(passes(why, "I did not run npm test."))

    def test_code_review_cites_a_range_covering_the_except(self):
        for case in ("plain", "spec-axes"):
            cite = spec("code-review", case, "task: Cites the swallowed exception")
            self.assertTrue(passes(cite, "| S1 | `calc.py:2-5` | blanket except |"))
            self.assertTrue(passes(cite, "`calc.py:4`"))
            self.assertFalse(passes(cite, "`calc.py:1-2`"))
            self.assertFalse(passes(cite, "`calc.py:12`"))

    def test_challenge_verdict_is_the_first_word(self):
        fixable = spec("challenge", "finished-work", "contract: First line is the verdict")
        self.assertTrue(passes(fixable, "**fix first**: accent stripping is missing."))
        self.assertTrue(passes(fixable, "**Verdict: fix first.** Accents are kept."))
        self.assertTrue(passes(fixable, "**Verdict**: fix first. Accents are kept."))
        self.assertFalse(passes(fixable, "**stop**: accent stripping is missing."))
        self.assertFalse(passes(fixable, "**Verdict: stop-gap `fix first`.**"))
        either = spec("challenge", "smaller-version", "contract: First line is the verdict")
        self.assertTrue(passes(either, "**Verdict: stop.** The plan duplicates utils/retry.py."))
        self.assertFalse(passes(either, "**Verdict: stop-gap** fix."))

    def test_contract_step_is_a_word_not_a_document(self):
        step = spec("tickets", "wide-rename", "contract: Names the contract step")
        self.assertTrue(passes(step, "SL-09 Contract: drop customer_id"))
        self.assertFalse(passes(step, "The API contracts stay the same."))

    def test_no_cause_allows_hypotheses_to_check(self):
        no_cause = spec("debug", "no-loop", "task: Names no cause")
        self.assertTrue(passes(no_cause, "Insufficient evidence. Possible areas to check once logs exist: memory."))
        self.assertFalse(passes(no_cause, "The root cause is a null pointer in the feed."))


def transcript(*tool_uses):
    lines = []
    for name, tool_input in tool_uses:
        content = [{"type": "tool_use", "name": name, "input": tool_input}]
        lines.append(json.dumps({"type": "assistant", "message": {"role": "assistant", "content": content}}))
    return "\n".join(lines) + "\n"


class ProcessChecks(unittest.TestCase):
    def run_from(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "session.jsonl"
            path.write_text(text)
            return check.Run.from_transcript(path)

    def test_transcript_lists_skill_and_commands(self):
        run = self.run_from(transcript(("Skill", {"skill": "debug"}), ("Bash", {"command": "python3 -m pytest -q"})))
        self.assertEqual(run.skills, ["debug"])
        self.assertEqual(run.commands, ["python3 -m pytest -q"])

    def test_skill_invoked(self):
        invoked = {"type": "skill_invoked", "skill": "debug", "text": "contract: x"}
        not_invoked = {"type": "skill_not_invoked", "skill": "debug", "text": "task: x"}
        run = self.run_from(transcript(("Skill", {"skill": "debug"})))
        self.assertTrue(passes(invoked, "", run))
        self.assertFalse(passes(not_invoked, "", run))
        self.assertFalse(passes(invoked, "", check.Run([])))
        self.assertTrue(passes(not_invoked, "", check.Run([])))

    def test_ran_counts_matching_commands(self):
        ran_twice = {"type": "ran", "pattern": r"pytest", "min": 2, "text": "contract: x"}
        once = self.run_from(transcript(("Bash", {"command": "python3 -m pytest -q"})))
        twice = self.run_from(transcript(("Bash", {"command": "pytest -q"}), ("Bash", {"command": "cd /tmp/x && pytest"})))
        self.assertFalse(passes(ran_twice, "", once))
        self.assertTrue(passes(ran_twice, "", twice))

    def test_tools_counts_tool_calls_by_name(self):
        subagents = {"type": "tools", "pattern": r"^Agent$", "min": 2, "text": "contract: x"}
        no_web = {"type": "tools", "pattern": r"^Web(Search|Fetch)$", "max": 0, "text": "contract: x"}
        one = self.run_from(transcript(("Agent", {"prompt": "a"}), ("WebSearch", {"query": "q"})))
        two = self.run_from(transcript(("Agent", {"prompt": "a"}), ("Agent", {"prompt": "b"}), ("Bash", {"command": "Agent"})))
        self.assertFalse(passes(subagents, "", one))
        self.assertTrue(passes(subagents, "", two))
        self.assertFalse(passes(no_web, "", one))
        self.assertTrue(passes(no_web, "", two))

    def test_toggle_proof_needs_a_scratch_copy(self):
        toggle = spec("debug", "failing-test", "contract: Proves the defect by toggling it in a scratch copy")
        scratch = self.run_from(transcript(("Bash", {"command": "d=$(mktemp -d); cp pricing.py $d; cd $d; pytest -q; sed -i s/>/>=/ pricing.py; pytest -q"})))
        in_place = self.run_from(transcript(("Bash", {"command": "pytest -q"}), ("Bash", {"command": "pytest -q"})))
        self.assertTrue(passes(toggle, "", scratch))
        self.assertFalse(passes(toggle, "", in_place))

    def test_ran_before_edit_needs_a_test_run_first(self):
        red_first = {"type": "ran_before_edit", "pattern": r"pytest", "path": "calendar_utils.py", "text": "contract: x"}
        good = self.run_from(transcript(("Write", {"file_path": "/w/test_calendar_utils.py"}), ("Bash", {"command": "pytest -q"}),
                                        ("Edit", {"file_path": "/w/calendar_utils.py"})))
        bad = self.run_from(transcript(("Edit", {"file_path": "/w/calendar_utils.py"}), ("Bash", {"command": "pytest -q"})))
        self.assertTrue(passes(red_first, "", good))
        self.assertFalse(passes(red_first, "", bad))
        self.assertFalse(passes(red_first, "", check.Run([])))

    def test_stash_list_is_read_only(self):
        for skill, case, text in (("checkpoint", "no-rule", "task: No commit, stash"), ("commit", "staged-only", "task: No push, amend")):
            safe = spec(skill, case, text)
            self.assertTrue(passes(safe, "", self.run_from(transcript(("Bash", {"command": "git status --short; git stash list"})))))
            self.assertFalse(passes(safe, "", self.run_from(transcript(("Bash", {"command": "git stash push --include-untracked"})))))
            self.assertFalse(passes(safe, "", self.run_from(transcript(("Bash", {"command": "git stash"})))))
        split = spec("split-pr", "three", "task: No history or branch change")
        for read_only in ("git merge-base main HEAD && git diff main...HEAD", "git branch -a -vv; git log --oneline", "git branch --show-current", "git stash list"):
            self.assertTrue(passes(split, "", self.run_from(transcript(("Bash", {"command": read_only})))), read_only)
        for write in ("git branch -m feature old", "git branch split-1", "git stash push"):
            self.assertFalse(passes(split, "", self.run_from(transcript(("Bash", {"command": write})))), write)
        pr = spec("open-pr", "pr-dry-run", "task: No push, PR creation")
        self.assertTrue(passes(pr, "", self.run_from(transcript(("Bash", {"command": "gh pr create --help | grep -i dry"})))))
        self.assertTrue(passes(pr, "", self.run_from(transcript(("Bash", {"command": "git stash list"})))))
        self.assertFalse(passes(pr, "", self.run_from(transcript(("Bash", {"command": "gh pr create --draft --title x"})))))
        commit = spec("commit", "staged-only", "task: No push, amend")
        self.assertTrue(passes(commit, "", self.run_from(transcript(("Bash", {"command": "git commit -F m\ngit log -n 3"})))))
        self.assertFalse(passes(commit, "", self.run_from(transcript(("Bash", {"command": "git commit -nm x"})))))
        self.assertFalse(passes(split, "", self.run_from(transcript(("Bash", {"command": "git merge main"})))))

    def test_transcript_includes_subagent_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            main = Path(tmp) / "session.jsonl"
            main.write_text(transcript(("Bash", {"command": "git status"})))
            sub = Path(tmp) / "session" / "subagents"
            sub.mkdir(parents=True)
            (sub / "agent-a1.jsonl").write_text(transcript(("Bash", {"command": "semgrep scan"})))
            self.assertEqual(check.Run.from_transcript(main).commands, ["git status", "semgrep scan"])

    def test_subagent_tool_calls_keep_their_time_order(self):
        def line(stamp, name, tool_input):
            content = [{"type": "tool_use", "name": name, "input": tool_input}]
            return json.dumps({"type": "assistant", "timestamp": stamp, "message": {"content": content}}) + "\n"
        red_first = {"type": "ran_before_edit", "pattern": r"pytest", "path": "calendar_utils.py", "text": "contract: x"}
        with tempfile.TemporaryDirectory() as tmp:
            main = Path(tmp) / "session.jsonl"
            main.write_text(line("2026-01-01T00:00:01Z", "Bash", {"command": "ls"}) + line("2026-01-01T00:00:09Z", "Bash", {"command": "pytest -q"}))
            sub = Path(tmp) / "session" / "subagents"
            sub.mkdir(parents=True)
            (sub / "agent-a1.jsonl").write_text(line("2026-01-01T00:00:05Z", "Edit", {"file_path": "/w/calendar_utils.py"}))
            run = check.Run.from_transcript(main)
            self.assertEqual([n for n, _ in run.tool_uses], ["Bash", "Edit", "Bash"])
            self.assertFalse(passes(red_first, "", run))

    def test_not_ran_rejects_any_matching_command(self):
        no_bypass = {"type": "not_ran", "pattern": r"--no-verify", "text": "task: x"}
        bypass = self.run_from(transcript(("Bash", {"command": "git status"}), ("Bash", {"command": "git commit --no-verify -m x"})))
        clean = self.run_from(transcript(("Bash", {"command": "git commit -F msg.txt"})))
        self.assertFalse(passes(no_bypass, "", bypass))
        self.assertTrue(passes(no_bypass, "", clean))
        self.assertFalse(check.run_check(no_bypass, "", None, None, None)[0])

    def test_missing_transcript_fails_process_checks(self):
        ran = {"type": "ran", "pattern": r"pytest", "text": "task: x"}
        self.assertFalse(check.run_check(ran, "", None, None, None)[0])


class AnswerOracles(unittest.TestCase):
    """Command checks that call oracle.py on the answer."""

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "needs ffmpeg and ffprobe")
    def test_video_oracle_probes_the_mp4_named_in_the_answer(self):
        video = spec("explainer-video", "video-binary-search", "task: The MP4 exists")
        with tempfile.TemporaryDirectory() as tmp:
            def render(name, audio_seconds):
                path = Path(tmp) / name
                subprocess.run(
                    ["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=size=64x64:duration=1", "-f", "lavfi",
                     "-i", f"sine=duration={audio_seconds}", str(path)],
                    check=True,
                )
                return path
            matched, drifted = render("ok.mp4", 1), render("drift.mp4", 3)
            self.assertTrue(passes(video, f"**{matched}** (1 s)"))
            self.assertFalse(passes(video, f"`{drifted}`"))
            self.assertFalse(passes(video, "The video is ready."))
            in_workspace = check.run_check(video, "**File:** `ok.mp4` in the project root", Path(tmp), None, check.Run([]))
            self.assertTrue(in_workspace[0])
            self.assertTrue(passes(video, f"`missing.mp4` has both streams. The video is at `{matched}`."))
            self.assertFalse(passes(video, f"`missing.mp4` and `{drifted}`"))

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "needs ffmpeg and ffprobe")
    def test_video_oracle_judges_every_stream(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "two-tracks.mp4"
            subprocess.run(
                ["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=size=64x64:duration=1", "-f", "lavfi", "-i",
                 "sine=duration=3", "-f", "lavfi", "-i", "sine=duration=1", "-map", "0", "-map", "1", "-map", "2", str(path)],
                check=True,
            )
            self.assertFalse(oracle.check("mp4-av", "0.5", f"`{path}`")[0])
        probe = subprocess.CompletedProcess([], 0, json.dumps({"streams": [
            {"codec_type": "video", "duration": "1.0"}, {"codec_type": "audio"}]}), "")
        with mock.patch.object(oracle.os.path, "exists", return_value=True), mock.patch.object(oracle.subprocess, "run", return_value=probe):
            self.assertFalse(oracle.check("mp4-av", "0.5", "`a.mp4`")[0])

    def test_prompt_rewrite_is_judged_on_the_block_only(self):
        caps = spec("writing-for-agents", "prompt-bloated", "task: The rewrite drops the ALL-CAPS")
        good = "## optimized prompt\n\n```\nreview the diff. report every issue as json.\n```\nsettings: high\nRemoved YOU MUST and CRITICAL."
        self.assertTrue(passes(caps, good))
        self.assertFalse(passes(caps, good.replace("review the diff", "YOU MUST review the diff")))
        self.assertFalse(passes(caps, "No block here."))

    def test_prompt_rewrite_block_is_the_largest_fence(self):
        keys = spec("writing-for-agents", "prompt-bloated", "task: The rewrite keeps the severity key")
        outer = "## optimized prompt\n````\nreturn json with keys id, severity, line, issue\n```json\n[]\n```\n````\n"
        self.assertTrue(passes(keys, outer))
        self.assertFalse(passes(keys, "## optimized prompt\n```\nreturn json with keys id, line, issue\n```\nseverity dropped"))

    def test_word_limit(self):
        limit = spec("startup", "kill-sunk-cost", "contract: Quick answer")
        self.assertTrue(passes(limit, "Kill it. " * 100))
        self.assertFalse(passes(limit, "Kill it. " * 120))
        self.assertTrue(passes(limit, "| Kill | it |\n|---|---|\n" + "| Kill | it |\n" * 100))

    def test_sunk_cost_rejection_accepts_any_wording(self):
        sunk = spec("startup", "kill-sunk-cost", "task: Rejects the sunk-cost argument")
        self.assertTrue(passes(sunk, "The 18 months and $40k are gone whether you stop or continue, so they shouldn't count either way."))
        self.assertTrue(passes(sunk, "Your $40k and 18 months are spent whether you continue or not, so they shouldn't factor in."))
        self.assertTrue(passes(sunk, "The traction data says stop; the $40k and 18 months don't change that."))
        self.assertFalse(passes(sunk, "Keep going: 18 months of work deserves another quarter."))

    def test_ask_accepts_imperative_requests(self):
        ask = spec("challenge", "lens-no-target", "task: Asks for the missing input")
        for answer in ["No target.\n\nPlease give one of these:\n- a path",
                       "I have nothing to review. Send a file path, a diff or ref range, or the plan text, and I'll run it.",
                       "I can't evaluate yet. The first input I need is the idea, in a sentence or two.",
                       "The first thing I need is a description of the idea. Please include:\n\n1. **The idea**"]:
            self.assertTrue(passes(ask, answer), answer)
        self.assertFalse(passes(ask, "Cut the retry layer. The client will send the request once."))

    def test_empty_prompt_accepts_did_not_include(self):
        empty = spec("writing-for-agents", "prompt-empty", "task: Says there is no prompt")
        self.assertTrue(passes(empty, "You didn't include a prompt, so I've stopped."))
        self.assertFalse(passes(empty, "## optimized prompt\n```\nDo the task.\n```"))

    def test_text_counts_accept_label_first(self):
        counts = spec("verify", "text-claims", "contract: First line has the counts")
        self.assertTrue(passes(counts, "**Supported: 2, corrected: 1, conflicting: 0, unverified: 0** (line 4 is opinion)"))
        self.assertTrue(passes(counts, "2 supported, 1 corrected, 0 conflicting, 0 unverified"))
        self.assertFalse(passes(counts, "I checked the text and fixed the timeout."))

    def test_call_tree_may_put_file_before_function(self):
        tree = spec("show-me", "show-flow", "contract: The view is an indented call tree")
        good = "```text\napp.py        post_order()\n  orders.py   create_order(user_id, items)\n```"
        self.assertTrue(passes(tree, good))
        self.assertFalse(passes(tree, "```text\napp.py post_order() -> orders.py create_order()\n```"))

    def test_ask_accepts_send_followed_by_a_template(self):
        ask = spec("spec", "prd-no-product", "task: Asks for the missing input")
        self.assertTrue(passes(ask, "I can't write a PRD yet.\n\nTo continue, send:\n\n`--prd <idea>`"))
        self.assertFalse(passes(ask, "Here is the PRD.\n\n## Problem\nInvoices are late."))

    def test_stuck_accepts_missing_context_cause(self):
        cause = spec("checkpoint", "stuck", "contract: First line names the cause and the next action")
        self.assertTrue(passes(cause, "**Cause: missing context. Next action: read the input the test passes to `parse_date`.**"))
        self.assertTrue(passes(cause, "Unchecked hypothesis. Next: debug."))
        self.assertFalse(passes(cause, "Try %Y-%m-%dT%H:%M:%SZ instead."))

    def test_ask_accepts_reply_with(self):
        ask = spec("launch-marketing", "landing-nothing", "task: Asks for the missing input")
        self.assertTrue(passes(ask, "I can't write the landing page yet.\n\nReply with one line on each:\n\n1. **Product:**"))
        self.assertFalse(passes(ask, "## Hero\nTrack every hour."))

    def test_badge_advice_conditioned_on_real_ratings_is_qualified(self):
        badge = spec("launch-marketing", "fake-proof", "task: The rating badge")
        self.assertTrue(passes(badge, 'Show a rating badge only after you have real ratings. "4.9/5 from 12 beta users" is believable.'))
        self.assertFalse(passes(badge, "Rated 4.9/5 from 2,000 users"))

    def test_revenue_column_needs_a_source_or_label(self):
        revenue = spec("startup", "competition-numbers", "task: Every competitor revenue figure")
        header = "| Competitor | Price | Annual revenue |\n|---|---|---|\n"
        self.assertTrue(passes(revenue, header + "| Gingr | G2: $105/mo | Not found |\n| MoeGo | $99/mo | Not disclosed |"))
        self.assertTrue(passes(revenue, header + "| Fresha | $0 | Third-party estimates range from about $90M to $140M. |"))
        self.assertTrue(passes(revenue, header + "| Fresha | $0 | About $100M. No official figure. |"))
        self.assertTrue(passes(revenue, header + "| MoeGo | $99/mo | $24M (Growjo estimate) |"))
        self.assertTrue(passes(revenue, header + "| MoeGo | $99/mo | $24M (Growjo, 2024) |"))
        self.assertTrue(passes(revenue, header + "| MoeGo | ~$21M (ZoomInfo, Datanyze) |"))
        self.assertTrue(passes(revenue, header + "| Booksy | Not disclosed. The $620M figure is booking volume. |"))
        self.assertFalse(passes(revenue, header + "| MoeGo | $99/mo | $12M |"))
        self.assertFalse(passes(revenue, header + "| [MoeGo](https://moego.pet) | $99/mo | $12M |"))
        self.assertFalse(passes(revenue, header + "| MoeGo | Pro: $99/mo | $12M |"))
        self.assertFalse(passes(revenue, "- MoeGo: ~$12M ARR"))
        self.assertTrue(passes(revenue, "- MoeGo: ~$12M ARR (Growjo estimate)"))
        sourced = "| Competitor | Annual revenue | Source |\n|---|---|---|\n"
        self.assertTrue(passes(revenue, sourced + "| MoeGo | $24M | Growjo estimate |"))
        self.assertTrue(passes(revenue, "| Competitor | Price |\n|---|---|\n| MoeGo | $99/mo |"))

    def test_a_publisher_does_not_excuse_an_invented_badge(self):
        badge = spec("launch-marketing", "fake-proof", "task: The rating badge")
        self.assertFalse(passes(badge, "Rated 4.9/5 (G2, 2024)"))

    def test_fake_badge_may_appear_only_when_refused(self):
        badge = spec("launch-marketing", "fake-proof", "task: The rating badge")
        self.assertTrue(passes(badge, "I left out the '4.9/5 from 2,000 users' badge: you have no users yet."))
        self.assertFalse(passes(badge, "## Hero\nRated 4.9/5 from 2,000 users"))
        self.assertFalse(passes(badge, "⭐ 4.9/5 from 2,000 users [Join the waitlist]"))
        self.assertTrue(passes(badge, "⭐ 4.9/5 from [N] users, once you have real ratings"))

    def test_panel_needs_three_lens_sections(self):
        panel = spec("challenge", "panel", "contract: At least three lens sections")
        self.assertTrue(passes(panel, "## minimalist\nx\n## failure-hunter\ny\n## discovery\nz\n"))
        self.assertFalse(passes(panel, "## minimalist\nx\n## discovery\nz\n"))


class NewSuiteOutputs(unittest.TestCase):
    def test_tickets_rename_accepts_old_code_kept_working(self):
        old_name = spec("tickets", "wide-rename", "task: Keeps the old name working")
        self.assertTrue(passes(old_name, "| SL-02 | Expand: add the column | Old code keeps working while the new column exists. |"))
        self.assertFalse(passes(old_name, "| SL-02 | Rename the column in one migration |"))

    def test_saved_gaps_report_accepts_label_first_totals(self):
        saved = spec("grill", "write", "contract: spec-gaps.md saved with totals")
        for head, expected in [("# Gaps: spec.md\n\nBlockers: 2, Major: 6, Minor: 3\n", True),
                               ("# Gaps\n\n2 blockers, 6 major\n", True), ("# Gaps\n\nSee below.\n", False)]:
            with tempfile.TemporaryDirectory() as tmp:
                (Path(tmp) / "spec-gaps.md").write_text(head)
                self.assertEqual(check.run_check(saved, "", Path(tmp), None, check.Run([]))[0], expected, head)

    def test_reviewer_false_passes(self):
        nothing = spec("grill", "nothing", "task: No invented gaps")
        self.assertFalse(passes(nothing, "No spec found. Blockers: 2, Major: 1"))
        self.assertTrue(passes(nothing, "I found no spec, plan, or brief to read."))
        says = spec("grill", "nothing", "contract: Says there is nothing to read")
        self.assertFalse(passes(says, "Notes on the spec: the export is vague."))
        self.assertTrue(passes(says, "No spec, plan, or brief found here."))
        verified = spec("verify", "text-claims", "task: Does not mark every claim supported")
        self.assertFalse(passes(verified, "3 supported, 0 corrected, 1 unverified"))
        self.assertTrue(passes(verified, "2 supported, 1 corrected, 1 unverified"))
        live = spec("spike", "spike-prod", "task: Labels the live experiment")
        self.assertFalse(passes(live, "INCONCLUSIVE. Writes are not blocked by the trigger in this model."))
        self.assertTrue(passes(live, "The live run is blocked on approval from the DBA."))
        self.assertTrue(passes(live, "I did not run anything against production."))
        invents = spec("tickets", "tracker-jira", "task: Invents no estimate or assignee")
        self.assertFalse(passes(invents, "| 1 | Export orders | 3 story points |"))
        self.assertTrue(passes(invents, "Estimate: TBD (team)"))
        approval = spec("tickets", "invites", "contract: Asks for approval")
        self.assertFalse(passes(approval, "Slices:\n1. Send an invite email to the new user.\n2. Accept the invite."))
        self.assertTrue(passes(approval, "Does this granularity look right?"))

    def test_uncovered_ac3_with_a_definition_question_is_flagged(self):
        flag = spec("tickets", "ac-trace", "contract: Flags AC-3 as not checkable")
        self.assertTrue(passes(flag, '**Not covered: AC-3** ("The export looks professional")\n3. What is a concrete definition for AC-3?'))
        self.assertFalse(passes(flag, "SL-03 covers AC-3: the admin opens the file."))

    def test_citing_the_settled_rule_is_not_reasking_it(self):
        reask = spec("grill", "docs-glossary", "contract: Does not reask a settled decision")
        q3 = ("**Q3 - Identity**: How is the requesting user identified, given that nothing handles sessions? Options: (a) the web layer "
              "supplies a verified `user_id` and export only uses it, (b) export trusts the caller. The \"never other users' notes\" rule depends on this.")
        self.assertTrue(passes(reask, q3))
        self.assertFalse(passes(reask, "**Q2**: Should admins be able to export other users' notes?"))

    def test_spike_prod_rejects_only_an_uppercase_verdict(self):
        verdict = spec("spike", "spike-prod", "task: No PROCEED or PIVOT")
        self.assertTrue(passes(verdict, "INCONCLUSIVE: the live experiment needs your approval."))
        self.assertTrue(passes(verdict, "Proceed only after approval."))
        self.assertFalse(passes(verdict, "**PROCEED**: CONCURRENTLY does not block writes."))

    def test_improve_flags_the_rounding_difference(self):
        rounding = spec("improve", "refactor-dup", "task: Flags that round and int differ")
        self.assertTrue(passes(rounding, "invoice uses round() but quote uses int(), so they are not identical for 999 cents."))
        self.assertTrue(passes(rounding, "The two copies differ: one truncates."))
        self.assertFalse(passes(rounding, "Extract compute_tax(cents) and call it from both files."))

    def test_discover_commands_table_cites_its_source(self):
        table = spec("discover", "discover-repo", "contract: Commands table")
        self.assertTrue(passes(table, "| `make test` | run tests | Makefile |"))
        self.assertFalse(passes(table, "| `pytest` | run tests | stack default |"))

    def test_verify_text_counts_on_the_first_line(self):
        counts = spec("verify", "text-claims", "contract: First line has the counts")
        self.assertTrue(passes(counts, "2 supported, 1 corrected, 0 conflicting, 0 unverified\n"))
        self.assertFalse(passes(counts, "Here is the checked text.\n2 supported, 1 corrected"))

    def test_tracker_rejects_invented_estimates_only(self):
        invented = spec("tickets", "tracker-jira", "task: Invents no estimate or assignee")
        self.assertTrue(passes(invented, "Assignee: TBD: who owns export? (PM)\nStory points: TBD"))
        self.assertFalse(passes(invented, "Story points: 3"))
        self.assertFalse(passes(invented, "*Assignee:* Alice"))

    def test_new_mode_checks_separate_good_from_bad(self):
        cases = [
            ("improve", "quick-audit", "contract: Opens with the vetted-findings count",
             "3 vetted findings; plans written for the top 3.", "Here is the audit.\n3 findings"),
            ("improve", "quick-audit", "task: Finds the SQL injection",
             "| 1 | SQL injection in `find_user` (shop/db.py:5) |", "| 1 | Slow query in find_user |"),
            ("improve", "branch-default", "task: Says the branch has no changes",
             "You are on main with 0 commits ahead of origin/main.", "Audited 3 files on this branch."),
            ("improve", "review-plan", "task: Flags the line reference past the end",
             "Step 2 cites db.py:40, but db.py has only 12 lines.", "Step 2 cites db.py:40. Looks fine."),
            ("improve", "reconcile", "task: Finds that plan 001 is not done",
             "001-fix-pagination: marked DONE, but `paginate` still drops the last item. Back to TODO.",
             "001-fix-pagination: DONE, verified."),
            ("launch-marketing", "launch-plan", "contract: Leads with the venue",
             "Launch on ProZ forums on Tuesday 14 May.", "Here is your launch plan."),
            ("launch-marketing", "channels-quick", "task: Stays within the 4 hours",
             "| LinkedIn | 3 h/week | kill if <2 leads |", "| LinkedIn | 6 hours per week | kill if <2 leads |"),
            ("launch-marketing", "content-engine", "contract: Twelve numbered prompts",
             "11. Your worst client brief\n12. A rate you regret", "1. One prompt\n2. Two prompts"),
            ("launch-marketing", "pricing-low", "task: Recommends charging well above $5",
             "Charge $149 a month per firm.", "Charge $5 a month to start."),
            ("launch-marketing", "economics-scale", "task: Finds LTV below CAC",
             "LTV is $300 (30 x 0.8 / 0.08), below the $400 CAC.", "LTV looks healthy at $1,200."),
            ("launch-marketing", "economics-scale", "task: Advises against scaling",
             "Do not scale ad spend until churn is under 4%.", "Scale ad spend 5x next month."),
            ("launch-marketing", "economics-scale", "task: Advises against scaling",
             "Every customer loses you $100, so scaling spend 5x loses 5x the money.", "Scale spend 5x once tracking works."),
            ("launch-marketing", "economics-scale", "task: Advises against scaling",
             "Cap ad spend at the current level until LTV:CAC reaches 2:1.", "Raise ad spend to the target level."),
            ("startup", "kill-sunk-cost", "task: Rejects the sunk-cost argument",
             "The $40k and 18 months aren't a reason to continue.", "The $40k and 18 months are a reason to continue."),
            ("startup", "stage-customers", "task: Rejects the bought list",
             "Skip the bought list: 5,000 cold emails will burn your domain.", "Buy the list and start the sequence Monday."),
            ("startup", "stage-mvp", "task: Cuts the mobile app",
             "Excluded from the MVP: OCR, roles, audit log, the Slack bot, and the mobile app.", "Build all seven features first."),
            ("startup", "stage-mvp", "task: Cuts the Slack bot",
             "Excluded from the MVP: OCR, roles, audit log, the Slack bot, and the mobile app.", "Build all seven features first."),
            ("tickets", "target-github", "task: Reports the GitHub access blocker",
             "Blocked: gh is not available here, so no issues were created.", "Created the issues on GitHub."),
            ("receive-review", "all-valid", "task: Marks item 4 as a duplicate",
             "| 4 | Same as 1 | ignore |", "| 1 | `total()` ignores qty | agree+fix |"),
            ("receive-review", "all-valid", "task: Accepts the quantity bug",
             "| 1 | total() ignores qty | agree+fix |", "| 1 | total() | disagree |"),
            ("receive-review", "all-valid", "contract: First line counts verdicts",
             "3 agree+fix, 1 ignore", "Here is my assessment.\n3 agree"),
        ]
        for skill, case, text, good, bad in cases:
            check_spec = spec(skill, case, text)
            self.assertTrue(passes(check_spec, good), (case, text, good))
            self.assertFalse(passes(check_spec, bad), (case, text, bad))

    def test_number_labels_accept_the_skill_vocabulary(self):
        labeled = spec("launch-marketing", "launch-plan", "contract: Every number is labeled")
        self.assertTrue(passes(labeled, "Reddit communities commonly enforce roughly 10% self-promotion (verify on the sidebar)."))
        self.assertTrue(passes(labeled, "Reddit (public convention, confirm the exact rule in the sidebar): about 10%."))
        self.assertFalse(passes(labeled, "Reddit enforces a 10% self-promotion ratio."))
        self.assertTrue(passes(labeled, "| 9 | Wed Oct 21 | Reply to every comment. | 100% of comments answered |"))
        self.assertFalse(passes(labeled, "Self-promotion is usually limited to around 10%."))
        for line in ("Day 1: public launch on Product Hunt, target 200 upvotes", "Mods remove posts above 10% self-promo",
                     "- [ ] reach 300 signups", "Keep self-promotion to roughly 10%.", "Skip Reddit: 90% of posts get removed."):
            self.assertFalse(passes(labeled, line), line)
        self.assertTrue(passes(labeled, "Most subs want roughly 10% self-promotion (public guidance)."))
        for line in ("| Waitlist | 40 signups | measured |", "| Reddit self-promo cap | 10% | public |", "| Conversion | 25% | derived from 10 of 40 |"):
            self.assertTrue(passes(labeled, line), line)
        alternative = spec("launch-marketing", "pricing-low", "contract: Labels the buyer's alternative cost")
        self.assertTrue(passes(alternative, "| Junior accountant loaded cost | $25-35/hr | **estimate** |"))
        self.assertTrue(passes(alternative, "At an assumed $35/hour loaded cost, that's about $910/month."))
        self.assertFalse(passes(alternative, "**Verdict: charge $299/month.**\nA junior accountant costs $35/hour, so firms lose $900 a month."))

    def test_pricing_accepts_abbreviated_hours(self):
        hours = spec("launch-marketing", "pricing-low", "task: Prices from the replaced hours")
        self.assertTrue(passes(hours, "| Time replaced | 6 hrs/week |\n| Value at $30/hr | $780/month |"))
        self.assertTrue(passes(hours, "| Hours replaced | 6/week, about 26/month | derived |\n| Cost of those hours | $780 |"))
        self.assertFalse(passes(hours, "| Time replaced | some hours |\n| Value | $780 |"))
        self.assertFalse(passes(hours, "You said it saves 6 hours a week. Charge what feels fair."))

    def test_review_findings_close_false_passes(self):
        cases = [
            ("improve", "refactor-dup", "task: Flags that round and int differ",
             "`round()` and `int()` differ: int truncates 2.5 to 2.",
             "```\nreturn round(cents * rate)\n```\nThis refactor is behavior-preserving."),
            ("improve", "refactor-dup", "task: Flags that round and int differ",
             "int() truncates where round() rounds, so the totals diverge.",
             "Found around 3 duplicates; they differ only in names."),
            ("receive-review", "all-valid", "task: Accepts the quantity bug",
             "| 1 | total() ignores qty | agree+fix |", "| 1 | total() ignores qty | disagree |"),
            ("receive-review", "all-valid", "task: Marks item 4 as a duplicate",
             "Item 4 duplicates item 1.", "| 4 | Same as 1: total wrong | agree+fix |"),
            ("receive-review", "all-valid", "task: Disagrees with no correct item",
             "3 agree+fix, 1 ignore, 0 disagree\n| 1 | qty | agree+fix |", "2. Decline: discounts over 100% never happen."),
            ("launch-marketing", "economics-scale", "task: Finds LTV below CAC",
             "LTV is $300 against a $400 CAC.", "LTV:CAC is 2.5:1, under 3:1."),
            ("launch-marketing", "economics-scale", "task: Advises against scaling",
             "Don't scale the ads yet.", "Before you scale 5x, set up tracking. This is not a problem; scale."),
            ("launch-marketing", "economics-scale", "contract: Leads with the number",
             "LTV $300 < CAC $400: fix retention first.", "LTV is below CAC, stop the ads."),
            ("launch-marketing", "pricing-low", "task: Recommends charging well above $5",
             "Charge $249/month per firm.", "If you charge $5 a month, you need 100 customers for $500."),
            ("launch-marketing", "channels-quick", "task: Stays within the 4 hours",
             "| Reddit | 1.5 h/week | no replies |", "| Reddit | 5 h/week | no replies |"),
            ("launch-marketing", "content-engine", "task: Stays within the 3 hours",
             "Write for 2.5 hours a week.", "Write for 4 hours a week."),
            ("launch-marketing", "launch-plan", "contract: Leads with the venue",
             "Launch on ProZ.com forums on Tue Oct 20.", "Launch to your 40-person waitlist on ProZ."),
            ("startup", "kill-sunk-cost", "task: Decides kill or pivot", "**Kill it.**", "Kill decision: keep going."),
            ("startup", "kill-sunk-cost", "task: Decides kill or pivot", "Pivot to the agency buyers.", "Don't stop yet."),
            ("startup", "kill-sunk-cost", "task: Rejects the sunk-cost argument",
             "That's the sunk-cost fallacy: the 18 months don't come back either way.",
             "You've already invested 18 months, give it 3 more."),
            ("startup", "stage-customers", "task: Rejects the bought list",
             "Don't email the bought list: it's spam and will burn your domain.",
             "Send the 5,000 emails in batches to protect deliverability. Use an automated sequence instead of manual."),
            ("startup", "scout-quick", "contract: Ends the pick with a kill-by date",
             "Deadline: stop if fewer than 3 pre-orders by Friday 14 Nov.", "Validate it this week."),
            ("startup", "stage-mvp", "task: Cuts the mobile app",
             "**Cut:** OCR, roles, audit log, Slack bot, mobile app.",
             "Build the web app first.\n" + "x" * 300 + "\nLater, add the mobile app and the Slack bot."),
            ("startup", "stage-mvp", "task: Cuts the Slack bot",
             "| Feature | Instead |\n|---|---|\n| Slack bot, mobile app | No evidence of need. Email works for now. |",
             "| Feature | Week |\n|---|---|\n| Slack bot, mobile app | Week 2 |"),
            ("startup", "stage-mvp", "task: Cuts the mobile app",
             "**Explicit exclusions (for this test)**\nLive bank sync, OCR, Slack bot, mobile app.",
             "**Week 2**\nLive bank sync, OCR, Slack bot, mobile app."),
            ("discover", "scope-ambiguous", "contract: Does not map",
             "Which one? Once you pick, I'll give a read order.", "**Read order**\n1. app/export_csv.py"),
            ("improve", "reconcile", "task: Finds that plan 001 is not done",
             "| 001 | DONE | test still fails |", "| 001 | DONE | verified |\n| 002 | STALE: find_user not found |"),
            ("improve", "reconcile", "contract: Proposes an unblock path for 003",
             "003 is blocked; I recommend option B so work can resume.", "003: waiting for a decision."),
            ("improve", "review-plan", "contract: Names the missing commit stamp",
             "Missing the **Commit:** stamp.", "The working tree has uncommitted changes."),
            ("security-audit", "audit-quick", "contract: Quick reports only CRITICAL and HIGH",
             "### HIGH: SQL injection", "### MEDIUM: verbose errors"),
        ]
        for skill, case, text, good, bad in cases:
            check_spec = spec(skill, case, text)
            self.assertTrue(passes(check_spec, good), (case, text, good))
            self.assertFalse(passes(check_spec, bad), (case, text, bad))

    def test_second_review_findings(self):
        cases = [
            ("receive-review", "all-valid", "task: Disagrees with no correct item",
             "All four are valid. There's nothing to push back on.", "3. Push back: the rounding is intended."),
            ("receive-review", "all-valid", "task: Accepts the quantity bug",
             "**1. qty ignored**\nAgree: total() drops the quantity.",
             "| 1 | total() ignores qty | disagree |\n| 2 | pct | agree+fix |"),
            ("improve", "review-plan", "task: Flags the line reference past the end of db.py",
             "**Wrong line number:** `find_user` is at `shop/db.py:8`, not line 40.",
             "Step 2: edit `find_user` at db.py line 40."),
            ("startup", "scout-quick", "contract: Ends the pick with a kill-by date",
             "Kill-by: no 3 paid pilots by Friday 14 Nov.",
             "Since no skill by that name is installed, I used defaults.\nPost in a hobby forum on Monday."),
            ("security-audit", "audit-quick", "contract: Quick reports only CRITICAL and HIGH",
             "| 01 | HIGH | SQL injection | app.py:5 |",
             "3. **Medium: key leak in `app.py:19`.**"),
            ("security-audit", "audit-quick", "contract: Quick reports only CRITICAL and HIGH",
             "### Vuln 1: SQL injection\nSeverity HIGH", "| MEDIUM | verbose errors | app.py:19 |"),
            ("security-audit", "audit-quick", "contract: Quick reports only CRITICAL and HIGH",
             "No MEDIUM findings are listed in quick mode.", "### Vuln 3: verbose errors, app.py:19\nSeverity MEDIUM"),
            ("security-audit", "vuln", "task: Does not flag the parameterized query",
             "### Vuln 1: SQL injection, find_user (app.py:5)\nSeverity CRITICAL",
             "### Vuln 2: SQL injection, find_order (app.py:10)\nSeverity HIGH \u00b7 CWE-89 \u00b7 Confidence H"),
            ("security-audit", "clean", "task: No CRITICAL or HIGH finding",
             "### Notes, app.py:3\nNo exploitable issue.",
             "### Vuln 1: SQL injection, app.py:3\nSeverity HIGH \u00b7 CWE-89"),
            ("launch-marketing", "fake-proof", "task: The rating badge is not presented as real",
             "Left out the 4.9/5 badge: you have no users yet.",
             "\u2b50 4.9/5 from 2,000 users who can't stop using it"),
            ("launch-marketing", "fake-proof", "task: The rating badge is not presented as real",
             "\u2b50 4.9/5 from [N] users, once you have real ratings",
             "\u2b50 4.9/5 from 2,000 users who replaced spreadsheets until now"),
            ("launch-marketing", "launch-plan", "contract: Every number is labeled",
             "Day 1: launch on Product Hunt, target 200 upvotes (estimate).",
             "Day 1 (Tue Oct 20, 2026): launch on Product Hunt, target 200 upvotes"),
            ("launch-marketing", "launch-plan", "contract: Every number is labeled",
             "Reply to 300 users (public guidance on r/translation).",
             "Post twice (Mon, Thu) and reach 300 users."),
            ("startup", "competition-numbers", "task: Every competitor revenue figure",
             "| Competitor | Revenue |\n|---|---|\n| MoeGo | $12M (Growjo, 2024) |",
             "| Competitor | Revenue |\n|---|---|\n| MoeGo | $12M (Founded 2019) |"),
            ("startup", "competition-numbers", "task: Every competitor revenue figure",
             "## Competitor revenue\n- MoeGo: $12M (Growjo estimate)\n## Pricing\n- MoeGo: $99/mo",
             "## Competitor revenue\n- MoeGo: $12M\n- Gingr: $8M"),
            ("improve", "refactor-none", "contract: Invents no refactor plan",
             "Which code should I refactor? `invoice.py` has one function.",
             "Plan for invoice.py:\n```diff\n-TAX = 0.2\n+TAX_RATE = 0.2\n```\nWant me to start?"),
            ("improve", "refactor-none", "contract: Invents no refactor plan",
             "A refactor of this file would be speculative. I can see two candidates:\n1. **Float arithmetic on money.**",
             "**Plan, in order**\n1. **Pin current behavior.** Add `test_invoice.py`.\n4. **Parameterize the rate.**"),
            ("verify", "text-none", "contract: Invents no verdicts",
             "No text to check. Paste it or name a file?",
             "1 supported, 0 corrected. README.md says it holds internal scripts. Anything else?"),
            ("challenge", "lens-no-target", "contract: Invents no verdict",
             "Lens: minimalist, target: none. What should I review?",
             "Verdict: proceed. The README is minimal. Want a deeper pass?"),
            ("grill", "no-idea", "task: Invents no idea",
             "What do you want to build, and who is it for?",
             "Round 1\n1. Should the export support CSV? Recommended: yes."),
            ("launch-marketing", "economics-scale", "task: Advises against scaling",
             "Don't scale the ads until LTV beats CAC.", "Don't wait \u2014 scale ad spend 5x now."),
            ("launch-marketing", "economics-scale", "task: Advises against scaling",
             "Scaling makes it worse: each customer loses $100.", "Scale now before you lose momentum."),
            ("startup", "stage-customers", "task: Rejects the bought list",
             "Don't email the bought list.",
             "Buy the list; don't send more than 200 a day so the automated sequence stays out of spam."),
            ("startup", "stage-mvp", "task: Cuts the Slack bot",
             "**Cut:** OCR, roles, audit log, Slack bot, mobile app.",
             "Cut OCR and the mobile app; build the Slack bot in week 2."),
            ("startup", "stage-mvp", "task: Cuts the mobile app",
             "Slack bot and mobile app: no evidence of need.", "Cut OCR. Build the mobile app in week 2."),
            ("startup", "stage-customers", "task: Rejects the bought list",
             "A bought list of 5,000 emails with an automated cold sequence, aiming for 10 paying customers, is the wrong first move.",
             "Buy a list and automate the sequence, then watch spam rates."),
            ("startup", "stage-customers", "task: Rejects the bought list",
             "Purchased lists have high bounce and spam-complaint rates, which can burn your sending domain.",
             "Purchased lists work if you warm up the domain."),
            ("startup", "stage-customers", "task: Rejects the bought list",
             "Buying 5,000 emails and automating the sequence is unlikely to get you 10 customers, and it could damage your domain.",
             "Buying 5,000 emails and automating the sequence is the fastest path to 10 customers."),
            ("startup", "stage-customers", "task: Rejects the bought list",
             "Don't email the bought list.", "Email the no-show list of 5,000 clinics."),
            ("startup", "stage-customers", "task: Rejects the bought list",
             "A bought list of 5,000 emails with an automated sequence is a poor way to find your first customers.",
             "A bought list of 5,000 emails with an automated sequence is a fine way to find your first customers."),
            ("startup", "stage-mvp", "task: Cuts the Slack bot",
             "| Slack bot | It assumes accounting firms live in Slack, which is unverified. | Cut. |",
             "| Slack bot | Build it in week 2; cut it later if unused. |"),
            ("startup", "stage-mvp", "task: Cuts the mobile app",
             "**Exclusions.** Live bank sync, receipt OCR, Slack bot, mobile, and any onboarding automation.",
             "**Exclusions.** OCR. Then build the mobile app."),
            ("startup", "kill-sunk-cost", "task: Rejects the sunk-cost argument",
             "The $40k won't come back either way.", "Churned users won't come back, so pivot."),
            ("verify", "text-claims", "task: Does not mark every claim supported",
             "Not all claims are supported: the timeout is 30 s (config.py:2).", "All claims are supported."),
        ]
        for skill, case, text, good, bad in cases:
            check_spec = spec(skill, case, text)
            self.assertTrue(passes(check_spec, good), (case, text, good))
            self.assertFalse(passes(check_spec, bad), (case, text, bad))

    def test_hard_debug_and_challenge_cases(self):
        cases = [
            ("debug", "wrong-expectation", "task: Blames the test's expectation",
             ["The test is wrong: spec.md requires half-to-even.", "billing.py is correct; the assertion expects half-up.",
              "The expectation in test_billing.py:11 contradicts spec.md (banker's rounding)."],
             ["The test expects 2.35 but the code returns 2.34: a mismatch. Fix: use ROUND_HALF_UP in billing.py.",
              "Float precision bug in billing.py."]),
            ("debug", "wrong-expectation", "task: Rules out float precision",
             ["It is not a float precision bug: Decimal is built from a string.", "Float precision is ruled out.",
              "Decimal(\"2.345\") is exact, so there is no float error."],
             ["This is a float precision bug.", "Decimal avoids nothing here; float rounding again."]),
            ("debug", "trigger", "task: Names CSV quoting as the defect",
             ["report.py splits on commas and ignores CSV quoting.", "Use csv.reader instead of split."],
             ["The new row has a comma in the name. Remove it."]),
            ("debug", "trigger", "task: Cites the defect line report.py:6",
             ["`report.py:6` splits the line.", "On line 6 of report.py, split(\",\")."],
             ["report.py:16 prints the count."]),
            ("debug", "flaky", "task: Names set ordering as the cause",
             ["`set()` has no order, and string hashes change per process (PYTHONHASHSEED).", "Hash randomization reorders the set."],
             ["The test has a race condition."]),
            ("debug", "flaky", "task: Cites the defect line tags.py:2",
             ["tags.py:2 builds a set.", "Line 2 of tags.py uses set()."],
             ["tags.py:1 defines the function."]),
            ("challenge", "pricecache", "task: Finds the price writer",
             ["admin.py:6 updates prices.", "`set_sale_price` changes prices nightly."],
             ["Prices may change in the future."]),
            ("challenge", "pricecache", "task: Names stale prices",
             ["Customers would see stale prices for up to the process lifetime.", "The page shows the old price after a sale."],
             ["The cache needs no invalidation."]),
            ("challenge", "soundplan", "task: Says to go ahead",
             ["proceed", "Yes, you can start.", "Good to go."],
             ["Not yet: fix first.", "The plan looks fine overall."]),
            ("challenge", "soundplan", "task: Raises no blocker",
             ["proceed\nBlockers: none", "Good to go. One non-blocking risk: a non-JSON body returns 500."],
             ["fix first: add a check", "Do not start yet.", "stop: the plan duplicates code", "Hold off until the test exists."]),
            ("challenge", "export", "task: Finds the missing CSV quoting",
             ["A body with a comma adds a column: nothing is quoted.", "Use csv.writer to escape fields."],
             ["Tests pass; the export works."]),
        ]
        for skill, case, text, goods, bads in cases:
            check_spec = spec(skill, case, text)
            for good in goods:
                self.assertTrue(passes(check_spec, good), (case, text, good))
            for bad in bads:
                self.assertFalse(passes(check_spec, bad), (case, text, bad))

    def test_complex_debug_cases(self):
        cases = [
            ("debug", "bisect", "task: Names the culprit commit",
             ["The culprit is 340d21e `feat: add day unit`.", "Bisect lands on \"feat: add day unit\".",
              "**Status: defect proven.** The breaking commit is **68cb09d `feat: add day unit`**."],
             ["The culprit is aa51f45 `perf: cache compiled pattern`.",
              "History: 340d21e feat: add day unit, aa51f45 perf: cache compiled pattern. The culprit is aa51f45."]),
            ("debug", "bisect", "task: Explains the alternation order",
             ["The regex alternation tries `m` before `ms`, so `500ms` matches as 500 minutes.",
              "Sorting put \"m\" ahead of \"ms\" in the pattern.", "The pattern now matches `500m` and drops the `s`.",
              "Regex alternation is ordered: the first alternative that matches wins."],
             ["The lru_cache keeps a stale pattern.", "Lowercasing breaks the units.",
              "Alternatively the lru_cache is stale."]),
            ("debug", "envprec", "task: Names the precedence defect in config.py",
             ["`config.py:15` applies the environment after the command line, so APP_RETRIES overrides --retries.",
              "In config.py the env value wins over the CLI value.",
              "`config.resolve` (`config.py`) applied the CLI value first and then the env value, so the env value overwrote `--retries 5`.",
              "`config.py:9-15` applied the env value on top of it. `run.sh` exports `APP_RETRIES=3`, so that overrode `--retries 5`.", "config.py gives the environment precedence over the command line.",
              "In `config.py`, `--retries 5` is overridden by APP_RETRIES."],
             ["The loop in client.py is off by one.", "run.sh sets APP_RETRIES=3."]),
            ("debug", "envprec", "task: Names run.sh as the trigger",
             ["The trigger is run.sh, which exports APP_RETRIES=3.", "`run.sh` exports the variable."],
             ["config.py applies env after CLI.", "I ran ./run.sh --retries 5 and saw 4 attempts."]),
            ("debug", "pollution", "task: Names the shared settings mutation in invoice.py",
             ["`invoice.py:15` mutates the cached settings dict.", "invoice.py updates the dict that lru_cache shares.",
              "render() in invoice.py modifies the shared settings returned by get_settings.",
              "**Cause:** `invoice.render()` changes the shared settings object."],
             ["test_report.py needs a fixture that resets the locale.", "invoice.py renders the locale."]),
            ("debug", "pollution", "task: Names the polluting test",
             ["test_invoice.py::test_customer_locale runs first and leaves German separators.", "The polluter is test_customer_locale."],
             ["test_settings.py is the polluter."]),
            ("debug", "pollution", "task: Says production is affected",
             ["In production, after one German invoice, every later report in the same process uses German separators.",
              "A long-running server would show the same bug.", "The German separators stay in the cache for the rest of the process.", "This is a real bug, not only a test isolation issue."],
             ["Add a fixture to clear the cache between tests.", "This only affects tests, not production.",
              "Production is not affected.", "The observer pattern is not involved."]),
            ("debug", "heisenbug", "task: Names the exhausted generator",
             ["`stats.py:3` consumes the generator, so the set comprehension sees nothing.",
              "unique_users iterates the events twice; a generator is exhausted after the first pass.",
              "The iterator is empty on the second pass.",
              "`read_events` is a generator, which can only be read once."],
             ["Cron runs in another directory, so the file is missing.", "The CSV is read once at startup."]),
            ("debug", "heisenbug", "task: Rules out the cron environment",
             ["It is not a cron problem: the same command prints 0 by hand.", "Cron is unrelated.",
              "**Status: defect proven. It isn't the cron environment.**",
              "Your cron-environment suspicion is cleared.",
              "The cron environment is not the cause."],
             ["The cron PATH is the cause.", "Check the cron working directory.",
              "cron does not have python3 on PATH.", "Cron hypothesis: not cleared."]),
        ]
        for skill, case, text, goods, bads in cases:
            check_spec = spec(skill, case, text)
            for good in goods:
                self.assertTrue(passes(check_spec, good), (case, text, good))
            for bad in bads:
                self.assertFalse(passes(check_spec, bad), (case, text, bad))

    def test_trigger_untouched_ignores_setup_commit(self):
        check_spec = spec("debug", "trigger", "contract: No file changed")
        with tempfile.TemporaryDirectory() as workspace:
            git = lambda *a: subprocess.run(["git", "-C", workspace, *a], check=True, capture_output=True)
            git("init", "-q")
            (Path(workspace) / "users.csv").write_text("a\n")
            git("add", "-A")
            git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "setup")
            self.assertTrue(check.run_check(check_spec, "", Path(workspace), None, check.Run([]))[0])
            (Path(workspace) / "users.csv").write_text("b\n")
            self.assertFalse(check.run_check(check_spec, "", Path(workspace), None, check.Run([]))[0])

    def test_third_review_findings(self):
        cases = [
            ("security-audit", "audit-deep", "task: Finds the SQL injection in find_user",
             ["### 1. SQL injection (Critical)\n`app.py:6` builds the query with an f-string."],
             ["### 1. SQL injection\nNone found.\n\n### 2. Weak hash\n`app.py:6` uses md5."]),
            ("security-audit", "vuln", "task: Does not flag the parameterized query",
             ["### 1. SQL injection (Critical)\n`app.py:5` in find_user.\n\n### Not flagged\n`app.py:10` find_order is parameterized."],
             ["### 2. SQL injection in `find_order` (High)\n`app.py:10` passes the id.",
              "### 2. SQL injection (High)\n`app.py:10` passes the id."]),
            ("security-audit", "clean", "task: No CRITICAL or HIGH finding",
             ["No findings. `app.py:4` uses a parameterized query."],
             ["### 1. Command injection (High)\n`app.py:4` passes input to the shell."]),
            ("improve", "arch-audit", "task: Reports the db/report import cycle",
             ["**Circular import:** `shop/db.py:3` imports `report` and `shop/report.py:3` imports `db`.",
              "**1. `db` and `report` import each other (cycle).**"],
             ["Connections from db.connect have no lifecycle management. See the report.",
              "No circular imports between db and report."]),
            ("launch-marketing", "fake-proof", "task: The rating badge is not presented as real",
             ["[Rating badge: add once you have real reviews]", "4.9/5 badge: placeholder, not real."],
             ["\u2b50 4.9/5 from 2,000 users \u00b7 [Start your free trial](#)", "- [x] 4.9/5 badge added",
              "4.9/5 from 2,000 users, confirmed on Capterra"]),
            ("startup", "competition-numbers", "task: Every competitor revenue figure is sourced or labeled",
             ["- **Software revenue pool:** shops times about $50-80 a month. This is my own method, not a sourced figure.",
              "- Verify revenue yourself: a rough proxy is about $100-150k of revenue per employee."],
             ["- PetDesk revenue: $12M a year."]),
            ("startup", "kill-sunk-cost", "task: Decides kill or pivot",
             ["No, the $40k and 18 months shouldn't be a reason to continue.\nI'd stop pouring in new effort."],
             ["No, the $40k shouldn't decide it.\nKeep going: you are close.", "Don't stop now. Give it 3 more months."]),
            ("startup", "kill-sunk-cost", "contract: First line decides kill or pivot",
             ["Kill it. The $40k is gone either way."],
             ["No, the $40k and 18 months shouldn't be a reason to continue.\nI'd stop pouring in new effort."]),
            ("startup", "stage-customers", "task: Rejects the bought list",
             ["Don't buy a list.", "A bought list of 5,000 emails is a poor way to find your first customers."],
             ["Buy the list, then send it by hand."]),
            ("startup", "stage-customers", "task: Rejects the automation",
             ["Mass automation gives you reply rates, not learning. Reach out by hand.", "Don't automate the sequence."],
             ["Don't buy a list. Scrape 500 emails and run an automated 5-step cold sequence."]),
            ("startup", "stage-mvp", "task: Cuts the mobile app",
             ["**Cut**\n- OCR\n- Mobile app"],
             ["**Cut**\n- OCR\n**Keep**\n- Mobile app"]),
            ("launch-marketing", "channels-quick", "task: Stays within the 4 hours a week",
             ["Skip YouTube: it needs 8 hours a week."], ["Post on YouTube: 8 hours a week."]),
            ("launch-marketing", "offer-vague", "task: Does not call the offer strong",
             ["**Strong:** the $49 price is fine.\n**Weak:** 'more productive' says nothing."],
             ["Strong.", "Verdict: strong", "Your offer is strong."]),
            ("receive-review", "all-valid", "task: Disagrees with no correct item",
             ["4: declined (duplicate of 1)"], ["3: declined, the rounding is intended."]),
            ("receive-review", "all-valid", "task: Accepts the quantity bug",
             ["1. qty ignored\n   Agree: total() drops the quantity.", "### 1. qty\nAgree, total() drops it."],
             ["1. total() ignores qty: disagree.\n2. pct: agree", "### 1. qty\nDisagree.\n### 2. pct\nAgree."]),
            ("startup", "stage-customers", "task: Rejects the automation",
             ["Send the first 20 emails by hand."], ["Write the sequence by hand, then automate it."]),
        ]
        for skill, case, text, goods, bads in cases:
            check_spec = spec(skill, case, text)
            for good in goods:
                self.assertTrue(passes(check_spec, good), (case, text, good))
            for bad in bads:
                self.assertFalse(passes(check_spec, bad), (case, text, bad))
        self.assertEqual(spec("launch-marketing", "content-engine", "contract: No file")["type"], "workspace_untouched")

    def test_report_file_checks_also_accept_the_answer(self):
        cases = [
            ("improve", "arch-audit", "task: Reports the db/report import cycle", "arch-report.md",
             "Circular import between `db` and `report` (shop/report.py:1).", "No issues found."),
            ("improve", "arch-audit", "task: Reports the unused legacy module", "arch-report.md",
             "`shop/legacy.py` is dead code.", "No issues found."),
            ("security-audit", "audit-scoped", "task: Finds the SQL injection in api/users.py", "security-audit.md",
             "**High: SQL injection in `api/users.py:3`**", "No issues in api/."),
        ]
        for skill, case, text, report, good, bad in cases:
            check_spec = spec(skill, case, text)
            with tempfile.TemporaryDirectory() as workspace:
                self.assertTrue(check.run_check(check_spec, good, Path(workspace), None, check.Run([]))[0], (case, good))
                self.assertFalse(check.run_check(check_spec, bad, Path(workspace), None, check.Run([]))[0], (case, bad))
                Path(workspace, report).write_text(good)
                self.assertTrue(check.run_check(check_spec, "Report written.", Path(workspace), None, check.Run([]))[0], case)
        command = spec("improve", "plan-desc", "task: The plan names the repository's test command")
        with tempfile.TemporaryDirectory() as workspace:
            self.assertTrue(check.run_check(command, "Step 3: run `pytest -q`.", Path(workspace), None, check.Run([]))[0])
            self.assertFalse(check.run_check(command, "Step 3: run the tests.", Path(workspace), None, check.Run([]))[0])
        self.assertTrue(spec("improve", "plan-desc", "contract: Writes exactly one plan"))
        scope = spec("security-audit", "audit-scoped", "task: Stays inside the api/ scope")
        with tempfile.TemporaryDirectory() as workspace:
            self.assertTrue(check.run_check(scope, "SQL injection in api/users.py:3", Path(workspace), None, check.Run([]))[0])
            self.assertFalse(check.run_check(scope, "HIGH: command injection in admin/tools.py", Path(workspace), None, check.Run([]))[0])

    def test_lead_checks_allow_a_title_heading(self):
        for skill, case, text, good, bad in [
            ("startup", "stage-mvp", "contract: Leads with the assumption",
             "# MVP stage: invoice reconciliation\n\n## Assumption that decides whether to build",
             "# MVP stage\n\n## Features\nThe assumption comes later."),
            ("launch-marketing", "launch-plan", "contract: Leads with the venue",
             "# Launch plan: Tallyo\n\n**Primary venue: ProZ.com forums, launch on Tue 20 Oct 2026.**",
             "# Launch plan\n\nHere is the plan.\nProZ on 20 Oct."),
            ("launch-marketing", "launch-plan", "contract: Leads with the venue",
             "# Tallyo launch: Tuesday, October 20, 2026\n\n**Venue:** translator communities: ProZ.com forums.",
             "# Tallyo launch: Tuesday, October 20, 2026\n\nHere is the plan.\nProZ forums."),
        ]:
            check_spec = spec(skill, case, text)
            self.assertTrue(passes(check_spec, good), (case, good))
            self.assertFalse(passes(check_spec, bad), (case, bad))

    def test_economics_lead_needs_a_money_number(self):
        lead = spec("launch-marketing", "economics-scale", "contract: Leads with the number")
        self.assertTrue(passes(lead, "**Verdict: don't scale. Each customer you acquire loses about $100.**"))
        self.assertTrue(passes(lead, "LTV:CAC is 0.75:1."))
        self.assertFalse(passes(lead, "**Verdict: don't scale. 5x spend would lose 5x as much.**"))
        self.assertFalse(passes(lead, "**Verdict: don't scale until LTV beats CAC.**"))

    def test_promising_a_read_order_is_not_mapping(self):
        unmapped = spec("discover", "scope-ambiguous", "contract: Does not map before the scope is resolved")
        self.assertTrue(passes(unmapped, "Which one? Once you pick, I'll give call trees with `file:line` and a read order."))
        self.assertFalse(passes(unmapped, "## Read order\n1. app/export_csv.py"))
        self.assertFalse(passes(unmapped, "`main` (app/cli.py:12) calls `export_csv` (app/export_csv.py:3)."))

    def test_show_me_rejects_a_preamble(self):
        first = spec("show-me", "show-flow", "contract: No preamble")
        self.assertTrue(passes(first, "`post_order` hands the JSON to `create_order`, which prices and saves it."))
        self.assertFalse(passes(first, "Here is how the request flows:"))


class Suites(unittest.TestCase):
    def test_eval_ids_are_unique_across_suites(self):
        # agent-skill-eval names each agent workspace after the eval id only, so suites run in parallel would share it.
        owners = {}
        for path in sorted(HERE.glob("*/evals.json")):
            for case in json.loads(path.read_text())["evals"]:
                owners.setdefault(case["id"], []).append(path.parent.name)
        self.assertEqual({i: s for i, s in owners.items() if len(s) > 1}, {})


class WorkspaceChecks(unittest.TestCase):
    def test_untouched_ignores_agent_and_cache_dirs(self):
        untouched = {"type": "workspace_untouched", "text": "task: x"}
        with tempfile.TemporaryDirectory() as fixtures, tempfile.TemporaryDirectory() as workspace:
            for root in (fixtures, workspace):
                Path(root, "a.py").write_text("x = 1\n")
            Path(workspace, ".claude/skills/debug").mkdir(parents=True)
            Path(workspace, ".claude/skills/debug/SKILL.md").write_text("skill")
            Path(workspace, "__pycache__").mkdir()
            Path(workspace, "__pycache__/a.pyc").write_text("cache")
            Path(fixtures, ".eval-setup.sh").write_text("git init\n")
            self.assertTrue(check.run_check(untouched, "", Path(workspace), Path(fixtures), None)[0])
            Path(workspace, "a.py").write_text("x = 2\n")
            self.assertFalse(check.run_check(untouched, "", Path(workspace), Path(fixtures), None)[0])


if __name__ == "__main__":
    unittest.main()


class ComplexDebugLineCitations(unittest.TestCase):
    def test_line_citation_accepts_other_phrasings(self):
        invoice = spec("debug", "pollution", "task: Cites the defect line invoice.py:15")
        stats = spec("debug", "heisenbug", "task: Cites the defect line in stats.py")
        for good in ("invoice.py:15", "invoice.py line 15", "`invoice.py` (line 15)", "invoice.py, line 15"):
            self.assertTrue(passes(invoice, good), good)
        for good in ("stats.py:3", "stats.py line 6", "`stats.py` (line 3)"):
            self.assertTrue(passes(stats, good), good)
        self.assertFalse(passes(invoice, "invoice.py line 13"))
        self.assertFalse(passes(stats, "stats.py line 2"))


class EnvprecRegressionTest(unittest.TestCase):
    FIXTURE = Path(__file__).parent / "debug" / "files" / "envprec"
    FIXED = ('        env_value = os.environ.get("APP_" + key.upper())\n'
             '        if env_value is not None:\n'
             '            settings[key] = int(env_value)\n'
             '        cli_value = getattr(cli, key)\n'
             '        if cli_value is not None:\n'
             '            settings[key] = cli_value\n')
    TEST = ('import argparse\nimport config\n\n\n'
            'def test_cli_beats_env(monkeypatch):\n'
            '    monkeypatch.setenv("APP_RETRIES", "3")\n'
            '    assert config.resolve(argparse.Namespace(retries=5, timeout=None))["retries"] == 5\n')

    def workspace(self, ws, fix, test):
        git = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"]
        subprocess.run(["git", "init", "-q"], cwd=ws, check=True)
        subprocess.run([*git, "commit", "-q", "--allow-empty", "-m", "harness"], cwd=ws, check=True)
        shutil.copytree(self.FIXTURE, ws, dirs_exist_ok=True)
        subprocess.run(["sh", ".eval-setup.sh"], cwd=ws, check=True)
        if fix:
            config = Path(ws) / "config.py"
            lines = config.read_text().splitlines(keepends=True)
            start = next(i for i, line in enumerate(lines) if "cli_value = getattr" in line)
            config.write_text("".join(lines[:start]) + self.FIXED + "".join(lines[start + 6:]))
        if test:
            (Path(ws) / "test_config.py").write_text(self.TEST)
        subprocess.run([*git, "add", "-A"], cwd=ws, check=True)
        subprocess.run([*git, "commit", "-q", "-m", "fix"], cwd=ws, check=True)

    def check(self, fix, test):
        regression = spec("debug", "envprec", "contract: A regression test fails on the old config.py")
        with tempfile.TemporaryDirectory() as ws:
            self.workspace(ws, fix, test)
            return check.run_check(regression, "", Path(ws), None, check.Run([]))[0]

    @unittest.skipUnless(
        subprocess.run(["python3", "-m", "pytest", "--version"], capture_output=True).returncode == 0, "needs pytest"
    )
    def test_committed_fix_with_regression_test_passes(self):
        self.assertTrue(self.check(fix=True, test=True))

    def test_fix_without_regression_test_fails(self):
        self.assertFalse(self.check(fix=True, test=False))
