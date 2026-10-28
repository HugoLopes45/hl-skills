#!/usr/bin/env python3
"""Check the structure and cross-record consistency of a security-audit.json report.

Usage: python3 validate_report.py <security-audit.json>

Exit 0: valid. Exit 1: invalid report. Exit 2: not checked (usage error or unreadable input).
Reads only the named file. Never opens cited paths or runs report content. Diagnostics name
locations, never report values. A valid report is consistent, not proven true.
"""
from __future__ import annotations

import datetime
import json
import math
import os
import re
import stat
import sys
import unicodedata
from typing import Callable

MAX_BYTES = 2 * 1024 * 1024
MAX_DEPTH = 64
MAX_ERRORS = 50

STATES = ("confirmed", "needs_validation", "rejected")
UNIT_STATUSES = ("planned", "reviewed", "blocked", "deferred", "out_of_scope", "not_applicable")
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
CWE_RE = re.compile(r"CWE-[1-9][0-9]{0,5}|unmapped")
CVSS_RE = re.compile(r"unscored|CVSS:(?:3\.0|3\.1|4\.0)(?:/[A-Za-z]{1,4}:[A-Za-z]{1,5})+")
DATE_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
BIDI = frozenset("\u061c\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069")
INVISIBLE = frozenset(("Cc", "Cf", "Cs", "Co", "Cn", "Zs", "Zl", "Zp"))

Checker = Callable[[object, str, list], None]


class NotChecked(Exception):
    """The input could not be read safely; nothing was validated."""


class Invalid(Exception):
    """The input is not a well-formed report document."""


class DuplicateKey(ValueError):
    pass


# Scalar checks


def text_problem(value: object) -> str | None:
    if not isinstance(value, str):
        return "must be a string"
    if any(ch in BIDI for ch in value):
        return "contains a bidirectional control character"
    if any(ch not in "\t\n" and unicodedata.category(ch) in ("Cc", "Cs") for ch in value):
        return "contains a control character"
    if not any(unicodedata.category(ch) not in INVISIBLE for ch in value):
        return "needs visible text"
    return None


def segment_problem(segment: str) -> str | None:
    if segment in ("", ".", ".."):
        return "must not contain empty, '.' or '..' segments"
    return None


def path_problem(value: object) -> str | None:
    problem = text_problem(value)
    if problem or value == ".":
        return problem
    assert isinstance(value, str)
    if len(value) > 1024 or value[0] in "/~" or "\\" in value or ":" in value or value != value.strip():
        return "must be a short repository-relative POSIX path"
    for segment in value.split("/"):
        problem = segment_problem(segment)
        if problem:
            return problem
    return None


def report_problem(problem: str | None, where: str, errors: list) -> None:
    if problem:
        errors.append(f"{where}: {problem}")


def text(value: object, where: str, errors: list) -> None:
    report_problem(text_problem(value), where, errors)


def safe_path(value: object, where: str, errors: list) -> None:
    report_problem(path_problem(value), where, errors)


def identifier(value: object, where: str, errors: list) -> None:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        errors.append(f"{where}: must be an ASCII identifier of letters, digits, '.', '_' or '-'")


def date(value: object, where: str, errors: list) -> None:
    try:
        valid = isinstance(value, str) and DATE_RE.fullmatch(value) and datetime.date.fromisoformat(value)
    except ValueError:
        valid = False
    if not valid:
        errors.append(f"{where}: must be a calendar date YYYY-MM-DD")


def positive_int(value: object, where: str, errors: list) -> None:
    if type(value) is not int or value < 1:
        errors.append(f"{where}: must be a positive integer")


def count(value: object, where: str, errors: list) -> None:
    if type(value) is not int or value < 0:
        errors.append(f"{where}: must be a nonnegative integer")


def version(value: object, where: str, errors: list) -> None:
    if type(value) is not int or value != 1:
        errors.append(f"{where}: must be 1")


def one_of(*choices: str) -> Checker:
    def check(value: object, where: str, errors: list) -> None:
        if not isinstance(value, str) or value not in choices:
            errors.append(f"{where}: must be one of {', '.join(choices)}")
    return check


def matching(regex: re.Pattern, description: str) -> Checker:
    def check(value: object, where: str, errors: list) -> None:
        if not isinstance(value, str) or not regex.fullmatch(value):
            errors.append(f"{where}: must be {description}")
    return check


