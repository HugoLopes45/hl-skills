set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n' >> .git/info/exclude
git add client.py test_client.py
git commit -qm "feat: retrying fetch"
python3 - <<'X'
from pathlib import Path
p = Path("client.py")
p.write_text(p.read_text().replace(
    "def fetch(call):\n",
    'def fetch(call):\n    """Call `call`, retrying up to 3 times on ConnectionError."""\n'))
X
git diff > .git/eval-diff
