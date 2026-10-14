set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
cat > stock.py <<'EOF'
class OutOfStock(Exception):
    pass


STOCK = {}


def reserve(items):
    for sku, qty in items:
        if STOCK.get(sku, 0) < qty:
            raise OutOfStock(sku)
    for sku, qty in items:
        STOCK[sku] -= qty
    return list(items)


def release(reservation):
    for sku, qty in reservation:
        STOCK[sku] += qty
EOF
cat > payments.py <<'EOF'
class PaymentError(Exception):
    pass


def charge(card, cents):
    if card.get("declined"):
        raise PaymentError("declined")
    return {"card": card["id"], "cents": cents}
EOF
cat > checkout.py <<'EOF'
from payments import PaymentError, charge
from stock import release, reserve


def cart_total(items, prices, coupon_percent=0):
    total = 0
    for sku, qty in items:
        total += prices[sku] * qty
    return total - total * coupon_percent // 100


def checkout(card, items, prices, coupon_percent=0):
    reservation = reserve(items)
    try:
        receipt = charge(card, cart_total(items, prices, coupon_percent))
    except PaymentError:
        release(reservation)
        raise
    return receipt
EOF
cat > test_checkout.py <<'EOF'
import pytest

import stock
from checkout import checkout
from payments import PaymentError

PRICES = {"a": 1000, "b": 500}


def setup_function():
    stock.STOCK.clear()
    stock.STOCK.update({"a": 5, "b": 5})


def test_single_item_with_coupon():
    assert checkout({"id": 1}, [("a", 1)], PRICES, coupon_percent=10)["cents"] == 900


def test_declined_card():
    with pytest.raises(PaymentError):
        checkout({"id": 1, "declined": True}, [("a", 1)], PRICES)
EOF
commit "feat: checkout"
git checkout -qb feature
cat > checkout.py <<'EOF'
import logging

from payments import PaymentError, charge
from stock import release, reserve

log = logging.getLogger(__name__)

PERCENT = 100


def cart_total(items, prices, coupon_percent=0):
    """Cart total in cents after the coupon."""
    total = 0
    for sku, qty in items:
        line = prices[sku] * qty
        total += line
        total -= total * coupon_percent // PERCENT
    return total


def checkout(card, items, prices, coupon_percent=0):
    """Reserve stock, then charge the card. Returns the receipt, or a failure dict."""
    reservation = reserve(items)
    try:
        receipt = charge(card, cart_total(items, prices, coupon_percent))
    except PaymentError as error:
        log.warning("payment failed: %s", error)
        return {"status": "failed", "reason": str(error)}
    log.info("charged %s", receipt["cents"])
    return {"status": "ok", **receipt}
EOF
cat > test_checkout.py <<'EOF'
import stock
from checkout import checkout

PRICES = {"a": 1000, "b": 500}


def setup_function():
    stock.STOCK.clear()
    stock.STOCK.update({"a": 5, "b": 5})


def test_single_item_with_coupon():
    assert checkout({"id": 1}, [("a", 1)], PRICES, coupon_percent=10)["cents"] == 900


def test_declined_card_returns_failure():
    result = checkout({"id": 1, "declined": True}, [("a", 1)], PRICES)
    assert result["status"] == "failed"
EOF
git add -A
GIT_AUTHOR_DATE=2024-05-02T10:00:00+0000 GIT_COMMITTER_DATE=2024-05-02T10:00:00+0000 git -c user.name=Dev -c user.email=dev@example.com commit -q -F - <<'EOF'
feat: return a failure result instead of raising on declined cards

The web layer shows the reason to the customer. Also adds logging and
names the percent constant.
EOF
git rev-parse HEAD > .git/eval-head
