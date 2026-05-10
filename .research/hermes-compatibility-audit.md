# Hermes Compatibility Audit

**Subject**: `WenyuChiou/ai-research-skills` — 14 skills across 5 upstream repos
**Target host**: `NousResearch/hermes-agent` 0.13.0 (claims compatibility with `agentskills.io` open standard)
**Date**: 2026-05-10
**Audit branch**: `claude/hermes-compat-audit` (not yet pushed to origin/main)
**Constraint**: read-only on the 14 SKILL.md files (per user); audit only, no edits.
**Outcome (TL;DR)**: 11/14 fully portable, 3/14 cosmetic tweaks, 0 claude-only. `literature-triage-matrix` verified end-to-end installable into Hermes (`hermes skills install` → SAFE → `enabled`). Inference-loop test was auth-gated and not run. See Phase 4 for the calibrated portfolio claim.

---

## Phase 1 — premise verification

### Did the verification myself, not trusting subagents

I dispatched 3 Explore agents and got back a "yes everything is real" story. Because the agent reports cited unusual figures (142k stars on a "new" CLI agent, 35-vendor adoption of a months-old standard, a `platform.claude.com` doc URL I didn't recognise), I distrusted them and re-verified with `gh api` (authoritative GitHub API via the user's authenticated CLI) plus direct `WebFetch` on the spec page and Hermes README.

### Ground-truth findings

