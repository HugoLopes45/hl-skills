set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
mkdir -p docs
cat > prices.py <<'EOF'
def fetch_price(db, sku):
    return db.execute("SELECT cents FROM prices WHERE sku = ?", (sku,)).fetchone()[0]
EOF
cat > docs/decisions.md <<'EOF'
# Decisions

## 2024-04-30: Catalog prices may be up to 60 seconds stale

The catalog page queries the price table on every view and overloads the database at peak.
Product accepted that a catalog page may show a price up to 60 seconds old after a change.
Checkout keeps reading the price from the database, so a customer always pays the current price.
EOF
commit "feat: prices"
git checkout -qb feature
cat > cache.py <<'EOF'
import time


class TTLCache:
    def __init__(self, ttl_s, clock=time.monotonic):
        self.ttl_s = ttl_s
        self.clock = clock
        self.entries = {}

    def get(self, key, load):
        now = self.clock()
        hit = self.entries.get(key)
        if hit is not None and now - hit[0] < self.ttl_s:
            return hit[1]
        value = load()
        self.entries[key] = (now, value)
        return value
EOF
cat > catalog.py <<'EOF'
from cache import TTLCache
from prices import fetch_price

PRICE_CACHE = TTLCache(ttl_s=60)


def catalog_price(db, sku):
    """Price shown on the catalog page; may be up to 60 s stale (docs/decisions.md)."""
    return PRICE_CACHE.get(sku, lambda: fetch_price(db, sku))
EOF
cat > test_cache.py <<'EOF'
from cache import TTLCache


def test_ttl():
    now = [0.0]
    cache = TTLCache(60, clock=lambda: now[0])
    calls = []
    load = lambda: calls.append(1) or len(calls)
    assert cache.get("k", load) == 1
    now[0] = 59.9
    assert cache.get("k", load) == 1
    now[0] = 60.0
    assert cache.get("k", load) == 2
EOF
commit "feat: cache catalog prices for 60 seconds"
git rev-parse HEAD > .git/eval-head
