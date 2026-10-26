# Setup Guide — From Zero to Working

Languages: [English](setup-guide.md) | [繁中](setup-guide.zh-TW.md)

Choose a route before installing anything. This guide covers native Stage 1
research and an optional Claude Code/plugin or Research Hub CLI setup. If you
already use the Claude Code installation path, [install.md](install.md)
covers the plugin install only.

## Choose a route before installing

- **Native AI Skills research:** Follow [Stage 1 — Discover literature](pipeline.md#1-discover-literature)
  with your host's actually available and authorized search/reading tools.
  Research Hub itself is optional; no Claude Code, Python or Git installation is required for this native route.
  Finish the discovery handoff and stop without Zotero or any storage destination.
  Native-route users skip Phases A–F below; missing optional integrations do not block this route.
- **Optional installation path:** Use Phases A–F for the Claude Code plugins
  and only the Hub CLI/integrations you select. Phase C is for Zotero; Phase D
  adds the Hub CLI and does not require Phase C. Install each selected component
  only when its operations are needed.

**Optional installation path time budget**:

- Phase A + B alone (~20 min) → 12 of 17 skills installed; the prompt-only and workspace-file skills inside the research-workspace plugin work immediately, no Zotero needed.
- Phase A + B + C (~40 min) → 15 of 17 skills wired with Zotero connectivity (add academic-writing-skills in B-extra, then zotero-skills in Phase C).
- Phase A + B + C + D (~60 min) → research-workspace skills connect to the research-hub Python pipeline; codex/antigravity delegates wait for Phase E3.

Stop after any phase and use what you've installed.

**Convention** in this guide: each step ends with a `# verify` block.
Run that command and check the expected output before moving on. If it
fails, see [Phase F — Troubleshooting](#phase-f--troubleshooting).

---

## Phase A — Foundation (install the runtimes)

For the optional Claude Code/plugin and Hub CLI route, the tools below are
**Claude Code**, **Python 3.10+**, and **Git**. They are not prerequisites for
native Stage 1 research. If `python` and `git` already work in your terminal,
you can skip A2 and A3.

### A1. Install Claude Code

1. Open https://claude.ai/code in a browser.
2. Download the installer for your OS (Windows `.msi`, macOS `.dmg`, or
   the Linux instructions on the same page).
3. Run the installer with default options.
4. Open a new terminal window (existing terminals won't see the new PATH).

```bash
# verify
claude --version
# expected: claude-code/<version>  (any version string is fine)
```

If `claude: command not found`, see [F1](#f1-claude-command-not-found).

### A2. Install Python 3.10 or newer

1. Open https://www.python.org/downloads/
2. Download the latest Python 3.x for your OS.
3. **Windows only**: on the first installer screen, check the box
   **"Add python.exe to PATH"** before clicking Install. This single
   checkbox is the #1 setup failure.
4. macOS / Linux: defaults are fine.

```bash
# verify
python --version
# expected: Python 3.10.x or higher  (3.10, 3.11, 3.12 all work)

pip --version
# expected: pip 23.x or higher
```

On macOS / Linux, the command may be `python3` and `pip3` instead of
`python` and `pip` — both are fine, just substitute through the rest of
this guide.

### A3. Install Git

1. Open https://git-scm.com/downloads
2. Download and install for your OS with default options.
3. On Windows, the installer is **Git for Windows** and includes
   git-bash (used internally by Claude Code on Windows).

```bash
# verify
git --version
# expected: git version 2.40.x or higher
```

### Phase A checkpoint

All three commands above print a version. You're ready for Phase B.

---

## Phase B — First plugins (usable immediately)

This installs 6 skills that work with pure Claude reasoning — no Zotero,
no Python pipeline, no API keys. Good enough for triaging papers from
a manual list, drafting outlines, and verifying NotebookLM briefs.

### B1. Add the marketplace

Open a terminal (not the interactive `/plugin` UI inside Claude — that
falls back to SSH and can fail):

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
```

```bash
# verify
claude plugin marketplace list
# expected: a line containing "ai-research-skills"
```

### B2. Install the research-workspace plugin

```bash
claude plugin install research-workspace@ai-research-skills
```

```bash
# verify
claude plugin list
# expected: research-workspace@ai-research-skills shows up with ✔ enabled.
# (Marketplace plugins do NOT extract into ~/.claude/skills/; they live
#  under ~/.claude/plugins/cache/ai-research-skills/research-workspace/
#  <version>/skills/<name>/. The plugin ships 12 skills:
#  literature-triage-matrix, research-hub, research-design-helper,
#  paper-memory-builder, paper-summarize, notebooklm-brief-verifier,
#  research-context-compressor, research-project-orienter,
#  research-hub-multi-ai, zotero-library-curator, gap-to-topic,
#  research-workflow-orchestrator.)
```

### B3. Smoke test: literature matrix from 3 papers

Open Claude Code in any folder and paste:

```
Make a literature triage matrix for these 3 papers:
- "Memory enables ToM-like behaviour in LLM poker agents", arXiv:2604.04157
- "Multi-agent LLM social learning", arXiv:2604.02677
- "Triadic Loop alignment framework", arXiv:2604.18850
```

```bash
# verify (run in Git Bash on Windows, or zsh / bash on macOS / Linux)
ls .research/
# expected: a file literature_matrix.md
cat .research/literature_matrix.md | head
# expected: a 9-column markdown table with Citation / Question / Method / etc.

# On Windows PowerShell, use this instead:
#   Get-Content .research/literature_matrix.md -TotalCount 10
```

If Claude says "I don't have a skill for that" or skips the matrix
output, see [F2](#f2-claude-doesnt-trigger-the-skill).

### Phase B checkpoint

You have 12 of 17 skills installed (the research-workspace plugin) and
a working literature matrix without Zotero or other external integrations.
Native Stage 1 discovery does not require Phase C / D / E; use the
[native discovery route](pipeline.md#1-discover-literature) and stop when the
handoff meets your needs. Selected runtime-backed operations need only their
corresponding setup: Phase C for Zotero CRUD/apply, Phase D for Hub CLI
operations, and Phase E for selected add-ons. Continue to Phase B-extra for
manuscript tooling, or to Phase C only if you want Zotero library operations;
otherwise stop here or select Phase D directly.

### B-extra. academic-writing-skills (optional, ~1 min)

If you'll be writing or revising manuscripts:

```bash
claude plugin install academic-writing-skills@ai-research-skills
```

```bash
# verify
claude plugin list
# expected: academic-writing-skills@ai-research-skills shows up with ✔ enabled.
# (Marketplace plugins do NOT extract into ~/.claude/skills/ — see the README
#  for where they actually land.)
```

This brings the setup to 14 of 17 skills — banned-word audit,
claim-evidence check, journal format, reviewer response, and
`paper-review`. Skip if you only need literature triage / lit review.

---

## Phase C — Zotero connectivity (optional)

Adds full Zotero CRUD and audit cleanup. Without Phase C, the
`zotero-library-curator` skill works only in preview mode (it can
*propose* cleanups but not *apply* them).

### C1. Install Zotero desktop

1. Open https://www.zotero.org/download/
2. Download Zotero (not Zotero Connector — that's the browser
   extension, separate). Install with defaults.
3. Launch Zotero and sign in (or create a free account). Sync happens
   in the background; you don't need to wait.

### C2. Enable the local API

In the Zotero desktop app:

1. **Edit → Settings** (Windows / Linux) or **Zotero → Settings** (macOS).
2. Click **Advanced** in the left sidebar.
3. Check the box: **"Allow other applications on this computer to
   communicate with Zotero"**.
4. Close the Settings window. (Zotero does NOT need restart for this.)

```bash
# verify (Zotero must be running)
curl http://localhost:23119/api/users/0
# expected: a JSON response with a "userID" field

# On Windows PowerShell, `curl` is aliased to Invoke-WebRequest which
# wraps the response. Use `curl.exe` (the real curl, bundled with Git
# for Windows) for the same raw JSON output:
#   curl.exe http://localhost:23119/api/users/0
```

If you get `Connection refused`, see [F3](#f3-zotero-local-api-port-23119-not-reachable).

**Alternative: Web API key.** If you can't run Zotero desktop locally
(headless server, shared lab machine), you can use Zotero's web API
instead — see [zotero-skills README](https://github.com/WenyuChiou/zotero-skills#readme)
for the API-key path. The rest of this guide assumes local API.

### C3. Install the zotero-skills plugin

```bash
claude plugin install zotero-skills@ai-research-skills
```

```bash
# verify
claude plugin list
# expected: zotero-skills@ai-research-skills shows up with ✔ enabled.
```

### C4. Test Zotero connectivity

In Claude Code, ask:

```
List the top 5 most recent items in my Zotero library.
```

Claude should call the Zotero local API and return real titles from
your library. If it returns "I can't access Zotero" or empty results,
see [F4](#f4-zotero-skill-cant-find-items).

### Phase C checkpoint

You have 15 of 17 skills wired up (12 from research-workspace +
2 from academic-writing-skills in Phase B-extra + zotero-skills), and the
zotero-library-curator skill is upgraded from preview-only to
apply-capable. The remaining 2 (`codex-delegate`, `antigravity-delegate`)
are installed in Phase E3 once you've installed their CLI binaries.
Phase D adds the optional Hub CLI route for selected pipeline operations.
Native discovery and paper search do not require Zotero or the Hub CLI;
you can select Phase D without completing Phase C.

---

## Phase D — research-hub Python CLI (full pipeline)

This is the optional Hub CLI path; native-only users skip this phase.
It adds Hub-backed paper discovery (arxiv / semantic scholar / pubmed search),
Obsidian / NotebookLM integration, cluster management, and the
backfill / dedup operations the curator skill defers to.

### D1. Install the package

```bash
pip install research-hub-pipeline
```

If you get `Permission denied` or want to keep things isolated, see
[F5](#f5-pip-install-permission-or-isolation).

```bash
# verify
research-hub --version
# expected: 0.45.0 or higher (the version range covered by docs/verification.md).
# Latest PyPI may be newer; older versions before 0.45 are unsupported.
```

### D2. Run interactive setup

```bash
research-hub setup --persona researcher
```

The wizard asks 3-4 questions:

- **Zotero default collection name**: pick one (e.g. `to-read`). Skip
  if you only use the root library.
- **NotebookLM login**: say `n` for now (you can add it later in
  Phase E2).
- **Install sample data**: `y` recommended; gives you something to
  smoke-test against.

The `setup` command is **idempotent** — re-run any time to change
persona or refresh.

Persona quick guide:

| Persona | When to pick |
|---|---|
| `researcher` | Zotero + Obsidian + NotebookLM workflow (most common) |
| `analyst` | Obsidian + NotebookLM only, no Zotero |
| `humanities` | Zotero + qualitative / archival work, no code repo |
| `internal` | Catalog reader, no install |

### D3. Verify the install is healthy

```bash
research-hub doctor
```

Expected output: a checklist with green checks for Python version,
Zotero local API connectivity (if Phase C done), and skill directory
presence. Yellow warnings for optional integrations you skipped are
fine.

### D4. Runtime smoke test

Native-only users skip this step. For the optional Hub CLI route, complete the
[first-live-run preflight](live-run-preflight.md) before running `auto`.
Reuse valid approved choices; resolve only missing material model,
authentication, budget and data-scope choices.

`--no-nlm` disables only NotebookLM; it does not disable other network requests, model calls or local/external writes.
This is a live integration smoke test, not a read-only or offline test.
Run it only for the selected operations within existing authorization:

```bash
research-hub describe --json
research-hub doctor
research-hub auto "agent-based flood modeling" --max-papers 3 --no-nlm
```

Record the actual capability/health results and any model, ingest or write
outcomes. Missing setup remains blocked; a command example or offline fixture
pass is not evidence that the live workflow ran. Add NotebookLM only when
separately selected and authorized.

### Phase D checkpoint

With Phase B-extra and Phase C completed, 15 of 17 skills are wired up.
Without Zotero, use only the Hub operations you selected; an unselected
integration is not a prerequisite for native research. Phase E3 adds the two
optional delegation skills.

---

## Phase E — Optional add-ons

Each is independent — install only what you'll actually use.

### E1. Obsidian (paper notes + cluster dashboards)

1. Install from https://obsidian.md
2. Create a vault (any folder you'll use for your research notes).
3. Tell research-hub the vault path:

```bash
research-hub config set obsidian.vault_path /path/to/your/vault
```

```bash
# verify
research-hub config get obsidian.vault_path
# expected: the path you set
```

### E2. NotebookLM browser automation

1. Install the playwright extras:
   ```bash
   pip install "research-hub-pipeline[playwright]"
   ```
2. Run the one-time browser login:
   ```bash
   research-hub notebooklm login --auto-detect
   ```
   This opens a browser. Sign in to your Google account that has
   NotebookLM access. Close the browser when redirected.

```bash
# verify
research-hub notebooklm status
# expected: "logged in" with your Google account email
```

### E3. Codex CLI / Antigravity CLI (multi-AI delegation)

**Prereq**: Node.js 18+ — both CLIs install via `npm`. Verify with
`node --version`; install from [nodejs.org](https://nodejs.org) if
missing. (If `npm` is not on PATH after install, restart your shell.)

Install the CLI binaries from their official upstream sources:

- [Codex CLI (OpenAI)](https://github.com/openai/codex) →
  `npm install -g @openai/codex`
- Antigravity CLI (`agy`) → install from the
  [antigravity-delegate](https://github.com/WenyuChiou/antigravity-delegate)
  source repo's current instructions.

The skill wrappers that delegate work TO these CLIs live in
[`WenyuChiou/codex-delegate`](https://github.com/WenyuChiou/codex-delegate)
and
[`WenyuChiou/antigravity-delegate`](https://github.com/WenyuChiou/antigravity-delegate)
— those are different from the CLI binaries themselves.

Then install the delegate plugins:

```bash
claude plugin install codex-delegate@ai-research-skills
claude plugin install antigravity-delegate@ai-research-skills
```

```bash
# verify
codex --version
agy --version
# expected: a version string for each
```

---

## Phase F — Troubleshooting

### F1. `claude: command not found`

Most common on Windows: you ran `claude --version` in the same terminal
you had open *before* installing Claude Code. The installer updates
PATH but only new terminals see it.

- **Windows**: close all PowerShell / Command Prompt windows and open a
  new one.
- **macOS / Linux**: `source ~/.zshrc` (or `~/.bashrc`), or open a new
  terminal window.

If still not found after a fresh terminal:

- Confirm install location:
  - macOS / Linux: `ls "$HOME/.claude/bin/"`
  - Windows PowerShell: `Get-ChildItem "$env:USERPROFILE\.claude\bin"`
  - Windows cmd.exe: `dir "%USERPROFILE%\.claude\bin"`
- Re-run the installer; allow it to update PATH.

### F2. Claude doesn't trigger the skill

The trigger phrase you used didn't match any skill's `description`.
Each skill has trigger phrases in its `SKILL.md` (the `description:`
frontmatter field).

Fix:

- Use the **exact** trigger phrase from the skill description, e.g.
  "**make a literature matrix** for these papers".
- Or, explicitly name the skill: "Use the `literature-triage-matrix`
  skill to compare these papers."

You can read the trigger phrases at
`~/.claude/skills/<skill-name>/SKILL.md` (look for "Trigger phrases").

### F3. Zotero local API (port 23119) not reachable

```bash
# diagnose
curl -v http://localhost:23119/api/users/0
```

- **`Connection refused`**: Zotero desktop is not running, OR the
  "Allow other applications..." checkbox in Phase C2 is not enabled.
- **Different process listening**: another app holds port 23119.
  Stop it (rare; Zotero's the only known user of this port).
- **Firewall**: Windows Defender or corporate firewall may block
  localhost-to-localhost. Add an inbound rule for port 23119 (TCP),
  scope `127.0.0.1`.

### F4. Zotero skill can't find items

- Confirm Zotero is running AND F3's `curl` returns JSON.
- Confirm your library is not empty — open Zotero desktop and add at
  least one item.
- If using Zotero Web API instead of local: confirm the API key is
  set per [zotero-skills README](https://github.com/WenyuChiou/zotero-skills#readme).

### F5. `pip install` permission or isolation

If `pip install research-hub-pipeline` gives **`Permission denied`** or
**`error: externally-managed-environment`**:

**Best** (isolated, no system pip needed):

```bash
pip install --user pipx
python -m pipx ensurepath   # adds pipx's bin dir to PATH; reopen terminal after
python -m pipx install research-hub-pipeline
```

Using `python -m pipx` (not bare `pipx`) sidesteps the case where the
user-scripts directory isn't on PATH yet right after `pip install --user`.

**Alternative** (venv):

```bash
python -m venv ~/.venvs/research-hub
source ~/.venvs/research-hub/bin/activate   # macOS / Linux
# OR on Windows:
~/.venvs/research-hub/Scripts/Activate.ps1
pip install research-hub-pipeline
```

After install, `research-hub --version` should work. With venv, you
need to activate the venv in any new terminal where you want to use it
(or add the venv's `bin/` to PATH permanently).

### F6. `research-hub doctor` shows red errors

Read the line above the red mark — `doctor` names the failing check
explicitly:

- `Zotero local API: unreachable` → see F3.
- `Python version: too old` → re-install Python 3.10+ per A2.
- `Skills directory not found` → re-run `claude plugin install
  research-workspace@ai-research-skills` per B2.

### F7. Cross-platform skill installation on non-Claude-Code hosts

If you're running these skills under Codex CLI, Gemini CLI, Cursor,
Hermes, or another agentskills.io-compliant host, see
[README → Compatibility](../README.md#7-compatibility)
and the
[Hermes compatibility audit](../.research/hermes-compatibility-audit.md)
for what's verified and what's host-specific.

---

## Next steps

- Skill-by-skill install reference: [install.md](install.md)
- Workflow-by-workflow guide: [researcher-workflow-checklist.md](researcher-workflow-checklist.md)
- Catalog of all 17 skills: [skill-directory.md](skill-directory.md)
