set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
git checkout -q -B main
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-03-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
cat > units.py <<'EOF'
UNITS = {
    "h": 3600,
    "ms": 0.001,
    "m": 60,
    "s": 1,
}
EOF
cat > parser.py <<'EOF'
import re

from units import UNITS


def _pattern():
    return re.compile(r"(\d+(?:\.\d+)?)(" + "|".join(UNITS) + r")")


def parse_duration(text):
    """Return seconds for strings such as '1h30m' or '1m500ms'."""
    total = 0.0
    for match in _pattern().finditer(text.replace(" ", "")):
        total += float(match.group(1)) * UNITS[match.group(2)]
    return total
EOF
commit "feat: parse durations"
cat > test_parser.py <<'EOF'
from parser import parse_duration


def test_hours_minutes():
    assert parse_duration("1h30m") == 5400


def test_mixed_ms():
    assert parse_duration("1m500ms") == 60.5


def test_spaces():
    assert parse_duration("2m 3s") == 123
EOF
commit "test: parser"
printf '# Changelog\n\n## 1.0.0\n- parse_duration\n' > CHANGELOG.md
commit "docs: changelog"
git tag v1.0
printf "\nExample: \`parse_duration('1h30m')\` returns \`5400.0\`.\n" >> README.md
commit "docs: usage in README"
cat > fmt.py <<'EOF'
def humanize(seconds):
    """Format seconds as '1h 30m 5s'."""
    seconds = int(seconds)
    parts = []
    for unit, size in (("h", 3600), ("m", 60), ("s", 1)):
        value, seconds = divmod(seconds, size)
        if value:
            parts.append(f"{value}{unit}")
    return " ".join(parts) or "0s"
EOF
cat > test_fmt.py <<'EOF'
from fmt import humanize


def test_humanize():
    assert humanize(5405) == "1h 30m 5s"
EOF
commit "feat(fmt): humanize seconds"
cat >> test_fmt.py <<'EOF'


def test_zero():
    assert humanize(0) == "0s"
EOF
commit "test(fmt): zero duration"
cat > parser.py <<'EOF'
import re
from functools import lru_cache

from units import UNITS


@lru_cache(maxsize=1)
def _pattern():
    return re.compile(r"(\d+(?:\.\d+)?)(" + "|".join(UNITS) + r")")


def parse_duration(text):
    """Return seconds for strings such as '1h30m' or '1m500ms'."""
    total = 0.0
    for match in _pattern().finditer(text.replace(" ", "")):
        total += float(match.group(1)) * UNITS[match.group(2)]
    return total
EOF
commit "perf: cache compiled pattern"
cat > cli.py <<'EOF'
import sys

from fmt import humanize
from parser import parse_duration


def main(argv):
    print(humanize(parse_duration(" ".join(argv))))


if __name__ == "__main__":
    main(sys.argv[1:])
EOF
commit "feat(cli): duration command"
printf '# Changelog\n\n## 1.1.0\n- humanize, cli\n\n## 1.0.0\n- parse_duration\n' > CHANGELOG.md
commit "docs: changelog for 1.1"
python3 - <<'EOF'
from pathlib import Path
p = Path("fmt.py")
p.write_text(p.read_text().replace('    return " ".join(parts) or "0s"', '    text = " ".join(parts)\n    return text if text else "0s"'))
EOF
commit "fix(fmt): explicit empty case"
cat > cli.py <<'EOF'
import argparse

from fmt import humanize
from parser import parse_duration


def main(argv=None):
    args = argparse.ArgumentParser().parse_known_args(argv)[1]
    print(humanize(parse_duration(" ".join(args))))


if __name__ == "__main__":
    main()
EOF
commit "refactor(cli): argparse"
cat > units.py <<'EOF'
UNITS = {
    "d": 86400,
    "h": 3600,
    "m": 60,
    "ms": 0.001,
    "s": 1,
}
EOF
cat >> test_parser.py <<'EOF'


def test_days():
    assert parse_duration("2d") == 172800
EOF
commit "feat: add day unit"
python3 - <<'EOF'
from pathlib import Path
p = Path("cli.py")
p.write_text(p.read_text().replace("import argparse\n", 'import argparse\n\n__version__ = "1.2.0"\n', 1))
EOF
commit "chore: bump version"
python3 - <<'EOF'
from pathlib import Path
p = Path("parser.py")
p.write_text(p.read_text().replace('text.replace(" ", "")', 'text.replace(" ", "").lower()'))
EOF
cat >> test_parser.py <<'EOF'


def test_uppercase():
    assert parse_duration("1H") == 3600
EOF
commit "fix: accept uppercase units"
cat > test_cli.py <<'EOF'
from cli import main


def test_cli(capsys):
    main(["1h", "30m"])
    assert capsys.readouterr().out == "1h 30m\n"
EOF
commit "test(cli): smoke test"
printf '# Changelog\n\n## 1.2.0\n- day unit, uppercase units\n\n## 1.1.0\n- humanize, cli\n\n## 1.0.0\n- parse_duration\n' > CHANGELOG.md
commit "docs: changelog for 1.2"
git rev-parse HEAD > .git/eval-head