def optional(checker: Checker) -> Checker:
    def check(value: object, where: str, errors: list) -> None:
        if value is not None:
            checker(value, where, errors)
    return check


# Containers


def has_duplicates(values: list) -> bool:
    strings = [value for value in values if isinstance(value, str)]
    return len(set(strings)) != len(strings)


def list_of(item: Checker, nonempty: bool = False, unique: bool = True) -> Checker:
    def check(value: object, where: str, errors: list) -> None:
        if not isinstance(value, list):
            errors.append(f"{where}: must be an array")
            return
        if nonempty and not value:
            errors.append(f"{where}: must not be empty")
        for index, entry in enumerate(value):
            item(entry, f"{where}[{index}]", errors)
        if unique and has_duplicates(value):
            errors.append(f"{where}: entries must be unique")
    return check


def apply_spec(value: object, spec: dict, where: str, errors: list) -> None:
    label = where or "report"
    if not isinstance(value, dict):
        errors.append(f"{label}: must be an object")
        return
    prefix = f"{where}." if where else ""
    for name in spec:
        if name not in value:
            errors.append(f"{prefix}{name}: missing")
    if value.keys() - spec.keys():
        errors.append(f"{label}: has unexpected fields")
    for name, checker in spec.items():
        if name in value:
            checker(value[name], f"{prefix}{name}", errors)


def record(spec: dict) -> Checker:
    def check(value: object, where: str, errors: list) -> None:
        apply_spec(value, spec, where, errors)
    return check


TEXTS = list_of(text)
PATHS = list_of(safe_path, nonempty=True)

CHECK = record({
    "method": one_of("source", "scanner", "supplied"),
    "evidence": text,
    "author": text,
    "paths": PATHS,
})

UNIT = record({
    "id": identifier,
    "surface": text,
    "boundary": text,
    "category": text,
    "paths": PATHS,
    "status": one_of(*UNIT_STATUSES),
    "checks": list_of(CHECK, unique=False),
    "finding_ids": list_of(identifier),
    "reason": optional(text),
})

HOP = record({
    "path": safe_path,
    "line": positive_int,
    "role": one_of("entry", "step", "sink"),
    "detail": text,
})

FINDING_FIELDS = {
    "id": identifier,
    "title": text,
    "state": one_of(*STATES),
    "unit_ids": list_of(identifier, nonempty=True),
    "author": text,
    "attacker": text,
    "boundary": text,
    "impact": text,
    "conditions": TEXTS,
    "trace": list_of(HOP, nonempty=True, unique=False),
    "evidence_basis": one_of("source", "observed"),
    "evidence": text,
    "reviewer": optional(record({"id": text, "decision": one_of(*STATES), "reason": text})),
}

STATE_FIELDS = {
    "confirmed": {
        "severity": one_of("CRITICAL", "HIGH", "MEDIUM", "LOW"),
        "cwe": matching(CWE_RE, "CWE-<number> or unmapped"),
        "cvss": matching(CVSS_RE, "unscored or a CVSS 3.0, 3.1 or 4.0 vector"),
        "remediation": text,
        "regression": text,
        "disposition": one_of("active", "accepted_risk"),
        "exception": optional(record({"source": safe_path, "rationale": text, "expires": date})),
    },
    "needs_validation": {"blocker": text, "next_check": text},
    "rejected": {"reason": text},
}


def finding(value: object, where: str, errors: list) -> None:
    state = value.get("state") if isinstance(value, dict) else None
    extra = STATE_FIELDS.get(state, {}) if isinstance(state, str) else {}
    apply_spec(value, {**FINDING_FIELDS, **extra}, where, errors)


SCANNER = record({
    "kind": one_of("deps", "secrets", "sast", "patterns"),
    "command": text,
    "directory": safe_path,
    "executions": count,
    "status": one_of("ran", "skipped", "failed", "denied"),
    "scope": PATHS,
    "preflight": text,
    "result": text,
})

