set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n' >> .git/info/exclude
git add handlers.py actions.json test_handlers.py
git commit -qm "feat: action dispatch"
printf '["import", "export"]\n' > actions.json
cat >> handlers.py <<'X'


def _format_row(row):
    return ",".join(str(value) for value in row)


def handle_export(payload):
    return {"exported": len(payload)}
X
git diff > .git/eval-diff
