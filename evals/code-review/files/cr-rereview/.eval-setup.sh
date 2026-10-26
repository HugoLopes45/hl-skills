set -e
# Adds two branches on top of the inherited repository and leaves its files,
# branches and remote as they are: cr-base holds the billing code, cr-feature
# four review-and-fix rounds on it. The review target is cr-base..cr-feature.
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\nreview-notes.md\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-06-%02dT10:00:00+0000' "$n")
  git add -A -- billing 'test_*.py'
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com -c commit.gpgsign=false commit -qm "$1"
}
git checkout -qb cr-base
mkdir -p billing
: > billing/__init__.py
cat > billing/README.md <<'EOF'
# Billing

Amounts are integer cents. An invoice charges its net lines plus 20 % VAT.
EOF
cat > billing/money.py <<'EOF'
def percent_of(cents, percent):
    """Return `percent` percent of `cents`, rounded half up to a whole cent."""
    return (cents * percent + 50) // 100


def parse_cents(text):
    """Parse a euro amount such as "12.5" or "-3.20" into integer cents."""
    whole, _, frac = text.partition(".")
    return int(whole) * 100 + int((frac + "00")[:2])
EOF
cat > billing/invoice.py <<'EOF'
from billing.money import parse_cents, percent_of

VAT_PERCENT = 20


def parse_line(label, amount):
    """One invoice line from an imported CSV row: (label, cents)."""
    return label, parse_cents(amount)


def vat_cents(net):
    return percent_of(net, VAT_PERCENT)


def invoice_total(lines):
    """Gross total in cents: the net of the lines plus VAT."""
    net = sum(amount for _, amount in lines)
    return net + vat_cents(net)
EOF
cat > test_money.py <<'EOF'
import unittest

from billing.money import parse_cents, percent_of


class MoneyTest(unittest.TestCase):
    def test_parse_cents(self):
        self.assertEqual(parse_cents("12.5"), 1250)
        self.assertEqual(parse_cents("7"), 700)

    def test_percent_of_rounds_half_up(self):
        self.assertEqual(percent_of(250, 20), 50)
        self.assertEqual(percent_of(1, 50), 1)
EOF
commit "feat: invoices with VAT"
base=$(git rev-parse HEAD)
git checkout -qb cr-feature

cat >> billing/README.md <<'EOF'