| Claim | Evidence | Status |
|---|---|---|
| `NousResearch/hermes-agent` exists | `gh api repos/NousResearch/hermes-agent` → 200 OK, `full_name` matches | TRUE |
| Star count = 142,142 | Same gh-api response: `stargazers_count: 142142` | TRUE per GitHub's database |
| Created 2025-07-22, actively pushed today | gh-api `created_at` and `pushed_at` fields | TRUE — ~10 months old, not "newly released" |
| `agentskills/agentskills` spec repo exists | `gh api repos/agentskills/agentskills` → 18,296 stars, created 2025-12-16 | TRUE |
| `agentskills.io/specification` documents a real schema | WebFetch returned full schema with required + optional fields, directory layout, progressive-disclosure rule | TRUE |
| Spec was "originally developed by Anthropic, released as an open standard" | Verbatim line from `agentskills.io` homepage | TRUE per the source page (could not independently verify Anthropic's framing without their own docs cross-reference, which is out of scope here) |
| Hermes README claims compatibility | `WebFetch raw.githubusercontent.com/.../README.md` → quote: skills are "Compatible with the agentskills.io open standard" | TRUE |
| 35+ vendor adoption | WebFetch agentskills.io — page lists 35+ named clients with logos, install URLs, and per-client docs URLs | TRUE per the page listing; no third-party cross-check performed |

### Honest caveat about Phase 1

I can verify *that pages exist with these claims*. I cannot verify in this session whether the broader ecosystem narrative matches the substance — i.e., whether all 35 listed vendors actually shipped working `SKILL.md` loaders or whether some are aspirational. **Phase 3 (real install + real test) is the actual integrity check.**

### Why my prior was wrong

My training cutoff is January 2026. The `agentskills/agentskills` repo was created 2025-12-16 — at the very edge of my cutoff. Broad ecosystem adoption visible on the page happened in Q1–Q2 2026, fully after the cutoff. Stale prior beat by current evidence. Updated belief: this is real enough to test.

---

## Phase 2 — portability audit (14 SKILL.md)

### Methodology

Read each of 14 installed `SKILL.md` files at `~/.claude/skills/<name>/...` (already at latest origin/master in this session). Check:

1. **Spec required**: `name` (≤64 chars, lowercase + hyphens, matches dir name), `description` (1–1024 chars).
2. **Spec recommended**: SKILL.md ≤500 lines.
3. **Spec optional**: `license`, `compatibility`, `metadata`, `allowed-tools`.
4. **Claude-Code-specific patterns** (red flags): `${CLAUDE_PLUGIN_ROOT}`, hardcoded `~/.claude/skills/...`, `.claude/settings.json`, `/plugin install`, MCP server explicit references.

### Audit table

All 14 skills pass `name` regex and `description` length. All ≤200 lines (well under spec's 500 recommended cap; reflects the lean refactors landed earlier in this session).

| Skill | Lines | Desc chars | Optional fields | Claude-only patterns | MCP refs | **Verdict** |
|---|---:|---:|---|---|---:|---|
| research-hub | 174 | 478 | none | 0 | 0 | **portable** |
| research-hub-multi-ai | 114 | 395 | none | 0 | 0 | **portable** |
| research-context-compressor | 137 | 365 | none | 0 | 0 | **portable** |
| research-project-orienter | 121 | 412 | none | 0 | 0 | **portable** |
| research-design-helper | 96 | 512 | none | 0 | 0 | **portable** |
| literature-triage-matrix | 127 | 344 | none | 0 | 0 | **portable** ★ |
| paper-memory-builder | 97 | 515 | none | 0 | 0 | **portable** |
| paper-summarize | 107 | 659 | none | 0 | 0 | **portable** |
| notebooklm-brief-verifier | 122 | 333 | none | 0 | 0 | **portable** |
| academic-writing-skills | 192 | 514 | none | 0 | 0 | **portable** |
| zotero-skills | 60 | 401 | `license` | 0 | 0 | **portable** |
| zotero-library-curator | 124 | 401 | none | 2× `~/.claude/skills/` | 0 | **needs-tweak** |
| codex-delegate | 67 | 406 | `license` | 2× `~/.claude/skills/` | 0 | **needs-tweak** |
| gemini-delegate | 95 | 511 | `license` | 2× `~/.claude/skills/` | 0 | **needs-tweak** |

★ = Phase 3 candidate.

**Tally**: 11 portable, 3 needs-tweak, 0 claude-only.

### needs-tweak detail

The 3 yellow-flag skills all hit the same pattern: hardcoded `~/.claude/skills/...` in instructions or example commands. Each is a small, mechanical fix.

**`zotero-library-curator`** (line 34, 45):
- L34: prerequisite check `ls ~/.claude/skills/zotero-skills/SKILL.md 2>/dev/null  # if zotero-skills skill installed` — host-specific path in a shell command.
- L45: install hint `git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills` — same.
Fix shape: replace with a host-agnostic discovery instruction ("check whether the `zotero-skills` skill is installed in your agent's skills directory") + a non-Claude-Code install pointer.

**`codex-delegate`** (line 28, 30):
- L28 prose: "from Claude Code Bash, invoke the wrapper from its install location (user-scope skills install at `~/.claude/skills/`)"
- L30 example: `bash ~/.claude/skills/codex-delegate/scripts/run_codex.sh ...`
Fix shape: parameterise the path. Either (a) document that the wrapper is at `<skill-root>/scripts/run_codex.sh` and let the host resolve `<skill-root>`, or (b) add `compatibility: Designed for Claude Code; portable hosts must adapt the skills-dir path.` field.

**`gemini-delegate`** (line 52, 54):
- Identical to codex-delegate (its sibling skill). Same fix.

None of these are structural blockers. The skill *bodies* (the markdown instructions) are agentskills.io-compliant. The Claude Code path leak is in concrete examples, which a savvy host could rewrite by templating.

### Spec gaps relative to ai-research-skills (informational)

The agentskills.io spec doesn't define:
- A standard way to declare cross-skill dependencies (zotero-library-curator depends on zotero-skills; how should it say so portably?).
- A standard way to declare CLI dependencies (research-hub family depends on `pip install research-hub-pipeline`; the closest field is `compatibility` but it's a free-text string).
- An interop story for skills that bundle wrapper scripts (codex-delegate / gemini-delegate / zotero-skills all have `scripts/`).

The 3 `needs-tweak` skills could use the optional `compatibility:` field to declare these dependencies portably without changing instruction bodies. **That's a one-line-per-skill fix, not a rewrite.**

### Lowest-cost first cross-platform skill

`literature-triage-matrix` (★ above): 127 lines, 0 Claude-only patterns, 0 MCP, only 2 mentions of `research-hub` and one of them explicitly says *"works without any other research-hub setup"* (L39) while the other is an optional enrichment suggestion (L124). Pure markdown-instruction skill that consumes a paper list and produces a comparison matrix. Closest fit to "drop into Hermes verbatim and see if it loads". This is the Phase 3 candidate.

---

## Phase 3 — install + skill-load test (executed 2026-05-10)

### Approach: WSL2 + rc-isolation trick (option chosen)

Instead of letting the installer modify `~/.bashrc` (the constraint), I exploited an existing escape hatch in install.sh L1130–1242: if `~/.local/bin` is *already* on `PATH` at install time, the installer's rc-modification block short-circuits. Setup:

```bash
export HERMES_HOME="$HOME/hermes-compat-test"   # divert state
export PATH="$HOME/.local/bin:$PATH"            # short-circuit rc-write
mkdir -p "$HOME/.local/bin"
setsid bash install.sh --skip-setup </dev/null  # detach tty, skip wizard
```

Three combined techniques (one per failure mode I knew about from reading the installer):

1. **`HERMES_HOME` override** → install state goes to a side directory, fully reversible by one `rm -rf`.
2. **rc-isolation** → no rc files written (proof: SHA256 unchanged, `hermes-experiment-log/rc-integrity.md`).
3. **`setsid` + `</dev/null`** → no controlling TTY, so the optional sudo prompts for ripgrep/ffmpeg take the documented non-interactive `log_warn` fallthrough at L800 instead of hanging on `/dev/tty`.

### Install outcome

- ✅ Exit code 0
- ✅ 207-line install log, no errors
- ✅ `hermes --version` works, `hermes doctor` clean
- ✅ rc files SHA256 byte-identical pre/post (verified — see `hermes-experiment-log/rc-integrity.md`)
- ✅ Optional ripgrep/ffmpeg gracefully skipped (Hermes falls back to grep)

Full transcript: `.research/hermes-experiment-log/install-summary.md`.

### Skill load test

```bash
hermes skills install --category research --yes \
  https://raw.githubusercontent.com/WenyuChiou/research-hub/master/skills/literature-triage-matrix/SKILL.md
```

Output (verbatim):

```
Fetching: .../literature-triage-matrix/SKILL.md
Quarantined to .hub/quarantine/literature-triage-matrix
Running security scan...
Scan: literature-triage-matrix  Verdict: SAFE
Decision: ALLOWED — Allowed (community source, safe verdict)
Installed: research/literature-triage-matrix
Files: SKILL.md
```

- ✅ Hermes accepts our minimal frontmatter (`name` + `description` only — strict agentskills.io spec minimum).
- ✅ Security scanner returns **SAFE** on the content.
- ✅ Skill registers in `hermes skills list` (status `enabled`), `hermes dump` features.skills=1, passes re-audit.
- ✅ SKILL.md installed byte-equivalent to source (no transformation needed).
- ⚠ Minor quirk: `hermes skills install` ignores `HERMES_HOME`, writes to `~/.hermes/` regardless. Hermes' bug, not a portability issue.

Full transcript: `.research/hermes-experiment-log/skill-install-transcript.md`.

### Inference loop test — STOPPED at auth gate

```bash
hermes -z "make a literature matrix for these 3 papers: arXiv:..., arXiv:..., arXiv:..."
```

Result: `AuthError: No inference provider configured.`

Hermes raised the error before any prompt assembly. Entering an API key was out of scope (would have shifted the test from "does the format work" to "does my account work"). **Stopped, did not enter credentials.** Detail: `.research/hermes-experiment-log/inference-gate-finding.md`.

This is the **"loads but inference loop not validated"** outcome from the Phase 3 budget. The skill-loading-layer evidence is strong; the agent-loop-layer evidence is missing by design (auth-gated).

---

## Phase 4 — verdict + summary

### Verdict

**Half-real, leaning real.** The compatibility premise is settled at the spec-implementation layer; the runtime-behavior layer is unverified by design.

What is verified:

- agentskills.io is a real open spec (Phase 1, gh api evidence).
- Hermes-agent is a real CLI agent that loads the spec (Phase 3, install transcript).
- Our 14 SKILL.md files are 11/14 fully spec-compliant, 3/14 cosmetically Claude-Code-leaning (Phase 2, audit table).
- Hermes installs a strict-minimum SKILL.md from our catalog without modification, scans it SAFE, and registers it as enabled (Phase 3).

What is **not** verified:

- That Hermes' LLM routing actually dispatches a triggering prompt through the installed skill (auth-gated).
- That Hermes produces output comparable to Claude Code's reference matrix (no run, no comparison).
- That the other 13 skills load the same way (only literature-triage-matrix was tested; the 11 portable ones *should* by Phase 2 reasoning, but were not run).
- That any of the other 34 listed agentskills.io hosts load these skills (only Hermes was tested).

### Portability count

| Bucket | Count | Skills |
|---|---:|---|
| **portable** | 11 | research-hub, research-hub-multi-ai, research-context-compressor, research-project-orienter, research-design-helper, literature-triage-matrix ★, paper-memory-builder, paper-summarize, notebooklm-brief-verifier, academic-writing-skills, zotero-skills |
| **needs-tweak** | 3 | zotero-library-curator, codex-delegate, gemini-delegate (all share hardcoded `~/.claude/skills/...` example paths) |
| **claude-only** | 0 | — |

★ = verified loaded by Hermes in Phase 3.

### Lowest-cost first cross-platform skill

`literature-triage-matrix`. **Ship time: ~30 min** of doc-only work — add a one-line `compatibility:` field stating "tested with NousResearch/hermes-agent 0.13.0 at skill-load level" and a short note in the catalog readme. No code changes needed.

To upgrade the 3 `needs-tweak` skills: ~1–2 hr — replace hardcoded `~/.claude/skills/...` example paths with host-agnostic phrasing like "`<skill-root>/scripts/run_codex.sh`" plus a `compatibility:` field declaring the dependency. Mechanical Codex-delegatable refactor across 3 files.

### Calibrated LinkedIn / portfolio wording

Honest claim shape (will fit in 1–2 sentences):

> Author and maintainer of `ai-research-skills`, a 14-skill Claude Code marketplace for research workflows. After agentskills.io became the de facto open spec for agent skills in early 2026, audited the catalog for portability and verified end-to-end skill installation on NousResearch/hermes-agent — 11 of 14 skills are strict-spec-compliant; the remaining 3 need only cosmetic example-path edits, no architectural rewrite.

The supportable subclaims (each tied to evidence in this repo):

- "14-skill marketplace" — links to the marketplace.json in WenyuChiou/ai-research-skills.
- "Audited the catalog for portability" — links to this audit document.
- "11 of 14 strict-spec-compliant" — links to the Phase 2 table.
- "Verified end-to-end skill installation on Hermes" — links to `.research/hermes-experiment-log/`.

### What NOT to claim

- ❌ "Works on all 35+ agentskills.io hosts" — only one host (Hermes) was tested.
- ❌ "Endorsed by Anthropic" — Anthropic released the format, did not endorse this specific catalog.
- ❌ "Same output on Claude Code and Hermes" — never compared outputs (Hermes inference run was auth-gated).
- ❌ "All 14 skills run on Hermes" — only literature-triage-matrix was test-installed; Phase 2 predicts 10 more should but they were not verified individually.
- ❌ "Better than X" or "outperforms Y" — no head-to-head, no benchmark.

---

## Decisions surfaced by this audit (not yet executed)

1. **3 cosmetic `needs-tweak` fixes** (zotero-library-curator, codex-delegate, gemini-delegate). Files + lines named in the Phase 2 audit table. ~1–2 hr Codex-delegatable refactor. Hold for user OK.
2. **Add a `compatibility:` line to literature-triage-matrix** declaring Hermes verification. ~10-line PR. Hold for user OK.
3. **Push branch `claude/hermes-compat-audit`** to origin (currently local-only). Hold for user OK — the audit doc surfaces audit findings publicly once pushed.
4. **Cleanup Hermes from WSL** (`rm -rf ~/.hermes ~/hermes-compat-test ~/.local/bin/{hermes,node,...}`). No rc-revert needed (rc files were never modified — see `rc-integrity.md`).
