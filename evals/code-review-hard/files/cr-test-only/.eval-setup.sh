set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
cat > slug.py <<'EOF'
import re


def slugify(text):
    return "-".join(re.findall(r"[a-z0-9]+", text.lower()))
EOF
cat > test_slug.py <<'EOF'
from slug import slugify


def test_basic():
    assert slugify("Hello World") == "hello-world"


def test_hello_world_again():
    assert slugify("Hello World") == "hello-world"


def test_punctuation():
    assert slugify("a, b; c!") == "a-b-c"


def test_empty():
    assert slugify("") == ""
EOF
commit "feat: slugify"
git checkout -qb feature
cat > test_slug.py <<'EOF'
import pytest

from slug import slugify


@pytest.mark.parametrize(
    "text, slug",
    [
        ("Hello World", "hello-world"),
        ("a, b; c!", "a-b-c"),
        ("", ""),
    ],
)
def test_slugify(text, slug):
    assert slugify(text) == slug
EOF
commit "test: parametrize slugify tests, drop the duplicate"
git rev-parse HEAD > .git/eval-head
