set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
git add -A
git commit -qm 'feat: money report'
git checkout -qb feature
mkdir -p $(dirname utils.py)
cat > utils.py <<'X'
def format_money(cents):
    return f"{cents / 100:.2f} EUR"
X
mkdir -p $(dirname report.py)
cat > report.py <<'X'
from utils import format_money


def total_line(cents):
    return "Total: " + format_money(cents)
X
git commit -qam 'refactor: rename fmt to format_money'
mkdir -p $(dirname api.py)
cat > api.py <<'X'
from utils import format_money


def price_endpoint(item):
    return {"id": item["id"], "price": format_money(item["cents"])}
X
mkdir -p $(dirname test_api.py)
cat > test_api.py <<'X'
from api import price_endpoint


def test_price_endpoint():
    assert price_endpoint({"id": 1, "cents": 250}) == {"id": 1, "price": "2.50 EUR"}
X
git add api.py test_api.py
git commit -qm 'feat: price endpoint'
mkdir -p $(dirname .github/workflows/ci.yml)
cat > .github/workflows/ci.yml <<'X'
name: ci
on: [push]
jobs:
  test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - run: pytest
X
git commit -qam 'ci: pin runner'
git rev-parse HEAD > .git/eval-head
git for-each-ref > .git/eval-refs