ROOT = {
    "schema_version": version,
    "source_ref": text,
    "scope": PATHS,
    "profile": one_of("quick", "standard", "deep"),
    "run_status": one_of("complete", "incomplete"),
    "assurance": one_of("HIGH", "MEDIUM", "LOW"),
    "limitations": TEXTS,
    "prior_runs": TEXTS,
    "coverage_review": record({"reviewer": optional(text), "uncovered": TEXTS, "notes": text}),
    "units": list_of(UNIT, unique=False),
    "findings": list_of(finding, unique=False),
    "scanners": list_of(SCANNER, unique=False),
}


# Relations between records


def ancestors(path: str) -> list:
    """Return '.', each parent directory of path, and path itself."""
    return [".", *(path[:index] for index, char in enumerate(path) if char == "/"), path]


def in_any(path: str, bases: set) -> bool:
    return not bases.isdisjoint(ancestors(path))


def actor(name: str) -> str:
    return " ".join(name.split()).casefold()


def check_scope(scope: list, errors: list) -> None:
    entries = set(scope)
    if "." in entries and len(scope) > 1:
        errors.append("scope: '.' must be the only entry")
    elif any(not entries.isdisjoint(ancestors(path)[1:-1]) for path in scope):
        errors.append("scope: entries must not contain one another")


def check_unique_ids(report: dict, errors: list) -> None:
    for name in ("units", "findings"):
        ids = [entry["id"] for entry in report[name]]
        if len(set(ids)) != len(ids):
            errors.append(f"{name}: ids must be unique")
    keys = [
        (actor(u["surface"]), actor(u["boundary"]), actor(u["category"]), tuple(sorted(u["paths"])))
        for u in report["units"]
    ]
    if len(set(keys)) != len(keys):
        errors.append("units: two units describe the same surface, boundary, category and paths")


def unit_status_problems(unit: dict) -> list:
    status, problems = unit["status"], []
    if (unit["reason"] is None) != (status in ("planned", "reviewed")):
        problems.append("reason: must be null for planned or reviewed units and present otherwise")
    if status == "reviewed" and not unit["checks"]:
        problems.append("checks: a reviewed unit needs at least one check")
    if status == "not_applicable" and not any(c["method"] in ("source", "supplied") for c in unit["checks"]):
        problems.append("checks: not_applicable needs a source or supplied check")
    if status in ("planned", "out_of_scope") and unit["checks"]:
        problems.append("checks: an unexamined unit has no checks")
    if status not in ("reviewed", "blocked", "deferred") and unit["finding_ids"]:
        problems.append("finding_ids: only reviewed, blocked or deferred units link findings")
    return problems


def unit_path_problems(unit: dict, scope: set, scope_ancestors: set) -> list:
    problems = []
    if unit["status"] == "out_of_scope":
        if any(path in scope_ancestors or in_any(path, scope) for path in unit["paths"]):
            problems.append("paths: an out_of_scope unit must lie outside the scope")
    elif not all(in_any(path, scope) for path in unit["paths"]):
        problems.append("paths: must lie within the scope")
    paths = set(unit["paths"])
    for index, check in enumerate(unit["checks"]):
        if not all(in_any(path, paths) for path in check["paths"]):
            problems.append(f"checks[{index}].paths: must lie within the unit's paths")
    return problems


def check_units(report: dict, finding_units: dict, errors: list) -> None:
    scope = set(report["scope"])
    scope_ancestors = {ancestor for base in scope for ancestor in ancestors(base)}
    for index, unit in enumerate(report["units"]):
        where = f"units[{index}]"
        problems = unit_status_problems(unit) + unit_path_problems(unit, scope, scope_ancestors)
        errors.extend(f"{where}.{problem}" for problem in problems)
        if any(unit["id"] not in finding_units.get(fid, ()) for fid in unit["finding_ids"]):
            errors.append(f"{where}.finding_ids: every linked finding must exist and link back")


def trace_problems(entry: dict, scope: set, owners: dict) -> list:
    roles = [hop["role"] for hop in entry["trace"]]
    problems = []
    if len(roles) == 1:
        ordered = roles[0] in ("entry", "sink")
    else:
        ordered = roles[0] == "entry" and roles[-1] == "sink" and set(roles[1:-1]) <= {"step"}
    if not ordered:
        problems.append("trace: must run from an entry through steps to a sink")
    linked = set(entry["unit_ids"])
    for index, hop in enumerate(entry["trace"]):
        hop_ancestors = ancestors(hop["path"])
        in_unit = any(not linked.isdisjoint(owners.get(ancestor, ())) for ancestor in hop_ancestors)
        if scope.isdisjoint(hop_ancestors) or not in_unit:
            problems.append(f"trace[{index}].path: must lie within the scope and a linked unit")
    return problems