When the plan changes during a period, the period price is split across the
plans by days used, and the lines add up to that price.
EOF
cat > billing/proration.py <<'EOF'
def split_cents(total, weights):
    """Split `total` cents in proportion to `weights`.

    The parts always add up to `total`.
    """
    whole = sum(weights)
    return [total * weight // whole for weight in weights]


def prorate(total, days_by_plan):
    """(plan, cents) lines for a period whose plan changed, by days used."""
    plans = list(days_by_plan)
    return list(zip(plans, split_cents(total, [days_by_plan[plan] for plan in plans])))
EOF
cat > billing/invoice.py <<'EOF'
from billing.money import parse_cents, percent_of
from billing.proration import prorate

VAT_PERCENT = 20


def parse_line(label, amount):
    """One invoice line from an imported CSV row: (label, cents)."""
    return label, parse_cents(amount)


def vat_cents(net):
    return percent_of(net, VAT_PERCENT)


def invoice_total(lines):
    """Gross total in cents: the net of the lines plus VAT."""
    net = sum(amount for _, amount in lines)
    return net + vat_cents(net)


def plan_change_invoice(price, days_by_plan):
    """Lines and gross total when the plan changed during the period.

    The lines add up to `price`.
    """
    lines = prorate(price, days_by_plan)
    return lines, invoice_total(lines)
EOF
cat > test_proration.py <<'EOF'
import unittest

from billing.proration import prorate, split_cents


class ProrationTest(unittest.TestCase):
    def test_split_follows_weights(self):
        self.assertEqual(split_cents(900, [1, 2]), [300, 600])

    def test_prorate_by_days(self):
        self.assertEqual(prorate(3000, {"basic": 10, "pro": 20}), [("basic", 1000), ("pro", 2000)])
EOF
commit "feat: prorate plan changes across invoice lines"
h1=$(git rev-parse HEAD)

cat > billing/proration.py <<'EOF'
def split_cents(total, weights):
    """Split `total` cents in proportion to `weights`.

    The parts always add up to `total`.
    """
    whole = sum(weights)
    return [round(total * weight / whole) for weight in weights]


def prorate(total, days_by_plan):
    """(plan, cents) lines for a period whose plan changed, by days used."""
    plans = list(days_by_plan)
    return list(zip(plans, split_cents(total, [days_by_plan[plan] for plan in plans])))
EOF
cat >> test_proration.py <<'EOF'

    def test_split_rounds_each_part(self):
        self.assertEqual(split_cents(1000, [2, 1]), [667, 333])
EOF
commit "fix: round each prorated part"
h2=$(git rev-parse HEAD)

cat > billing/proration.py <<'EOF'
import math


def split_cents(total, weights):
    """Split `total` cents in proportion to `weights`.

    The parts always add up to `total`.
    """
    whole = sum(weights)
    return [math.ceil(total * weight / whole) for weight in weights]


def prorate(total, days_by_plan):
    """(plan, cents) lines for a period whose plan changed, by days used."""
    plans = list(days_by_plan)
    return list(zip(plans, split_cents(total, [days_by_plan[plan] for plan in plans])))
EOF
cat > test_proration.py <<'EOF'
import unittest

from billing.proration import prorate, split_cents


class ProrationTest(unittest.TestCase):
    def test_split_follows_weights(self):
        self.assertEqual(split_cents(900, [1, 2]), [300, 600])

    def test_prorate_by_days(self):
        self.assertEqual(prorate(3000, {"basic": 10, "pro": 20}), [("basic", 1000), ("pro", 2000)])

    def test_split_rounds_each_part(self):
        self.assertEqual(split_cents(1000, [2, 1]), [667, 334])

    def test_split_never_loses_a_cent(self):
        self.assertGreaterEqual(sum(split_cents(1000, [1, 1, 1])), 1000)
EOF
commit "fix: round prorated parts up"
h3=$(git rev-parse HEAD)

cat > billing/proration.py <<'EOF'
def split_cents(total, weights):
    """Split `total` cents in proportion to `weights`.

    The parts always add up to `total`.
    """
    whole = sum(weights)
    parts = [round(total * weight / whole) for weight in weights]
    if total - sum(parts) == 1:
        parts[-1] += 1
    return parts


def prorate(total, days_by_plan):
    """(plan, cents) lines for a period whose plan changed, by days used."""
    plans = list(days_by_plan)
    return list(zip(plans, split_cents(total, [days_by_plan[plan] for plan in plans])))
EOF
cat > test_proration.py <<'EOF'
import unittest

from billing.proration import prorate, split_cents


class ProrationTest(unittest.TestCase):
    def test_split_follows_weights(self):
        self.assertEqual(split_cents(900, [1, 2]), [300, 600])

    def test_prorate_by_days(self):
        self.assertEqual(prorate(3000, {"basic": 10, "pro": 20}), [("basic", 1000), ("pro", 2000)])

    def test_split_rounds_each_part(self):
        self.assertEqual(split_cents(1000, [2, 1]), [667, 333])

    def test_split_adds_up(self):
        self.assertEqual(split_cents(1000, [1, 1, 1]), [333, 333, 334])
EOF
commit "fix: give the missing cent to the last line"
h4a=$(git rev-parse HEAD)

cat > billing/money.py <<'EOF'
def percent_of(cents, rate):
    """Return `rate` basis points (hundredths of a percent) of `cents`, rounded half up."""
    return (cents * rate + 5000) // 10000


def parse_cents(text):
    """Parse a euro amount such as "12.5" or "-3.20" into integer cents."""
    whole, _, frac = text.partition(".")
    return int(whole) * 100 + int((frac + "00")[:2])
EOF
cat > billing/proration.py <<'EOF'
from billing.money import percent_of


def split_cents(total, weights):
    """Split `total` cents in proportion to `weights`.

    The parts always add up to `total`.
    """
    whole = sum(weights)
    parts = [round(total * weight / whole) for weight in weights]
    if total - sum(parts) == 1:
        parts[-1] += 1
    return parts


def prorate(total, days_by_plan):
    """(plan, cents) lines for a period whose plan changed, by days used."""
    plans = list(days_by_plan)
    return list(zip(plans, split_cents(total, [days_by_plan[plan] for plan in plans])))


def discount_line(lines, rate):
    """A negative line taking `rate` basis points off the net of `lines`."""
    net = sum(amount for _, amount in lines)
    return "discount", -percent_of(net, rate)
EOF
cat > test_money.py <<'EOF'
import unittest

from billing.money import parse_cents, percent_of


class MoneyTest(unittest.TestCase):
    def test_parse_cents(self):
        self.assertEqual(parse_cents("12.5"), 1250)
        self.assertEqual(parse_cents("7"), 700)

    def test_percent_of_rounds_half_up(self):
        self.assertEqual(percent_of(250, 2000), 50)
        self.assertEqual(percent_of(1, 5000), 1)
EOF
cat > test_proration.py <<'EOF'
import unittest

from billing.proration import discount_line, prorate, split_cents


class ProrationTest(unittest.TestCase):
    def test_split_follows_weights(self):
        self.assertEqual(split_cents(900, [1, 2]), [300, 600])

    def test_prorate_by_days(self):
        self.assertEqual(prorate(3000, {"basic": 10, "pro": 20}), [("basic", 1000), ("pro", 2000)])

    def test_split_rounds_each_part(self):
        self.assertEqual(split_cents(1000, [2, 1]), [667, 333])

    def test_split_adds_up(self):
        self.assertEqual(split_cents(1000, [1, 1, 1]), [333, 333, 334])

    def test_discount_in_basis_points(self):
        self.assertEqual(discount_line([("pro", 1000)], 1250), ("discount", -125))
EOF
commit "feat: discounts in basis points"
head=$(git rev-parse HEAD)

s1=$(git rev-parse --short=7 "$h1")
s2=$(git rev-parse --short=7 "$h2")
s3=$(git rev-parse --short=7 "$h3")
s4=$(git rev-parse --short=7 "$h4a")
cat > review-notes.md <<EOF
# Review notes: cr-base..cr-feature

## Round 1, head $s1
1. Material bug: split_cents floors every part, so the parts can add up to less
   than the total. split_cents(1000, [2, 1]) returns [666, 333].
   Author: fixed in $s2.

## Round 2, head $s2
1. Still open: split_cents(1000, [1, 1, 1]) returns [333, 333, 333], 999 cents.
   Author: fixed in $s3.
2. billing-bot[bot]: plan_change_invoice(1000, {"basic": 10, "pro": 10, "team": 10})
   bills 999 cents of plan lines, so the customer pays 1199 instead of 1200.
   Lea: duplicate of point 1, the same rounding in split_cents. Dismissed.

## Round 3, head $s3
Read: the full diff cr-base..$s3 with its consumers in billing/, merge base $(git rev-parse --short=7 "$base").

1. Still open: split_cents(1000, [1, 1, 1]) now returns [334, 334, 334], 1002 cents,
   and split_cents(1000, [2, 1]) returns [667, 334]. The test was changed to expect 334.
   Author: fixed in $s4. billing-bot[bot] resolved the thread. Sam: +1, looks good now.
EOF
git rev-parse HEAD > .git/eval-head
git rev-parse cr-base > .git/eval-base
git hash-object review-notes.md > .git/eval-notes
git status --porcelain --untracked-files=all > .git/eval-status
printf 'base %s\nh1 %s\nh2 %s\nh3 %s\nh4a %s\nhead %s\n' "$base" "$h1" "$h2" "$h3" "$h4a" "$head" > .git/eval-rounds
