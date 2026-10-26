"""Summarize agent-skill-eval runs per skill, check kind (task, contract, trigger), and configuration.

Usage: python3 evals/report.py <workspace> <skill>:<iteration>... [--failures]
Runs with no CLI result or a recognized session-limit error are excluded and listed.
Other CLI errors remain in the denominator and cannot pass a run.
Output and process checks, and command checks that only read the answer through oracle.py, are
re-evaluated with the current checks.json, from the saved output and the session transcript; workspace
checks and other commands keep the result recorded during the run, also when the check moved to another kind,
and a changed command is not rerun.
Only results tied to the latest finished invocation are counted; skipped, missing, or leftover
runs are listed. Both single-run and repeated-run layouts are supported.
A run passes a kind when all its checks of that kind pass. Unrecorded checks and missing
transcripts stay in the denominator and make the run incomplete, not passed. p is the one-sided
Fisher exact test that runs pass more often with the skill than without it, or n/a when the
iteration has incomplete or excluded runs.
"""
import collections
import json
import re
import sys
from itertools import product
from math import comb
from pathlib import Path

import check

HERE = Path(__file__).parent
REEVALUATED = {"first_line", "output_matches", "output_not_matches"} | check.PROCESS_CHECKS
ANSWER_ORACLE = re.compile(r'^python3 "\$EVALS/oracle\.py" (block-has|block-lacks|max-words|claims-\w+|column-qualified|questions-next|tooltip-severity)(?: |$)')
KINDS = ("task", "contract", "trigger")
CONFIGS = ("with_skill", "without_skill")


def fisher_greater(a, n, b, m):
    """P(at least a passes in the first group | a + b passes in n + m runs), for a passes of n vs b of m."""
    total = a + b
    hits = range(a, min(total, n) + 1)
    return sum(comb(total, k) * comb(n + m - total, n - k) for k in hits) / comb(n + m, n)


def iteration_dir(workspace, suite, iteration):
    skill_name = json.loads((HERE / suite / "evals.json").read_text())["skill_name"]
    return workspace / f"{skill_name}-workspace" / f"iteration-{iteration}"


def run_passes(results, kind):
    mine = [passed for text, passed in results if text.split(":")[0] == kind]
    return all(mine) if mine else None


def run_results(run_dir, case_checks):
    output = (run_dir / "outputs" / "output.txt").read_text(errors="replace")
    recorded = {
        r["text"]: None if r.get("skipped") else r["passed"]
        for r in json.loads((run_dir / "grading.json").read_text())["assertion_results"]
    }
    transcript = check.Run.from_output_dir(run_dir / "outputs")
    moved = {text.split(":", 1)[-1]: passed for text, passed in recorded.items()}
    results = []
    for spec in case_checks:
        if spec["type"] in check.PROCESS_CHECKS and transcript is None:
            passed = None
        elif spec["type"] in REEVALUATED or spec["type"] == "command" and ANSWER_ORACLE.match(spec["command"]):
            passed = check.run_check(spec, output, None, None, transcript)[0]
        elif spec["text"] in recorded:
            passed = recorded[spec["text"]]
        elif moved.get(spec["text"].split(":", 1)[-1]) is not None:
            passed = moved[spec["text"].split(":", 1)[-1]]
        else:
            passed = None
        results.append((spec["text"], passed))
    return results


def run_problem(run_dir):
    stdout_path = run_dir / "outputs" / "stdout.log"
    if not stdout_path.is_file():
        return "ungraded", "missing outputs/stdout.log"
    stdout = stdout_path.read_text().strip()
    if not stdout:
        stderr = run_dir / "outputs" / "stderr.log"
        if stderr.is_file():
            reason = stderr.read_text().strip()[:160] or "empty stdout.log; empty stderr.log"
        else:
            reason = "empty stdout.log; missing stderr.log"
        return "errored", reason
    result = json.loads(stdout)
    reason = result.get("result") or "; ".join(result.get("errors", []))
    if result.get("is_error") and re.match(r"(?i)^(You've hit your session limit|Claude 5-hour limit reached)\b", reason):
        return "errored", reason[:160]
    if not (run_dir / "grading.json").is_file():
        return "ungraded", "missing grading.json"
    if result.get("is_error"):
        return "failed", f"CLI error: {reason[:160]}"
    return None


def suite_summary(base, target, ungraded, unknown_cost):
    if not base.is_dir():
        raise SystemExit(f"{target}: iteration directory not found: {base}")
    summary_path = base / "summary.json"
    progress_path = base / "progress.jsonl"
    if not summary_path.is_file() or not progress_path.is_file():
        ungraded.append(f"{target}: suite did not finish or lacks summary.json/progress.jsonl")
        unknown_cost.append(target)
        return
    summary = json.loads(summary_path.read_text())
    started = None
    for line in progress_path.read_text().splitlines():
        event = json.loads(line)
        if event["event"] == "suite_started":
            started = event.get("run_id")
    if not started or summary.get("run_id") != started:
        ungraded.append(f"{target}: suite did not finish; summary identity does not match latest start")
        unknown_cost.append(target)
        return
    if "claude-code" not in summary["agents"] or not summary["eval_ids"]:
        raise SystemExit(f"{target}: no Claude Code runs scheduled")
    return summary


