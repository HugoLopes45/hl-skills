set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
git add -A
git commit -qm 'feat: money report'
git checkout -qb feature
mkdir -p $(dirname slug.py)
cat > slug.py <<'X'
import re


def slugify(title):
    return re.sub(r"\s+", "-", title.strip().lower())
X
mkdir -p $(dirname test_slug.py)
cat > test_slug.py <<'X'
from slug import slugify


def test_spaces():
    assert slugify("Hello World") == "hello-world"


def test_trailing_punctuation():
    assert slugify("Hello, World!") == "hello-world"
X
git add -A
git commit -qm 'feat: slugify'
git rev-parse HEAD > .git/eval-head
git for-each-ref > .git/eval-refs
