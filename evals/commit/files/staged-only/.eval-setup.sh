set -e
printf '.claude/\n' >> .git/info/exclude
git add calc.py test_calc.py README.md
git commit -qm "feat: add calculator"
git rev-parse HEAD > .git/eval-base
cat > calc.py <<'X'
def average(values):
    return sum(values) / len(values)


def clamp(x, low, high):
    return max(low, min(x, high))
X
git add calc.py
printf '\n## Usage\n\nImport the functions from calc.py.\n' >> README.md
