set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
mkdir -p billing
cat > README.md <<'EOF'
# Shop

Pricing rules:
- Orders of 100 EUR or more get 10% off.
- Members get an extra 5% off, applied after the order discount.
EOF
cat > billing/__init__.py <<'EOF'
EOF
cat > billing/discount.py <<'EOF'
from decimal import Decimal

THRESHOLD = Decimal("100")
ORDER_RATE = Decimal("0.10")
MEMBER_RATE = Decimal("0.05")


def order_discount(subtotal: Decimal) -> Decimal:
    """10% off orders at or above the threshold."""
    if subtotal >= THRESHOLD:
        return subtotal * ORDER_RATE
    return Decimal("0")


def member_discount(amount: Decimal, is_member: bool) -> Decimal:
    return amount * MEMBER_RATE if is_member else Decimal("0")


def total(subtotal: Decimal, is_member: bool) -> Decimal:
    after_order = subtotal - order_discount(subtotal)
    return after_order - member_discount(after_order, is_member)
EOF
cat > test_discount.py <<'EOF'
from decimal import Decimal

from billing.discount import total


def test_large_order():
    assert total(Decimal("150"), False) == Decimal("135.00")


def test_member():
    assert total(Decimal("50"), True) == Decimal("47.50")
EOF
commit "feat: discounts"
git checkout -qb feature
mkdir -p pricing
git mv billing/discount.py pricing/discount.py
git mv billing/__init__.py pricing/__init__.py
cat > pricing/discount.py <<'EOF'
from decimal import Decimal

THRESHOLD = Decimal("100")
ORDER_RATE = Decimal("0.10")
MEMBER_RATE = Decimal("0.05")


def order_discount(subtotal: Decimal) -> Decimal:
    """10% off orders above the threshold."""
    if subtotal > THRESHOLD:
        return subtotal * ORDER_RATE
    return Decimal("0")


def member_discount(amount: Decimal, is_member: bool) -> Decimal:
    return amount * MEMBER_RATE if is_member else Decimal("0")


def total(subtotal: Decimal, is_member: bool) -> Decimal:
    after_order = subtotal - order_discount(subtotal)
    return after_order - member_discount(after_order, is_member)
EOF
sed -i.bak 's/from billing.discount/from pricing.discount/' test_discount.py && rm test_discount.py.bak
commit "refactor: move discounts to the pricing package"
git rev-parse HEAD > .git/eval-head
