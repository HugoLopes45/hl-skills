"""Tests for the run-level statistics in report.py.

Run: python3 -m unittest discover -s evals
"""
import json
import tempfile
import unittest

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

    def test_a_check_moved_to_another_kind_keeps_its_recorded_result(self):
        moved = {"type": "command", "command": "test -f plan.md", "text": "contract: writes a plan"}
        with tempfile.TemporaryDirectory() as tmp:
            run = report.Path(tmp)
            (run / "outputs").mkdir()
            (run / "outputs" / "output.txt").write_text("")
            (run / "outputs" / "stdout.log").write_text(json.dumps({"session_id": "no-such-session"}))
            (run / "grading.json").write_text(json.dumps({"assertion_results": [{"text": "task: writes a plan", "passed": False}]}))
            self.assertEqual(report.run_results(run, [moved]), [("contract: writes a plan", False)])


if __name__ == "__main__":
    unittest.main()
