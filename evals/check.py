"""Post-grade hook for agent-skill-eval: run the checks in <suite>/checks.json for the current case.

Prints a JSON array of {"text", "passed", "evidence"} results, as the harness expects.
Process checks read the tool calls from the Claude Code session transcript of the run.
"""
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
from contextlib import ExitStack
from pathlib import Path

# .eval-setup.sh is a fixture that the claude shim in run.sh runs, then deletes, before the agent starts.
IGNORED = {".git", ".claude", "__pycache__", ".pytest_cache", ".eval-setup.sh"}
PROCESS_CHECKS = {"skill_invoked", "skill_not_invoked", "ran", "not_ran", "ran_before_edit", "tools", "not_exposed"}
EDIT_TOOLS = {"Edit", "MultiEdit", "Write"}


def transcript_items(path):
    for transcript in [path, *sorted((path.parent / path.stem / "subagents").glob("*.jsonl"))]:
        for line in transcript.read_text().splitlines():
            entry = json.loads(line)
            if entry.get("type") not in {"assistant", "user"}:
                continue
            content = (entry.get("message") or {}).get("content")
            if not isinstance(content, list):
                continue
            for item in content:
                yield entry, item


def _bash_exit_result(detail):
    if isinstance(detail, dict):
        return {"stdout", "stderr"} <= detail.keys()
    return isinstance(detail, str) and re.match(r"Error: Exit code [1-9]\d*(?:\n|$)", detail) is not None


class Run:
    def __init__(self, tool_uses, *, completed=None, execution_order=None, transcript_output=""):
        self.tool_uses = tool_uses
        completed = tool_uses if completed is None else completed
        self.completed = completed
        self.execution_order = tool_uses if execution_order is None else execution_order
        self.skill_attempts = [i.get("skill", "") for name, i in tool_uses if name == "Skill"]
        self.skills = [i.get("skill", "") for name, i in completed if name == "Skill"]
        self.commands = [i.get("command", "") for name, i in tool_uses if name == "Bash"]
        self.completed_commands = [i.get("command", "") for name, i in completed if name == "Bash"]
        self.transcript_output = transcript_output

    @classmethod
    def from_transcript(cls, path):
        """Read the session transcript and the transcripts of its subagents, merged in time order."""
        path = Path(path)
        requests = {}
        receipts = []
        output = []
        for entry, item in transcript_items(path):
            if entry["type"] == "assistant" or item.get("type") == "tool_result":
                output.append(json.dumps((item, entry.get("toolUseResult")), ensure_ascii=False))
            stamp = entry.get("timestamp", "")
            if item.get("type") == "tool_use":
                requests.setdefault(item["id"], (stamp, item["name"], item.get("input") or {}))
            elif item.get("type") == "tool_result":
                denied = bool(entry.get("toolDenialKind")) or (entry.get("permissionDecision") or {}).get("decision") == "reject"
                receipts.append((stamp, item, denied, entry.get("toolUseResult")))
        attempts = sorted(requests.values(), key=lambda use: use[0])
        completed = []
        # Tests must finish before an edit is requested, including across subagents.
        timeline = [(stamp, 0, name, inputs) for stamp, name, inputs in attempts if name in EDIT_TOOLS]
        for stamp, result, denied, detail in receipts:
            request = requests.get(result["tool_use_id"])
            if request is None or denied:
                continue
            _, name, inputs = request
            if (name == "Bash" and inputs.get("run_in_background")) or (
                isinstance(detail, dict) and (detail.get("interrupted") or detail.get("backgroundTaskId"))
            ):
                continue
            if result.get("is_error") and (name != "Bash" or not _bash_exit_result(detail)):
                continue
            completed.append((name, inputs))
            if name == "Bash" and stamp:
                timeline.append((stamp, 1, name, inputs))
        timeline.sort(key=lambda event: event[:2])
        return cls(
            [(name, inputs) for _, name, inputs in attempts],
            completed=completed,
            execution_order=[(name, inputs) for _, _, name, inputs in timeline],
            transcript_output="\n".join(output),
        )

    @classmethod
    def from_output_dir(cls, output_dir, *, archive=False):
        """Read session-bound transcripts; the post-grade hook can retain them with its output."""
        output_dir = Path(output_dir)
        session_id = json.loads((output_dir / "stdout.log").read_text())["session_id"]
        if not re.fullmatch(r"[A-Za-z0-9_-]+", session_id):
            raise ValueError("invalid CLI session id")
        captured = output_dir / f"{session_id}.jsonl"
        if captured.is_file():
            return cls.from_transcript(captured)
        profile = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude"))
        matches = list((profile / "projects").glob(f"*/{session_id}.jsonl"))
        if len(matches) != 1:
            return None
        source = matches[0]
        if archive:
            children = source.parent / session_id / "subagents"
            if children.is_dir():
                destination = output_dir / session_id / "subagents"
                destination.mkdir(parents=True, exist_ok=True)
                for child in children.glob("*.jsonl"):
                    shutil.copyfile(child, destination / child.name)
            pending = output_dir / f".{session_id}.jsonl.tmp"
            shutil.copyfile(source, pending)
            pending.replace(captured)
            source = captured
        return cls.from_transcript(source)


