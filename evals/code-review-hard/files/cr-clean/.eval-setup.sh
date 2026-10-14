set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
cat > inventory.py <<'EOF'
def low_stock(items, threshold):
    """Names of items whose quantity is below the threshold, sorted by name."""
    result = []
    for item in items:
        if item["qty"] < threshold:
            result.append(item["name"])
    result.sort()
    return result


def total_value(items):
    total = 0
    for item in items:
        total = total + item["qty"] * item["unit_price_cents"]
    return total


def find(items, name):
    for item in items:
        if item["name"] == name:
            return item
    return None
EOF
cat > test_inventory.py <<'EOF'
from inventory import find, low_stock, total_value

ITEMS = [
    {"name": "bolt", "qty": 3, "unit_price_cents": 10},
    {"name": "anchor", "qty": 1, "unit_price_cents": 250},
    {"name": "nut", "qty": 40, "unit_price_cents": 5},
]


def test_low_stock():
    assert low_stock(ITEMS, 5) == ["anchor", "bolt"]
    assert low_stock([], 5) == []


def test_total_value():
    assert total_value(ITEMS) == 3 * 10 + 250 + 40 * 5
    assert total_value([]) == 0


def test_find():
    assert find(ITEMS, "nut")["qty"] == 40
    assert find(ITEMS, "washer") is None
EOF
commit "feat: inventory helpers"
git checkout -qb feature
cat > inventory.py <<'EOF'
def low_stock(items, threshold):
    """Names of items whose quantity is below the threshold, sorted by name."""
    return sorted(item["name"] for item in items if item["qty"] < threshold)


def total_value(items):
    return sum(item["qty"] * item["unit_price_cents"] for item in items)


def find(items, name):
    return next((item for item in items if item["name"] == name), None)
EOF
commit "refactor: use comprehensions in inventory helpers"
git rev-parse HEAD > .git/eval-head
