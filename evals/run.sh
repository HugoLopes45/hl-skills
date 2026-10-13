#!/bin/sh
# Usage: evals/run.sh <suite> [extra agent-skill-eval run flags]
# Runs the suite with and without the skill in Claude Code.
# User-level settings, skills, commands, and CLAUDE.md are excluded so the baseline is a bare agent.
# EVAL_SKILLS: directory holding the skills under test (default: the repository's skills/).
# EVAL_SKILL: skill to install when it is not hl-<suite>.
# gh, jira, and acli are stubs that fail. A case fixture .eval-setup.sh runs in the workspace before the agent.
# A suite with repo.sh gets a git repository built by `repo.sh <dir> <skills dir>` as every workspace.
set -eu
suite=$1; shift
root=$(cd "$(dirname "$0")/.." && pwd)
skills=$(cd "${EVAL_SKILLS:-$root/skills}" && pwd)
shim=$(mktemp -d)
real=$(command -v claude)
# Stubs, no tokens, and an empty gh config keep runs away from real GitHub and Jira accounts.
mkdir "$shim/bin" "$shim/gh"
for tool in gh jira acli; do
  printf '#!/bin/sh\necho "%s: not available in this environment" >&2\nexit 1\n' "$tool" > "$shim/bin/$tool"
done
# Setup scripts, the agent, and the checks use git with a fixed identity, no signing, only the fixture's own hooks,
# and none of the caller's ignore or status settings.
printf '[user]\n\tname = Eval\n\temail = eval@example.com\n[commit]\n\tgpgsign = false\n' > "$shim/gitconfig"
export GIT_CONFIG_GLOBAL="$shim/gitconfig" GIT_CONFIG_NOSYSTEM=1
# uvx puts its own Python first on PATH; the agent and the checks get the caller's PATH back.
# A case fixture .eval-setup.sh builds its git state in the workspace, then is deleted before the agent starts.
cat > "$shim/claude" <<EOF
#!/bin/sh
PATH="$shim/bin:$PATH"
unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN
for v in \$(env | sed -nE 's/^((JIRA|ATLASSIAN)[A-Za-z0-9_]*)=.*/\1/p'); do unset "\$v"; done
export GH_CONFIG_DIR="$shim/gh"
# Auto memory is keyed by workspace path, which repeats across iterations.
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
# The agent shell inherits the caller's interactive aliases; a zsh alias such as ls=eza can block on stdin.
export CLAUDE_CODE_SHELL=/bin/bash
if [ -f .eval-setup.sh ]; then
  sh .eval-setup.sh >&2 && rm .eval-setup.sh || exit 1
fi
exec "$real" --setting-sources project,local "\$@"
EOF
chmod +x "$shim/claude" "$shim"/bin/*
if [ -f "$root/evals/$suite/repo.sh" ]; then
  repo=$(mktemp -d)
  sh "$root/evals/$suite/repo.sh" "$repo" "$skills"
  set -- --source-repo "$repo" "$@"
fi
PATH="$shim:$PATH" uvx --from agent-skill-eval==0.7.0 agent-skill-eval run \
  --skill "$skills/${EVAL_SKILL:-hl-$suite}" --evals "$root/evals/$suite/evals.json" \
  --agent claude-code --agent-model "claude-code=${EVAL_MODEL:-sonnet}" \
  --workspace "${EVAL_WORKSPACE:-/tmp/hl-evals}" \
  --post-grade-command "PATH='$PATH' python3 '$root/evals/check.py'" \
  --max-cost-per-case "${EVAL_MAX_COST:-1.5}" --budget-action stop-suite \
  "$@"
