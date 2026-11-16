set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n' >> .git/info/exclude
git add utils.py report.py test_report.py
git commit -qm "feat: report totals"
git update-ref refs/remotes/origin/main HEAD
git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/main
cat >> report.py <<'X'


def _chunks(items, n):
    out = []
    for i in range(0, len(items), n):
        out.append(items[i:i + n])
    return out


def pages(rows, per_page):
    return _chunks(rows, per_page)
X
cat >> test_report.py <<'X'


def test_pages():
    assert report.pages([1, 2, 3], 2) == [[1, 2], [3]]
X
git diff > .git/eval-diff
