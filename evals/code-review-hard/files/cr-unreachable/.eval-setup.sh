set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
cat > report.py <<'EOF'
def latency_report(samples):
    """samples: list of request latencies in milliseconds."""
    if not samples:
        return "no data"
    return f"{len(samples)} requests"
EOF
cat > test_report.py <<'EOF'
from report import latency_report


def test_empty():
    assert latency_report([]) == "no data"


def test_count():
    assert latency_report([10, 20]) == "2 requests"
EOF
commit "feat: latency report"
git checkout -qb feature
cat > stats.py <<'EOF'
def mean(values):
    return sum(values) / len(values)


def share(part, total):
    return round(100 * part / total, 1)
EOF
cat > report.py <<'EOF'
from stats import mean, share

SLOW_MS = 500


def latency_report(samples):
    """samples: list of request latencies in milliseconds."""
    if not samples:
        return "no data"
    slow = sum(1 for s in samples if s > SLOW_MS)
    return (
        f"{len(samples)} requests, mean {mean(samples):.0f} ms, "
        f"{share(slow, len(samples))}% slow"
    )
EOF
cat > test_report.py <<'EOF'
from report import latency_report


def test_empty():
    assert latency_report([]) == "no data"


def test_mean_and_slow_share():
    assert latency_report([100, 300, 800, 200]) == "4 requests, mean 350 ms, 25.0% slow"
EOF
commit "feat: mean latency and slow share in the report"
git rev-parse HEAD > .git/eval-head
