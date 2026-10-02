#!/usr/bin/env bash
# Install the five Claude marketplace plugins. --dry-run only prints a plan.
# Usage: bash scripts/install-all.sh [--scope user|project|local] [--dry-run]
set -euo pipefail
MARKETPLACE="WenyuChiou/ai-research-skills"
PLUGINS=(research-workspace academic-writing-skills zotero-skills codex-delegate antigravity-delegate)
SCOPE="user"
DRY_RUN=0
while (($#)); do
  case "$1" in
    --scope)
      [[ $# -ge 2 ]] || { echo "error: --scope requires an argument" >&2; exit 2; }
      SCOPE="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --help|-h) echo "Usage: $0 [--scope user|project|local] [--dry-run]"; exit 0 ;;
    *) echo "error: unknown argument: $1" >&2; exit 2 ;;
  esac
done
case "$SCOPE" in user|project|local) ;; *) echo "error: invalid scope: $SCOPE" >&2; exit 2 ;; esac
run_claude() {
  if ((DRY_RUN)); then
    printf 'claude'; printf ' %q' "$@"; printf '\n'
  else
    claude "$@"
  fi
}
if ((!DRY_RUN)) && ! command -v claude >/dev/null 2>&1; then
  echo "error: 'claude' CLI not found on PATH. Install Claude Code: https://claude.ai/code" >&2
  exit 1
fi
run_claude plugin marketplace add "$MARKETPLACE"
for p in "${PLUGINS[@]}"; do
  run_claude plugin install "$p@ai-research-skills" --scope "$SCOPE"
done
if ((!DRY_RUN)); then
  echo "Done. Run 'claude plugin list' to verify the installed state."
fi
