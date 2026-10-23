#!/bin/sh
# Usage: evals/run.sh <suite> [extra agent-skill-eval run flags]
# Runs the suite with and without the skill in Claude Code.
# The without-skill condition omits the tested skill; other host capabilities may remain.
# EVAL_SKILLS: directory holding the skills under test (default: the repository's skills/).
# EVAL_SKILL: skill to install when it is not hl-<suite>.
# gh, jira, and acli are stubs that fail. A case fixture .eval-setup.sh runs in the workspace before the agent.
# A suite with repo.sh gets a git repository built by `repo.sh <dir> <skills dir>` as every workspace.
set -eu
suite=$1; shift
root=$(cd "$(dirname "$0")/.." && pwd)
skills=$(cd "${EVAL_SKILLS:-$root/skills}" && pwd)
shim=$(mktemp -d "${TMPDIR:-/tmp}/hl-eval-shim.XXXXXX")
real=$(command -v claude)
# These stubs reduce accidental forge access; they are not filesystem or network isolation.
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
[ "\$#" -eq 1 ] && [ "\$1" = --version ] && exec "$real" "\$@"
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
exec python3 -c '
import os
import sys
args = [arg for arg in sys.argv[2:] if arg != "--dangerously-skip-permissions"]
settings = os.environ.get("EVAL_CLAUDE_SETTINGS")
if settings:
    args = ["--settings", settings, *args]
os.execv(sys.argv[1], [sys.argv[1], "--setting-sources", "project,local", *args])
' "$real" "\$@"
EOF
chmod +x "$shim/claude" "$shim"/bin/*
if [ -f "$root/evals/$suite/repo.sh" ]; then
  repo=$(mktemp -d "${TMPDIR:-/tmp}/hl-eval-repo.XXXXXX")
  sh "$root/evals/$suite/repo.sh" "$repo" "$skills"
  set -- --source-repo "$repo" "$@"
fi
caller_path="$shim/bin:$PATH"
if [ -n "${EVAL_MAX_COST:-}" ]; then
  set -- --max-cost-per-case "$EVAL_MAX_COST" --budget-action stop-suite "$@"
fi
PATH="$shim:$caller_path" uvx --from agent-skill-eval==0.7.0 agent-skill-eval run \
  --skill "$skills/${EVAL_SKILL:-hl-$suite}" --evals "$root/evals/$suite/evals.json" \
  --agent claude-code --agent-model "claude-code=${EVAL_MODEL:-sonnet}" \
  --workspace "${EVAL_WORKSPACE:-/tmp/hl-evals}" \
  --post-grade-command "PATH='$caller_path' python3 '$root/evals/check.py'" \
  --retries 0 \
  "$@"
