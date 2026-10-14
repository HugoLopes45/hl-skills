set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
cat > wallet.py <<'EOF'
import threading


class InsufficientFunds(Exception):
    pass


class Wallet:
    """One wallet per customer, shared by the payment worker threads."""

    def __init__(self, balance_cents):
        self.balance_cents = balance_cents
        self._lock = threading.Lock()

    def withdraw(self, cents):
        with self._lock:
            if self.balance_cents < cents:
                raise InsufficientFunds(cents)
            self.balance_cents -= cents
            return self.balance_cents
EOF
cat > workers.py <<'EOF'
from concurrent.futures import ThreadPoolExecutor


def pay_all(wallet, charges, threads=8):
    with ThreadPoolExecutor(threads) as pool:
        return list(pool.map(wallet.withdraw, charges))
EOF
commit "feat: wallet"
git checkout -qb feature
cat > wallet.py <<'EOF'
class InsufficientFunds(Exception):
    pass


class Wallet:
    """One wallet per customer, shared by the payment worker threads."""

    def __init__(self, balance_cents):
        self.balance_cents = balance_cents

    def withdraw(self, cents):
        if self.balance_cents < cents:
            raise InsufficientFunds(cents)
        self.balance_cents -= cents
        return self.balance_cents
EOF
git add -A
GIT_AUTHOR_DATE=2024-05-02T10:00:00+0000 GIT_COMMITTER_DATE=2024-05-02T10:00:00+0000 git -c user.name=Dev -c user.email=dev@example.com commit -q -F - <<'EOF'
perf: drop the wallet lock

The lock showed up in profiles. withdraw is a few integer operations, and the
GIL makes them effectively atomic.
EOF
git rev-parse HEAD > .git/eval-head
