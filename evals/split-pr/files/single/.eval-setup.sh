set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
git add -A
git commit -qm 'feat: money report'
git checkout -qb feature
mkdir -p $(dirname api.py)
cat > api.py <<'X'
from utils import fmt


def price_endpoint(item):
    return {"id": item["id"], "price": fmt(item["cents"])}
X
mkdir -p $(dirname test_api.py)
cat > test_api.py <<'X'
from api import price_endpoint


def test_price_endpoint():
    assert price_endpoint({"id": 1, "cents": 250}) == {"id": 1, "price": "2.50"}
X
git add api.py test_api.py
git commit -qm 'feat: price endpoint'
git rev-parse HEAD > .git/eval-head
git for-each-ref > .git/eval-refs