def review_problems(entry: dict) -> list:
    reviewer = entry["reviewer"]
    if reviewer is None:
        return ["reviewer: a confirmed finding needs an independent reviewer"] if entry["state"] == "confirmed" else []
    problems = []
    if actor(reviewer["id"]) == actor(entry["author"]):
        problems.append("reviewer.id: must differ from the author")
    if reviewer["decision"] != entry["state"]:
        problems.append("reviewer.decision: must match the state")
    return problems


def disposition_problems(entry: dict, today: datetime.date) -> list:
    if entry["state"] != "confirmed":
        return []
    exception = entry["exception"]
    if entry["disposition"] == "active":
        return [] if exception is None else ["exception: an active finding has no exception"]
    if exception is None:
        return ["exception: accepted risk needs an exception"]
    if datetime.date.fromisoformat(exception["expires"]) <= today:
        return ["exception.expires: must be after today's UTC date"]
    return []


def link_problems(entry: dict, unit_findings: dict, supplied: set) -> list:
    problems = []
    if any(entry["id"] not in unit_findings.get(uid, ()) for uid in entry["unit_ids"]):
        problems.append("unit_ids: every linked unit must exist and link back")
    if entry["evidence_basis"] == "observed" and supplied.isdisjoint(entry["unit_ids"]):
        problems.append("evidence_basis: observed evidence needs a supplied check in a linked unit")
    return problems


def check_findings(report: dict, units: dict, today: datetime.date, errors: list) -> None:
    scope = set(report["scope"])
    unit_findings = {uid: set(unit["finding_ids"]) for uid, unit in units.items()}
    supplied = {uid for uid, unit in units.items() if any(check["method"] == "supplied" for check in unit["checks"])}
    owners: dict = {}
    for uid, unit in units.items():
        for path in unit["paths"]:
            owners.setdefault(path, set()).add(uid)
    for index, entry in enumerate(report["findings"]):
        problems = (
            link_problems(entry, unit_findings, supplied)
            + trace_problems(entry, scope, owners)
            + review_problems(entry)
            + disposition_problems(entry, today)
        )
        errors.extend(f"findings[{index}].{problem}" for problem in problems)


def check_scanners(report: dict, errors: list) -> None:
    for index, scanner in enumerate(report["scanners"]):
        if (scanner["status"] in ("ran", "failed")) != (scanner["executions"] > 0):
            errors.append(f"scanners[{index}].executions: ran or failed needs executions; skipped or denied has none")
    cited = any(check["method"] == "scanner" for unit in report["units"] for check in unit["checks"])
    if cited and not any(scanner["status"] == "ran" for scanner in report["scanners"]):
        errors.append("units: a scanner check needs a scanner that ran")


def incomplete_reasons(report: dict) -> list:
    statuses = {unit["status"] for unit in report["units"]}
    review = report["coverage_review"]
    reasons = [
        ("profile is quick", report["profile"] == "quick"),
        ("no unit is reviewed", "reviewed" not in statuses),
        ("a unit is planned, blocked or deferred", bool(statuses & {"planned", "blocked", "deferred"})),
        ("a finding needs validation", any(f["state"] == "needs_validation" for f in report["findings"])),
        ("a finding has no independent review", any(f["reviewer"] is None for f in report["findings"])),
        ("the coverage review is missing or left uncovered surface", review["reviewer"] is None or bool(review["uncovered"])),
    ]
    return [reason for reason, applies in reasons if applies]


def check_run_status(report: dict, errors: list) -> None:
    if report["run_status"] == "incomplete":
        if not report["limitations"]:
            errors.append("limitations: an incomplete run must state its limitations")
        return
    errors.extend(f"run_status: cannot be complete because {reason}" for reason in incomplete_reasons(report))