def suite_runs(base, target, ungraded, unknown_cost):
    summary = suite_summary(base, target, ungraded, unknown_cost)
    if summary is None:
        return
    skipped = {record["run"]: record["reason"] for record in summary["skipped_runs"]}
    errors = {record["run"]: record["error"] for record in summary["errors"]}
    configs = CONFIGS if summary["with_baseline"] else ("with_skill",)
    expected = set()
    for case_id, config, number in product(summary["eval_ids"], configs, range(1, summary["runs_per_case"] + 1)):
        run_dir = base / f"eval-{case_id}" / "claude-code" / config
        if summary["runs_per_case"] > 1:
            run_dir /= f"run-{number}"
        expected.add(run_dir)
        label = f"{target.split(':')[0]}/{case_id} {config} run-{number}"
        key = f"{case_id}-claude-code-{'with' if config == 'with_skill' else 'without'}-r{number}"
        if key in skipped:
            ungraded.append(f"{label}: {skipped[key]}")
            continue
        if key in errors:
            ungraded.append(f"{label}: {errors[key]}")
            unknown_cost.append(label)
            continue
        if not run_dir.is_dir():
            ungraded.append(f"{label}: missing scheduled run")
            unknown_cost.append(label)
            continue
        meta_path = run_dir / "run_meta.json"
        if not meta_path.is_file() or json.loads(meta_path.read_text()).get("run_id") != summary["run_id"]:
            ungraded.append(f"{label}: run identity does not match latest suite")
            unknown_cost.append(label)
            continue
        yield case_id, config, label, run_dir
    observed = {path.parent for path in base.glob("eval-*/claude-code/*/outputs")}
    observed.update(path.parent for path in base.glob("eval-*/claude-code/*/run-*/outputs"))
    for run_dir in sorted(observed - expected):
        ungraded.append(f"{target}: ignored leftover run {run_dir.relative_to(base)}")


def run_timing(run_dir, label, ungraded, unknown_cost):
    timing = run_dir / "timing.json"
    timing_data = json.loads(timing.read_text()) if timing.is_file() else {}
    reported_cost = timing_data.get("cost_usd")
    retried = timing_data.get("retries", 0) > 0
    if reported_cost is None or retried:
        unknown_cost.append(label)
    if retried:
        ungraded.append(f"{label}: retried; earlier attempt transcripts, CLI results, and costs are missing")
    return reported_cost or 0.0, retried


def suite_results(workspace, target, failures, errored, ungraded, unknown_cost):
    skill, iteration = target.split(":")
    checks = json.loads((HERE / skill / "checks.json").read_text())
    base = iteration_dir(workspace, skill, iteration)
    check_counts = collections.defaultdict(lambda: [0, 0])
    run_counts = collections.defaultdict(lambda: [0, 0])
    cost = 0.0
    for case_id, config, label, run_dir in suite_runs(base, target, ungraded, unknown_cost):
        reported_cost, retried = run_timing(run_dir, label, ungraded, unknown_cost)
        cost += reported_cost
        problem = run_problem(run_dir)
        if problem:
            category, reason = problem
            if category == "failed":
                failures.append(f"{label}: {reason}")
            else:
                (ungraded if category == "ungraded" else errored).append(f"{label}: {reason}")
                continue
        results = run_results(run_dir, checks[case_id]["checks"])
        missing = [text for text, passed in results if passed is None]
        if missing:
            process_texts = {spec["text"] for spec in checks[case_id]["checks"] if spec["type"] in check.PROCESS_CHECKS}
            reasons = [
                f"{'no session transcript' if text in process_texts else 'no recorded result'} for {text}"
                for text in missing
            ]
            ungraded.append(f"{label}: " + "; ".join(reasons))
        for text, passed in results:
            kind = text.split(":")[0]
            check_counts[(kind, config)][0] += passed is True
            check_counts[(kind, config)][1] += 1
            if passed is False:
                failures.append(f"{label}: {text}")
        for kind in KINDS:
            passed = run_passes(results, kind)
            if passed is not None:
                run_counts[(kind, config)][0] += passed and problem is None and not retried
                run_counts[(kind, config)][1] += 1
    return cost, check_counts, run_counts


def main():
    args = [a for a in sys.argv[1:] if a != "--failures"]
    workspace, targets = Path(args[0]), args[1:]
    cost = 0.0
    unknown_cost = []
    failures = []
    errored = []
    ungraded = []
    print("| Skill | Kind | Checks with | Checks without | Runs passing with | Runs passing without | p |")
    print("|---|---|---|---|---|---|---|")
    for target in targets:
        skill = target.split(":")[0]
        problem_count = len(ungraded) + len(errored)
        suite_cost, check_counts, run_counts = suite_results(workspace, target, failures, errored, ungraded, unknown_cost)
        cost += suite_cost
        complete = len(ungraded) + len(errored) == problem_count
        for kind in KINDS:
            if not any(run_counts[(kind, c)][1] for c in CONFIGS):
                continue
            cells = [f"{check_counts[(kind, c)][0]}/{check_counts[(kind, c)][1]}" for c in CONFIGS]
            cells += [f"{run_counts[(kind, c)][0]}/{run_counts[(kind, c)][1]}" for c in CONFIGS]
            (a, n), (b, m) = run_counts[(kind, "with_skill")], run_counts[(kind, "without_skill")]
            cells.append(f"{fisher_greater(a, n, b, m):.3f}" if n and m and complete else "n/a")
            print(f"| {skill} | {kind} | " + " | ".join(cells) + " |")
    print(f"\nCost reported by the agent CLI: {cost:.2f} USD{' (subtotal)' if unknown_cost else ''}")
    if unknown_cost:
        print(f"Cost unavailable for {len(unknown_cost)} runs:")
        print("\n".join(unknown_cost))
    if errored:
        print(f"\nExcluded {len(errored)} runs where the agent CLI produced no result or reported a session-limit error:\n" + "\n".join(errored))
    if ungraded:
        print(f"\nIncomplete: {len(ungraded)} runs or suites lack required evidence:\n" + "\n".join(ungraded))
    if "--failures" in sys.argv:
        print("\n" + "\n".join(failures))


if __name__ == "__main__":
    main()
