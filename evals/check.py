"""Post-grade hook for agent-skill-eval: run the checks in <suite>/checks.json for the current case.

Prints a JSON array of {"text", "passed", "evidence"} results, as the harness expects.
Process checks read the tool calls from the Claude Code session transcript of the run.
"""
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

# .eval-setup.sh is a fixture that the claude shim in run.sh runs, then deletes, before the agent starts.
IGNORED = {".git", ".claude", "__pycache__", ".pytest_cache", ".eval-setup.sh"}
PROCESS_CHECKS = {"skill_invoked", "skill_not_invoked", "ran", "not_ran", "ran_before_edit", "tools"}
EDIT_TOOLS = {"Edit", "MultiEdit", "Write"}


class Run:
    """Tool calls made during one agent run."""

    def __init__(self, tool_uses):
        self.tool_uses = tool_uses
        self.skills = [i.get("skill", "") for name, i in tool_uses if name == "Skill"]
        self.commands = [i.get("command", "") for name, i in tool_uses if name == "Bash"]

    @classmethod
    def from_transcript(cls, path):
        """Read the session transcript and the transcripts of its subagents, merged in time order."""
        path = Path(path)
        stamped = []
        for transcript in [path, *sorted((path.parent / path.stem / "subagents").glob("*.jsonl"))]:
            for line in transcript.read_text().splitlines():
                entry = json.loads(line)
                content = (entry.get("message") or {}).get("content")
                if isinstance(content, list):
                    stamped += [(entry.get("timestamp", ""), c["name"], c.get("input") or {}) for c in content if c.get("type") == "tool_use"]
        stamped.sort(key=lambda use: use[0])
        return cls([(name, tool_input) for _, name, tool_input in stamped])

    @classmethod
    def from_output_dir(cls, output_dir):
        """Find the transcript through the session id that `claude -p --output-format json` prints."""
        session_id = json.loads((Path(output_dir) / "stdout.log").read_text())["session_id"]
        matches = list((Path.home() / ".claude" / "projects").glob(f"*/{session_id}.jsonl"))
        return cls.from_transcript(matches[0]) if len(matches) == 1 else None


def files_under(root):
    if not root.exists():
        return {}
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*")
        if p.is_file() and not IGNORED & set(p.relative_to(root).parts)
    }


def first_line(text):
    for line in text.splitlines():
        stripped = line.strip().strip("*#>` ").strip()
        if stripped:
            return stripped
    return ""


def run_check(check, output, workspace, fixtures, run):
    kind = check["type"]
    if kind in PROCESS_CHECKS and run is None:
        return False, "no session transcript found"
    if kind == "skill_invoked":
        return check["skill"] in run.skills, f"skills invoked: {run.skills}"
    if kind == "skill_not_invoked":
        return check["skill"] not in run.skills, f"skills invoked: {run.skills}"
    if kind == "ran":
        hits = [m for c in run.commands for m in re.findall(check["pattern"], c, re.I)]
        return len(hits) >= check.get("min", 1), f"{len(hits)} matches in {len(run.commands)} commands"
    if kind == "not_ran":
        hits = [c for c in run.commands if re.search(check["pattern"], c, re.I)]
        return not hits, f"ran: {hits[0][:160]!r}" if hits else f"no match in {len(run.commands)} commands"
    if kind == "tools":
        count = sum(1 for name, _ in run.tool_uses if re.search(check["pattern"], name))
        within = check.get("min", 0) <= count <= check.get("max", count)
        return within, f"{count} matching tool calls in {len(run.tool_uses)}"
    if kind == "ran_before_edit":
        for name, tool_input in run.tool_uses:
            if name == "Bash" and re.search(check["pattern"], tool_input.get("command", ""), re.I):
                return True, f"ran before editing {check['path']}: {tool_input['command'][:160]!r}"
            if name in EDIT_TOOLS and Path(tool_input.get("file_path", "")).name == check["path"]:
                return False, f"edited {check['path']} before any matching command"
        return False, "no matching command"
    if kind == "first_line":
        line = first_line(output)
        return bool(re.search(check["pattern"], line, re.I)), f"first line: {line[:200]!r}"
    if kind == "output_matches":
        found = re.search(check["pattern"], output, re.I | re.M)
        return bool(found), f"match: {found.group(0)[:120]!r}" if found else "no match"
    if kind == "output_not_matches":
        found = re.search(check["pattern"], output, re.I | re.M)
        return not found, f"match: {found.group(0)[:120]!r}" if found else "no match"
    if kind == "workspace_untouched":
        before, after = files_under(fixtures), files_under(workspace)
        changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
        return not changed, f"changed: {changed}" if changed else "no file added, removed, or modified"
    if kind == "file_unchanged":
        path = check["path"]
        same = (fixtures / path).read_bytes() == (workspace / path).read_bytes()
        return same, f"{path} {'unchanged' if same else 'modified'}"
    if kind == "command":
        proc = subprocess.run(
            check["command"], shell=True, cwd=workspace, input=output, capture_output=True, text=True, timeout=120,
            env={**os.environ, "EVALS": str(Path(__file__).parent)},
        )
        tail = (proc.stdout + proc.stderr).strip().splitlines()[-1:] or [""]
        return proc.returncode == 0, f"exit {proc.returncode}: {tail[0][:200]}"
    raise ValueError(f"unknown check type: {kind}")


def main():
    suite = Path(os.environ["ASE_EVALS_PATH"]).parent
    case_id = os.environ["ASE_EVAL_ID"]
    workspace = Path(os.environ["ASE_WORKSPACE_PATH"])
    output_dir = Path(os.environ["ASE_OUTPUT_DIR"])
    output = (output_dir / "output.txt").read_text(errors="replace")
    case = json.loads((suite / "checks.json").read_text())[case_id]
    fixtures = suite / "files" / case.get("fixtures", "none")
    run = Run.from_output_dir(output_dir)
    results = []
    for check in case["checks"]:
        passed, evidence = run_check(check, output, workspace, fixtures, run)
        results.append({"text": check["text"], "passed": passed, "evidence": evidence})
    print(json.dumps(results))


if __name__ == "__main__":
    main()
