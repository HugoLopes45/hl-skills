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
mkdir -p deploy
cat > deploy/Dockerfile <<'X'
FROM python:3.12-slim
COPY . /app
X
git add calc.py deploy/Dockerfile
