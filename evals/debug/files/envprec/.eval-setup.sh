set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
chmod +x run.sh
git add -A
git -c user.name=t -c user.email=t@t commit -qm 'feat: fetcher'
