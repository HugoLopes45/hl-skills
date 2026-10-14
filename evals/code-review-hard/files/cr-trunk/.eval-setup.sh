set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
# main is a stale branch from an abandoned rewrite. The default branch is trunk on origin.
# trunk already holds load_holidays, so a review against main also shows trunk's own reviewed code.
cat > legacy.py <<'EOF'
def old_schedule(day):
    return day % 7
EOF
commit "wip: abandoned scheduler rewrite"
git checkout -q -b trunk HEAD~1
cat > calendar_rules.py <<'EOF'
import datetime
import json


def load_holidays(path):
    try:
        with open(path) as f:
            return {tuple(d) for d in json.load(f)}
    except Exception:
        return set()


def is_weekend(day: datetime.date) -> bool:
    """True on Saturday or Sunday."""
    return day.weekday() >= 5
EOF
commit "feat: calendar rules"
git init -q --bare -b trunk .git/origin.git
git remote add origin "$PWD/.git/origin.git"
git push -q origin trunk
git remote set-head origin trunk
git checkout -qb feature
cat > calendar_rules.py <<'EOF'
import datetime
import json

HOLIDAYS = {(1, 1), (5, 1), (7, 14), (12, 25)}


def load_holidays(path):
    try:
        with open(path) as f:
            return {tuple(d) for d in json.load(f)}
    except Exception:
        return set()


def is_weekend(day: datetime.date) -> bool:
    """True on Saturday or Sunday."""
    return day.weekday() > 5


def is_business_day(day: datetime.date) -> bool:
    return not is_weekend(day) and (day.month, day.day) not in HOLIDAYS
EOF
cat > test_calendar_rules.py <<'EOF'
import datetime

from calendar_rules import is_business_day


def test_holiday():
    assert not is_business_day(datetime.date(2024, 12, 25))


def test_weekday():
    assert is_business_day(datetime.date(2024, 5, 7))
EOF
commit "feat: business days"
git rev-parse HEAD > .git/eval-head
