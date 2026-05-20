# install-all.ps1 — install every plugin in the ai-research-skills
# Claude Code marketplace in one go.
#
# Usage:
#   pwsh scripts/install-all.ps1
#   pwsh scripts/install-all.ps1 -Scope project
#
# Default scope is `user` (this OS account, all projects). Pass
# -Scope project to install only for the current project.
#
# Prerequisite: Claude Code CLI on PATH (`claude --version`).

param(
  [ValidateSet("user", "project", "local")]
  [string]$Scope = "user"
)

$ErrorActionPreference = "Stop"

$Marketplace = "WenyuChiou/ai-research-skills"
$Plugins = @(
  "research-workspace"
  "academic-writing-skills"
  "zotero-skills"
  "codex-delegate"
  "gemini-delegate"
)

if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
  Write-Error "'claude' CLI not found on PATH. Install Claude Code first: https://claude.ai/code"
  exit 1
}

Write-Host ">> Adding marketplace: $Marketplace"
claude plugin marketplace add $Marketplace

Write-Host ""
foreach ($p in $Plugins) {
  Write-Host ">> Installing $p (scope: $Scope)"
  claude plugin install "$p@ai-research-skills" --scope $Scope
}

Write-Host ""
Write-Host "Done. Run 'claude plugin list' to confirm all 5 plugins show as ✔ enabled."
