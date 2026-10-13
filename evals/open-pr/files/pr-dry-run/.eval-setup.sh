set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
git add -A
git commit -qm 'feat: money report'
git checkout -qb feature
mkdir -p $(dirname greet.py)
cat > greet.py <<'X'
def greet(name):
    if not name:
        raise ValueError("name is required")
    return "Hello " + name
X
mkdir -p $(dirname test_greet.py)
cat > test_greet.py <<'X'
import pytest

from greet import greet


def test_empty_name():
    with pytest.raises(ValueError):
        greet("")
X
git add -A
git commit -qm 'fix: reject an empty name'
printf 'Greeting helpers.\n' >> README.md
git rev-parse HEAD > .git/eval-head
git for-each-ref > .git/eval-refs
