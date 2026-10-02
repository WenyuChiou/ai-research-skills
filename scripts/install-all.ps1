# Install all five Claude marketplace plugins; -DryRun prints without changes.
param(
  [ValidateSet("user", "project", "local")]
  [string]$Scope = "user",
  [switch]$DryRun
)
$ErrorActionPreference = "Stop"
$Marketplace = "WenyuChiou/ai-research-skills"
$Plugins = @("research-workspace", "academic-writing-skills", "zotero-skills", "codex-delegate", "antigravity-delegate")
function Invoke-Claude {
  param([string[]]$Arguments)
  if ($DryRun) {
    Write-Output ("claude " + ($Arguments -join " "))
    return
  }
  & claude @Arguments
  # ErrorActionPreference alone does not catch a native executable's failure.
  if ($LASTEXITCODE -ne 0) { throw "claude failed with exit code $LASTEXITCODE" }
}
if (-not $DryRun -and -not (Get-Command claude -ErrorAction SilentlyContinue)) {
  Write-Error "'claude' CLI not found on PATH. Install Claude Code: https://claude.ai/code"
  exit 1
}
Invoke-Claude -Arguments @("plugin", "marketplace", "add", $Marketplace)
foreach ($p in $Plugins) {
  Invoke-Claude -Arguments @("plugin", "install", "$p@ai-research-skills", "--scope", $Scope)
}
if (-not $DryRun) { Write-Output "Done. Run 'claude plugin list' to verify the installed state." }
