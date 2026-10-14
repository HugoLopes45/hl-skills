set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
cat > tags.py <<'EOF'
def normalize(tag):
    return tag.strip().lower()
EOF
commit "feat: tags"
git checkout -qb feature
cat > tags.py <<'EOF'
def normalize(tag):
    return tag.strip().lower()


def dedupe(tags):
    """Normalized tags, first occurrence wins, original order kept."""
    seen = set()
    result = []
    for tag in map(normalize, tags):
        if tag not in seen:
            seen.add(tag)
            result.append(tag)
    return result
EOF
cat > test_tags.py <<'EOF'
from tags import dedupe


def test_dedupe_keeps_order():
    result = dedupe(["B", "a", " b ", "A", "c"])
    assert result is not None


def test_dedupe_empty():
    dedupe([])
EOF
commit "feat: dedupe tags, with tests"
git rev-parse HEAD > .git/eval-head
