# Setup Guide — From Zero to Working

Languages: [English](setup-guide.md) | [繁中](setup-guide.zh-TW.md)

This is the step-by-step path from "I don't have anything installed" to
"I can ask Claude to make a literature matrix and it works." If you
already have Claude Code, Python, and Zotero working, skip to
[install.md](install.md) — it covers the plugin install only.

**Time budget**:

- Phase A + B alone (~20 min) → 10 of 14 skills installed; the 6 pure-reasoning ones inside the research-workspace plugin work immediately, no Zotero needed.
- Phase A + B + C (~40 min) → 12 of 14 skills wired with Zotero connectivity (add academic-writing-skills in B-extra for the 12th).
- Phase A + B + C + D (~60 min) → research-hub Python pipeline behind 13 skills; codex/gemini delegates wait for Phase E3.

Stop after any phase and use what you've installed.

**Convention** in this guide: each step ends with a `# verify` block.
Run that command and check the expected output before moving on. If it
fails, see [Phase F — Troubleshooting](#phase-f--troubleshooting).

---

## Phase A — Foundation (install the runtimes)

You need three command-line tools before anything else: **Claude Code**,
**Python 3.10+**, and **Git**. If `python` and `git` already work in
your terminal, you can skip A2 and A3.

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
ls ~/.claude/skills/
# expected: 10 directories — literature-triage-matrix,
# research-hub, research-design-helper, paper-memory-builder,
# paper-summarize, notebooklm-brief-verifier,
# research-context-compressor, research-project-orienter,
# research-hub-multi-ai, zotero-library-curator
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

You have 10 of 14 skills installed (the research-workspace plugin) and
a working literature matrix without any external setup. The 6 pure-
reasoning skills inside research-workspace work immediately; the other
4 (research-hub, research-hub-multi-ai, zotero-library-curator's apply
mode, and full literature-triage-matrix with paper search) need
Phase C / D / E. Continue to Phase B-extra if you also want manuscript
work tooling, or skip to Phase C for Zotero.

### B-extra. academic-writing-skills (optional, ~1 min)

If you'll be writing or revising manuscripts:

```bash
claude plugin install academic-writing-skills@ai-research-skills
```

```bash
# verify
ls ~/.claude/skills/academic-writing-skills/
# expected: SKILL.md plus references/
```

This adds the 11th skill — banned-word audit, claim-evidence check,
journal format, reviewer response. Skip if you only need literature
triage / lit review.

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
ls ~/.claude/skills/zotero-skills/
# expected: SKILL.md plus any references/
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

You have 12 of 14 skills wired up (10 from research-workspace +
academic-writing-skills from Phase B-extra + zotero-skills), and the
zotero-library-curator skill is upgraded from preview-only to
apply-capable. The remaining 2 (`codex-delegate`, `gemini-delegate`)
are installed in Phase E3 once you've installed their CLI binaries.
Phase D activates the full power of `research-hub`,
`research-hub-multi-ai`, and `literature-triage-matrix`'s paper-search
mode by adding the Python CLI behind them.

---

## Phase D — research-hub Python CLI (full pipeline)

Adds paper discovery (arxiv / semantic scholar / pubmed search),
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
# expected: research-hub 0.7x or higher
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

### D4. End-to-end smoke test

In Claude Code:

```
Use research-hub discover to find 5 recent papers on
"agent-based flood modeling", then make a literature triage matrix.
```

Expected: Claude calls `research-hub discover`, gets a paper list, then
hands the list to `literature-triage-matrix`, and writes
`.research/literature_matrix.md`.

### Phase D checkpoint

All 14 skills are wired up. You're done with the core setup.

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
   research-hub notebooklm login
   ```
   This opens a browser. Sign in to your Google account that has
   NotebookLM access. Close the browser when redirected.

```bash
# verify
research-hub notebooklm status
# expected: "logged in" with your Google account email
```

### E3. Codex CLI / Gemini CLI (multi-AI delegation)

Install the CLI binaries first per their upstream READMEs:

- [Codex CLI](https://github.com/WenyuChiou/codex-delegate#readme) →
  `npm install -g @openai/codex`
- [Gemini CLI](https://github.com/WenyuChiou/gemini-delegate-skill#readme) →
  `npm install -g @google/gemini-cli`

Then install the delegate plugins:

```bash
claude plugin install codex-delegate@ai-research-skills
claude plugin install gemini-delegate@ai-research-skills
```

```bash
# verify
codex --version
gemini --version
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
[README → Using these skills outside Claude Code](../README.md#using-these-skills-outside-claude-code)
and the
[Hermes compatibility audit](../.research/hermes-compatibility-audit.md)
for what's verified and what's host-specific.

---

## Next steps

- Skill-by-skill install reference: [install.md](install.md)
- Workflow-by-workflow guide: [researcher-workflow-checklist.md](researcher-workflow-checklist.md)
- Demo: [demo-walkthrough.md](demo-walkthrough.md)
- Catalog of all 14 skills: [skill-directory.md](skill-directory.md)
