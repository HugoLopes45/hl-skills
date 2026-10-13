set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
git add -A
git -c user.name=t -c user.email=t@t commit -qm 'feat: user report'
printf '"Lee, Ann",ann@example.com\n' >> users.csv
git -c user.name=t -c user.email=t@t commit -qam 'data: add Ann Lee'
