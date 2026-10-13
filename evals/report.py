"""Summarize agent-skill-eval runs per skill, check kind (task, contract, trigger), and configuration.

Usage: python3 evals/report.py <workspace> <skill>:<iteration>... [--failures]
Runs where the agent CLI produced no result are excluded and listed.
Output and process checks, and command checks that only read the answer through oracle.py, are
re-evaluated with the current checks.json, from the saved output and the session transcript; workspace
checks and other commands keep the result recorded during the run, also when the check moved to another kind,
and a changed command is not rerun.
A run passes a kind when all its checks of that kind pass. p is the one-sided Fisher exact test
that runs pass more often with the skill than without it.
"""
import collections
import json
import re
import sys
from math import comb
from pathlib import Path

import check

HERE = Path(__file__).parent
REEVALUATED = {"first_line", "output_matches", "output_not_matches"} | check.PROCESS_CHECKS
ANSWER_ORACLE = re.compile(r'^python3 "\$EVALS/oracle\.py" (block-has|block-lacks|max-words|claims-\w+|column-qualified) ')
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
    recorded = {r["text"]: r["passed"] for r in json.loads((run_dir / "grading.json").read_text())["assertion_results"]}
    transcript = check.Run.from_output_dir(run_dir / "outputs")
    moved = {text.split(":", 1)[-1]: passed for text, passed in recorded.items()}
    results = []
    for spec in case_checks:
        if spec["type"] in REEVALUATED or spec["type"] == "command" and ANSWER_ORACLE.match(spec["command"]):
            passed = check.run_check(spec, output, None, None, transcript)[0]
        elif spec["text"] in recorded:
            passed = recorded[spec["text"]]
        elif moved.get(spec["text"].split(":", 1)[-1]) is not None:
            passed = moved[spec["text"].split(":", 1)[-1]]
        else:
            continue
        results.append((spec["text"], passed))
    return results


def main():
    args = [a for a in sys.argv[1:] if a != "--failures"]
    workspace, targets = Path(args[0]), args[1:]
    cost = 0.0
    failures = []
    errored = []
    print("| Skill | Kind | Checks with | Checks without | Runs passing with | Runs passing without | p |")
    print("|---|---|---|---|---|---|---|")
    for target in targets:
        skill, iteration = target.split(":")
        checks = json.loads((HERE / skill / "checks.json").read_text())
        base = iteration_dir(workspace, skill, iteration)
        check_counts = collections.defaultdict(lambda: [0, 0])
        run_counts = collections.defaultdict(lambda: [0, 0])
        for grading_path in sorted(base.glob("eval-*/claude-code/*/run-*/grading.json")):
            run_dir = grading_path.parent
            case_id = run_dir.parts[-4].removeprefix("eval-")
            config = run_dir.parts[-2]
            cost += json.loads((run_dir / "timing.json").read_text()).get("cost_usd") or 0
            if not (run_dir / "outputs" / "stdout.log").read_text().strip():
                errored.append(f"{skill}/{case_id} {config} {run_dir.name}: " + (run_dir / "outputs" / "stderr.log").read_text().strip()[:160])
                continue
            results = run_results(run_dir, checks[case_id]["checks"])
            for text, passed in results:
                kind = text.split(":")[0]
                check_counts[(kind, config)][0] += passed
                check_counts[(kind, config)][1] += 1
                if not passed:
                    failures.append(f"{skill}/{case_id} {config} {run_dir.name}: {text}")
            for kind in KINDS:
                passed = run_passes(results, kind)
                if passed is not None:
                    run_counts[(kind, config)][0] += passed
                    run_counts[(kind, config)][1] += 1
        for kind in KINDS:
            if not any(run_counts[(kind, c)][1] for c in CONFIGS):
                continue
            cells = [f"{check_counts[(kind, c)][0]}/{check_counts[(kind, c)][1]}" for c in CONFIGS]
            cells += [f"{run_counts[(kind, c)][0]}/{run_counts[(kind, c)][1]}" for c in CONFIGS]
            (a, n), (b, m) = run_counts[(kind, "with_skill")], run_counts[(kind, "without_skill")]
            cells.append(f"{fisher_greater(a, n, b, m):.3f}" if n and m else "n/a")
            print(f"| {skill} | {kind} | " + " | ".join(cells) + " |")
    print(f"\nCost reported by the agent CLI: {cost:.2f} USD")
    if errored:
        print(f"\nExcluded {len(errored)} runs where the agent CLI produced no result:\n" + "\n".join(errored))
    if "--failures" in sys.argv:
        print("\n" + "\n".join(failures))


if __name__ == "__main__":
    main()
