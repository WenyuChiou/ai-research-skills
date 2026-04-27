#!/usr/bin/env bash
# install-all.sh — install every plugin in the ai-research-skills
# Claude Code marketplace in one go.
#
# Usage:
#   bash scripts/install-all.sh
#
# Run from any directory; the script uses absolute marketplace and
# plugin names. Default scope is `user` (this OS account, all
# projects). Pass --scope project as the first argument to install
# only for the current project.
#
# Prerequisite: Claude Code CLI on PATH (`claude --version`).

set -euo pipefail

MARKETPLACE="WenyuChiou/ai-research-skills"
PLUGINS=(
  "research-workspace"
  "academic-writing-skills"
  "zotero-skills"
  "codex-delegate"
  "gemini-delegate"
)

SCOPE="user"
if [[ "${1:-}" == "--scope" && -n "${2:-}" ]]; then
  SCOPE="$2"
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "error: 'claude' CLI not found on PATH." >&2
  echo "Install Claude Code first: https://claude.ai/code" >&2
  exit 1
fi

echo ">> Adding marketplace: $MARKETPLACE"
claude plugin marketplace add "$MARKETPLACE"

echo ""
for p in "${PLUGINS[@]}"; do
  echo ">> Installing $p (scope: $SCOPE)"
  claude plugin install "$p@ai-research-skills" --scope "$SCOPE"
done

echo ""
echo "Done. Run 'claude plugin list' to confirm all 5 plugins show as ✔ enabled."