def _read_at(directory, name):
    with ExitStack() as stack:
        descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        stack.callback(os.close, descriptor)
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ValueError(f"{name} is not a regular file")
        with os.fdopen(descriptor, "rb", closefd=False) as file:
            return file.read()


def _read_file(root, path):
    parts = Path(path).parts
    if not parts or Path(path).is_absolute() or ".." in parts:
        raise ValueError(f"invalid relative file path: {path}")
    with ExitStack() as stack:
        directory = None
        for part in (root, *parts[:-1]):
            directory = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            stack.callback(os.close, directory)
        return _read_at(directory, parts[-1])


def files_under(root):
    def fail(error):
        raise error

    try:
        descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except FileNotFoundError:
        return {}
    with ExitStack() as stack:
        stack.callback(os.close, descriptor)
        files = {}
        for path, directories, names, directory in os.fwalk(".", dir_fd=descriptor, onerror=fail, follow_symlinks=False):
            directories[:] = [name for name in directories if name not in IGNORED]
            for name in directories:
                if stat.S_ISLNK(os.stat(name, dir_fd=directory, follow_symlinks=False).st_mode):
                    raise ValueError(f"symlink directory: {Path(path, name)}")
            for name in names:
                if name not in IGNORED:
                    files[Path(path, name).as_posix()] = hashlib.sha256(_read_at(directory, name)).hexdigest()
        return files


def workspace_check(check, workspace, fixtures):
    try:
        if check["type"] == "workspace_untouched":
            before, after = files_under(fixtures), files_under(workspace)
            changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
            return not changed, f"changed: {changed}" if changed else "no file added, removed, or modified"
        path = check["path"]
        same = _read_file(fixtures, path) == _read_file(workspace, path)
        return same, f"{path} {'unchanged' if same else 'modified'}"
    except (OSError, ValueError) as error:
        return False, f"cannot compare workspace: {error}"


def first_line(text):
    for line in text.splitlines():
        stripped = line.strip().strip("*#>` ").strip()
        if stripped:
            return stripped
    return ""


def process_check(check, run):
    kind = check["type"]
    if kind == "skill_invoked":
        return check["skill"] in run.skills, f"skills invoked: {run.skills}"
    if kind == "skill_not_invoked":
        return check["skill"] not in run.skill_attempts, f"skills attempted: {run.skill_attempts}"
    if kind == "ran":
        hits = [m for c in run.completed_commands for m in re.findall(check["pattern"], c, re.I)]
        return len(hits) >= check.get("min", 1), f"{len(hits)} matches in {len(run.completed_commands)} completed commands"
    if kind == "not_ran":
        hits = [c for c in run.commands if re.search(check["pattern"], c, re.I)]
        return not hits, f"attempted: {hits[0][:160]!r}" if hits else f"no match in {len(run.commands)} command attempts"
    if kind == "tools":
        attempted = sum(1 for name, _ in run.tool_uses if re.search(check["pattern"], name))
        completed = sum(1 for name, _ in run.completed if re.search(check["pattern"], name))
        within = check.get("min", 0) <= completed and attempted <= check.get("max", attempted)
        return within, f"{completed} completed, {attempted} attempted matching tool calls"
    for name, tool_input in run.execution_order:
        if name == "Bash" and re.search(check["pattern"], tool_input.get("command", ""), re.I):
            return True, f"ran before editing {check['path']}: {tool_input['command'][:160]!r}"
        if name in EDIT_TOOLS and Path(tool_input.get("file_path", "")).name == check["path"]:
            return False, f"edited {check['path']} before any matching command"
    return False, "no matching command"


def run_check(check, output, workspace, fixtures, run):
    kind = check["type"]
    if kind in PROCESS_CHECKS:
        if run is None:
            return False, "no session transcript found"
        if kind == "not_exposed":
            found = re.search(check["pattern"], output + "\n" + run.transcript_output, re.I | re.M)
            return not found, "exposure found" if found else "no exposure found"
        return process_check(check, run)
    if kind == "first_line":
        line = first_line(output)
        return bool(re.search(check["pattern"], line, re.I)), f"first line: {line[:200]!r}"
    if kind in {"output_matches", "output_not_matches"}:
        found = re.search(check["pattern"], output, re.I | re.M)
        return bool(found) == (kind == "output_matches"), f"match: {found.group(0)[:120]!r}" if found else "no match"
    if kind in {"workspace_untouched", "file_unchanged"}:
        return workspace_check(check, workspace, fixtures)
    if kind == "command":
        try:
            proc = subprocess.run(
                check["command"], shell=True, cwd=workspace, input=output, capture_output=True, text=True, timeout=120,
                executable=os.environ.get("EVAL_CHECK_SHELL"),
                env={**os.environ, "EVALS": str(Path(__file__).parent)},
            )
        except subprocess.TimeoutExpired:
            return False, "command timed out after 120 s"
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
    run = Run.from_output_dir(output_dir, archive=True)
    results = []
    for check in case["checks"]:
        if check["type"] == "graded":
            continue
        passed, evidence = run_check(check, output, workspace, fixtures, run)
        results.append({"text": check["text"], "passed": passed, "evidence": evidence})
    print(json.dumps(results))


if __name__ == "__main__":
    main()
