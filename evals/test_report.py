"""Tests for the run-level statistics in report.py.

Run: python3 -m unittest discover -s evals
"""
import contextlib
import io
import json
import tempfile
import unittest
from unittest import mock

import report


class FisherOneSided(unittest.TestCase):
    def test_known_values(self):
        self.assertAlmostEqual(report.fisher_greater(3, 3, 0, 3), 1 / 20)
        self.assertAlmostEqual(report.fisher_greater(4, 4, 0, 4), 1 / 70)
        self.assertAlmostEqual(report.fisher_greater(9, 9, 3, 9), 0.0045249, places=6)

    def test_no_difference_is_not_significant(self):
        self.assertAlmostEqual(report.fisher_greater(3, 6, 3, 6), 662 / 924)
        self.assertEqual(report.fisher_greater(0, 3, 3, 3), 1.0)


class RunPasses(unittest.TestCase):
    def test_a_run_passes_only_when_all_its_checks_of_that_kind_pass(self):
        results = [("task: a", True), ("task: b", False), ("contract: c", True)]
        self.assertEqual(report.run_passes(results, "task"), False)
        self.assertEqual(report.run_passes(results, "contract"), True)
        self.assertIsNone(report.run_passes(results, "trigger"))


class IterationDir(unittest.TestCase):
    def test_uses_the_skill_name_of_the_suite(self):
        self.assertEqual(report.iteration_dir(report.Path("/w"), "routing", "10"), report.Path("/w/hl-debug-workspace/iteration-10"))
        self.assertEqual(report.iteration_dir(report.Path("/w"), "tdd", "3"), report.Path("/w/hl-tdd-workspace/iteration-3"))


class RunResults(unittest.TestCase):
    def test_answer_oracles_are_reevaluated_and_workspace_commands_keep_the_recorded_result(self):
        oracle = {"type": "command", "command": "python3 \"$EVALS/oracle.py\" max-words '3'", "text": "contract: short"}
        tests = {"type": "command", "command": "pytest -q", "text": "task: tests pass"}
        with tempfile.TemporaryDirectory() as tmp:
            run = report.Path(tmp)
            (run / "outputs").mkdir()
            (run / "outputs" / "output.txt").write_text("one two")
            (run / "outputs" / "stdout.log").write_text(json.dumps({"session_id": "no-such-session"}))
            recorded = [{"text": "contract: short", "passed": False}, {"text": "task: tests pass", "passed": True}]
            (run / "grading.json").write_text(json.dumps({"assertion_results": recorded}))
            self.assertEqual(report.run_results(run, [oracle, tests]), [("contract: short", True), ("task: tests pass", True)])

    def test_next_question_oracle_rechecks_a_stale_passing_grade(self):
        question = {"type": "command", "command": 'python3 "$EVALS/oracle.py" questions-next', "text": "contract: questions"}
        with tempfile.TemporaryDirectory() as tmp:
            run = report.Path(tmp)
            (run / "outputs").mkdir()
            (run / "outputs" / "output.txt").write_text("**Open questions**\nWhich editor?\n**Next:**\n1. Confirm the editor.")
            (run / "outputs" / "stdout.log").write_text(json.dumps({"session_id": "no-such-session"}))
            (run / "grading.json").write_text(json.dumps({"assertion_results": [{"text": question["text"], "passed": True}]}))
            self.assertEqual(report.run_results(run, [question]), [(question["text"], False)])

    def test_tooltip_oracle_recomputes_stale_and_missing_grades(self):
        checks = json.loads((report.HERE / "code-review-hard" / "checks.json").read_text())
        tooltip = next(c for c in checks["cr-revise"]["checks"] if c["text"] == "task: Rates the tooltip limited or cosmetic")
        cases = (
            ("The tooltip shows raw watts. It is a limited issue.", False, True),
            ("The tooltip is a limited issue, whereas the tooltip is a material bug.", True, False),
            ("The tooltip shows raw watts. It is a limited issue.", None, True),
        )
        for output, recorded, expected in cases:
            with self.subTest(output=output, recorded=recorded), tempfile.TemporaryDirectory() as tmp:
                run = report.Path(tmp)
                (run / "outputs").mkdir()
                (run / "outputs" / "output.txt").write_text(output)
                (run / "outputs" / "stdout.log").write_text(json.dumps({"session_id": "no-such-session"}, indent=2) + "\n")
                grades = [] if recorded is None else [{"text": tooltip["text"], "passed": recorded}]
                (run / "grading.json").write_text(json.dumps({"assertion_results": grades}, indent=2) + "\n")
                self.assertEqual(report.run_results(run, [tooltip]), [(tooltip["text"], expected)])

    def test_a_check_moved_to_another_kind_keeps_its_recorded_result(self):
        moved = {"type": "command", "command": "test -f plan.md", "text": "contract: writes a plan"}
        with tempfile.TemporaryDirectory() as tmp:
            run = report.Path(tmp)
            (run / "outputs").mkdir()
            (run / "outputs" / "output.txt").write_text("")
            (run / "outputs" / "stdout.log").write_text(json.dumps({"session_id": "no-such-session"}))
            (run / "grading.json").write_text(json.dumps({"assertion_results": [{"text": "task: writes a plan", "passed": False}]}))
            self.assertEqual(report.run_results(run, [moved]), [("contract: writes a plan", False)])


