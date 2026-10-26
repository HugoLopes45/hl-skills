set -e
printf ".claude/\n__pycache__/\n.eval-setup.sh\n" >> .git/info/exclude
git add -A
git commit -qm "feat: support assistant"
