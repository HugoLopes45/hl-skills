set -e
git init -q -b main
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\nlocal.toml\n' >> .git/info/exclude
git add -A
git -c user.name=t -c user.email=t@t commit -qm 'feat: ledger'
git checkout -qb feature/csv-import
printf '\n# wip\n' >> ledger.py