class ReportErrors(unittest.TestCase):
    def summary(
        self, is_error, passed, result=None, graded=True, missing=(), cost_usd=0, unrecorded=False,
        process=False, flat=True, scheduled=None, baseline=False, stale=False, retries=0,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = report.Path(tmp)
            suite = root / "evals" / "sample"
            suite.mkdir(parents=True)
            (suite / "evals.json").write_text(json.dumps({"skill_name": "hl-sample"}))
            spec = (
                {"type": "not_ran", "pattern": "git push", "text": "task: no push"} if process else
                {"type": "command", "command": "pytest -q", "text": "task: tests pass"}
            )
            checks = [spec]
            if unrecorded:
                checks.append({"type": "file_unchanged", "path": "input.txt", "text": "task: input preserved"})
            (suite / "checks.json").write_text(json.dumps({"case": {"checks": checks}}))
            base = root / "hl-sample-workspace/iteration-1"
            base.mkdir(parents=True)
            if "progress" not in missing:
                (base / "progress.jsonl").write_text(json.dumps({
                    "event": "suite_started", "run_id": "new" if "finish" in missing else "current",
                }) + "\n")
            if "summary" not in missing:
                plan = {
                    "eval_ids": ["case"], "agents": ["claude-code"], "run_id": "current",
                    "runs_per_case": 1, "with_baseline": baseline, "skipped_runs": [], "errors": [],
                    **(scheduled or {}),
                }
                (base / "summary.json").write_text(json.dumps(plan))
            if result is None:
                result = "You've hit your session limit" if is_error else "The test fails."
            for config in (report.CONFIGS if baseline else ("with_skill",)):
                run = base / "eval-case" / "claude-code" / config / ("" if flat else "run-1")
                (run / "outputs").mkdir(parents=True)
                (run / "run_meta.json").write_text(json.dumps({"run_id": "old" if stale else "current"}))
                (run / "outputs/output.txt").write_text(result)
                if "stdout" not in missing:
                    (run / "outputs/stdout.log").write_text(json.dumps({
                        "session_id": "no-such-session", "is_error": is_error, "result": result,
                    }) if result else "")
                if "timing" not in missing:
                    (run / "timing.json").write_text(json.dumps({"cost_usd": cost_usd, "retries": retries}))
                if graded:
                    recorded = [{"text": spec["text"], "passed": passed}]
                    if baseline and config == "with_skill" and unrecorded:
                        recorded.append({"text": checks[1]["text"], "passed": True})
                    (run / "grading.json").write_text(json.dumps({"assertion_results": recorded}))
            out = io.StringIO()
            with mock.patch.object(report, "HERE", root / "evals"), mock.patch.object(
                report.sys, "argv", ["report.py", str(root), "sample:2" if "iteration" in missing else "sample:1", "--failures"],
            ), mock.patch.object(report.check.Run, "from_output_dir", return_value=None), contextlib.redirect_stdout(out):
                report.main()
            return out.getvalue()

    def test_a_retry_cannot_hide_the_unrecorded_attempt_or_its_cost(self):
        output = self.summary(is_error=False, passed=True, cost_usd=0.25, retries=1, baseline=True)
        self.assertIn("| sample | task | 1/1 | 1/1 | 0/1 | 0/1 | n/a |", output)
        self.assertIn("retried", output)
        self.assertIn("Incomplete:", output)
        self.assertIn("(subtotal)", output)

    def test_complete_paired_runs_keep_the_statistical_comparison(self):
        output = self.summary(is_error=False, passed=True, baseline=True)
        self.assertIn("| sample | task | 1/1 | 1/1 | 1/1 | 1/1 | 1.000 |", output)
        self.assertNotIn("Incomplete:", output)

    def test_an_unrecorded_required_check_prevents_a_passing_run(self):
        output = self.summary(is_error=False, passed=True, unrecorded=True)
        self.assertIn("| sample | task | 1/2 | 0/0 | 0/1 | 0/0 |", output)
        self.assertIn("Incomplete: 1 runs", output)
        self.assertIn("no recorded result for task: input preserved", output)

    def test_cli_error_cannot_pass_from_otherwise_passing_checks(self):
        output = self.summary(is_error=True, passed=True, result="Reached max turns")
        self.assertIn("| sample | task | 1/1 | 0/0 | 0/1 | 0/0 |", output)
        self.assertIn("CLI error: Reached max turns", output)

    def test_missing_transcript_is_incomplete_not_an_observed_failure(self):
        output = self.summary(is_error=False, passed=True, process=True)
        self.assertIn("Incomplete:", output)
        self.assertIn("no session transcript", output)
        self.assertNotIn("\nsample/case with_skill run-1: task: no push", output)

    def test_incomplete_baseline_does_not_get_a_significance_score(self):
        output = self.summary(is_error=False, passed=True, unrecorded=True, baseline=True)
        self.assertIn("| sample | task | 2/2 | 1/2 | 1/1 | 0/1 | n/a |", output)

    def test_stale_run_results_are_not_counted(self):
        output = self.summary(is_error=False, passed=True, stale=True)
        self.assertNotIn("| sample | task |", output)
        self.assertIn("run identity does not match", output)

    def test_an_earlier_summary_does_not_seal_a_killed_rerun(self):
        output = self.summary(is_error=False, passed=True, missing=("finish",))
        self.assertNotIn("| sample | task |", output)
        self.assertIn("suite did not finish", output)

    def test_a_skipped_run_cannot_reuse_an_earlier_result(self):
        output = self.summary(is_error=False, passed=True, scheduled={
            "skipped_runs": [{"run": "case-claude-code-with-r1", "reason": "skipped: budget exceeded"}],
        })
        self.assertNotIn("| sample | task |", output)
        self.assertIn("skipped: budget exceeded", output)

    def test_unfinished_suite_is_reported(self):
        output = self.summary(is_error=False, passed=True, missing=("summary",))
        self.assertIn("suite did not finish", output)

    def test_missing_scheduled_runs_are_reported(self):
        output = self.summary(is_error=False, passed=True, flat=False, scheduled={
            "eval_ids": ["case"], "agents": ["claude-code"], "runs_per_case": 2,
            "with_baseline": True, "skipped_runs": [], "errors": [],
        })
        self.assertIn("with_skill run-2: missing scheduled run", output)
        self.assertIn("without_skill run-1: missing scheduled run", output)
        self.assertIn("without_skill run-2: missing scheduled run", output)

    def test_missing_iteration_is_rejected(self):
        with self.assertRaises(SystemExit):
            self.summary(is_error=False, passed=True, missing=("iteration",))

    def test_cli_error_is_excluded_and_its_reason_is_reported(self):
        output = self.summary(is_error=True, passed=False)
        self.assertNotIn("| sample | task |", output)
        self.assertIn("Excluded 1 runs", output)
        self.assertIn("You've hit your session limit", output)

    def test_a_session_limit_without_grading_is_still_reported(self):
        output = self.summary(is_error=True, passed=False, graded=False)
        self.assertIn("Excluded 1 runs", output)
        self.assertIn("You've hit your session limit", output)

    def test_a_missing_grade_is_reported_as_incomplete(self):
        output = self.summary(is_error=False, passed=False, graded=False)
        self.assertIn("sample/case with_skill run-1: missing grading.json", output)
        self.assertNotIn("| sample | task |", output)

    def test_a_sparse_run_is_reported_without_claiming_a_known_cost(self):
        output = self.summary(is_error=False, passed=False, graded=False, missing=("timing", "stdout"))
        self.assertIn("Incomplete: 1 runs", output)
        self.assertIn("missing outputs/stdout.log", output)
        self.assertIn("Cost unavailable for 1 runs", output)
        self.assertIn("subtotal", output)

    def test_missing_stdout_with_grading_is_reported_as_incomplete(self):
        output = self.summary(is_error=False, passed=True, missing=("stdout",))
        self.assertIn("Incomplete: 1 runs", output)
        self.assertIn("missing outputs/stdout.log", output)
        self.assertNotIn("| sample | task |", output)

    def test_a_null_cost_is_unavailable_but_zero_is_known(self):
        output = self.summary(is_error=False, passed=True, cost_usd=None)
        self.assertIn("Cost unavailable for 1 runs", output)
        self.assertNotIn("Cost unavailable", self.summary(is_error=False, passed=True, cost_usd=0))

    def test_blank_stdout_without_stderr_is_reported(self):
        output = self.summary(is_error=False, passed=False, result="")
        self.assertIn("Excluded 1 runs", output)
        self.assertIn("empty stdout.log; missing stderr.log", output)

    def test_missing_timing_does_not_hide_a_genuine_failed_run(self):
        output = self.summary(is_error=False, passed=False, missing=("timing",))
        self.assertIn("| sample | task | 0/1 | 0/0 | 0/1 | 0/0 |", output)
        self.assertIn("Cost unavailable for 1 runs", output)
        self.assertNotIn("Excluded", output)

    def test_a_real_failed_run_stays_in_the_denominator(self):
        output = self.summary(is_error=False, passed=False)
        self.assertIn("| sample | task | 0/1 | 0/0 | 0/1 | 0/0 |", output)
        self.assertNotIn("Excluded", output)

    def test_a_turn_limit_error_stays_in_the_denominator(self):
        output = self.summary(is_error=True, passed=False, result="Reached max turns")
        self.assertIn("| sample | task | 0/1 | 0/0 | 0/1 | 0/0 |", output)
        self.assertNotIn("Excluded", output)

    def test_an_unknown_cli_error_stays_in_the_denominator(self):
        output = self.summary(is_error=True, passed=False, result="The agent could not finish")
        self.assertIn("| sample | task | 0/1 | 0/0 | 0/1 | 0/0 |", output)
        self.assertNotIn("Excluded", output)

    def test_a_real_passed_run_stays_in_the_denominator(self):
        output = self.summary(is_error=False, passed=True)
        self.assertIn("| sample | task | 1/1 | 0/0 | 1/1 | 0/0 |", output)
        self.assertNotIn("Excluded", output)


if __name__ == "__main__":
    unittest.main()
