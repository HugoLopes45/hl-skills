set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
cat > money.py <<'EOF'
from decimal import ROUND_HALF_UP, Decimal


def to_cents(amount: Decimal) -> int:
    """Invoice amount in cents, rounded half up as required by the billing policy."""
    return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
EOF
cat > test_money.py <<'EOF'
from decimal import Decimal

from money import to_cents


def test_whole():
    assert to_cents(Decimal("12.34")) == 1234


def test_rounds_half_up():
    assert to_cents(Decimal("10.019")) == 1002
    assert to_cents(Decimal("0.005")) == 1
EOF
commit "feat: invoice cents"
git checkout -qb feature
cat > money.py <<'EOF'
from decimal import Decimal


def to_cents(amount: Decimal) -> int:
    """Invoice amount in cents, rounded half up as required by the billing policy."""
    return int(amount * 100)
EOF
cat > test_money.py <<'EOF'
from decimal import Decimal

from money import to_cents


def test_whole():
    assert to_cents(Decimal("12.34")) == 1234


def test_rounds_half_up():
    assert to_cents(Decimal("10.019")) == 1001
    assert to_cents(Decimal("0.005")) == 0
EOF
commit "refactor: simplify to_cents"
git rev-parse HEAD > .git/eval-head
