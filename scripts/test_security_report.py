"""Tests for the hl-security-audit report validator. Run: python3 -m unittest discover scripts"""
import copy
import datetime
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "hl-security-audit"
SCRIPT = SKILL / "scripts" / "validate_report.py"
EXAMPLE = json.loads((SKILL / "references" / "report-example.json").read_text(encoding="utf-8"))
TODAY = datetime.date(2026, 10, 26)

sys.dont_write_bytecode = True
_spec = importlib.util.spec_from_file_location("validate_report", SCRIPT)
assert _spec and _spec.loader
validate_report = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_report)


def run_cli(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-B", str(SCRIPT), str(path)], capture_output=True, text=True, check=False)


def high_assurance_report() -> dict:
    """The example made complete by removing its blocked units and open lead, with every scanner run."""
    report = copy.deepcopy(EXAMPLE)
    report["units"] = [u for u in report["units"] if u["status"] != "blocked"]
    report["findings"] = [f for f in report["findings"] if f["state"] != "needs_validation"]
    for scanner in report["scanners"]:
        scanner.update(status="ran", executions=1)
    report["coverage_review"]["uncovered"] = []
    report.update(run_status="complete", assurance="HIGH", limitations=[])
    return report


def finding(report: dict, state: str) -> dict:
    return next(f for f in report["findings"] if f["state"] == state)


class ReportRulesTest(unittest.TestCase):
    def assertRejected(self, report: dict, location: str) -> None:
        errors = validate_report.validate(report, TODAY)
        self.assertTrue(any(error.startswith(location) for error in errors), errors)

    def assertAccepted(self, report: dict) -> None:
        self.assertEqual(validate_report.validate(report, TODAY), [])

    def test_example_and_high_assurance_variant_are_valid(self) -> None:
        self.assertAccepted(copy.deepcopy(EXAMPLE))
        self.assertAccepted(high_assurance_report())

    def test_source_coverage_can_establish_assurance_without_scanners(self) -> None:
        complete = high_assurance_report()
        partial = copy.deepcopy(EXAMPLE)
        partial["assurance"] = "MEDIUM"
        for report in (complete, partial):
            report["scanners"] = []
            for unit in report["units"]:
                unit["checks"] = [check for check in unit["checks"] if check["method"] != "scanner"]
            self.assertAccepted(report)

    def test_scanner_volume_cannot_replace_boundary_review(self) -> None:
        report = high_assurance_report()
        for unit in report["units"]:
            for check in unit["checks"]:
                check["method"] = "scanner"
        self.assertRejected(report, "assurance")

    def test_confirmed_finding_needs_a_reviewer_other_than_its_author(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        finding(report, "confirmed")["reviewer"] = None
        self.assertRejected(report, "findings[0].reviewer")
        report = copy.deepcopy(EXAMPLE)
        finding(report, "confirmed")["reviewer"]["id"] = " Hunter-AUTHZ "
        self.assertRejected(report, "findings[0].reviewer.id")

    def test_reviewer_decision_must_match_state(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        finding(report, "rejected")["reviewer"]["decision"] = "confirmed"
        self.assertRejected(report, "findings[2].reviewer.decision")

    def test_unresolved_finding_cannot_carry_severity(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        finding(report, "needs_validation")["severity"] = "HIGH"
        self.assertRejected(report, "findings[1]: has unexpected fields")

    def test_confirmed_finding_needs_cwe_and_checked_cvss(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        del finding(report, "confirmed")["cwe"]
        self.assertRejected(report, "findings[0].cwe: missing")
        report = copy.deepcopy(EXAMPLE)
        finding(report, "confirmed")["cvss"] = "8.1"
        self.assertRejected(report, "findings[0].cvss")

    def test_cvss4_provider_urgency_is_accepted(self) -> None:
        vector = "CVSS:4.0/AV:P/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:A/S:P/AU:Y/R:A/V:D/RE:L"
        for urgency in ("Clear", "Green", "Amber", "Red"):
            with self.subTest(urgency=urgency):
                report = copy.deepcopy(EXAMPLE)
                finding(report, "confirmed")["cvss"] = f"{vector}/U:{urgency}"
                self.assertAccepted(report)

    def test_complete_run_rejects_open_work(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        report["run_status"] = "complete"
        errors = validate_report.validate(report, TODAY)
        for reason in ("planned, blocked or deferred", "needs validation", "uncovered surface"):
            self.assertTrue(any(reason in error for error in errors), (reason, errors))

    def test_complete_run_needs_a_reviewed_unit_and_a_reviewed_finding(self) -> None:
        report = high_assurance_report()
        finding(report, "rejected")["reviewer"] = None
        self.assertRejected(report, "run_status")
        report = high_assurance_report()
        report.update(units=[], findings=[], assurance="LOW")
        self.assertRejected(report, "run_status")

    def test_quick_run_is_never_complete(self) -> None:
        report = high_assurance_report()
        report["profile"] = "quick"
        self.assertRejected(report, "run_status")

    def test_incomplete_run_states_limitations(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        report["limitations"] = []
        self.assertRejected(report, "limitations")

    def test_high_assurance_needs_source_or_supplied_evidence_on_every_reviewed_unit(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        report["assurance"] = "HIGH"
        self.assertRejected(report, "assurance")
        report = high_assurance_report()
        search = next(u for u in report["units"] if u["id"] == "search.sort.injection")
        search["checks"][0]["method"] = "scanner"
        self.assertRejected(report, "assurance")
        report["assurance"] = "MEDIUM"
        self.assertAccepted(report)

    def test_medium_assurance_needs_source_or_supplied_evidence_on_a_reviewed_unit(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        report["scanners"][0].update(status="ran", executions=1)
        for unit in report["units"]:
            if unit["status"] == "reviewed":
                for check in unit["checks"]:
                    check["method"] = "scanner"
        self.assertRejected(report, "assurance")
        report["assurance"] = "LOW"
        self.assertAccepted(report)
        report["units"][0]["checks"][0]["method"] = "supplied"
        report["assurance"] = "MEDIUM"
        self.assertAccepted(report)

    def test_scanner_records_do_not_decide_assurance(self) -> None:
        for status, executions in (("failed", 1), ("denied", 0), ("skipped", 0)):
            with self.subTest(status=status):
                report = high_assurance_report()
                for scanner in report["scanners"]:
                    scanner.update(status=status, executions=executions, scope=["app/search.py"])
                for unit in report["units"]:
                    unit["checks"] = [c for c in unit["checks"] if c["method"] != "scanner"]
                self.assertAccepted(report)

    def test_execution_count_matches_scanner_status(self) -> None:
        for status, executions in (("failed", 0), ("ran", 0), ("denied", 1), ("skipped", 2)):
            report = copy.deepcopy(EXAMPLE)
            report["scanners"][1].update(status=status, executions=executions)
            self.assertRejected(report, "scanners[1].executions")

    def test_scanner_check_needs_a_scanner_that_ran(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        report["units"][2]["checks"][0]["method"] = "scanner"
        report["scanners"][0].update(status="denied", executions=0)
        report["assurance"] = "LOW"
        self.assertRejected(report, "units: a scanner check")
        report["scanners"][0].update(status="ran", executions=1)
        self.assertAccepted(report)

    def test_units_and_findings_link_both_ways(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        report["units"][2]["finding_ids"] = []
        self.assertRejected(report, "findings[2].unit_ids")
        report = copy.deepcopy(EXAMPLE)
        report["units"][0]["finding_ids"].append("search-sort-sql")
        self.assertRejected(report, "units[0].finding_ids")

    def test_planned_unit_holds_no_evidence(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        report["units"][2].update(status="planned", reason=None)
        self.assertRejected(report, "units[2].checks")
        self.assertRejected(report, "units[2].finding_ids")

    def test_deferred_unit_retains_evidence_without_closing_coverage(self) -> None:
        report = high_assurance_report()
        report["units"][0].update(status="deferred", reason="An alternate writer needs further review.")
        report.update(run_status="incomplete", assurance="MEDIUM", limitations=["Alternate writer not checked."])
        self.assertAccepted(report)
        report["run_status"] = "complete"
        self.assertRejected(report, "run_status")

    def test_not_applicable_requires_source_or_supplied_evidence(self) -> None:
        report = high_assurance_report()
        unit = copy.deepcopy(report["units"][0])
        unit.update(id="browser-surface", surface="Browser execution", category="DOM XSS",
                    status="not_applicable", finding_ids=[], reason="The service returns JSON only.")
        report["units"].append(unit)
        for method in ("source", "supplied"):
            with self.subTest(method=method):
                unit["checks"] = [{"method": method, "evidence": "No browser document is served.",
                                   "author": "analyst-a", "paths": unit["paths"]}]
                self.assertAccepted(report)
        for checks in ([], [{"method": "scanner", "evidence": "No matches.",
                             "author": "analyst-a", "paths": unit["paths"]}]):
            with self.subTest(checks=checks):
                unit["checks"] = checks
                self.assertRejected(report, f"units[{len(report['units']) - 1}].checks")

    def test_trace_runs_from_entry_to_sink_inside_linked_units(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        finding(report, "confirmed")["trace"].reverse()
        self.assertRejected(report, "findings[0].trace")
        report = copy.deepcopy(EXAMPLE)
        finding(report, "confirmed")["trace"][2]["path"] = "app/search.py"
        self.assertRejected(report, "findings[0].trace[2].path")

    def test_paths_respect_the_scope(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        report["scope"] = ["app/reservations.py", "app/routes.py"]
        report["units"] = report["units"][:3]
        report["units"][1].update(status="out_of_scope", checks=[], finding_ids=[])
        report["units"][2].update(status="out_of_scope", checks=[], finding_ids=[], reason="Outside the requested files.")
        report["findings"] = [finding(report, "confirmed")]
        self.assertAccepted(report)
        report["units"][2]["paths"] = ["app"]
        self.assertRejected(report, "units[2].paths")

    def test_unsafe_paths_are_rejected(self) -> None:
        for path in ("../secret", "/etc/hosts", "app//x.py", "C:/x.py", "app\\x.py", "app/./x.py", "app/x. "):
            report = copy.deepcopy(EXAMPLE)
            report["units"][0]["paths"].append(path)
            self.assertRejected(report, "units[0].paths[2]")

    def test_posix_record_paths_are_not_windows_device_paths(self) -> None:
        for path in ("app/aux.c", "con.go", "nul.txt", "app/name./module.py"):
            with self.subTest(path=path):
                report = copy.deepcopy(EXAMPLE)
                report["units"][0]["paths"].append(path)
                self.assertAccepted(report)

    def test_scope_entries_stand_apart(self) -> None:
        for scope in ([".", "app"], ["app", "app/routes.py"], ["app", "app"]):
            report = copy.deepcopy(EXAMPLE)
            report["scope"] = scope
            self.assertRejected(report, "scope")

    def test_accepted_risk_needs_an_unexpired_exception(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        confirmed = finding(report, "confirmed")
        confirmed["disposition"] = "accepted_risk"
        self.assertRejected(report, "findings[0].exception")
        exception = {"source": "security-exceptions.json", "rationale": "Admin-only pilot.", "expires": TODAY.isoformat()}
        confirmed["exception"] = exception
        self.assertRejected(report, "findings[0].exception.expires")
        exception["expires"] = (TODAY + datetime.timedelta(days=1)).isoformat()
        self.assertAccepted(report)
        confirmed["disposition"] = "active"
        self.assertRejected(report, "findings[0].exception")

    def test_observed_evidence_needs_a_supplied_check(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        finding(report, "confirmed")["evidence_basis"] = "observed"
        self.assertRejected(report, "findings[0].evidence_basis")
        report["units"][0]["checks"].append(
            {"method": "supplied", "evidence": "Owner-supplied log, revision checked.", "author": "hunter-authz", "paths": ["app/routes.py"]}
        )
        self.assertAccepted(report)

    def test_coverage_reviewer_is_not_an_author(self) -> None:
        for author in ("hunter-injection", "HUNTER-AUTH"):
            report = copy.deepcopy(EXAMPLE)
            report["coverage_review"]["reviewer"] = author
            self.assertRejected(report, "coverage_review.reviewer")

    def test_duplicate_units_are_rejected(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        twin = copy.deepcopy(report["units"][0])
        twin.update(id="reservations.cancel.ownership-2", finding_ids=[])
        report["units"].append(twin)
        self.assertRejected(report, "units: two units")
        report["units"][-1]["id"] = "reservations.cancel.ownership"
        self.assertRejected(report, "units: ids")

    def test_text_needs_visible_safe_characters(self) -> None:
        for value in ("", " \n\t", "\u200b", "ok\x1b[2J", "admin\u202eexe"):
            report = copy.deepcopy(EXAMPLE)
            finding(report, "confirmed")["impact"] = value
            self.assertRejected(report, "findings[0].impact")

    def test_booleans_are_not_counts(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        report["scanners"][0]["executions"] = True
        self.assertRejected(report, "scanners[0].executions")
        report = copy.deepcopy(EXAMPLE)
        report["schema_version"] = True
        self.assertRejected(report, "schema_version")


class CommandLineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, content: str) -> Path:
        path = self.root / "security-audit.json"
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_and_invalid_reports(self) -> None:
        self.assertEqual(run_cli(self.write(json.dumps(EXAMPLE))).returncode, 0)
        report = copy.deepcopy(EXAMPLE)
        report["assurance"] = "HIGH"
        self.assertEqual(run_cli(self.write(json.dumps(report))).returncode, 1)

    def test_diagnostics_do_not_echo_report_content(self) -> None:
        report = copy.deepcopy(EXAMPLE)
        report["units"][0]["checks"][0]["SYNTHETIC-MARKER-key"] = "SYNTHETIC-MARKER-value"
        report["findings"][0]["impact"] = "SYNTHETIC-MARKER\x1b]0;x\x07"
        result = run_cli(self.write(json.dumps(report)))
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("SYNTHETIC-MARKER", result.stdout + result.stderr)

    def test_malformed_documents_are_invalid_without_crashing(self) -> None:
        body = json.dumps(EXAMPLE)
        repeated = body.replace('"assurance":', '"assurance": "HIGH", "assurance":', 1)
        malformed = copy.deepcopy(EXAMPLE)
        malformed["scanners"][0]["executions"] = float("nan")
        not_finite = json.dumps(malformed)
        for content in (repeated, not_finite, "[" * 100 + "]" * 100, "[" * 100000, "{", "\ufeff" + body):
            result = run_cli(self.write(content))
            self.assertEqual(result.returncode, 1, content[:40])
            self.assertNotIn("Traceback", result.stderr)

    def test_unreadable_inputs_are_not_checked(self) -> None:
        target = self.write(json.dumps(EXAMPLE))
        link = self.root / "link.json"
        link.symlink_to(target)
        large = self.root / "large.json"
        large.write_bytes(b" " * (2 * 1024 * 1024 + 1))
        for path in (link, self.root / "missing.json", self.root, large):
            self.assertEqual(run_cli(path).returncode, 2, path.name)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "needs named pipes")
    def test_named_pipe_is_not_read(self) -> None:
        pipe = self.root / "pipe.json"
        os.mkfifo(pipe)
        self.assertEqual(run_cli(pipe).returncode, 2)


if __name__ == "__main__":
    unittest.main()
