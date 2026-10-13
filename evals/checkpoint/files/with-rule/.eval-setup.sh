set -e
printf '.claude/\n__pycache__/\n.eval-setup.sh\n' >> .git/info/exclude
git add -A
git commit -qm "feat: config parser"
cat > parser.py <<'X'
def parse_line(line):
    key, _, value = line.partition("=")
    return key.strip(), value.strip()
X
git rev-parse HEAD > .git/eval-base