def check_assurance(report: dict, errors: list) -> None:
    reviewed = [unit for unit in report["units"] if unit["status"] == "reviewed"]
    examined = [unit for unit in reviewed if any(check["method"] in ("source", "supplied") for check in unit["checks"])]
    level = report["assurance"]
    if level == "MEDIUM" and not examined:
        errors.append("assurance: MEDIUM needs a reviewed unit with a source or supplied check")
    if level == "HIGH" and (report["run_status"] != "complete" or not examined or len(examined) < len(reviewed)):
        errors.append("assurance: HIGH needs a complete run and a source or supplied check on every reviewed unit")


def check_coverage_reviewer(report: dict, errors: list) -> None:
    reviewer = report["coverage_review"]["reviewer"]
    if reviewer is None:
        return
    authors = {actor(check["author"]) for unit in report["units"] for check in unit["checks"]}
    authors |= {actor(entry["author"]) for entry in report["findings"]}
    if actor(reviewer) in authors:
        errors.append("coverage_review.reviewer: must differ from every check and finding author")


def check_relations(report: dict, today: datetime.date, errors: list) -> None:
    units = {unit["id"]: unit for unit in report["units"]}
    finding_units = {entry["id"]: set(entry["unit_ids"]) for entry in report["findings"]}
    check_scope(report["scope"], errors)
    check_unique_ids(report, errors)
    check_units(report, finding_units, errors)
    check_findings(report, units, today, errors)
    check_scanners(report, errors)
    check_run_status(report, errors)
    check_assurance(report, errors)
    check_coverage_reviewer(report, errors)


# Input handling


def too_deep(value: object) -> bool:
    stack = [(value, 1)]
    while stack:
        item, depth = stack.pop()
        if depth > MAX_DEPTH:
            return True
        children = item.values() if isinstance(item, dict) else item if isinstance(item, list) else ()
        stack.extend((child, depth + 1) for child in children)
    return False


def validate(report: object, today: datetime.date) -> list:
    """Return one 'location: problem' line per error; an empty list means valid."""
    if too_deep(report):
        return [f"report: nested deeper than {MAX_DEPTH} levels"]
    errors: list = []
    apply_spec(report, ROOT, "", errors)
    if not errors:
        assert isinstance(report, dict)
        check_relations(report, today, errors)
    return errors


def unique_object(pairs: list) -> dict:
    keys = [key for key, _ in pairs]
    if len(set(keys)) != len(keys):
        raise DuplicateKey
    return dict(pairs)


def reject_constant(_: str) -> float:
    raise ValueError


def finite_float(literal: str) -> float:
    value = float(literal)
    if not math.isfinite(value):
        raise ValueError
    return value


def parse(data: bytes) -> object:
    try:
        return json.loads(
            data.decode("utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
            parse_float=finite_float,
        )
    except DuplicateKey:
        raise Invalid("an object repeats a key") from None
    except (ValueError, RecursionError):
        raise Invalid("not UTF-8 JSON with finite numbers") from None


def load(path: str) -> bytes:
    try:
        info = os.lstat(path)
        if not stat.S_ISREG(info.st_mode):
            raise NotChecked("the report path is not a regular file")
        if info.st_size > MAX_BYTES:
            raise NotChecked(f"the report exceeds {MAX_BYTES} bytes")
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
        with os.fdopen(descriptor, "rb") as handle:
            if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
                raise NotChecked("the report path is not a regular file")
            data = handle.read(MAX_BYTES + 1)
    except OSError:
        raise NotChecked("the report file cannot be read") from None
    if len(data) > MAX_BYTES:
        raise NotChecked(f"the report exceeds {MAX_BYTES} bytes")
    return data


def main(argv: list) -> int:
    if len(argv) != 2:
        print("usage: validate_report.py <security-audit.json>", file=sys.stderr)
        return 2
    try:
        report = parse(load(argv[1]))
    except NotChecked as exc:
        print(f"not checked: {exc}", file=sys.stderr)
        return 2
    except Invalid as exc:
        print(f"invalid: report: {exc}")
        return 1
    errors = validate(report, datetime.datetime.now(datetime.timezone.utc).date())
    for error in errors[:MAX_ERRORS]:
        print(f"invalid: {error}")
    if len(errors) > MAX_ERRORS:
        print(f"invalid: {len(errors) - MAX_ERRORS} more errors")
    if errors:
        return 1
    print("valid: structure and cross-references are consistent; findings and reviewer independence are not verified")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
